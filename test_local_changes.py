#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地测试脚本 - 使用测试机器人
用于测试代码改动，不影响工作群
"""

import os
import sys
from datetime import datetime

# 设置测试环境变量
os.environ['FEISHU_WEBHOOK_URL'] = 'https://open.feishu.cn/open-apis/bot/v2/hook/9803c75c-0a2f-4044-b973-f98441f1804b'

# 导入主程序
from run_api_crawler import main, send_to_feishu

def test_format_changes():
    """测试格式改动"""
    print("🧪 测试新的统一格式...")
    
    # 模拟文章数据
    test_articles = [
        {
            'account_name': '机器之心',
            'title': '数字生命「培养皿」里，AI竟然学会了打架、结盟、抢地盘',
            'ai_summary': 'AI在模拟环境中展现出复杂的社会行为（竞争、合作），紧密的每行不同的内容就行了',
            'link': 'https://mp.weixin.qq.com/s/example1',
            'published': '2025-11-05 10:30:00'
        },
        {
            'account_name': '短剧自习室',
            'title': '快讯｜「红果免费追剧」App上线，抖音再下一城',
            'ai_summary': '抖音推出「红果免费追剧」标志其内容生态向短剧/微剧垂类深度渗透，利用其庞大流量基础和推荐算法，直接冲击专业短剧平台，比竞对化了抖音构筑与竞对的差异化，成为短剧赛道内容分发的新变量',
            'link': 'https://mp.weixin.qq.com/s/example2',
            'published': '2025-11-02 14:46:44'
        },
        {
            'account_name': '漫剧有数',
            'title': '日播2000万，席卷+后台的漫剧情款公式来了？',
            'ai_summary': '席卷+后台漫剧模式在短剧平台用户增长乏力，日播千万级数据显示了待发掘的巨大驱动力，其核心价值在于内容生产效率与用户粘性的平衡，技术实现难度相对可控，重要流量分配机制',
            'link': 'https://mp.weixin.qq.com/s/example3',
            'published': '2025-11-04 07:14:58'
        }
    ]
    
    print(f"📊 测试数据：{len(test_articles)} 篇文章")
    print("📤 发送到测试机器人...")
    
    # 调用发送函数
    success = send_to_feishu(test_articles)
    
    if success:
        print("✅ 测试成功！")
        print("📋 新格式特点：")
        print("   - 统一格式：📍 📰 💡 🔗")
        print("   - 紧密排列，无多余空行")
        print("   - 文章间用分隔线分隔")
        print("   - 移除了加粗等格式标记")
        return True
    else:
        print("❌ 测试失败！")
        return False

def test_ai_summary_format():
    """测试AI摘要格式清理"""
    print("\n🔬 测试AI摘要格式清理...")
    
    from wechat_rss.ai_summarizer import AISummarizer
    
    # 创建摘要器实例
    summarizer = AISummarizer()
    
    # 测试格式清理功能
    test_texts = [
        "**短视频平台内容付费转化的强劲势头**，这是加粗文本",
        "*斜体文本*和__下划线加粗__的混合",
        "正常文本和`代码标记`以及~~删除线~~",
        "**多个** *格式* `混合` 的__复杂__文本"
    ]
    
    print("📝 测试格式清理：")
    for i, text in enumerate(test_texts, 1):
        cleaned = summarizer._clean_markdown_formatting(text)
        print(f"   {i}. 原文：{text}")
        print(f"      清理后：{cleaned}")
        print()
    
    return True

def run_full_test():
    """运行完整测试"""
    print("🚀 运行完整的微信公众号爬虫测试...")
    
    # 设置必要的环境变量
    required_env_vars = {
        'OPENROUTER_API_KEY': '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',
        'WEWE_RSS_BASE_URL': 'https://ssys2025.zeabur.app',
        'AI_MODEL': 'google/gemini-2.5-flash-lite-preview-09-2025'
    }
    
    for key, value in required_env_vars.items():
        os.environ[key] = value
    
    print("📡 环境变量已设置")
    print("🔗 使用测试机器人：https://open.feishu.cn/open-apis/bot/v2/hook/9803c75c-0a2f-4044-b973-f98441f1804b")
    
    try:
        # 运行主程序
        main()
        print("✅ 完整测试成功！")
        return True
    except Exception as e:
        print(f"❌ 完整测试失败：{e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 本地测试脚本 - 使用测试机器人")
    print("=" * 60)
    print(f"🕐 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🤖 测试机器人：https://open.feishu.cn/open-apis/bot/v2/hook/9803c75c-0a2f-4044-b973-f98441f1804b")
    print()
    
    # 选择测试类型
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
    else:
        print("请选择测试类型：")
        print("1. format  - 测试格式改动")
        print("2. ai      - 测试AI摘要格式清理")
        print("3. full    - 运行完整测试")
        print()
        choice = input("请输入选择 (1/2/3): ").strip()
        
        if choice == "1":
            test_type = "format"
        elif choice == "2":
            test_type = "ai"
        elif choice == "3":
            test_type = "full"
        else:
            test_type = "format"
    
    print(f"🎯 执行测试类型：{test_type}")
    print("-" * 60)
    
    success = False
    
    if test_type == "format":
        success = test_format_changes()
    elif test_type == "ai":
        success = test_ai_summary_format()
    elif test_type == "full":
        success = run_full_test()
    else:
        print("❌ 未知的测试类型")
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 测试完成！")
        print("✅ 所有改动都可以正常工作")
        print("📝 现在可以安全地提交代码到仓库")
    else:
        print("❌ 测试失败！")
        print("🔧 请检查代码并修复问题")
    print("=" * 60)
