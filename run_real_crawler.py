#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
import feedparser
from pathlib import Path
from datetime import datetime

# 设置UTF-8编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

print("🚀 开始运行真实的微信公众号RSS爬虫...")

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

def fetch_real_articles(feed_id, base_url, account_name):
    """获取真实的RSS文章"""
    try:
        # 尝试不同的RSS URL格式
        possible_urls = [
            f"{base_url}/rss/{feed_id}",
            f"{base_url}/rss/{feed_id}.atom",
            f"{base_url}/feed/{feed_id}",
            f"{base_url}/feed/{feed_id}.atom"
        ]

        rss_url = None
        response = None

        for url in possible_urls:
            try:
                print(f"📡 尝试RSS: {url}")
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    rss_url = url
                    print(f"✅ RSS可用: {url}")
                    break
                else:
                    print(f"❌ 状态码: {response.status_code}")
            except Exception as e:
                print(f"❌ 请求失败: {e}")

        if not rss_url or not response:
            raise Exception("所有RSS URL都不可用")
        
        feed = feedparser.parse(response.content)
        articles = []
        
        print(f"📋 Feed标题: {feed.feed.get('title', '未知')}")
        print(f"📊 总文章数: {len(feed.entries)}")
        
        for entry in feed.entries[:5]:  # 取前5篇
            article = {
                'title': entry.title,
                'link': entry.link,
                'published': entry.get('published', ''),
                'summary': entry.get('summary', ''),
                'account_name': account_name
            }
            articles.append(article)
            print(f"   📰 {entry.title[:50]}...")
            
        return articles
        
    except Exception as e:
        print(f"❌ 获取RSS失败: {e}")
        return []

def filter_by_keywords(articles, keywords):
    """关键词筛选"""
    filtered = []
    for article in articles:
        title_content = f"{article['title']} {article['summary']}"
        if any(keyword in title_content for keyword in keywords):
            filtered.append(article)
            print(f"✅ 匹配关键词: {article['title'][:50]}...")
        else:
            print(f"⏭️  跳过: {article['title'][:50]}...")
    return filtered

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
        
        print(f"🤖 生成AI摘要: {title[:30]}...")
        summary = summarizer.generate_summary(content, title)
        print(f"✅ AI摘要完成")
        return summary
        
    except Exception as e:
        print(f"❌ AI摘要生成失败: {e}")
        return f"文章标题：{title}"

def send_to_feishu(articles):
    """发送到飞书"""
    try:
        webhook_url = os.getenv('FEISHU_WEBHOOK_URL')
        
        # 构建消息内容
        text_content = []
        titles_list = []
        
        for article in articles:
            account_name = article['account_name']
            title = article['title']
            ai_summary = article['ai_summary']
            link = article['link']
            published = article['published']
            
            titles_list.append(f"{account_name}: {title}")
            
            # 格式化时间
            try:
                from email.utils import parsedate_to_datetime
                dt = parsedate_to_datetime(published)
                pub_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                pub_time = published or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 新格式
            text_content.append(f"📍 {account_name}")
            text_content.append(f"📰 {title}")
            text_content.append(f"💡 {ai_summary}")
            text_content.append(f"🔗 阅读原文 | {pub_time}")
            text_content.append(f"   {link}")
            text_content.append("")
        
        message = {
            "content": {
                "report_type": "微信公众号AI摘要",
                "text": "\n".join(text_content),
                "total_titles": ", ".join(titles_list),
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        
        print("📤 发送到飞书...")
        response = requests.post(
            webhook_url,
            json=message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print("🎉 飞书推送成功！")
                return True
        
        print(f"❌ 飞书推送失败: {response.status_code}")
        return False
        
    except Exception as e:
        print(f"❌ 飞书推送异常: {e}")
        return False

def main():
    # 加载环境变量
    load_env()
    
    # 配置
    base_url = os.getenv('WEWE_RSS_BASE_URL', 'https://ssys2025.zeabur.app').rstrip('/')
    
    # 测试多个公众号，每个筛选2篇
    test_accounts = [
        {
            'name': '机器之心',
            'feed_id': 'MP_WXS_3073282833',
            'keywords': ['AI', '大模型', '人工智能', '机器学习', '深度学习', '模型']
        },
        {
            'name': '短剧自习室',
            'feed_id': 'MP_WXS_3906677264',
            'keywords': ['漫剧', 'AI漫剧', '短剧', '红果', '播放量']
        },
        {
            'name': '漫剧有数',
            'feed_id': 'MP_WXS_3621201576',
            'keywords': ['漫剧', '抖音漫剧', '女频', '爆款', '播放']
        }
    ]
    
    all_filtered_articles = []

    # 处理每个公众号
    for test_account in test_accounts:
        print(f"\n{'='*60}")
        print(f"📰 处理公众号: {test_account['name']}")
        print(f"   Feed ID: {test_account['feed_id']}")
        print(f"   关键词: {', '.join(test_account['keywords'])}")
        print(f"{'='*60}")

        # 1. 获取文章
        articles = fetch_real_articles(
            test_account['feed_id'],
            base_url,
            test_account['name']
        )

        if not articles:
            print("❌ 未获取到文章，跳过此公众号")
            continue

        # 2. 关键词筛选
        filtered_articles = filter_by_keywords(articles, test_account['keywords'])

        if not filtered_articles:
            print("❌ 筛选后无匹配文章，跳过此公众号")
            continue

        print(f"🔍 筛选结果: {len(articles)} → {len(filtered_articles)} 篇")

        # 3. 每个公众号只取前2篇
        selected_articles = filtered_articles[:2]
        print(f"📋 选择文章: {len(selected_articles)} 篇")

        # 4. 生成AI摘要
        for article in selected_articles:
            ai_summary = generate_ai_summary(article['summary'], article['title'])
            article['ai_summary'] = ai_summary

        all_filtered_articles.extend(selected_articles)

    # 5. 推送所有文章到飞书
    if all_filtered_articles:
        print(f"\n📱 准备推送总共 {len(all_filtered_articles)} 篇文章到飞书...")
        success = send_to_feishu(all_filtered_articles)

        if success:
            print("🎉 真实文章推送成功！请检查您的飞书群组。")
        else:
            print("❌ 推送失败")
    else:
        print("❌ 没有找到任何匹配的文章")

if __name__ == "__main__":
    main()
