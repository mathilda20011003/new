# 快速入门 - 微信公众号 AI 助手

> 🎯 **目标**：30 分钟内完成配置，开始接收微信公众号 AI 摘要推送  
> 👤 **适用人群**：零基础实习生  
> ⏰ **预计时间**：30 分钟

---

## 📋 准备清单

在开始之前，请确保你有：

- [ ] GitHub 账号
- [ ] 飞书账号（已配置好机器人 Webhook）
- [ ] 微信账号（用于登录微信读书）

---

## 🚀 三步完成配置

### 第一步：部署 WeWe RSS（10分钟）

#### 1.1 注册 Zeabur

1. 访问：https://zeabur.com
2. 点击右上角 "Sign in with GitHub"
3. 授权登录

#### 1.2 一键部署 WeWe RSS

1. 访问：https://zeabur.com/templates/DI9BBD
2. 点击 "Deploy" 按钮
3. 选择一个区域（推荐：Hong Kong）
4. 等待部署完成（约 2-3 分钟）

#### 1.3 配置环境变量

部署完成后，点击 "wewe-rss" 服务：

1. 点击 "Variables" 标签
2. 添加环境变量：
   - `AUTH_CODE`: 设置为 `123456`（你的访问密码）
3. 点击 "Save"

#### 1.4 获取访问地址

1. 点击 "Networking" 标签
2. 点击 "Generate Domain"
3. 复制生成的域名（类似：`xxx.zeabur.app`）
4. **保存到记事本**，后面会用到

#### 1.5 登录微信读书

1. 打开你的 WeWe RSS 地址（刚才复制的域名）
2. 点击 "账号管理" → "添加账号"
3. 微信扫码登录微信读书
4. ⚠️ **重要**：不要勾选"24小时后自动退出"

---

### 第二步：添加公众号并获取 Feed ID（10分钟）

#### 2.1 获取公众号分享链接

在微信中：

1. 找到你想订阅的公众号
2. 点击右上角 "..." → "分享"
3. 选择 "复制链接"

#### 2.2 在 WeWe RSS 中添加公众号

1. 打开 WeWe RSS 网页
2. 点击 "公众号源" → "添加"
3. 粘贴刚才复制的链接
4. 点击 "添加"

#### 2.3 获取 Feed ID

添加成功后，会显示 Feed ID（类似：`MP_WXS_123456`）

**保存到记事本**，格式如下：

```
公众号名称: 36氪
Feed ID: MP_WXS_123456

公众号名称: 机器之心
Feed ID: MP_WXS_789012
```

**推荐订阅的 AIGC 相关公众号**：

- 36氪
- 机器之心
- 量子位
- AI科技评论
- 新智元
- 硅星人
- 爱范儿

---

### 第三步：配置项目并运行（10分钟）

#### 3.1 获取 OpenRouter API Key（推荐）

**为什么选择 OpenRouter？**
- ✅ 完全免费（使用免费模型）
- ✅ 无需信用卡
- ✅ 多种模型可选
- ✅ 注册简单（Google/GitHub 登录）

**操作步骤**：

1. 访问：https://openrouter.ai
2. 点击 "Sign In" → 选择 "Sign in with Google" 或 "Sign in with GitHub"
3. 授权登录
4. 访问：https://openrouter.ai/keys
5. 点击 "Create Key"
6. 输入名称（如：`WeChat RSS Bot`）
7. 复制 API Key（类似：`sk-or-v1-xxxxxxxxxxxxx`）
8. **保存到记事本**

**备选方案：DeepSeek API Key**

如果你更喜欢 DeepSeek：
1. 访问：https://platform.deepseek.com
2. 注册并登录
3. 点击 "API Keys" → "创建新密钥"
4. 复制 API Key（类似：`sk-xxxxxxxxxxxxx`）
5. **保存到记事本**

#### 3.2 配置 GitHub Secrets

1. 进入你的 GitHub 项目：https://github.com/mathilda20011003/new
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下 Secret：
   - **使用 OpenRouter**：
     - Name: `OPENROUTER_API_KEY`
     - Value: 你的 OpenRouter API Key（刚才复制的）
   - **使用 DeepSeek**：
     - Name: `DEEPSEEK_API_KEY`
     - Value: 你的 DeepSeek API Key（刚才复制的）
5. 点击 **Add secret**

#### 3.3 配置公众号列表

1. 在本地打开项目文件夹：`d:\new`
2. 编辑文件：`config/wechat_accounts.yaml`
3. 修改以下内容：

```yaml
wewe_rss:
  base_url: "https://你的zeabur地址.zeabur.app"  # 替换为你的 WeWe RSS 地址

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
```

4. 保存文件

#### 3.4 提交到 GitHub

在 PowerShell 中运行：

```powershell
cd d:\new
git add .
git commit -m "配置微信公众号AI助手"
git push
```

#### 3.5 手动运行测试

1. 进入 GitHub 项目
2. 点击 **Actions** 标签
3. 选择 **WeChat RSS Crawler**
4. 点击 **Run workflow** → **Run workflow**
5. 等待运行完成（约 1-2 分钟）

#### 3.6 检查飞书消息

打开飞书，检查是否收到类似这样的消息：

```
📰 微信公众号 AI 摘要推送
⏰ 2024-11-04 16:30:00
📊 共 5 篇文章

---

📱 36氪 (2 篇)

1. OpenAI 发布 Sora 视频生成模型
📝 OpenAI 发布了全新的视频生成模型...
🔗 https://...
```

---

## ✅ 完成！

恭喜！你已经成功配置了微信公众号 AI 助手！

### 接下来会发生什么？

- ⏰ **每天自动运行**：北京时间 8:00 自动爬取并推送
- 📱 **自动推送到飞书**：无需任何手动操作
- 🤖 **AI 智能摘要**：每篇文章都有 AI 生成的摘要

### 如何添加更多公众号？

1. 在 WeWe RSS 中添加公众号，获取 Feed ID
2. 编辑 `config/wechat_accounts.yaml`，添加配置
3. 提交到 GitHub：`git add . && git commit -m "添加新公众号" && git push`

### 如何修改推送时间？

编辑 `.github/workflows/wechat-crawler.yml`：

```yaml
schedule:
  - cron: '0 0 * * *'  # 每天 8:00 (UTC+8)
```

常用时间：
- 8:00 → `0 0 * * *`
- 12:00 → `0 4 * * *`
- 18:00 → `0 10 * * *`

---

## 🐛 遇到问题？

### 问题 1: 飞书收不到消息

**检查清单**：
- [ ] GitHub Actions 是否运行成功？（查看 Actions 页面）
- [ ] `FEISHU_WEBHOOK_URL` 是否正确配置？
- [ ] 飞书机器人是否已发布？

### 问题 2: AI 总结失败

**检查清单**：
- [ ] `DEEPSEEK_API_KEY` 是否正确配置？
- [ ] DeepSeek 是否有剩余额度？（访问 https://platform.deepseek.com/usage）

### 问题 3: WeWe RSS 添加公众号失败

**解决方法**：
- 等待 24 小时后重试（可能是添加频率过高）
- 确保公众号链接是正确的分享链接
- 重新登录微信读书

---

## 📚 更多文档

- 📖 [详细配置文档](README-WeChat-RSS.md)
- 🔧 [完整集成方案](微信公众号AI助手集成方案.md)
- 🐛 [提交问题](https://github.com/mathilda20011003/new/issues)

---

**祝你使用愉快！** 🎉

