#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试飞书推送格式
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wechat_rss.feishu_sender import FeishuSender
from datetime import datetime

def test_new_format():
    """测试新的推送格式"""
    
    # 模拟文章数据
    test_articles = [
        {
            'title': 'Vibe Working: AI 编码泛化的终局想象 | AGIX PM Notes',
            'ai_summary': '文章探讨了"Vibe Working"的概念，即通过自然语言描述目标，由AI自动生成代码或完成工作。其核心在于环境需具备可判定性、稳定上下文和可控执行。作者认为，将这一模式从编码推广到更广泛的办公、营销等领域，需要环境和工作流本身"API化"，并指向代码化的工作流管理和作为企业Context的数字孪生两个方向。',
            'link': 'https://mp.weixin.qq.com/s/example1',
            'published': '2025-09-15 20:02:58',
            'account_name': '海外独角兽'
        },
        {
            'title': '太上头了，字节的新模型。',
            'ai_summary': '文章分享了字节跳动最新发布的图像创作模型Seedream 4.0的实测体验。该模型在中文、动漫等场景的能力被认为超越Nano Banana，并在第三方评测中拿下文生图和图像编辑双第一。作者通过多个实际案例展示了Seedream 4.0的强大功能，包括生成海报、手机壁纸、文创产品、证件照、中秋海报、绘本、建筑漫画、连环画和小红书封面等，强调其指令遵循能力强、生图速度快、支持多图融合、中文排版靠谱且画质极高。目前用户可在火山方舟免费体验该模型。',
            'link': 'https://mp.weixin.qq.com/s/example2',
            'published': '2025-09-15 17:24:18',
            'account_name': 'AI产品阿颂'
        }
    ]
    
    # 创建FeishuSender实例（不需要真实的webhook_url）
    sender = FeishuSender("test_webhook_url")
    
    # 测试格式化消息
    print("=== 测试新的飞书推送格式 ===\n")

    # 1. 测试工作流格式
    print("1️⃣ 工作流格式（用于飞书工作流）：")
    print("=" * 60)
    workflow_message = sender._format_workflow_message(test_articles)
    print(workflow_message['content']['text'])
    print("=" * 60)
    print(f"报告类型: {workflow_message['content']['report_type']}")
    print(f"时间戳: {workflow_message['content']['timestamp']}")
    print(f"标题列表: {workflow_message['content']['total_titles']}")

    print("\n" + "="*80 + "\n")

    # 2. 测试机器人格式
    print("2️⃣ 机器人格式（用于飞书机器人）：")
    print("=" * 60)
    bot_message = sender._format_bot_message(test_articles)
    print("消息类型:", bot_message['msg_type'])
    print("卡片标题:", bot_message['card']['header']['title']['content'])
    print("卡片元素数量:", len(bot_message['card']['elements']))

    # 显示前几个元素的内容
    print("\n卡片内容预览:")
    for i, element in enumerate(bot_message['card']['elements'][:12]):  # 显示前12个元素
        if element.get('tag') == 'div' and 'text' in element:
            content = element['text'].get('content', '')
            if content:
                print(f"  {i+1}. {content}")
        elif element.get('tag') == 'hr':
            print(f"  {i+1}. [分隔线]")
    print("=" * 60)

if __name__ == "__main__":
    test_new_format()
