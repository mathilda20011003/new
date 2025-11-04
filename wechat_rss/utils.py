#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
"""

import os
import yaml
from typing import List, Dict, Any


def load_config(config_path: str) -> Dict[str, Any]:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
    
    Returns:
        配置字典
    """
    try:
        # 支持相对路径和绝对路径
        if not os.path.isabs(config_path):
            # 获取项目根目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            config_path = os.path.join(project_root, config_path)
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        return config
        
    except FileNotFoundError:
        print(f"❌ 配置文件不存在: {config_path}")
        raise
    except yaml.YAMLError as e:
        print(f"❌ 配置文件格式错误: {e}")
        raise


def filter_by_keywords(articles: List[Dict], keywords: List[str]) -> List[Dict]:
    """
    根据关键词筛选文章
    
    Args:
        articles: 文章列表
        keywords: 关键词列表
    
    Returns:
        筛选后的文章列表
    """
    if not keywords:
        return articles
    
    filtered = []
    
    for article in articles:
        title = article.get('title', '').lower()
        summary = article.get('summary', '').lower()
        content = article.get('content', '').lower()
        
        # 组合所有文本
        text = f"{title} {summary} {content}"
        
        # 检查是否包含任意关键词
        for keyword in keywords:
            if keyword.lower() in text:
                filtered.append(article)
                break
    
    return filtered


def format_article_message(article: Dict) -> str:
    """
    格式化文章消息
    
    Args:
        article: 文章字典
    
    Returns:
        格式化后的消息
    """
    title = article.get('title', '无标题')
    link = article.get('link', '')
    ai_summary = article.get('ai_summary', '暂无摘要')
    account_name = article.get('account_name', '未知公众号')
    published = article.get('published', '')
    
    message_parts = [
        f"📰 **{title}**",
        f"📱 来源: {account_name}",
        f"📝 摘要: {ai_summary}",
    ]
    
    if published:
        message_parts.append(f"⏰ 发布: {published}")
    
    if link:
        message_parts.append(f"🔗 链接: {link}")
    
    return "\n".join(message_parts)


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断文本
    
    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 后缀
    
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + suffix


def load_frequency_words(file_path: str = "config/frequency_words.txt") -> List[str]:
    """
    加载关键词文件（复用现有的 frequency_words.txt）
    
    Args:
        file_path: 关键词文件路径
    
    Returns:
        关键词列表
    """
    try:
        # 支持相对路径和绝对路径
        if not os.path.isabs(file_path):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            file_path = os.path.join(project_root, file_path)
        
        keywords = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue
                # 跳过过滤词（!开头）
                if line.startswith('!'):
                    continue
                # 移除必须词标记（+开头）
                if line.startswith('+'):
                    line = line[1:]
                
                keywords.append(line)
        
        return keywords
        
    except FileNotFoundError:
        print(f"⚠️  关键词文件不存在: {file_path}")
        return []


def save_articles_to_json(articles: List[Dict], output_path: str = "data/wechat_articles.json"):
    """
    保存文章到 JSON 文件
    
    Args:
        articles: 文章列表
        output_path: 输出文件路径
    """
    import json
    from datetime import datetime
    
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 添加时间戳
        data = {
            'timestamp': datetime.now().isoformat(),
            'count': len(articles),
            'articles': articles
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 文章已保存到: {output_path}")
        
    except Exception as e:
        print(f"❌ 保存文章失败: {e}")


def load_articles_from_json(input_path: str = "data/wechat_articles.json") -> List[Dict]:
    """
    从 JSON 文件加载文章
    
    Args:
        input_path: 输入文件路径
    
    Returns:
        文章列表
    """
    import json
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get('articles', [])
        
    except FileNotFoundError:
        print(f"⚠️  文件不存在: {input_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        return []


# 测试代码
if __name__ == "__main__":
    # 测试加载配置
    try:
        config = load_config("config/wechat_accounts.yaml")
        print("✅ 配置加载成功:")
        print(f"   公众号数量: {len(config.get('accounts', []))}")
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
    
    # 测试关键词筛选
    test_articles = [
        {'title': 'OpenAI 发布 Sora', 'summary': 'AI 视频生成'},
        {'title': '今天天气不错', 'summary': '阳光明媚'},
        {'title': 'Midjourney V7', 'summary': 'AI 绘画工具'}
    ]
    
    keywords = ['AI', 'Sora', 'Midjourney']
    filtered = filter_by_keywords(test_articles, keywords)
    print(f"\n✅ 关键词筛选测试:")
    print(f"   原始: {len(test_articles)} 篇")
    print(f"   筛选后: {len(filtered)} 篇")
    
    # 测试加载关键词文件
    frequency_words = load_frequency_words()
    if frequency_words:
        print(f"\n✅ 关键词文件加载成功:")
        print(f"   关键词数量: {len(frequency_words)}")
        print(f"   前 5 个: {frequency_words[:5]}")

