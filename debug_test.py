#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json
from pathlib import Path
from datetime import datetime

print("开始调试测试...")

# 加载环境变量
env_file = Path('.env')
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

webhook_url = os.getenv('FEISHU_WEBHOOK_URL')
print(f"Webhook URL: {webhook_url}")

# 简单的测试消息
test_message = {
    "content": {
        "report_type": "测试报告",
        "text": "这是一个测试消息",
        "total_titles": "测试标题",
        "timestamp": "2025-11-05 10:30:00"
    }
}

print("准备发送请求...")

try:
    print("发送中...")
    response = requests.post(
        webhook_url,
        json=test_message,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
except requests.exceptions.Timeout:
    print("请求超时")
except requests.exceptions.RequestException as e:
    print(f"请求异常: {e}")
except Exception as e:
    print(f"其他错误: {e}")

print("调试完成")
