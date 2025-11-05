# 🤖 微信公众号AI摘要爬虫 - 完整部署指南

## 📋 项目概述

这是一个自动化的微信公众号AI摘要系统，每天定时：
1. 从WeWe RSS获取指定公众号的最新文章
2. 根据关键词筛选相关文章
3. 使用AI生成专业摘要
4. 推送到飞书群组

## 🚀 快速部署（5分钟完成）

### 步骤1：推送代码到GitHub

```bash
# 添加所有文件
git add .

# 提交更改
git commit -m "部署微信公众号AI摘要爬虫"

# 推送到GitHub
git push origin main
```

### 步骤2：配置GitHub Secrets

在GitHub仓库页面：
1. 点击 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret** 添加以下密钥：

#### 必需配置：
- **FEISHU_WEBHOOK_URL**: `https://www.feishu.cn/flow/api/trigger-webhook/您的webhook地址`
- **OPENROUTER_API_KEY**: `sk-or-v1-您的OpenRouter密钥`
- **WEWE_RSS_BASE_URL**: `https://ssys2025.zeabur.app`

#### 可选配置：
- **AI_MODEL**: `google/gemini-2.5-flash-lite-preview-09-2025` (默认模型)

### 步骤3：验证部署

1. 进入GitHub仓库的 **Actions** 页面
2. 找到 **WeChat AI Summary Crawler** 工作流
3. 点击 **Run workflow** 进行手动测试
4. 检查飞书群组是否收到消息

## ⏰ 运行时间设置

### 当前配置
- **自动运行**: 每天上午10:00（北京时间）
- **手动触发**: 随时可用

### 修改运行时间
编辑 `.github/workflows/wechat-crawler.yml` 中的时间：

```yaml
schedule:
  - cron: '0 2 * * *'  # 北京时间10:00 = UTC 02:00
```

**常用时间对照**：
- 08:00 → `'0 0 * * *'`
- 09:00 → `'0 1 * * *'`  
- 10:00 → `'0 2 * * *'` ✅ 当前设置
- 11:00 → `'0 3 * * *'`

## 🔧 手动触发方法

### 方法1：GitHub网页（推荐）
1. 打开GitHub仓库 → **Actions**
2. 选择 **WeChat AI Summary Crawler**
3. 点击 **Run workflow** → **Run workflow**

### 方法2：本地脚本
```bash
# 确保.env文件配置正确
python manual_trigger.py
```

### 方法3：GitHub CLI
```bash
# 安装GitHub CLI后
gh workflow run "WeChat AI Summary Crawler"
```

## 📊 监控和维护

### 查看运行日志
1. GitHub仓库 → **Actions**
2. 点击具体的运行记录
3. 展开步骤查看详细日志

### 常见问题解决

| 问题 | 解决方案 |
|------|----------|
| API密钥错误 | 检查GitHub Secrets中的密钥 |
| 飞书推送失败 | 验证Webhook URL是否正确 |
| RSS获取失败 | 检查WeWe RSS服务状态 |
| 时间显示错误 | 查看时间解析日志 |

## 📝 配置文件说明

### config/wechat_accounts.yaml
```yaml
accounts:
  - name: "机器之心"
    feed_id: "MP_WXS_3073282833"
    keywords:
      - "AI"
      - "大模型"
      - "人工智能"
```

### 获取Feed ID步骤
1. 在WeWe RSS中添加公众号
2. 复制生成的Feed ID
3. 更新配置文件

## 🎯 部署检查清单

部署完成后请确认：

- [ ] GitHub Secrets已配置
- [ ] 工作流文件已更新  
- [ ] 配置文件格式正确
- [ ] 手动触发测试成功
- [ ] 飞书群组收到消息
- [ ] 时间显示正确
- [ ] 格式简洁无重复

## 🔄 从旧系统迁移

如果您之前使用的是新闻爬虫系统：

1. **旧系统已自动禁用** - `crawler.yml`中的定时任务已注释
2. **新系统已启用** - `wechat-crawler.yml`将接管推送任务
3. **配置独立** - 两个系统使用不同的配置文件

## 📞 技术支持

### 获取帮助
1. 查看GitHub Actions运行日志
2. 检查飞书工作流配置
3. 验证WeWe RSS服务状态
4. 确认API密钥有效性

### 紧急处理
如需紧急推送，使用本地手动触发：
```bash
python manual_trigger.py
```

## 🎉 部署完成

恭喜！您的微信公众号AI摘要系统已成功部署。

**下一步**：
- 等待明天上午10点的自动推送
- 或立即进行手动测试
- 根据需要调整公众号和关键词配置

**享受每日精准的AI摘要推送！** 🚀
