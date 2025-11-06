#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号RSS爬虫启动脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'wechat_rss'))

# 加载 .env 文件
def load_env_file():
    """加载 .env 文件中的环境变量"""
    env_file = Path(current_dir) / '.env'
    if env_file.exists():
        print("📁 加载 .env 文件...")
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print("✅ .env 文件加载完成")
    else:
        print("⚠️  未找到 .env 文件，使用系统环境变量")

def main():
    """主函数"""
    print("🚀 启动微信公众号RSS爬虫...")
    print("=" * 60)

    # 加载环境变量
    load_env_file()

    # 检查配置文件
    config_path = os.path.join(current_dir, 'config', 'wechat_accounts.yaml')
    if not os.path.exists(config_path):
        print(f"❌ 配置文件不存在: {config_path}")
        return

    # 检查环境变量
    feishu_webhook = os.getenv('FEISHU_WEBHOOK_URL')
    if not feishu_webhook:
        print("⚠️  警告: 未设置 FEISHU_WEBHOOK_URL 环境变量，将无法推送到飞书")
        print("💡 提示: 请创建 .env 文件或设置环境变量")
    else:
        print(f"✅ 飞书Webhook已配置: {feishu_webhook[:50]}...")
    
    try:
        # 导入并运行爬虫
        from wechat_rss.wechat_rss_crawler import WeChatRSSCrawler
        
        crawler = WeChatRSSCrawler(config_path)
        crawler.run()
        
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
