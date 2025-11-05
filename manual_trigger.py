#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动触发微信公众号AI摘要爬虫
用于本地测试和紧急推送
"""

import os
import sys
import subprocess
from datetime import datetime

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    required_vars = [
        'FEISHU_WEBHOOK_URL',
        'OPENROUTER_API_KEY',
        'WEWE_RSS_BASE_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少环境变量: {', '.join(missing_vars)}")
        print("请检查 .env 文件或设置环境变量")
        return False
    
    print("✅ 环境配置检查通过")
    return True

def check_config_files():
    """检查配置文件"""
    print("📁 检查配置文件...")
    
    config_file = "config/wechat_accounts.yaml"
    if not os.path.exists(config_file):
        print(f"❌ 配置文件不存在: {config_file}")
        return False
    
    print("✅ 配置文件检查通过")
    return True

def run_crawler():
    """运行爬虫"""
    print("🚀 开始运行微信公众号AI摘要爬虫...")
    print(f"⏰ 运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # 运行爬虫脚本
        result = subprocess.run([
            sys.executable, "run_api_crawler.py"
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print("=" * 60)
            print("🎉 爬虫运行成功！")
            return True
        else:
            print("=" * 60)
            print(f"❌ 爬虫运行失败，退出码: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ 运行爬虫时出错: {e}")
        return False

def main():
    """主函数"""
    print("🤖 微信公众号AI摘要爬虫 - 手动触发工具")
    print("=" * 60)
    
    # 检查环境
    if not check_environment():
        sys.exit(1)
    
    # 检查配置文件
    if not check_config_files():
        sys.exit(1)
    
    # 确认运行
    print("\n📋 准备运行爬虫，将会:")
    print("1. 从WeWe RSS获取最新文章")
    print("2. 根据关键词筛选文章")
    print("3. 生成AI摘要")
    print("4. 推送到飞书群组")
    
    confirm = input("\n是否继续？(y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ 用户取消操作")
        sys.exit(0)
    
    # 运行爬虫
    success = run_crawler()
    
    if success:
        print("\n✅ 手动触发完成！请检查飞书群组是否收到消息。")
        sys.exit(0)
    else:
        print("\n❌ 手动触发失败！请检查错误信息。")
        sys.exit(1)

if __name__ == "__main__":
    main()
