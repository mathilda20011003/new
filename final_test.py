#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json
from pathlib import Path
from datetime import datetime

# 设置UTF-8编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

print("🚀 开始最终格式测试...")

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

# 获取配置
webhook_url = os.getenv('FEISHU_WEBHOOK_URL')
print(f"✅ 飞书Webhook: {webhook_url[:50] if webhook_url else '未设置'}...")

if not webhook_url:
    print("❌ 错误: 未设置 FEISHU_WEBHOOK_URL")
    exit(1)

# 构建测试消息 - 使用完整的新格式（包含emoji）
test_message = {
    "content": {
        "report_type": "微信公众号AI摘要",
        "text": """📍 海外独角兽
📰 Vibe Working: AI 编码泛化的终局想象 | AGIX PM Notes
💡 文章探讨了"Vibe Working"的概念，即通过自然语言描述目标，由AI自动生成代码或完成工作。其核心在于环境需具备可判定性、稳定上下文和可控执行。作者认为，将这一模式从编码推广到更广泛的办公、营销等领域，需要环境和工作流本身"API化"，并指向代码化的工作流管理和作为企业Context的数字孪生两个方向。
🔗 阅读原文 | 2025-09-15 20:02:58
   https://mp.weixin.qq.com/s/example1

📍 AI产品阿颂
📰 太上头了，字节的新模型。
💡 文章分享了字节跳动最新发布的图像创作模型Seedream 4.0的实测体验。该模型在中文、动漫等场景的能力被认为超越Nano Banana，并在第三方评测中拿下文生图和图像编辑双第一。作者通过多个实际案例展示了Seedream 4.0的强大功能，包括生成海报、手机壁纸、文创产品、证件照、中秋海报、绘本、建筑漫画、连环画和小红书封面等，强调其指令遵循能力强、生图速度快、支持多图融合、中文排版靠谱且画质极高。目前用户可在火山方舟免费体验该模型。
🔗 阅读原文 | 2025-09-15 17:24:18
   https://mp.weixin.qq.com/s/example2

📍 漫剧有数
📰 10月漫剧市场播放量超60亿，头部平台格局发生变化
💡 10月漫剧市场播放规模达61.46亿，显示强劲增长势头，每周上新超千部。头部玩家格局微调，市场集中度变化值得关注。观众对"奇幻"题材偏好显著，月增量超亿。付费漫剧增速领先免费模式，预示商业化潜力加大。奇幻/末日题材是当前重要的商业增长点，AI技术正驱动解说漫内容生产流水线化。
🔗 阅读原文 | 2025-10-28 14:30:00
   https://mp.weixin.qq.com/s/example3""",
        "total_titles": "海外独角兽: Vibe Working: AI 编码泛化的终局想象, AI产品阿颂: 太上头了，字节的新模型, 漫剧有数: 10月漫剧市场播放量超60亿",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
}

try:
    print("📤 发送完整格式测试消息到飞书...")
    
    response = requests.post(
        webhook_url,
        json=test_message,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    
    print(f"📊 HTTP状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"📋 响应内容: {result}")
        
        if result.get('code') == 0 or result.get('StatusCode') == 0:
            print("🎉 推送成功！请检查您的飞书群组，应该能看到完整的新格式：")
            print("   📍 公众号名称")
            print("   📰 文章标题") 
            print("   💡 AI智能摘要")
            print("   🔗 阅读原文链接 + ⏰ 发布时间")
        else:
            print(f"❌ 推送失败: {result}")
    else:
        print(f"❌ HTTP请求失败: {response.status_code}")
        print(f"📄 响应内容: {response.text}")
        
except Exception as e:
    print(f"❌ 发送失败: {e}")
    import traceback
    traceback.print_exc()

print("✅ 测试完成")
