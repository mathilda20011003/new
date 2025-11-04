# 微信公众号 AI 助手集成方案

> 📌 **目标**：在现有 TrendRadar 项目基础上，增加微信公众号文章爬取、AI 总结、飞书推送功能  
> 👤 **适用人群**：零基础实习生  
> ⏰ **预计时间**：4-6 小时（今天完成）

---

## 📋 目录

1. [方案概述](#1-方案概述)
2. [技术架构](#2-技术架构)
3. [准备工作](#3-准备工作)
4. [详细实施步骤](#4-详细实施步骤)
5. [测试与调试](#5-测试与调试)
6. [常见问题](#6-常见问题)

---

## 1. 方案概述

### 1.1 功能需求

✅ **爬取微信公众号文章**（基于 WeWe RSS）  
✅ **关键词筛选**（复用现有的 frequency_words.txt）  
✅ **AI 总结**（使用 DeepSeek/ChatGPT/通义千问等）  
✅ **飞书推送**（复用现有的飞书机器人）  
✅ **定时发送**（每日定时 + 手动触发）

### 1.2 工作流程

```
微信公众号 → WeWe RSS → 获取文章列表 → 关键词筛选 → AI 总结 → 飞书推送
```

### 1.3 技术选型

| 组件 | 技术方案 | 说明 |
|------|---------|------|
| 公众号爬取 | WeWe RSS | 开源项目，基于微信读书 |
| AI 总结 | DeepSeek API | 免费额度大，性价比高 |
| 飞书推送 | 现有机器人 | 复用已配置的飞书 Webhook |
| 定时任务 | GitHub Actions | 与现有项目一致 |
| 数据存储 | JSON 文件 | 轻量级，易于调试 |

---

## 2. 技术架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Actions                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │  定时触发 (每天 8:00) / 手动触发                  │  │
│  └──────────────────────────────────────────────────┘  │
│                          ↓                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Python 脚本: wechat_rss_crawler.py              │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │ 1. 从 WeWe RSS 获取文章列表                │  │  │
│  │  │ 2. 关键词筛选 (frequency_words.txt)        │  │  │
│  │  │ 3. 调用 AI API 生成摘要                    │  │  │
│  │  │ 4. 格式化消息                              │  │  │
│  │  │ 5. 推送到飞书                              │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
   WeWe RSS API        DeepSeek API         飞书 Webhook
```

### 2.2 文件结构

```
d:\new\
├── config/
│   ├── config.yaml                    # 现有配置
│   ├── frequency_words.txt            # 现有关键词
│   └── wechat_accounts.yaml           # 新增：公众号配置
├── wechat_rss/                        # 新增目录
│   ├── wechat_rss_crawler.py          # 主爬虫脚本
│   ├── ai_summarizer.py               # AI 总结模块
│   ├── feishu_sender.py               # 飞书推送模块
│   └── utils.py                       # 工具函数
├── .github/workflows/
│   └── wechat-crawler.yml             # 新增：公众号爬虫定时任务
└── README-WeChat-RSS.md               # 新增：使用文档
```

---

## 3. 准备工作

### 3.1 部署 WeWe RSS（30分钟）

#### 方案一：使用 Zeabur 一键部署（推荐）

1. **注册 Zeabur 账号**
   - 访问：https://zeabur.com
   - 使用 GitHub 账号登录

2. **一键部署 WeWe RSS**
   - 访问：https://zeabur.com/templates/DI9BBD
   - 点击 "Deploy" 按钮
   - 等待部署完成（约 2-3 分钟）

3. **配置环境变量**
   - `AUTH_CODE`: 设置为 `123456`（你的访问密码）
   - `DATABASE_URL`: 自动配置（无需修改）

4. **获取访问地址**
   - 部署完成后，复制你的服务地址（类似：`https://xxx.zeabur.app`）
   - 保存到记事本，后面会用到

#### 方案二：使用 Docker 本地部署（备选）

```bash
# 1. 创建网络
docker network create wewe-rss

# 2. 启动数据库
docker run -d \
  --name db \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e TZ='Asia/Shanghai' \
  -e MYSQL_DATABASE='wewe-rss' \
  -v db_data:/var/lib/mysql \
  --network wewe-rss \
  mysql:8.3.0 --mysql-native-password=ON

# 3. 启动 WeWe RSS
docker run -d \
  --name wewe-rss \
  -p 4000:4000 \
  -e DATABASE_URL='mysql://root:123456@db:3306/wewe-rss?schema=public&connect_timeout=30&pool_timeout=30&socket_timeout=30' \
  -e AUTH_CODE=123456 \
  --network wewe-rss \
  cooderl/wewe-rss:latest
```

### 3.2 添加微信公众号（10分钟）

1. **登录微信读书**
   - 打开 WeWe RSS 网页（你的 Zeabur 地址）
   - 点击"账号管理" → "添加账号"
   - 微信扫码登录微信读书
   - ⚠️ **注意**：不要勾选"24小时后自动退出"

2. **添加公众号**
   - 点击"公众号源" → "添加"
   - 获取公众号分享链接：
     - 打开微信 → 找到公众号
     - 点击右上角"..." → "分享" → "复制链接"
   - 粘贴链接到 WeWe RSS
   - 点击"添加"

3. **获取 Feed ID**
   - 添加成功后，会显示 Feed ID（类似：`MP_WXS_123456`）
   - 保存到记事本

### 3.3 获取 AI API Key（10分钟）

#### 推荐：DeepSeek（免费额度大）

1. **注册账号**
   - 访问：https://platform.deepseek.com
   - 注册并登录

2. **获取 API Key**
   - 进入"API Keys"页面
   - 点击"创建新密钥"
   - 复制 API Key（类似：`sk-xxxxxxxxxxxxx`）
   - 保存到记事本

3. **查看额度**
   - 新用户有 500 万 tokens 免费额度
   - 足够使用很长时间

#### 备选：通义千问（国内稳定）

1. 访问：https://dashscope.aliyun.com
2. 注册并获取 API Key
3. 新用户有免费额度

---

## 4. 详细实施步骤

### 步骤 1：创建公众号配置文件（5分钟）

在 `config` 目录下创建 `wechat_accounts.yaml`：

```yaml
# 微信公众号配置
wewe_rss:
  base_url: "https://你的zeabur地址.zeabur.app"  # 替换为你的 WeWe RSS 地址
  auth_code: "123456"  # 你设置的 AUTH_CODE

# AI 配置
ai:
  provider: "deepseek"  # 可选: deepseek, qwen, openai
  api_key: "sk-xxxxxxxxxxxxx"  # 替换为你的 API Key
  model: "deepseek-chat"  # DeepSeek 模型
  max_tokens: 150  # 摘要最大长度

# 公众号列表
accounts:
  - name: "36氪"
    feed_id: "MP_WXS_123456"  # 替换为实际的 Feed ID
    keywords:
      - "AI"
      - "AIGC"
      - "人工智能"
  
  - name: "机器之心"
    feed_id: "MP_WXS_789012"  # 替换为实际的 Feed ID
    keywords:
      - "深度学习"
      - "大模型"
      - "AI"
  
  - name: "量子位"
    feed_id: "MP_WXS_345678"  # 替换为实际的 Feed ID
    keywords:
      - "AI"
      - "机器学习"
      - "科技"

# 推送配置
push:
  enabled: true
  time: "08:00"  # 每天推送时间
  max_articles: 10  # 每次最多推送文章数
```

### 步骤 2：创建 Python 脚本（30分钟）

我会为你创建完整的 Python 脚本，包括：

1. `wechat_rss_crawler.py` - 主爬虫脚本
2. `ai_summarizer.py` - AI 总结模块
3. `feishu_sender.py` - 飞书推送模块
4. `utils.py` - 工具函数

**这些脚本我会在下一步为你生成。**

### 步骤 3：配置 GitHub Actions（10分钟）

创建 `.github/workflows/wechat-crawler.yml`：

```yaml
name: WeChat RSS Crawler

on:
  schedule:
    - cron: '0 0 * * *'  # 每天 8:00 (UTC+8)
  workflow_dispatch:  # 支持手动触发

jobs:
  crawl:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install requests pyyaml feedparser
      
      - name: Run crawler
        env:
          FEISHU_WEBHOOK_URL: ${{ secrets.FEISHU_WEBHOOK_URL }}
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        run: |
          python wechat_rss/wechat_rss_crawler.py
```

### 步骤 4：配置 GitHub Secrets（5分钟）

1. 进入你的 GitHub 项目
2. Settings → Secrets and variables → Actions
3. 添加以下 Secrets：
   - `DEEPSEEK_API_KEY`: 你的 DeepSeek API Key
   - `FEISHU_WEBHOOK_URL`: 已有的飞书 Webhook（复用）

---

## 5. 测试与调试

### 5.1 本地测试（10分钟）

```bash
# 1. 安装依赖
pip install requests pyyaml feedparser

# 2. 设置环境变量
export FEISHU_WEBHOOK_URL="你的飞书webhook"
export DEEPSEEK_API_KEY="你的deepseek_api_key"

# 3. 运行脚本
python wechat_rss/wechat_rss_crawler.py
```

### 5.2 GitHub Actions 测试

1. 进入 Actions 页面
2. 选择 "WeChat RSS Crawler"
3. 点击 "Run workflow"
4. 等待运行完成
5. 检查飞书是否收到消息

---

## 6. 常见问题

### Q1: WeWe RSS 添加公众号失败？

**原因**：添加频率过高被封控  
**解决**：等待 24 小时后重试

### Q2: AI 总结失败？

**检查**：
1. API Key 是否正确
2. 是否有剩余额度
3. 网络是否正常

### Q3: 飞书收不到消息？

**检查**：
1. Webhook 地址是否正确
2. 飞书机器人是否已发布
3. 查看 GitHub Actions 日志

### Q4: 如何添加更多公众号？

编辑 `config/wechat_accounts.yaml`，在 `accounts` 下添加：

```yaml
- name: "新公众号名称"
  feed_id: "MP_WXS_xxxxxx"
  keywords:
    - "关键词1"
    - "关键词2"
```

---

## 📝 下一步

我现在会为你创建所有需要的 Python 脚本文件。请确认：

1. ✅ 你已经部署好 WeWe RSS 了吗？
2. ✅ 你已经获取到 DeepSeek API Key 了吗？
3. ✅ 你已经添加了至少一个公众号并获取到 Feed ID 了吗？

如果都准备好了，我会立即为你生成所有代码文件！

