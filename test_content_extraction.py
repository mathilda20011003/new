#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试内容提取和AI摘要生成
"""

import os
import requests
import feedparser
from dotenv import load_dotenv

def test_rss_content():
    """测试RSS内容提取"""
    load_dotenv()
    
    base_url = os.getenv('WEWE_RSS_BASE_URL', 'https://ssys2025.zeabur.app')
    test_feed_id = "MP_WXS_3073282833"  # 机器之心
    
    print("🔍 测试RSS内容提取...")
    print(f"📡 RSS地址: {base_url}/feeds/{test_feed_id}")
    
    try:
        response = requests.get(f"{base_url}/feeds/{test_feed_id}", timeout=10)
        
        if response.status_code == 200:
            print("✅ RSS获取成功")
            
            feed = feedparser.parse(response.content)
            print(f"📊 获取到 {len(feed.entries)} 篇文章")
            
            if feed.entries:
                entry = feed.entries[0]  # 测试第一篇文章
                
                print(f"\n📰 测试文章: {entry.get('title', '无标题')[:50]}...")
                
                # 测试不同的内容字段
                print("\n🔍 可用字段:")
                for field in ['title', 'summary', 'description', 'content']:
                    value = entry.get(field, '')
                    if value:
                        if field == 'content':
                            if isinstance(value, list) and len(value) > 0:
                                content_value = value[0].get('value', '') if isinstance(value[0], dict) else str(value[0])
                                print(f"  {field}: {len(content_value)} 字符")
                                if len(content_value) > 100:
                                    print(f"    预览: {content_value[:100]}...")
                            else:
                                print(f"  {field}: {len(str(value))} 字符")
                        else:
                            print(f"  {field}: {len(str(value))} 字符")
                            if len(str(value)) > 100:
                                print(f"    预览: {str(value)[:100]}...")
                
                # 使用改进的内容提取逻辑
                content = ''
                if entry.get('content'):
                    if isinstance(entry.content, list) and len(entry.content) > 0:
                        content = entry.content[0].get('value', '')
                    else:
                        content = str(entry.content)
                
                if not content:
                    content = entry.get('description', '') or entry.get('summary', '')
                
                summary = entry.get('summary', '') or entry.get('description', '')
                
                print(f"\n📝 提取结果:")
                print(f"  标题: {entry.get('title', '无标题')}")
                print(f"  摘要长度: {len(summary)} 字符")
                print(f"  内容长度: {len(content)} 字符")
                
                if content:
                    print(f"  内容预览: {content[:200]}...")
                    
                    # 测试AI摘要生成
                    print(f"\n🤖 测试AI摘要生成...")
                    test_ai_summary(content, entry.get('title', '无标题'))
                else:
                    print("  ⚠️ 未获取到文章内容")
                    
        else:
            print(f"❌ RSS获取失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_ai_summary(content, title):
    """测试AI摘要生成"""
    try:
        from wechat_rss.ai_summarizer import AISummarizer
        
        api_key = os.getenv('OPENROUTER_API_KEY')
        model = os.getenv('AI_MODEL', 'google/gemini-2.5-flash-lite-preview-09-2025')
        
        if not api_key:
            print("❌ 未配置OpenRouter API密钥")
            return
        
        # 如果内容太长，截取前2000字符
        if len(content) > 2000:
            content = content[:2000] + "..."
            print(f"📝 内容过长，截取前2000字符")
        
        summarizer = AISummarizer(
            api_key=api_key,
            model=model,
            max_tokens=150
        )
        
        print(f"🤖 调用AI模型: {model}")
        print(f"📝 输入内容长度: {len(content)} 字符")
        
        summary = summarizer.summarize(title, content)
        
        print(f"✅ AI摘要生成成功:")
        print(f"   {summary}")
        
        # 检查摘要质量
        if len(summary) < 20:
            print("⚠️ 摘要过短，可能质量不佳")
        elif title in summary:
            print("⚠️ 摘要包含标题，可能只是基于标题生成")
        else:
            print("✅ 摘要质量良好")
            
    except Exception as e:
        print(f"❌ AI摘要生成失败: {e}")

if __name__ == "__main__":
    test_rss_content()
