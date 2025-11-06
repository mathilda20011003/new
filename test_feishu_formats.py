#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试飞书群机器人支持的各种消息格式
"""

import requests
import json
from datetime import datetime

def test_text_format():
    """测试纯文本格式"""
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/9803c75c-0a2f-4044-b973-f98441f1804b"
    
    message = {
        "msg_type": "text",
        "content": {
            "text": "🧪 纯文本格式测试 - " + datetime.now().strftime('%H:%M:%S')
        }
    }
    
    print("📤 测试纯文本格式...")
    response = requests.post(webhook_url, json=message, timeout=10)
    result = response.json()
    print(f"纯文本结果: {result}")
    return result.get("code") == 0

def test_rich_text_format():
    """测试富文本格式"""
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/9803c75c-0a2f-4044-b973-f98441f1804b"
    
    message = {
        "msg_type": "rich_text",
        "content": {
            "rich_text": {
                "elements": [
                    {
                        "tag": "text",
                        "text": "📍 ",
                        "style": {}
                    },
                    {
                        "tag": "text", 
                        "text": "机器之心",
                        "style": {
                            "bold": True
                        }
                    },
                    {
                        "tag": "text",
                        "text": "\n📰 昆仑万维发布SkyReels AI视频创作平台\n💡 这是富文本测试消息\n"
                    },
                    {
                        "tag": "a",
                        "text": "🔗 阅读原文",
                        "href": "https://mp.weixin.qq.com/s/example"
                    }
                ]
            }
        }
    }
    
    print("📤 测试富文本格式...")
    response = requests.post(webhook_url, json=message, timeout=10)
    result = response.json()
    print(f"富文本结果: {result}")
    return result.get("code") == 0

def test_interactive_format():
    """测试交互式卡片格式"""
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/9803c75c-0a2f-4044-b973-f98441f1804b"
    
    message = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "📰 微信公众号AI摘要"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "**📍 机器之心**\n**📰 昆仑万维发布SkyReels AI视频创作平台**\n💡 这是交互式卡片测试消息\n[🔗 阅读原文](https://mp.weixin.qq.com/s/example)"
                    }
                }
            ]
        }
    }
    
    print("📤 测试交互式卡片格式...")
    response = requests.post(webhook_url, json=message, timeout=10)
    result = response.json()
    print(f"交互式卡片结果: {result}")
    return result.get("code") == 0

def test_markdown_in_text():
    """测试文本中的Markdown格式"""
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/9803c75c-0a2f-4044-b973-f98441f1804b"
    
    # 尝试在文本中使用一些特殊格式
    text_with_formatting = f"""📰 微信公众号AI摘要（格式测试）

📍 **机器之心**
📰 **昆仑万维发布SkyReels AI视频创作平台**
💡 昆仑万维SkyReels发布了多模态平台战略，核心在于"无限画布"及SkyReels V3模型
🔗 阅读原文: https://mp.weixin.qq.com/s/example
📅 *{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

──────────────────────────────────────

📍 **短剧自习室**
📰 **2024年短剧市场数据报告**
💡 短剧市场呈现爆发式增长，用户规模达5.27亿
🔗 阅读原文: https://mp.weixin.qq.com/s/example2"""

    message = {
        "msg_type": "text",
        "content": {
            "text": text_with_formatting
        }
    }
    
    print("📤 测试文本中的格式...")
    response = requests.post(webhook_url, json=message, timeout=10)
    result = response.json()
    print(f"文本格式结果: {result}")
    return result.get("code") == 0

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 飞书群机器人消息格式测试")
    print("=" * 60)
    
    formats = [
        ("纯文本格式", test_text_format),
        ("富文本格式", test_rich_text_format), 
        ("交互式卡片格式", test_interactive_format),
        ("文本中的格式", test_markdown_in_text)
    ]
    
    results = {}
    
    for name, test_func in formats:
        print(f"\n🔬 测试 {name}...")
        try:
            success = test_func()
            results[name] = "✅ 成功" if success else "❌ 失败"
            print(f"{name}: {results[name]}")
        except Exception as e:
            results[name] = f"❌ 异常: {e}"
            print(f"{name}: {results[name]}")
        
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("📊 测试结果总结:")
    for name, result in results.items():
        print(f"  {name}: {result}")
    print("=" * 60)
