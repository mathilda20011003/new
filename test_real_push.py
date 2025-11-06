#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试真实的公众号推送
"""

import os
import sys
import requests
import feedparser
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.append('.')
sys.path.append('wechat_rss')

# 加载环境变量
def load_env():
    env_file = Path('.env')
    if env_file.exists():
        print("📁 加载 .env 文件...")
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print("✅ .env 文件加载完成")

def get_rss_articles(feed_id, base_url):
    """获取RSS文章"""
    try:
        rss_url = f"{base_url}/rss/{feed_id}"
        print(f"📡 获取RSS: {rss_url}")
        
        response = requests.get(rss_url, timeout=30)
        response.raise_for_status()
        
        feed = feedparser.parse(response.content)
        articles = []
        
        for entry in feed.entries[:3]:  # 只取前3篇
            article = {
                'title': entry.title,
                'link': entry.link,
                'published': entry.get('published', ''),
                'summary': entry.get('summary', ''),
                'account_name': feed.feed.get('title', '未知公众号')
            }
            articles.append(article)
            
        print(f"✅ 获取到 {len(articles)} 篇文章")
        return articles
        
    except Exception as e:
        print(f"❌ 获取RSS失败: {e}")
        return []

def generate_ai_summary(content, title):
    """生成AI摘要"""
    try:
        from wechat_rss.ai_summarizer import AISummarizer
        
        api_key = os.getenv('OPENROUTER_API_KEY')
        model = os.getenv('AI_MODEL', 'google/gemini-2.5-flash-lite-preview-09-2025')
        
        summarizer = AISummarizer(
            provider='openrouter',
            api_key=api_key,
            model=model,
            max_tokens=150
        )
        
        summary = summarizer.generate_summary(content, title)
        return summary
        
    except Exception as e:
        print(f"❌ AI摘要生成失败: {e}")
        return f"文章标题：{title}"

def send_to_feishu(articles):
    """发送到飞书"""
    try:
        from wechat_rss.feishu_sender import FeishuSender
        
        webhook_url = os.getenv('FEISHU_WEBHOOK_URL')
        sender = FeishuSender(webhook_url)
        
        return sender.send_articles(articles)
        
    except Exception as e:
        print(f"❌ 飞书推送失败: {e}")
        return False

def main():
    print("🚀 开始测试真实公众号推送...")
    print("=" * 60)
    
    # 加载环境变量
    load_env()
    
    # 检查配置
    base_url = os.getenv('WEWE_RSS_BASE_URL', 'https://ssys2025.zeabur.app').rstrip('/')
    webhook_url = os.getenv('FEISHU_WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ 未设置 FEISHU_WEBHOOK_URL")
        return
        
    print(f"✅ WeWe RSS: {base_url}")
    print(f"✅ 飞书Webhook: {webhook_url[:50]}...")
    
    # 测试公众号配置
    test_accounts = [
        {
            'name': '短剧自习室',
            'feed_id': 'MP_WXS_3906677264.atom',
            'keywords': ['漫剧', 'AI漫剧', '短剧']
        },
        {
            'name': '机器之心', 
            'feed_id': 'MP_WXS_3073282833.atom',
            'keywords': ['AI视频', 'AI生图', '大模型']
        }
    ]
    
    all_articles = []
    
    # 获取文章
    for account in test_accounts:
        print(f"\n📋 处理公众号: {account['name']}")
        articles = get_rss_articles(account['feed_id'], base_url)
        
        for article in articles:
            # 关键词筛选
            title_content = f"{article['title']} {article['summary']}"
            if any(keyword in title_content for keyword in account['keywords']):
                print(f"✅ 匹配关键词: {article['title'][:50]}...")
                
                # 生成AI摘要
                ai_summary = generate_ai_summary(article['summary'], article['title'])
                article['ai_summary'] = ai_summary
                article['account_name'] = account['name']
                
                all_articles.append(article)
            else:
                print(f"⏭️  跳过: {article['title'][:50]}...")
    
    # 推送到飞书
    if all_articles:
        print(f"\n📱 准备推送 {len(all_articles)} 篇文章到飞书...")
        success = send_to_feishu(all_articles)
        
        if success:
            print("🎉 推送成功！请检查您的飞书群组。")
        else:
            print("❌ 推送失败")
    else:
        print("\n⚠️  没有匹配的文章")

if __name__ == "__main__":
    main()
