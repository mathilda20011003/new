# OpenRouter 使用教程

> 🎯 **目标**：配置 OpenRouter API 用于微信公众号 AI 摘要  
> ⏰ **预计时间**：5 分钟  
> 💰 **费用**：完全免费（使用免费模型）

---

## 📋 什么是 OpenRouter？

**OpenRouter** 是一个统一的 AI API 平台，提供：

- ✅ **多种免费模型**：Meta Llama、Google Gemma、Microsoft Phi-3、Qwen 等
- ✅ **统一接口**：兼容 OpenAI API 格式
- ✅ **无需信用卡**：免费模型无需绑卡
- ✅ **稳定可靠**：专业的 API 服务

---

## 🚀 快速开始

### 第一步：注册 OpenRouter（2分钟）

1. **访问官网**
   - 打开：https://openrouter.ai

2. **注册账号**
   - 点击右上角 "Sign In"
   - 选择 "Sign in with Google" 或 "Sign in with GitHub"
   - 授权登录

3. **完成注册**
   - 登录成功后，会自动跳转到控制台

---

### 第二步：创建 API Key（2分钟）

1. **进入 API Keys 页面**
   - 访问：https://openrouter.ai/keys
   - 或点击左侧菜单 "API Keys"

2. **创建新密钥**
   - 点击 "Create Key" 按钮
   - 输入密钥名称（如：`WeChat RSS Bot`）
   - 点击 "Create"

3. **复制 API Key**
   - 复制显示的 API Key（格式：`sk-or-v1-xxxxxxxxxxxxx`）
   - ⚠️ **重要**：保存到安全的地方，只显示一次！
   - **保存到记事本** ✏️

---

### 第三步：配置到项目（1分钟）

#### 方法一：配置 GitHub Secrets（推荐）

1. **进入 GitHub 项目**
   - 访问：https://github.com/mathilda20011003/new
   - 点击 **Settings** → **Secrets and variables** → **Actions**

2. **添加 Secret**
   - 点击 **New repository secret**
   - Name: `OPENROUTER_API_KEY`
   - Value: 粘贴你的 OpenRouter API Key
   - 点击 **Add secret**

#### 方法二：本地测试（可选）

在 PowerShell 中设置环境变量：

```powershell
$env:OPENROUTER_API_KEY="sk-or-v1-xxxxxxxxxxxxx"
```

---

## 🎨 可用的免费模型

OpenRouter 提供多个完全免费的模型：

### 推荐模型

| 模型名称 | 模型 ID | 特点 | 推荐度 |
|---------|---------|------|--------|
| **Llama 3.1 8B** | `meta-llama/llama-3.1-8b-instruct:free` | Meta 出品，速度快，质量高 | ⭐⭐⭐⭐⭐ |
| **Gemma 2 9B** | `google/gemma-2-9b-it:free` | Google 出品，性能优秀 | ⭐⭐⭐⭐ |
| **Phi-3 Mini** | `microsoft/phi-3-mini-128k-instruct:free` | 微软出品，支持长文本 | ⭐⭐⭐⭐ |
| **Qwen 2 7B** | `qwen/qwen-2-7b-instruct:free` | 阿里出品，中文友好 | ⭐⭐⭐⭐ |

### 如何选择模型？

- **默认推荐**：`meta-llama/llama-3.1-8b-instruct:free`（速度快，质量好）
- **中文优先**：`qwen/qwen-2-7b-instruct:free`（阿里出品，中文更好）
- **长文本**：`microsoft/phi-3-mini-128k-instruct:free`（支持 128K 上下文）

---

## ⚙️ 配置文件说明

编辑 `config/wechat_accounts.yaml`：

```yaml
# AI 配置
ai:
  provider: "openrouter"  # 使用 OpenRouter
  api_key: ""  # 留空，从环境变量读取
  model: "meta-llama/llama-3.1-8b-instruct:free"  # 免费模型
  max_tokens: 150  # 摘要长度
```

### 切换模型

只需修改 `model` 字段：

```yaml
# 使用 Google Gemma
model: "google/gemma-2-9b-it:free"

# 使用 Microsoft Phi-3
model: "microsoft/phi-3-mini-128k-instruct:free"

# 使用 Qwen（中文更好）
model: "qwen/qwen-2-7b-instruct:free"
```

---

## 🧪 测试 API

### 方法一：使用 Python 测试

创建测试文件 `test_openrouter.py`：

