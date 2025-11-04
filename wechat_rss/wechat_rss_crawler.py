#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号 RSS 爬虫主程序
功能：从 WeWe RSS 获取文章，关键词筛选，AI 总结，推送到飞书
"""

import os
import sys
import yaml
import json
import time
from datetime import datetime
from typing import List, Dict, Optional

# 导入自定义模块
from ai_summarizer import AISummarizer
from feishu_sender import FeishuSender
from utils import load_config, filter_by_keywords, format_article_message

class WeChatRSSCrawler:
    """微信公众号 RSS 爬虫"""
    
    def __init__(self, config_path: str = "config/wechat_accounts.yaml"):
        """初始化爬虫"""
        self.config = load_config(config_path)
        self.base_url = self.config['wewe_rss']['base_url'].rstrip('/')
        self.auth_code = self.config['wewe_rss'].get('auth_code', '')
        
        # 初始化 AI 总结器
        ai_config = self.config.get('ai', {})
        self.ai_summarizer = AISummarizer(
            provider=ai_config.get('provider', 'deepseek'),
            api_key=os.getenv('DEEPSEEK_API_KEY') or ai_config.get('api_key'),
            model=ai_config.get('model', 'deepseek-chat'),
            max_tokens=ai_config.get('max_tokens', 150)
        )
        
        # 初始化飞书推送
        feishu_webhook = os.getenv('FEISHU_WEBHOOK_URL')
        self.feishu_sender = FeishuSender(feishu_webhook)
        
        # 推送配置
        self.push_config = self.config.get('push', {})
        self.max_articles = self.push_config.get('max_articles', 10)
        
        print(f"✅ 爬虫初始化完成")
        print(f"📡 WeWe RSS: {self.base_url}")
        print(f"🤖 AI Provider: {ai_config.get('provider', 'deepseek')}")
        print(f"📱 飞书推送: {'已配置' if feishu_webhook else '未配置'}")
    
    def fetch_feed(self, feed_id: str) -> List[Dict]:
        """
        从 WeWe RSS 获取指定 Feed 的文章列表
        
        Args:
            feed_id: Feed ID (如 MP_WXS_123456)
        
        Returns:
            文章列表
        """
        import requests
        import feedparser
        
        try:
            # 构建 RSS URL
            rss_url = f"{self.base_url}/feeds/{feed_id}.rss"
            
            # 添加认证头
            headers = {}
            if self.auth_code:
                headers['Authorization'] = f'Bearer {self.auth_code}'
            
            print(f"📡 正在获取 Feed: {feed_id}")
            print(f"   URL: {rss_url}")
            
            # 获取 RSS
            response = requests.get(rss_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # 解析 RSS
            feed = feedparser.parse(response.content)
            
            articles = []
            for entry in feed.entries:
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', ''),
                    'content': entry.get('content', [{}])[0].get('value', '') if entry.get('content') else ''
                }
                articles.append(article)
            
            print(f"✅ 获取到 {len(articles)} 篇文章")
            return articles
            
        except Exception as e:
            print(f"❌ 获取 Feed 失败: {e}")
            return []
    
    def process_account(self, account: Dict) -> List[Dict]:
        """
        处理单个公众号
        
        Args:
            account: 公众号配置
        
        Returns:
            处理后的文章列表
        """
        name = account.get('name', '未知公众号')
        feed_id = account.get('feed_id', '')
        keywords = account.get('keywords', [])
        
        print(f"\n{'='*60}")
        print(f"📰 处理公众号: {name}")
        print(f"   Feed ID: {feed_id}")
        print(f"   关键词: {', '.join(keywords)}")
        print(f"{'='*60}")
        
        if not feed_id:
            print(f"⚠️  跳过: 未配置 Feed ID")
            return []
        
        # 1. 获取文章列表
        articles = self.fetch_feed(feed_id)
        if not articles:
            print(f"⚠️  未获取到文章")
            return []
        
        # 2. 关键词筛选
        if keywords:
            filtered_articles = filter_by_keywords(articles, keywords)
            print(f"🔍 关键词筛选: {len(articles)} → {len(filtered_articles)} 篇")
            articles = filtered_articles
        
        if not articles:
            print(f"⚠️  筛选后无文章")
            return []
        
        # 3. 限制数量
        if len(articles) > self.max_articles:
            articles = articles[:self.max_articles]
            print(f"📊 限制数量: 取前 {self.max_articles} 篇")
        
        # 4. AI 总结
        processed_articles = []
        for i, article in enumerate(articles, 1):
            print(f"\n📝 处理文章 {i}/{len(articles)}: {article['title'][:50]}...")
            
            # 生成摘要
            summary = self.ai_summarizer.summarize(
                title=article['title'],
                content=article.get('content') or article.get('summary', '')
            )
            
            if summary:
                article['ai_summary'] = summary
                article['account_name'] = name
                processed_articles.append(article)
                print(f"   ✅ 摘要: {summary[:100]}...")
            else:
                print(f"   ⚠️  摘要生成失败")
            
            # 避免 API 限流
            time.sleep(1)
        
        return processed_articles
    
    def run(self):
        """运行爬虫"""
        print(f"\n{'='*60}")
        print(f"🚀 微信公众号 RSS 爬虫启动")
        print(f"⏰ 运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        all_articles = []
        accounts = self.config.get('accounts', [])
        
        if not accounts:
            print("❌ 错误: 未配置任何公众号")
            return
        
        print(f"📋 共配置 {len(accounts)} 个公众号\n")
        
        # 处理每个公众号
        for account in accounts:
            try:
                articles = self.process_account(account)
                all_articles.extend(articles)
            except Exception as e:
                print(f"❌ 处理公众号失败: {e}")
                continue
        
        # 推送到飞书
        if all_articles:
            print(f"\n{'='*60}")
            print(f"📱 准备推送到飞书")
            print(f"   共 {len(all_articles)} 篇文章")
            print(f"{'='*60}\n")
            
            success = self.feishu_sender.send_articles(all_articles)
            if success:
                print(f"✅ 飞书推送成功!")
            else:
                print(f"❌ 飞书推送失败")
        else:
            print(f"\n⚠️  没有文章需要推送")
        
        print(f"\n{'='*60}")
        print(f"🎉 爬虫运行完成")
        print(f"{'='*60}\n")


def main():
    """主函数"""
    try:
        # 检查环境变量
        if not os.getenv('FEISHU_WEBHOOK_URL'):
            print("⚠️  警告: 未设置 FEISHU_WEBHOOK_URL 环境变量")
        
        if not os.getenv('DEEPSEEK_API_KEY'):
            print("⚠️  警告: 未设置 DEEPSEEK_API_KEY 环境变量")
        
        # 运行爬虫
        crawler = WeChatRSSCrawler()
        crawler.run()
        
    except Exception as e:
        print(f"❌ 程序运行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

