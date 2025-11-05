#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终部署测试脚本
验证所有组件是否正常工作
"""

import os
import sys
import yaml
import requests
import feedparser
from datetime import datetime
from dotenv import load_dotenv

def print_header(title):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)

def test_environment():
    """测试环境变量"""
    print_header("环境变量检查")
    
    # 加载.env文件
    load_dotenv()
    
    required_vars = {
        'FEISHU_WEBHOOK_URL': '飞书Webhook URL',
        'OPENROUTER_API_KEY': 'OpenRouter API密钥',
        'WEWE_RSS_BASE_URL': 'WeWe RSS服务地址'
    }
    
    all_good = True
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if value:
            # 隐藏敏感信息
            if 'KEY' in var or 'TOKEN' in var:
                display_value = f"{value[:10]}...{value[-10:]}" if len(value) > 20 else "***"
            else:
                display_value = value
            print(f"✅ {desc}: {display_value}")
        else:
            print(f"❌ {desc}: 未设置")
            all_good = False
    
    return all_good

def test_config_files():
    """测试配置文件"""
    print_header("配置文件检查")
    
    config_file = "config/wechat_accounts.yaml"
    
    if not os.path.exists(config_file):
        print(f"❌ 配置文件不存在: {config_file}")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if not config or 'accounts' not in config:
            print("❌ 配置文件格式错误：缺少accounts字段")
            return False
        
        accounts = config['accounts']
        if not accounts:
            print("❌ 配置文件中没有配置任何公众号")
            return False
        
        print(f"✅ 配置文件格式正确")
        print(f"📊 配置了 {len(accounts)} 个公众号:")
        
        for i, account in enumerate(accounts, 1):
            name = account.get('name', '未知')
            feed_id = account.get('feed_id', '未设置')
            keywords = account.get('keywords', [])
            print(f"  {i}. {name} (Feed ID: {feed_id}, 关键词: {len(keywords)}个)")
        
        return True
        
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False

def test_wewe_rss():
    """测试WeWe RSS服务"""
    print_header("WeWe RSS服务检查")
    
    base_url = os.getenv('WEWE_RSS_BASE_URL')
    if not base_url:
        print("❌ WeWe RSS服务地址未配置")
        return False
    
    try:
        # 测试服务根路径
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ WeWe RSS服务正常: {base_url}")
        else:
            print(f"⚠️ WeWe RSS服务响应异常: {response.status_code}")
        
        # 测试具体的RSS feed
        test_feed_id = "MP_WXS_3073282833"  # 机器之心
        rss_url = f"{base_url}/feeds/{test_feed_id}"
        
        response = requests.get(rss_url, timeout=10)
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            if feed.entries:
                print(f"✅ RSS解析正常，获取到 {len(feed.entries)} 篇文章")
                
                # 测试时间解析
                entry = feed.entries[0]
                time_info = entry.get('published', '') or entry.get('updated', '') or entry.get('date', '')
                if time_info:
                    try:
                        from dateutil import parser
                        dt = parser.parse(time_info)
                        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                        print(f"✅ 时间解析正常: {formatted_time}")
                    except Exception as e:
                        print(f"⚠️ 时间解析异常: {e}")
                else:
                    print("⚠️ 未找到时间信息")
            else:
                print("⚠️ RSS中没有文章")
        else:
            print(f"❌ RSS获取失败: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ WeWe RSS服务测试失败: {e}")
        return False

def test_openrouter_api():
    """测试OpenRouter API"""
    print_header("OpenRouter API检查")
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OpenRouter API密钥未配置")
        return False
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # 测试API连接
        response = requests.get('https://openrouter.ai/api/v1/models', headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ OpenRouter API连接正常")
            
            # 检查模型可用性
            models = response.json().get('data', [])
            model_name = os.getenv('AI_MODEL', 'google/gemini-2.5-flash-lite-preview-09-2025')
            
            model_found = any(model.get('id') == model_name for model in models)
            if model_found:
                print(f"✅ AI模型可用: {model_name}")
            else:
                print(f"⚠️ AI模型未找到: {model_name}")
                print("将使用默认可用模型")
            
            return True
        else:
            print(f"❌ OpenRouter API连接失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ OpenRouter API测试失败: {e}")
        return False

def test_feishu_webhook():
    """测试飞书Webhook"""
    print_header("飞书Webhook检查")
    
    webhook_url = os.getenv('FEISHU_WEBHOOK_URL')
    if not webhook_url:
        print("❌ 飞书Webhook URL未配置")
        return False
    
    # 发送测试消息
    test_message = {
        "content": {
            "report_type": "微信公众号AI摘要",
            "text": "🧪 这是一条部署测试消息\n\n📍 测试公众号\n📰 测试文章标题\n💡 这是一条测试摘要，用于验证系统部署是否成功。\n🔗 阅读原文 | 2025-11-05 10:00:00\n   https://example.com/test",
            "total_titles": "",
            "timestamp": ""
        }
    }
    
    try:
        response = requests.post(webhook_url, json=test_message, timeout=10)
        
        if response.status_code == 200:
            print("✅ 飞书Webhook测试成功")
            print("📱 请检查飞书群组是否收到测试消息")
            return True
        else:
            print(f"❌ 飞书Webhook测试失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 飞书Webhook测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 微信公众号AI摘要爬虫 - 最终部署测试")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("环境变量", test_environment),
        ("配置文件", test_config_files),
        ("WeWe RSS服务", test_wewe_rss),
        ("OpenRouter API", test_openrouter_api),
        ("飞书Webhook", test_feishu_webhook)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 汇总结果
    print_header("测试结果汇总")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统已准备就绪。")
        print("\n下一步:")
        print("1. 推送代码到GitHub仓库")
        print("2. 配置GitHub Secrets")
        print("3. 手动触发工作流进行最终测试")
        return True
    else:
        print(f"\n⚠️ 有 {total - passed} 项测试失败，请修复后重新测试。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
