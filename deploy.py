#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键部署脚本
自动执行Git提交和推送
"""

import os
import sys
import subprocess
from datetime import datetime

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description}成功")
            if result.stdout.strip():
                print(f"   输出: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description}失败")
            if result.stderr.strip():
                print(f"   错误: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description}异常: {e}")
        return False

def check_git_status():
    """检查Git状态"""
    print("🔍 检查Git状态...")
    
    # 检查是否有未提交的更改
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    
    if result.stdout.strip():
        print("📝 发现未提交的更改:")
        changes = result.stdout.strip().split('\n')
        for change in changes[:10]:  # 只显示前10个
            print(f"   {change}")
        if len(changes) > 10:
            print(f"   ... 还有 {len(changes) - 10} 个文件")
        return True
    else:
        print("✅ 没有未提交的更改")
        return False

def deploy():
    """执行部署"""
    print("🚀 开始部署微信公众号AI摘要爬虫")
    print(f"⏰ 部署时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 检查Git状态
    has_changes = check_git_status()
    
    if not has_changes:
        print("ℹ️ 没有需要提交的更改，跳过Git操作")
        print("\n📋 请手动完成以下步骤:")
        print("1. 在GitHub仓库中配置Secrets")
        print("2. 手动触发工作流进行测试")
        return True
    
    # 确认部署
    print(f"\n准备提交并推送所有更改到GitHub仓库")
    confirm = input("是否继续？(y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ 用户取消部署")
        return False
    
    # Git操作
    steps = [
        ("git add .", "添加所有文件"),
        (f'git commit -m "部署微信公众号AI摘要爬虫 - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"', "提交更改"),
        ("git push origin main", "推送到GitHub")
    ]
    
    for command, description in steps:
        if not run_command(command, description):
            print(f"\n❌ 部署失败在步骤: {description}")
            return False
    
    print("\n🎉 代码推送成功！")
    
    # 显示后续步骤
    print("\n📋 接下来请完成以下步骤:")
    print("1. 在GitHub仓库中配置以下Secrets:")
    print("   - FEISHU_WEBHOOK_URL")
    print("   - OPENROUTER_API_KEY") 
    print("   - WEWE_RSS_BASE_URL")
    print("2. 进入GitHub仓库的Actions页面")
    print("3. 找到'WeChat AI Summary Crawler'工作流")
    print("4. 点击'Run workflow'进行手动测试")
    print("5. 检查飞书群组是否收到消息")
    
    print(f"\n🔗 GitHub仓库地址: https://github.com/YOUR_USERNAME/YOUR_REPO")
    print("📖 详细说明请参考: README_部署指南.md")
    
    return True

def main():
    """主函数"""
    try:
        success = deploy()
        if success:
            print("\n✅ 部署脚本执行完成！")
            sys.exit(0)
        else:
            print("\n❌ 部署失败！")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ 用户中断部署")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 部署异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
