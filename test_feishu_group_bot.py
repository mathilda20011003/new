#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书群机器人测试脚本
测试新的群机器人Webhook是否能正常工作
"""

import requests
import json
from datetime import datetime

def test_feishu_group_bot():
    """测试飞书群机器人推送"""
    
    # 您的飞书群机器人Webhook URL
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/9803c75c-0a2f-4044-b973-f98441f1804b"
    
    print("🧪 开始测试飞书群机器人...")
    print(f"📡 Webhook URL: {webhook_url}")
    
    # 测试消息内容
    test_content = f"""📰 微信公众号AI摘要测试

🕐 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📍 机器之心
📰 昆仑万维发布SkyReels AI视频创作平台，推出"无限画布"概念
💡 昆仑万维SkyReels发布了多模态平台战略，核心在于"无限画布"及SkyReels V3模型，通过Agent驱动实现零门槛创作，标志着AI视频从单点工具向全链路平台演进。
🔗 阅读原文 | 2025-11-05 10:30:00
   https://mp.weixin.qq.com/s/example123

📍 短剧自习室  
📰 2024年短剧市场数据报告：用户规模突破5亿
💡 短剧市场呈现爆发式增长，用户规模达5.27亿，同比增长78%，付费用户转化率提升至12.3%，头部平台月活跃用户超1.2亿，预计2025年市场规模将达800亿元。
🔗 阅读原文 | 2025-11-05 09:15:00
   https://mp.weixin.qq.com/s/example456

✅ 这是一条测试消息，验证飞书群机器人功能是否正常！"""

    # 飞书群机器人标准格式（参考TrendRadar实现）
    message = {
        "msg_type": "text",
        "content": {
            "text": test_content
        }
    }
    
    try:
        print("📤 发送测试消息到飞书群...")
        
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
            
            # 检查飞书群机器人的响应状态
            if result.get("StatusCode") == 0 or result.get("code") == 0:
                print("🎉 飞书群机器人测试成功！")
                print("✅ 消息已成功发送到群组")
                return True
            else:
                error_msg = result.get("msg") or result.get("StatusMessage", "未知错误")
                print(f"❌ 飞书群机器人返回错误: {error_msg}")
                return False
        else:
            print(f"❌ HTTP请求失败，状态码: {response.status_code}")
            print(f"📄 响应内容: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误，请检查网络或Webhook URL")
        return False
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def test_different_message_types():
    """测试不同类型的消息格式"""
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/9803c75c-0a2f-4044-b973-f98441f1804b"
    
    print("\n🔬 测试不同消息格式...")
    
    # 测试1: 简单文本消息
    simple_message = {
        "msg_type": "text",
        "content": {
            "text": "🧪 简单文本消息测试 - " + datetime.now().strftime('%H:%M:%S')
        }
    }
    
    print("📤 测试简单文本消息...")
    try:
        response = requests.post(webhook_url, json=simple_message, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("StatusCode") == 0 or result.get("code") == 0:
                print("✅ 简单文本消息发送成功")
            else:
                print(f"❌ 简单文本消息失败: {result}")
        else:
            print(f"❌ 简单文本消息HTTP失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 简单文本消息异常: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 飞书群机器人功能测试")
    print("=" * 60)
    
    # 主要测试
    success = test_feishu_group_bot()
    
    if success:
        print("\n" + "=" * 60)
        print("🎊 测试结果: 成功！")
        print("✅ 您的飞书群机器人Webhook工作正常")
        print("✅ 可以正常接收和显示消息")
        print("✅ 现在可以更新GitHub Secrets中的FEISHU_WEBHOOK_URL")
        print("=" * 60)
        
        # 额外测试
        test_different_message_types()
        
    else:
        print("\n" + "=" * 60)
        print("❌ 测试结果: 失败！")
        print("🔧 请检查以下项目:")
        print("   1. Webhook URL是否正确")
        print("   2. 机器人是否已添加到群组")
        print("   3. 机器人是否有发送消息权限")
        print("   4. 网络连接是否正常")
        print("=" * 60)
