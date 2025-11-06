#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书群机器人富文本格式测试脚本
测试样式渲染功能
"""

import requests
import json
from datetime import datetime

def build_rich_content_test():
    """构建测试用的富文本内容"""
    content = []
    
    # 测试文章数据
    test_articles = [
        {
            'account_name': '机器之心',
            'title': '昆仑万维发布SkyReels AI视频创作平台，推出"无限画布"概念',
            'ai_summary': '昆仑万维SkyReels发布了多模态平台战略，核心在于"无限画布"及SkyReels V3模型，通过Agent驱动实现零门槛创作，标志着AI视频从单点工具向全链路平台演进。',
            'link': 'https://mp.weixin.qq.com/s/example123',
            'published': '2025-11-05 10:30:00'
        },
        {
            'account_name': '短剧自习室',
            'title': '2024年短剧市场数据报告：用户规模突破5亿',
            'ai_summary': '短剧市场呈现爆发式增长，用户规模达5.27亿，同比增长78%，付费用户转化率提升至12.3%，头部平台月活跃用户超1.2亿，预计2025年市场规模将达800亿元。',
            'link': 'https://mp.weixin.qq.com/s/example456',
            'published': '2025-11-05 09:15:00'
        }
    ]
    
    for i, article in enumerate(test_articles):
        # 添加分隔线（除了第一篇文章）
        if i > 0:
            content.append([{"tag": "text", "text": ""}])  # 空行
            content.append([{"tag": "text", "text": "─" * 50}])  # 分隔线
            content.append([{"tag": "text", "text": ""}])  # 空行
        
        # 公众号名称（加粗）
        content.append([
            {"tag": "text", "text": "📍 ", "style": []},
            {"tag": "text", "text": article['account_name'], "style": ["bold"]}
        ])
        
        # 文章标题（加粗）
        content.append([
            {"tag": "text", "text": "📰 ", "style": []},
            {"tag": "text", "text": article['title'], "style": ["bold"]}
        ])
        
        # AI摘要
        content.append([
            {"tag": "text", "text": "💡 ", "style": []},
            {"tag": "text", "text": article['ai_summary'], "style": []}
        ])
        
        # 阅读链接和时间
        content.append([
            {"tag": "text", "text": "🔗 ", "style": []},
            {"tag": "a", "text": "阅读原文", "href": article['link']},
            {"tag": "text", "text": f" | {article['published']}", "style": ["italic"]}
        ])
    
    return content

def test_feishu_rich_text():
    """测试飞书群机器人富文本推送"""
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/9803c75c-0a2f-4044-b973-f98441f1804b"
    
    print("🎨 测试飞书群机器人富文本格式...")
    print(f"📡 Webhook URL: {webhook_url}")
    
    # 构建富文本消息
    rich_content = build_rich_content_test()
    
    message = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "📰 微信公众号AI摘要（富文本测试）",
                    "content": rich_content
                }
            }
        }
    }
    
    print("📋 富文本消息结构:")
    print(json.dumps(message, indent=2, ensure_ascii=False))
    
    try:
        print("📤 发送富文本消息到飞书群...")
        
        response = requests.post(
            webhook_url,
            json=message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📊 HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📋 响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get("StatusCode") == 0 or result.get("code") == 0:
                print("🎉 飞书群机器人富文本推送成功！")
                print("✅ 应该可以看到样式渲染效果：")
                print("   - 📍 公众号名称加粗")
                print("   - 📰 文章标题加粗")
                print("   - 🔗 可点击的链接")
                print("   - 📅 斜体时间显示")
                print("   - ➖ 文章间分隔线")
                return True
            else:
                error_msg = result.get("msg") or result.get("StatusMessage", "未知错误")
                print(f"❌ 飞书群机器人富文本推送失败: {error_msg}")
                return False
        else:
            print(f"❌ HTTP请求失败，状态码: {response.status_code}")
            print(f"📄 响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 富文本测试异常: {e}")
        return False

def test_simple_vs_rich():
    """对比简单文本和富文本效果"""
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/9803c75c-0a2f-4044-b973-f98441f1804b"
    
    print("\n🔄 对比测试：简单文本 vs 富文本")
    
    # 1. 简单文本消息
    simple_message = {
        "msg_type": "text",
        "content": {
            "text": f"""📰 微信公众号AI摘要（简单文本）

📍 机器之心
📰 昆仑万维发布SkyReels AI视频创作平台
💡 这是简单文本格式，没有样式渲染
🔗 阅读原文 | {datetime.now().strftime('%H:%M:%S')}"""
        }
    }
    
    print("📤 发送简单文本消息...")
    try:
        response = requests.post(webhook_url, json=simple_message, timeout=10)
        if response.status_code == 200 and (response.json().get("StatusCode") == 0 or response.json().get("code") == 0):
            print("✅ 简单文本消息发送成功")
        else:
            print("❌ 简单文本消息发送失败")
    except Exception as e:
        print(f"❌ 简单文本消息异常: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🎨 飞书群机器人富文本格式测试")
    print("=" * 60)
    
    # 主要测试
    success = test_feishu_rich_text()
    
    if success:
        print("\n" + "=" * 60)
        print("🎊 富文本测试成功！")
        print("✅ 群机器人支持样式渲染")
        print("✅ 可以看到加粗、链接、斜体等效果")
        print("✅ 现在可以更新代码并推送")
        print("=" * 60)
        
        # 对比测试
        test_simple_vs_rich()
        
    else:
        print("\n" + "=" * 60)
        print("❌ 富文本测试失败！")
        print("🔧 可能的原因:")
        print("   1. 富文本格式不正确")
        print("   2. 群机器人不支持post类型")
        print("   3. 内容结构有误")
        print("=" * 60)
