#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试RSS原始内容
"""

import os
import requests
import feedparser
from dotenv import load_dotenv

def debug_rss_raw():
    """调试RSS原始内容"""
    load_dotenv()
    
    base_url = os.getenv('WEWE_RSS_BASE_URL', 'https://ssys2025.zeabur.app')
    test_feed_id = "MP_WXS_3073282833"  # 机器之心
    
    print("🔍 调试RSS原始内容...")
    
    try:
        response = requests.get(f"{base_url}/feeds/{test_feed_id}", timeout=10)
        
        if response.status_code == 200:
            print("✅ RSS获取成功")
            print(f"📄 原始内容长度: {len(response.text)} 字符")
            
            # 显示原始XML的前1000字符
            print(f"\n📄 原始RSS内容预览:")
            print("="*60)
            print(response.text[:1000])
            print("="*60)
            
            # 解析RSS
            feed = feedparser.parse(response.content)
            print(f"\n📊 解析结果: {len(feed.entries)} 篇文章")
            
            if feed.entries:
                entry = feed.entries[0]
                print(f"\n📰 第一篇文章详细信息:")
                print(f"标题: {entry.get('title', '无标题')}")
                
                # 显示所有可用字段
                print(f"\n🔍 所有可用字段:")
                for key, value in entry.items():
                    if isinstance(value, str):
                        if len(value) > 100:
                            print(f"  {key}: {value[:100]}... ({len(value)} 字符)")
                        else:
                            print(f"  {key}: {value}")
                    else:
                        print(f"  {key}: {type(value)} - {str(value)[:100]}")
                        
        else:
            print(f"❌ RSS获取失败: {response.status_code}")
            print(f"响应内容: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ 调试失败: {e}")

if __name__ == "__main__":
    debug_rss_raw()
