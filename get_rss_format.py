#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json
from pathlib import Path

print("🔍 获取正确的RSS格式...")

# 加载环境变量
env_file = Path('.env')
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

base_url = os.getenv('WEWE_RSS_BASE_URL', 'https://ssys2025.zeabur.app').rstrip('/')

# 1. 获取feeds列表
try:
    print("📡 获取feeds列表...")
    response = requests.get(f"{base_url}/feeds", timeout=10)
    
    if response.status_code == 200:
        feeds = response.json()
        print(f"✅ 找到 {len(feeds)} 个feeds")
        
        for feed in feeds[:3]:  # 只显示前3个
            print(f"\n📰 {feed['name']}")
            print(f"   ID: {feed['id']}")
            print(f"   简介: {feed.get('intro', '无')}")
            
            # 尝试不同的RSS URL格式
            feed_id = feed['id']
            possible_rss_urls = [
                f"{base_url}/rss/{feed_id}",
                f"{base_url}/rss/{feed_id}.xml",
                f"{base_url}/rss/{feed_id}.atom",
                f"{base_url}/feed/{feed_id}",
                f"{base_url}/feed/{feed_id}.xml", 
                f"{base_url}/feed/{feed_id}.atom",
                f"{base_url}/api/rss/{feed_id}",
                f"{base_url}/api/feed/{feed_id}",
                f"{base_url}/{feed_id}/rss",
                f"{base_url}/{feed_id}/feed"
            ]
            
            print("   尝试RSS URL:")
            for rss_url in possible_rss_urls:
                try:
                    rss_response = requests.get(rss_url, timeout=5)
                    if rss_response.status_code == 200:
                        content_type = rss_response.headers.get('content-type', '')
                        if 'xml' in content_type or 'rss' in content_type or 'atom' in content_type:
                            print(f"   ✅ 可用: {rss_url}")
                            print(f"      Content-Type: {content_type}")
                            
                            # 尝试解析RSS内容
                            try:
                                import feedparser
                                feed_data = feedparser.parse(rss_response.content)
                                if feed_data.entries:
                                    print(f"      文章数: {len(feed_data.entries)}")
                                    if feed_data.entries:
                                        print(f"      最新文章: {feed_data.entries[0].title[:50]}...")
                                else:
                                    print("      ⚠️ 无文章内容")
                            except Exception as e:
                                print(f"      ⚠️ RSS解析失败: {e}")
                            break
                        else:
                            print(f"   ❌ 非RSS格式: {rss_url} ({content_type})")
                    else:
                        print(f"   ❌ {rss_response.status_code}: {rss_url}")
                except Exception as e:
                    print(f"   ❌ 错误: {rss_url} - {e}")
    else:
        print(f"❌ 获取feeds失败: {response.status_code}")
        
except Exception as e:
    print(f"❌ 请求失败: {e}")

print("\n✅ 检查完成")
