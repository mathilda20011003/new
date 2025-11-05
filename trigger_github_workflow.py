#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过GitHub API手动触发工作流
需要GitHub Personal Access Token
"""

import os
import sys
import requests
import json
from datetime import datetime

def get_github_config():
    """获取GitHub配置"""
    config = {
        'token': os.getenv('GITHUB_TOKEN'),
        'owner': os.getenv('GITHUB_OWNER'),  # 您的GitHub用户名
        'repo': os.getenv('GITHUB_REPO'),    # 仓库名称
        'workflow': 'wechat-crawler.yml'     # 工作流文件名
    }
    
    # 检查必需的配置
    missing = [k for k, v in config.items() if not v and k != 'workflow']
    if missing:
        print(f"❌ 缺少GitHub配置: {', '.join(missing)}")
        print("\n请设置以下环境变量:")
        print("- GITHUB_TOKEN: GitHub Personal Access Token")
        print("- GITHUB_OWNER: GitHub用户名")
        print("- GITHUB_REPO: 仓库名称")
        print("\n或者直接在脚本中输入:")
        
        if not config['token']:
            config['token'] = input("GitHub Token: ").strip()
        if not config['owner']:
            config['owner'] = input("GitHub用户名: ").strip()
        if not config['repo']:
            config['repo'] = input("仓库名称: ").strip()
    
    return config

def trigger_workflow(config):
    """触发GitHub工作流"""
    url = f"https://api.github.com/repos/{config['owner']}/{config['repo']}/actions/workflows/{config['workflow']}/dispatches"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f"token {config['token']}",
        'Content-Type': 'application/json'
    }
    
    data = {
        'ref': 'main'  # 或者您的默认分支名
    }
    
    print(f"🚀 触发工作流: {config['workflow']}")
    print(f"📍 仓库: {config['owner']}/{config['repo']}")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 204:
            print("✅ 工作流触发成功！")
            print(f"🔗 查看运行状态: https://github.com/{config['owner']}/{config['repo']}/actions")
            return True
        else:
            print(f"❌ 工作流触发失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def check_workflow_runs(config):
    """检查最近的工作流运行"""
    url = f"https://api.github.com/repos/{config['owner']}/{config['repo']}/actions/workflows/{config['workflow']}/runs"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f"token {config['token']}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            runs = response.json().get('workflow_runs', [])
            if runs:
                print(f"\n📊 最近的工作流运行:")
                for i, run in enumerate(runs[:3], 1):
                    status = run['status']
                    conclusion = run['conclusion']
                    created_at = run['created_at']
                    
                    status_emoji = {
                        'completed': '✅' if conclusion == 'success' else '❌',
                        'in_progress': '🔄',
                        'queued': '⏳'
                    }.get(status, '❓')
                    
                    print(f"  {i}. {status_emoji} {status} - {created_at}")
            else:
                print("📊 暂无工作流运行记录")
        else:
            print(f"❌ 获取工作流运行失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 获取工作流运行失败: {e}")

def main():
    """主函数"""
    print("🤖 GitHub工作流手动触发工具")
    print("=" * 50)
    
    # 获取GitHub配置
    config = get_github_config()
    
    # 检查最近的运行
    check_workflow_runs(config)
    
    # 确认触发
    print(f"\n准备触发工作流: {config['workflow']}")
    confirm = input("是否继续？(y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ 用户取消操作")
        sys.exit(0)
    
    # 触发工作流
    success = trigger_workflow(config)
    
    if success:
        print("\n🎉 工作流触发成功！")
        print("请稍等几分钟，然后检查GitHub Actions页面查看运行状态。")
    else:
        print("\n❌ 工作流触发失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()
