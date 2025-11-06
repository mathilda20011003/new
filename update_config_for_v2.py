#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置更新脚本 - 适配WeWe RSS v2.x
"""

import os
import yaml
from pathlib import Path

def update_env_config():
    """更新环境变量配置"""
    print("🔧 更新环境变量配置...")
    
    env_file = Path('.env')
    env_content = []
    
    # 读取现有配置
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            env_content = f.readlines()
    
    # 更新WeWe RSS配置
    new_config = {
        'WEWE_RSS_BASE_URL': 'http://localhost:4000',  # WeWe RSS v2.x 地址
        'WEWE_RSS_AUTH_CODE': '123567',                # 授权码
        'WEWE_RSS_VERSION': 'v2.x',                    # 版本标识
    }
    
    # 更新或添加配置
    updated_lines = []
    existing_keys = set()
    
    for line in env_content:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key = line.split('=', 1)[0].strip()
            if key in new_config:
                updated_lines.append(f"{key}={new_config[key]}\n")
                existing_keys.add(key)
            else:
                updated_lines.append(line + '\n')
        else:
            updated_lines.append(line + '\n')
    
    # 添加新配置
    updated_lines.append('\n# WeWe RSS v2.x 配置\n')
    for key, value in new_config.items():
        if key not in existing_keys:
            updated_lines.append(f"{key}={value}\n")
    
    # 写入文件
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)
    
    print("✅ 环境变量配置已更新")

def update_wechat_accounts_config():
    """更新微信公众号配置"""
    print("🔧 更新微信公众号配置...")
    
    config_file = Path('config/wechat_accounts.yaml')
    
    if not config_file.exists():
        print("❌ 配置文件不存在")
        return
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 添加WeWe RSS v2.x相关配置
    if 'wewe_rss' not in config:
        config['wewe_rss'] = {}
    
    config['wewe_rss'].update({
        'version': 'v2.x',
        'base_url': 'http://localhost:4000',
        'auth_code': '123567',
        'auto_update': True,
        'update_schedule': '35 5,17 * * *',  # 每天5:35和17:35自动更新
        'fulltext_mode': True,
        'notes': [
            '1. 首次使用需要访问 http://localhost:4000 添加公众号',
            '2. 扫码登录微信读书账号（不要勾选24小时后自动退出）',
            '3. 添加公众号后获取Feed ID，更新下面的feed_id配置',
            '4. Feed ID格式：MP_WXS_xxxxxxxx（不需要.rss/.atom后缀）'
        ]
    })
    
    # 更新现有账号配置的注释
    if 'accounts' in config:
        for account in config['accounts']:
            if 'feed_id' in account:
                # 移除.atom后缀，WeWe RSS v2.x会自动处理
                feed_id = account['feed_id'].replace('.atom', '').replace('.rss', '')
                account['feed_id'] = feed_id
                account['_note'] = f"从WeWe RSS v2.x获取: http://localhost:4000/feeds/{feed_id}.rss"
    
    # 写入更新后的配置
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)
    
    print("✅ 微信公众号配置已更新")

def create_migration_guide():
    """创建迁移指南"""
    print("📝 创建迁移指南...")
    
    guide_content = """# WeWe RSS v2.x 升级指南

## 🎯 升级完成！

您的系统已成功升级到WeWe RSS v2.x，现在具备以下优势：

### ✅ 新功能特性
- **自动更新**：每天5:35和17:35自动更新RSS内容
- **全文输出**：支持完整文章内容抓取
- **更稳定**：v2.x版本使用全新接口，更加稳定
- **无需手动维护**：告别每天手动更新的烦恼

### 📋 下一步操作

#### 1. 启动WeWe RSS v2.x服务
```bash
chmod +x deploy_wewe_rss_v2.sh
./deploy_wewe_rss_v2.sh
```

#### 2. 配置公众号
1. 访问 http://localhost:4000
2. 使用授权码 `123567` 登录
3. 点击"账号管理" → "添加账号"
4. 扫码登录微信读书（**不要勾选24小时后自动退出**）
5. 点击"公众号源" → "添加"
6. 提交微信公众号分享链接

#### 3. 获取Feed ID并更新配置
添加公众号后，系统会显示Feed ID（如：MP_WXS_1234567890）
将这些Feed ID更新到 `config/wechat_accounts.yaml` 文件中：

```yaml
accounts:
  - name: "短剧自习室"
    feed_id: "MP_WXS_3906677264"  # 更新为实际的Feed ID
    keywords: [...]
    
  - name: "机器之心"  
    feed_id: "MP_WXS_3073282833"  # 更新为实际的Feed ID
    keywords: [...]
```

#### 4. 测试系统
```bash
# 本地测试
python test_local_changes.py full

# 或快速测试
python quick_test.py
```

### 🔄 系统架构
```
WeWe RSS v2.x (自动更新) → RSS数据 → AI摘要系统 → 飞书推送
```

### ⚠️ 注意事项
1. **添加频率**：添加公众号不要太频繁，容易被封控
2. **账号状态**：定期检查微信读书账号状态
3. **Feed ID**：每个公众号的Feed ID是唯一的，添加后不会改变

### 🎉 升级优势
- ✅ **告别手动更新**：系统自动维护RSS数据源
- ✅ **保持AI摘要**：继续使用您优化的AI摘要功能
- ✅ **稳定性提升**：v2.x版本更加稳定可靠
- ✅ **全文支持**：获取完整文章内容用于AI分析

升级完成后，您的系统将更加稳定和自动化！
"""
    
    with open('UPGRADE_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("✅ 迁移指南已创建：UPGRADE_GUIDE.md")

def main():
    """主函数"""
    print("🚀 开始配置更新...")
    print("=" * 60)
    
    try:
        # 更新环境变量
        update_env_config()
        
        # 更新微信公众号配置
        update_wechat_accounts_config()
        
        # 创建迁移指南
        create_migration_guide()
        
        print("=" * 60)
        print("🎉 配置更新完成！")
        print("")
        print("📋 下一步操作：")
        print("1. 运行部署脚本：./deploy_wewe_rss_v2.sh")
        print("2. 访问 http://localhost:4000 配置公众号")
        print("3. 更新 config/wechat_accounts.yaml 中的 feed_id")
        print("4. 运行测试：python test_local_changes.py full")
        print("")
        print("📖 详细说明请查看：UPGRADE_GUIDE.md")
        
    except Exception as e:
        print(f"❌ 配置更新失败：{e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
