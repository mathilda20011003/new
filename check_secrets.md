# 🔧 GitHub Secrets 配置检查

## 必需的 Secrets

您需要在GitHub仓库中配置以下4个Secrets：

### 1. FEISHU_WEBHOOK_URL
- **值**: `https://www.feishu.cn/flow/api/trigger-webhook/b232e47aa5317de195c5716e45c5aaf5`
- **说明**: 飞书工作流Webhook地址

### 2. OPENROUTER_API_KEY  
- **值**: `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`
- **说明**: OpenRouter API密钥

### 3. WEWE_RSS_BASE_URL
- **值**: `https://ssys2025.zeabur.app`
- **说明**: WeWe RSS服务地址

### 4. AI_MODEL (可选)
- **值**: `google/gemini-2.5-flash-lite-preview-09-2025`
- **说明**: AI模型名称（如果不设置会使用默认值）

## 配置步骤

1. 进入GitHub仓库页面
2. 点击 **Settings** 
3. 在左侧菜单中点击 **Secrets and variables** → **Actions**
4. 点击 **New repository secret**
5. 输入Name和Secret值
6. 点击 **Add secret**

## 验证配置

配置完成后，重新运行工作流：
1. 进入 Actions 页面
2. 点击 "WeChat AI Summary Crawler"
3. 点击 "Run workflow"
4. 选择 "Run workflow"

如果仍然失败，请检查日志中的具体错误信息。
