#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from pathlib import Path

print("🔍 检查WeWe RSS服务...")

# 加载环境变量
env_file = Path('.env')
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

base_url = os.getenv('WEWE_RSS_BASE_URL', 'https://ssys2025.zeabur.app').rstrip('/')
print(f"📡 WeWe RSS服务地址: {base_url}")

# 1. 检查服务是否可访问
try:
    print("\n1️⃣ 检查服务状态...")
    response = requests.get(base_url, timeout=10)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ 服务正常")
    else:
        print("   ❌ 服务异常")
except Exception as e:
    print(f"   ❌ 服务不可访问: {e}")

# 2. 尝试获取RSS列表或首页信息
try:
    print("\n2️⃣ 尝试获取RSS信息...")
    
    # 尝试常见的RSS端点
    endpoints = [
        '/rss',
        '/feeds',
        '/api/feeds',
        '/list',
        ''
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            print(f"   尝试: {url}")
            response = requests.get(url, timeout=5)
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text[:500]  # 只显示前500字符
                print(f"   内容预览: {content}...")
                break
                
        except Exception as e:
            print(f"   错误: {e}")
            
except Exception as e:
    print(f"❌ 获取RSS信息失败: {e}")

# 3. 尝试一些常见的测试Feed ID
print("\n3️⃣ 尝试常见的Feed ID...")
test_feeds = [
    'test.atom',
    'demo.atom', 
    'sample.atom',
    'MP_WXS_test.atom'
]

for feed_id in test_feeds:
    try:
        url = f"{base_url}/rss/{feed_id}"
        print(f"   测试: {url}")
        response = requests.get(url, timeout=5)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ 找到可用Feed: {feed_id}")
            break
        elif response.status_code == 404:
            print(f"   ❌ Feed不存在")
        else:
            print(f"   ⚠️  其他状态: {response.status_code}")
            
    except Exception as e:
        print(f"   错误: {e}")

print("\n📋 建议:")
print("1. 检查WeWe RSS服务是否正确配置")
print("2. 确认Feed ID是否正确")
print("3. 可能需要重新添加公众号到WeWe RSS")
print("4. 或者使用其他可用的RSS源进行测试")

print("\n✅ 检查完成")
