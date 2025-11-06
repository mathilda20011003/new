#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

print("开始测试...")

import os
import sys
from pathlib import Path

# 加载环境变量
env_file = Path('.env')
if env_file.exists():
    print("📁 加载 .env 文件...")
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
    print("✅ .env 文件加载完成")

# 检查环境变量
webhook_url = os.getenv('FEISHU_WEBHOOK_URL')
api_key = os.getenv('OPENROUTER_API_KEY')

print(f"✅ 飞书Webhook: {webhook_url[:50] if webhook_url else '未设置'}...")
print(f"✅ OpenRouter API: {api_key[:20] if api_key else '未设置'}...")

# 添加路径
sys.path.append('.')
sys.path.append('wechat_rss')

# 测试导入
try:
    from wechat_rss.feishu_sender import FeishuSender
    print("✅ FeishuSender 导入成功")
    
    # 创建测试数据
    test_articles = [
        {
            'title': '测试文章标题',
            'ai_summary': '这是一个测试摘要，用于验证新的推送格式是否正常工作。',
            'link': 'https://example.com/test',
            'published': '2025-11-05 10:00:00',
            'account_name': '测试公众号'
        }
    ]
    
    # 发送测试
    sender = FeishuSender(webhook_url)
    print("📤 开始发送测试消息...")
    
    result = sender.send_articles(test_articles)
    
    if result:
        print("🎉 测试推送成功！")
    else:
        print("❌ 测试推送失败")
        
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print("✅ 测试完成")
