#!/bin/bash
# WeWe RSS v2.x 部署脚本
# 用于替换旧版本，提供稳定的RSS数据源

echo "🚀 开始部署 WeWe RSS v2.x..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# 停止并删除旧容器（如果存在）
echo "🧹 清理旧容器..."
docker stop wewe-rss-old 2>/dev/null || true
docker rm wewe-rss-old 2>/dev/null || true

# 创建数据目录
echo "📁 创建数据目录..."
mkdir -p ./wewe-rss-data

# 部署 WeWe RSS v2.x (SQLite版本，更简单)
echo "🐳 启动 WeWe RSS v2.x 容器..."
docker run -d \
  --name wewe-rss-v2 \
  --restart unless-stopped \
  -p 4000:4000 \
  -e DATABASE_TYPE=sqlite \
  -e AUTH_CODE=123567 \
  -e CRON_EXPRESSION="35 5,17 * * *" \
  -e UPDATE_DELAY_TIME="60s" \
  -e FEED_MODE="fulltext" \
  -e ENABLE_CLEAN_HTML="false" \
  -e MAX_REQUEST_PER_MINUTE="30" \
  -v $(pwd)/wewe-rss-data:/app/data \
  cooderl/wewe-rss-sqlite:latest

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
if docker ps | grep -q wewe-rss-v2; then
    echo "✅ WeWe RSS v2.x 部署成功！"
    echo ""
    echo "📋 服务信息："
    echo "   🌐 访问地址: http://localhost:4000"
    echo "   🔑 授权码: 123567"
    echo "   ⏰ 自动更新: 每天 5:35 和 17:35"
    echo "   📊 全文模式: 已启用"
    echo ""
    echo "📝 下一步操作："
    echo "   1. 访问 http://localhost:4000"
    echo "   2. 使用授权码 123567 登录"
    echo "   3. 添加微信公众号（扫码登录微信读书）"
    echo "   4. 获取 Feed ID 并更新配置文件"
    echo ""
    echo "🔗 RSS 访问格式："
    echo "   http://localhost:4000/feeds/MP_WXS_xxxxxx.rss"
    echo "   http://localhost:4000/feeds/MP_WXS_xxxxxx.atom"
    echo "   http://localhost:4000/feeds/MP_WXS_xxxxxx.json"
else
    echo "❌ WeWe RSS v2.x 部署失败！"
    echo "📋 查看日志："
    docker logs wewe-rss-v2
    exit 1
fi

echo ""
echo "🎉 部署完成！WeWe RSS v2.x 现在将自动维护RSS数据源。"
echo "💡 您的AI摘要系统将从这个稳定的数据源获取文章内容。"
