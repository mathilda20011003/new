#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书推送模块
复用现有的飞书 Webhook，支持富文本消息
"""

import json
from typing import List, Dict, Optional
from datetime import datetime


class FeishuSender:
    """飞书消息推送器"""
    
    def __init__(self, webhook_url: str):
        """
        初始化飞书推送器
        
        Args:
            webhook_url: 飞书 Webhook URL
        """
        self.webhook_url = webhook_url
        
        if not self.webhook_url:
            print("⚠️  警告: 未设置飞书 Webhook URL")
    
    def send_articles(self, articles: List[Dict]) -> bool:
        """
        发送文章列表到飞书
        
        Args:
            articles: 文章列表
        
        Returns:
            是否发送成功
        """
        if not self.webhook_url:
            print("❌ 未配置飞书 Webhook，跳过推送")
            return False
        
        if not articles:
            print("⚠️  没有文章需要推送")
            return False
        
        try:
            # 构建消息
            message = self._build_message(articles)
            
            # 发送消息
            success = self._send_message(message)
            
            return success
            
        except Exception as e:
            print(f"❌ 飞书推送失败: {e}")
            return False
    
    def _build_message(self, articles: List[Dict]) -> Dict:
        """
        构建飞书消息
        
        Args:
            articles: 文章列表
        
        Returns:
            飞书消息 JSON
        """
        # 按公众号分组
        grouped = {}
        for article in articles:
            account_name = article.get('account_name', '未知公众号')
            if account_name not in grouped:
                grouped[account_name] = []
            grouped[account_name].append(article)
        
        # 构建消息内容
        content_parts = []
        
        # 标题
        content_parts.append(f"📰 **微信公众号 AI 摘要推送**")
        content_parts.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content_parts.append(f"📊 共 {len(articles)} 篇文章\n")
        content_parts.append("---\n")
        
        # 按公众号输出
        for i, (account_name, account_articles) in enumerate(grouped.items(), 1):
            content_parts.append(f"## 📱 {account_name} ({len(account_articles)} 篇)\n")
            
            for j, article in enumerate(account_articles, 1):
                title = article.get('title', '无标题')
                link = article.get('link', '')
                ai_summary = article.get('ai_summary', '暂无摘要')
                published = article.get('published', '')
                
                # 格式化发布时间
                pub_time = self._format_time(published)
                
                # 文章条目
                content_parts.append(f"### {i}.{j} {title}\n")
                content_parts.append(f"**📝 AI 摘要**: {ai_summary}\n")
                if pub_time:
                    content_parts.append(f"**⏰ 发布时间**: {pub_time}\n")
                if link:
                    content_parts.append(f"**🔗 原文链接**: {link}\n")
                content_parts.append("")  # 空行
            
            content_parts.append("---\n")
        
        # 构建飞书消息
        message = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": f"📰 微信公众号 AI 摘要 ({len(articles)} 篇)"
                    },
                    "template": "blue"
                },
                "elements": self._build_card_elements(grouped)
            }
        }
        
        return message
    
    def _build_card_elements(self, grouped: Dict[str, List[Dict]]) -> List[Dict]:
        """
        构建飞书卡片元素
        
        Args:
            grouped: 按公众号分组的文章
        
        Returns:
            卡片元素列表
        """
        elements = []
        
        # 添加时间信息
        elements.append({
            "tag": "div",
            "text": {
                "tag": "plain_text",
                "content": f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            }
        })
        
        elements.append({"tag": "hr"})
        
        # 按公众号输出
        for account_name, articles in grouped.items():
            # 公众号标题
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**📱 {account_name}** ({len(articles)} 篇)"
                }
            })
            
            # 文章列表
            for i, article in enumerate(articles, 1):
                title = article.get('title', '无标题')
                link = article.get('link', '')
                ai_summary = article.get('ai_summary', '暂无摘要')
                published = article.get('published', '')
                
                # 格式化发布时间
                pub_time = self._format_time(published)
                
                # 文章标题（带链接）
                if link:
                    title_md = f"**{i}. [{title}]({link})**"
                else:
                    title_md = f"**{i}. {title}**"
                
                elements.append({
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": title_md
                    }
                })
                
                # AI 摘要
                elements.append({
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": f"📝 {ai_summary}"
                    }
                })
                
                # 发布时间
                if pub_time:
                    elements.append({
                        "tag": "div",
                        "text": {
                            "tag": "plain_text",
                            "content": f"⏰ {pub_time}"
                        }
                    })
                
                # 分隔线（最后一篇文章不加）
                if i < len(articles):
                    elements.append({"tag": "hr"})
            
            # 公众号之间的分隔
            elements.append({"tag": "hr"})
        
        return elements
    
    def _format_time(self, time_str: str) -> str:
        """
        格式化时间字符串
        
        Args:
            time_str: 原始时间字符串
        
        Returns:
            格式化后的时间
        """
        if not time_str:
            return ""
        
        try:
            # 尝试解析常见的时间格式
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(time_str)
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return time_str
    
    def _send_message(self, message: Dict) -> bool:
        """
        发送消息到飞书
        
        Args:
            message: 消息 JSON
        
        Returns:
            是否发送成功
        """
        import requests
        
        try:
            print(f"📤 正在发送消息到飞书...")
            
            response = requests.post(
                self.webhook_url,
                json=message,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get('code') == 0 or result.get('StatusCode') == 0:
                print(f"✅ 飞书推送成功")
                return True
            else:
                print(f"❌ 飞书推送失败: {result}")
                return False
                
        except Exception as e:
            print(f"❌ 飞书推送异常: {e}")
            return False


# 测试代码
if __name__ == "__main__":
    import os
    
    webhook_url = os.getenv('FEISHU_WEBHOOK_URL')
    if webhook_url:
        sender = FeishuSender(webhook_url)
        
        # 测试文章
        test_articles = [
            {
                'title': 'OpenAI 发布 Sora 视频生成模型',
                'link': 'https://example.com/article1',
                'ai_summary': 'OpenAI 发布了全新的视频生成模型 Sora，能够根据文本描述生成高质量的视频内容，标志着 AI 视频生成技术的重大突破。',
                'published': 'Mon, 04 Nov 2024 10:30:00 GMT',
                'account_name': '36氪'
            },
            {
                'title': 'Midjourney V7 版本发布',
                'link': 'https://example.com/article2',
                'ai_summary': 'Midjourney 发布 V7 版本，图像生成质量大幅提升，支持更精细的细节控制和更自然的人物表情。',
                'published': 'Mon, 04 Nov 2024 09:15:00 GMT',
                'account_name': '机器之心'
            }
        ]
        
        sender.send_articles(test_articles)
    else:
        print("请设置 FEISHU_WEBHOOK_URL 环境变量")

