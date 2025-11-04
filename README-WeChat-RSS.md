# 微信公众号 AI 助手使用文档

> 📌 **功能**：自动爬取微信公众号文章，AI 总结，推送到飞书  
> ⏰ **更新频率**：每天自动运行 1 次，也可手动触发  
> 🤖 **AI 支持**：DeepSeek / 通义千问 / OpenAI

---

## 📋 目录

1. [快速开始](#快速开始)
2. [详细配置](#详细配置)
3. [使用方法](#使用方法)
4. [常见问题](#常见问题)

---

## 快速开始

### 前置条件

✅ 已部署 WeWe RSS（参考 [微信公众号AI助手集成方案.md](微信公众号AI助手集成方案.md)）  
✅ 已获取 DeepSeek API Key  
✅ 已配置飞书 Webhook

### 5 分钟快速配置

#### 1️⃣ 配置公众号（2分钟）

编辑 `config/wechat_accounts.yaml`：

```yaml
wewe_rss:
  base_url: "https://你的zeabur地址.zeabur.app"  # 替换！

accounts:
  - name: "36氪"
    feed_id: "MP_WXS_123456"  # 替换为实际的 Feed ID
    keywords:
      - "AI"
      - "AIGC"
```

#### 2️⃣ 配置 GitHub Secrets（2分钟）

进入 GitHub 项目 → Settings → Secrets and variables → Actions

添加：
- `DEEPSEEK_API_KEY`: 你的 DeepSeek API Key
- `FEISHU_WEBHOOK_URL`: 你的飞书 Webhook（已有）

#### 3️⃣ 测试运行（1分钟）

1. 进入 Actions 页面
2. 选择 "WeChat RSS Crawler"
3. 点击 "Run workflow"
4. 等待运行完成
5. 检查飞书是否收到消息

---

## 详细配置

### 配置文件说明

`config/wechat_accounts.yaml` 包含以下配置：

#### WeWe RSS 配置

```yaml
wewe_rss:
  base_url: "https://你的zeabur地址.zeabur.app"
  auth_code: "123456"  # 可选，如果设置了认证
```

#### AI 配置

```yaml
ai:
  provider: "deepseek"  # 可选: deepseek, qwen, openai
  api_key: ""  # 留空，从环境变量读取
  model: "deepseek-chat"
  max_tokens: 150  # 摘要长度
```

**支持的 AI 提供商**：

| 提供商 | 模型 | 免费额度 | 推荐度 |
|--------|------|---------|--------|
| DeepSeek | deepseek-chat | 500万 tokens | ⭐⭐⭐⭐⭐ |
| 通义千问 | qwen-turbo | 100万 tokens | ⭐⭐⭐⭐ |
| OpenAI | gpt-3.5-turbo | 需付费 | ⭐⭐⭐ |

#### 公众号配置

```yaml
accounts:
  - name: "公众号名称"
    feed_id: "MP_WXS_123456"  # 从 WeWe RSS 获取
    keywords:  # 关键词筛选（可选）
      - "AI"
      - "AIGC"
```

**如何获取 Feed ID**：

1. 登录 WeWe RSS 网页
2. 点击"公众号源" → "添加"
3. 粘贴公众号分享链接
4. 添加成功后，复制显示的 Feed ID

**关键词筛选规则**：

- 只要文章标题/内容包含**任意一个**关键词，就会被筛选出来
- 如果不设置关键词，则推送该公众号的所有文章
- 关键词不区分大小写

#### 推送配置

```yaml
push:
  enabled: true
  time: "08:00"  # 每天推送时间
  max_articles: 10  # 每次最多推送文章数
```

---

## 使用方法

### 方法 1: 自动定时运行

配置完成后，GitHub Actions 会**每天自动运行**：

- ⏰ 运行时间：每天北京时间 8:00
- 📱 自动推送到飞书
- 🔄 无需任何手动操作

### 方法 2: 手动触发

随时可以手动运行：

1. 进入 GitHub 项目
2. 点击 **Actions** 标签
3. 选择 **WeChat RSS Crawler**
4. 点击 **Run workflow**
5. 等待运行完成（约 1-2 分钟）

### 方法 3: 本地运行

在本地测试或调试：

```bash
# 1. 安装依赖
pip install requests pyyaml feedparser

# 2. 设置环境变量
export FEISHU_WEBHOOK_URL="你的飞书webhook"
export DEEPSEEK_API_KEY="你的deepseek_api_key"

# 3. 运行脚本
python wechat_rss/wechat_rss_crawler.py
```

---

## 常见问题

### Q1: 如何添加新的公众号？

编辑 `config/wechat_accounts.yaml`，在 `accounts` 下添加：

```yaml
- name: "新公众号名称"
  feed_id: "MP_WXS_xxxxxx"  # 从 WeWe RSS 获取
  keywords:
    - "关键词1"
    - "关键词2"
```

然后提交到 GitHub：

```bash
git add config/wechat_accounts.yaml
git commit -m "添加新公众号"
git push
```

### Q2: 如何修改推送时间？

编辑 `.github/workflows/wechat-crawler.yml`：

```yaml
schedule:
  - cron: '0 0 * * *'  # 每天 8:00 (UTC+8)
```

**常用时间**：

| 北京时间 | Cron 表达式 |
|---------|------------|
| 8:00 | `0 0 * * *` |
| 12:00 | `0 4 * * *` |
| 18:00 | `0 10 * * *` |
| 20:00 | `0 12 * * *` |

### Q3: 如何查看运行日志？

1. 进入 GitHub 项目
2. 点击 **Actions** 标签
3. 选择最近的运行记录
4. 点击 **crawl** 查看详细日志

### Q4: 飞书收不到消息？

**检查清单**：

- [ ] `FEISHU_WEBHOOK_URL` 是否正确配置
- [ ] 飞书机器人是否已发布
- [ ] 查看 GitHub Actions 日志是否有错误
- [ ] 手动测试飞书 Webhook 是否可用

**测试 Webhook**：

```bash
curl -X POST "你的webhook地址" \
  -H "Content-Type: application/json" \
  -d '{"msg_type":"text","content":{"text":"测试消息"}}'
```

### Q5: AI 总结失败？

**检查清单**：

- [ ] `DEEPSEEK_API_KEY` 是否正确配置
- [ ] API Key 是否有剩余额度
- [ ] 网络是否正常

**查看额度**：

访问 https://platform.deepseek.com/usage 查看剩余额度

### Q6: WeWe RSS 添加公众号失败？

**常见原因**：

1. **添加频率过高**：等待 24 小时后重试
2. **公众号链接错误**：确保是正确的分享链接
3. **微信读书未登录**：重新扫码登录

**获取公众号链接的正确方法**：

1. 打开微信
2. 找到公众号
3. 点击右上角 "..." → "分享"
4. 选择 "复制链接"
5. 粘贴到 WeWe RSS

### Q7: 如何复用现有的关键词配置？

如果你想使用 `config/frequency_words.txt` 中的关键词：

编辑 `wechat_rss/wechat_rss_crawler.py`，在 `process_account` 方法中：

```python
# 使用公众号自己的关键词
keywords = account.get('keywords', [])

# 或者使用全局关键词
from utils import load_frequency_words
keywords = load_frequency_words()
```

### Q8: 如何调整摘要长度？

编辑 `config/wechat_accounts.yaml`：

```yaml
ai:
  max_tokens: 150  # 调整这个值
```

**推荐值**：

- 简短摘要：100
- 标准摘要：150
- 详细摘要：300

---

## 📊 推送效果预览

配置完成后，你会在飞书收到类似这样的消息：

```
📰 微信公众号 AI 摘要推送
⏰ 2024-11-04 08:00:00
📊 共 5 篇文章

---

📱 36氪 (2 篇)

1. OpenAI 发布 Sora 视频生成模型
📝 OpenAI 发布了全新的视频生成模型 Sora，能够根据文本描述生成高质量的视频内容，标志着 AI 视频生成技术的重大突破。
⏰ 2024-11-04 10:30
🔗 https://...

2. Midjourney V7 版本发布
📝 Midjourney 发布 V7 版本，图像生成质量大幅提升，支持更精细的细节控制和更自然的人物表情。
⏰ 2024-11-04 09:15
🔗 https://...

---

📱 机器之心 (3 篇)
...
```

---

## 🔧 高级功能

### 保存文章到本地

编辑 `config/wechat_accounts.yaml`：

```yaml
advanced:
  save_to_file: true
  output_path: "data/wechat_articles.json"
```

文章会保存到 `data/wechat_articles.json`，可以在 GitHub Actions 的 Artifacts 中下载。

### 文章去重

编辑 `config/wechat_accounts.yaml`：

```yaml
advanced:
  deduplicate: true
```

基于文章链接去重，避免重复推送。

---

## 📞 需要帮助？

- 📖 查看详细教程：[微信公众号AI助手集成方案.md](微信公众号AI助手集成方案.md)
- 🐛 提交问题：[GitHub Issues](https://github.com/mathilda20011003/new/issues)
- 📧 联系作者：在 GitHub 上留言

---

**祝你使用愉快！** 🎉

