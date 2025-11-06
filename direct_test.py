#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json
from pathlib import Path
from datetime import datetime

print("开始直接测试飞书推送...")

# 加载环境变量
env_file = Path('.env')
if env_file.exists():
    print("加载 .env 文件...")
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
    print("env 文件加载完成")

# 获取配置
webhook_url = os.getenv('FEISHU_WEBHOOK_URL')
print(f"飞书Webhook: {webhook_url[:50] if webhook_url else '未设置'}...")

if not webhook_url:
    print("错误: 未设置 FEISHU_WEBHOOK_URL")
    exit(1)

# 构建测试消息 - 使用新格式
test_message = {
    "content": {
        "report_type": "微信公众号AI摘要",
        "text": """公众号测试
标题测试：AI技术最新进展
摘要测试：本文介绍了最新的AI技术发展趋势，包括大模型的突破、多模态AI的应用以及未来发展方向。重点分析了技术创新对行业的影响和商业价值。
链接测试 阅读原文 | 2025-11-05 10:00:00
   https://example.com/test-article

公众号测试2
标题测试：漫剧市场分析报告
摘要测试：10月漫剧市场播放规模达到新高，头部平台格局发生变化。用户对奇幻题材偏好明显，付费模式增长迅速，预示着商业化潜力巨大。
链接测试 阅读原文 | 2025-11-05 09:30:00
   https://example.com/test-article-2""",
        "total_titles": "测试公众号: AI技术最新进展, 行业分析: 漫剧市场分析报告",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
}

try:
    print("发送测试消息到飞书...")
    
    response = requests.post(
        webhook_url,
        json=test_message,
        headers={'Content-Type': 'application/json'},
        timeout=30
    )
    
    print(f"HTTP状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"响应内容: {result}")
        
        if result.get('code') == 0 or result.get('StatusCode') == 0:
            print("推送成功！请检查您的飞书群组。")
        else:
            print(f"推送失败: {result}")
    else:
        print(f"HTTP请求失败: {response.status_code}")
        print(f"响应内容: {response.text}")
        
except Exception as e:
    print(f"发送失败: {e}")
    import traceback
    traceback.print_exc()

print("测试完成")
