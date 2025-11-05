#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文章内容获取功能
"""

import os
import requests
import feedparser
from dotenv import load_dotenv

def test_content_fetcher():
    """测试内容获取器"""
    load_dotenv()
    
    print("🧪 测试文章内容获取功能...")
    
    # 1. 先从RSS获取文章链接
    base_url = os.getenv('WEWE_RSS_BASE_URL', 'https://ssys2025.zeabur.app')
    test_feed_id = "MP_WXS_3073282833"  # 机器之心
    
    print(f"📡 获取RSS文章列表...")
    try:
        response = requests.get(f"{base_url}/feeds/{test_feed_id}", timeout=10)
        
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            
            if feed.entries:
                # 取第一篇文章进行测试
                entry = feed.entries[0]
                article_url = entry.get('link', '')
                article_title = entry.get('title', '无标题')
                
                print(f"📰 测试文章: {article_title}")
                print(f"🔗 文章链接: {article_url}")
                
                if article_url:
                    # 2. 测试内容获取
                    test_fetch_content(article_url, article_title)
                else:
                    print("❌ 未找到文章链接")
            else:
                print("❌ RSS中没有文章")
        else:
            print(f"❌ RSS获取失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ RSS获取异常: {e}")

def test_fetch_content(url, title):
    """测试获取单篇文章内容"""
    try:
        from wechat_rss.content_fetcher import WeChatContentFetcher
        
        print(f"\n🔍 开始获取文章内容...")
        
        fetcher = WeChatContentFetcher(timeout=15, retry_times=2)
        content_data = fetcher.fetch_article_content(url)
        
        if content_data:
            print(f"\n✅ 内容获取成功!")
            print(f"📰 标题: {content_data['title']}")
            print(f"📝 内容长度: {content_data['length']} 字符")
            print(f"📄 内容预览:")
            print("-" * 60)
            print(content_data['content'][:500] + "..." if len(content_data['content']) > 500 else content_data['content'])
            print("-" * 60)
            
            # 测试AI摘要生成
            test_ai_summary_with_content(content_data['content'], content_data['title'])
            
        else:
            print(f"❌ 内容获取失败")
            
    except ImportError as e:
        print(f"❌ 导入内容获取模块失败: {e}")
        print(f"💡 请确保已安装 beautifulsoup4: pip install beautifulsoup4")
    except Exception as e:
        print(f"❌ 内容获取异常: {e}")

def test_ai_summary_with_content(content, title):
    """测试使用完整内容生成AI摘要"""
    try:
        from wechat_rss.ai_summarizer import AISummarizer
        
        api_key = os.getenv('OPENROUTER_API_KEY')
        model = os.getenv('AI_MODEL', 'google/gemini-2.5-flash-lite-preview-09-2025')
        
        if not api_key:
            print("⚠️ 未配置OpenRouter API密钥，跳过AI摘要测试")
            return
        
        print(f"\n🤖 测试AI摘要生成...")
        print(f"📝 输入内容长度: {len(content)} 字符")
        
        summarizer = AISummarizer(
            api_key=api_key,
            model=model,
            max_tokens=150
        )
        
        summary = summarizer.summarize(title, content)
        
        if summary:
            print(f"✅ AI摘要生成成功:")
            print(f"💡 摘要: {summary}")
            
            # 分析摘要质量
            analyze_summary_quality(summary, title, content)
        else:
            print(f"❌ AI摘要生成失败")
            
    except Exception as e:
        print(f"❌ AI摘要测试失败: {e}")

def analyze_summary_quality(summary, title, content):
    """分析摘要质量"""
    print(f"\n📊 摘要质量分析:")
    
    # 检查摘要长度
    if len(summary) < 20:
        print(f"⚠️ 摘要过短 ({len(summary)} 字符)")
    elif len(summary) > 200:
        print(f"⚠️ 摘要过长 ({len(summary)} 字符)")
    else:
        print(f"✅ 摘要长度适中 ({len(summary)} 字符)")
    
    # 检查是否只是重复标题
    if title.lower() in summary.lower():
        print(f"⚠️ 摘要包含标题，可能质量不佳")
    else:
        print(f"✅ 摘要不重复标题")
    
    # 检查是否包含实质内容
    content_keywords = extract_keywords_from_content(content)
    summary_keywords = extract_keywords_from_content(summary)
    
    common_keywords = set(content_keywords) & set(summary_keywords)
    if len(common_keywords) > 0:
        print(f"✅ 摘要包含 {len(common_keywords)} 个关键词，质量良好")
        print(f"   关键词: {', '.join(list(common_keywords)[:5])}")
    else:
        print(f"⚠️ 摘要与原文关键词匹配度低")

def extract_keywords_from_content(text):
    """从文本中提取关键词"""
    import re
    
    # 简单的关键词提取（可以改进）
    # 移除标点符号，分割成词
    words = re.findall(r'[\u4e00-\u9fff]+', text)  # 提取中文词汇
    
    # 过滤常见停用词
    stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
    
    keywords = [word for word in words if len(word) > 1 and word not in stop_words]
    
    # 返回出现频率最高的词
    from collections import Counter
    word_counts = Counter(keywords)
    return [word for word, count in word_counts.most_common(10)]

def test_batch_processing():
    """测试批量处理功能"""
    print(f"\n🔄 测试批量处理功能...")
    
    # 模拟文章列表
    test_articles = [
        {
            'title': '测试文章1',
            'link': 'https://mp.weixin.qq.com/s/test1',
            'summary': '这是测试文章1的摘要'
        },
        {
            'title': '测试文章2', 
            'link': 'https://mp.weixin.qq.com/s/test2',
            'summary': '这是测试文章2的摘要'
        }
    ]
    
    try:
        from wechat_rss.content_fetcher import WeChatContentFetcher
        
        fetcher = WeChatContentFetcher(timeout=10, retry_times=1)
        updated_articles = fetcher.batch_fetch_contents(test_articles)
        
        print(f"✅ 批量处理完成，处理了 {len(updated_articles)} 篇文章")
        
        for article in updated_articles:
            print(f"   📰 {article['title']}: {article.get('content_length', 0)} 字符")
            
    except Exception as e:
        print(f"❌ 批量处理测试失败: {e}")

if __name__ == "__main__":
    print("🚀 开始测试文章内容获取功能\n")
    
    # 测试单篇文章内容获取
    test_content_fetcher()
    
    # 测试批量处理
    test_batch_processing()
    
    print(f"\n🎉 测试完成！")