```python
import os
import requests

api_key = os.getenv('OPENROUTER_API_KEY')

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}',
    'HTTP-Referer': 'https://github.com/mathilda20011003/new',
    'X-Title': 'WeChat RSS AI Assistant'
}

data = {
    'model': 'meta-llama/llama-3.1-8b-instruct:free',
    'messages': [
        {'role': 'user', 'content': '用一句话介绍人工智能'}
    ],
    'max_tokens': 100
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

运行测试：

```powershell
python test_openrouter.py
```

### 方法二：使用 curl 测试

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "HTTP-Referer: https://github.com/mathilda20011003/new" \
  -H "X-Title: WeChat RSS AI Assistant" \
  -d '{
    "model": "meta-llama/llama-3.1-8b-instruct:free",
    "messages": [
      {"role": "user", "content": "用一句话介绍人工智能"}
    ],
    "max_tokens": 100
  }'
```

---

## 📊 查看使用情况

1. **访问控制台**
   - 打开：https://openrouter.ai/activity

2. **查看请求记录**
   - 可以看到所有 API 调用记录
   - 免费模型显示 $0.00

3. **查看额度**
   - 免费模型无限制使用
   - 无需担心额度问题

---

## 🔧 高级配置

### 自定义请求头

OpenRouter 要求设置 `HTTP-Referer` 和 `X-Title`，代码中已自动配置：

```python
extra_headers = {
    'HTTP-Referer': 'https://github.com/mathilda20011003/new',
    'X-Title': 'WeChat RSS AI Assistant'
}
```

### 调整温度参数

编辑 `wechat_rss/ai_summarizer.py`，修改 `temperature`：

```python
data = {
    'model': model,
    'messages': [...],
    'max_tokens': self.max_tokens,
    'temperature': 0.7  # 0.0-1.0，越高越随机
}
```

---

## ❓ 常见问题

### Q1: OpenRouter 和 DeepSeek 有什么区别？

| 特性 | OpenRouter | DeepSeek |
|------|-----------|----------|
| 免费额度 | 无限（免费模型） | 500万 tokens |
| 模型选择 | 多种免费模型 | 仅 DeepSeek |
| 注册难度 | 简单（Google/GitHub） | 需要手机号 |
| 稳定性 | 高 | 高 |
| 推荐度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**推荐**：优先使用 OpenRouter，更灵活且完全免费。

### Q2: 免费模型有限制吗？

- ✅ **无使用次数限制**
- ✅ **无每日额度限制**
- ⚠️ **有速率限制**（每分钟请求数，但对我们的使用场景足够）

### Q3: 如何切换回 DeepSeek？

编辑 `config/wechat_accounts.yaml`：

```yaml
ai:
  provider: "deepseek"
  api_key: ""  # 从环境变量 DEEPSEEK_API_KEY 读取
  model: "deepseek-chat"
```

同时在 GitHub Secrets 中配置 `DEEPSEEK_API_KEY`。

### Q4: 可以同时配置多个 API Key 吗？

可以！在 GitHub Secrets 中同时添加：

- `OPENROUTER_API_KEY`
- `DEEPSEEK_API_KEY`

然后在配置文件中选择使用哪个 `provider`。

### Q5: 哪个模型中文效果最好？

**推荐顺序**：

1. `qwen/qwen-2-7b-instruct:free` - 阿里出品，专门优化中文
2. `meta-llama/llama-3.1-8b-instruct:free` - Meta 出品，中文也不错
3. `google/gemma-2-9b-it:free` - Google 出品，中文一般

---

## 🎯 完整配置示例

### 1. GitHub Secrets

添加以下 Secret：

- Name: `OPENROUTER_API_KEY`
- Value: `sk-or-v1-xxxxxxxxxxxxx`

### 2. 配置文件

`config/wechat_accounts.yaml`：

```yaml
wewe_rss:
  base_url: "https://你的zeabur地址.zeabur.app"

ai:
  provider: "openrouter"
  api_key: ""
  model: "meta-llama/llama-3.1-8b-instruct:free"
  max_tokens: 150

accounts:
  - name: "36氪"
    feed_id: "MP_WXS_123456"
    keywords:
      - "AI"
      - "AIGC"
```

### 3. 提交并测试

```powershell
cd d:\new
git add config/wechat_accounts.yaml
git commit -m "配置 OpenRouter API"
git push
```

然后在 GitHub Actions 中手动运行测试。

---

## 📞 需要帮助？

- 📖 OpenRouter 官方文档：https://openrouter.ai/docs
- 🔍 模型列表：https://openrouter.ai/models
- 💬 GitHub Issues：https://github.com/mathilda20011003/new/issues

---

**祝你使用愉快！** 🎉

