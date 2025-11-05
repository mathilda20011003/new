#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试改进后的AI摘要提示词效果
"""

import os
import requests
import feedparser
from dotenv import load_dotenv

def test_improved_prompts():
    """测试改进后的提示词"""
    load_dotenv()
    
    print("🧪 测试改进后的AI摘要提示词...")
    
    # 获取真实文章进行测试
    base_url = os.getenv('WEWE_RSS_BASE_URL', 'https://ssys2025.zeabur.app')
    test_feed_id = "MP_WXS_3073282833"  # 机器之心
    
    try:
        response = requests.get(f"{base_url}/feeds/{test_feed_id}", timeout=10)
        
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            
            if feed.entries:
                # 测试前3篇文章
                for i, entry in enumerate(feed.entries[:3], 1):
                    print(f"\n{'='*60}")
                    print(f"📰 测试文章 {i}: {entry.get('title', '无标题')}")
                    print(f"{'='*60}")
                    
                    article_url = entry.get('link', '')
                    article_title = entry.get('title', '无标题')
                    
                    if article_url:
                        test_single_article(article_url, article_title)
                    else:
                        print("❌ 未找到文章链接")
            else:
                print("❌ RSS中没有文章")
        else:
            print(f"❌ RSS获取失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ RSS获取异常: {e}")

def test_single_article(url, title):
    """测试单篇文章的摘要生成"""
    try:
        # 1. 获取文章内容
        from wechat_rss.content_fetcher import WeChatContentFetcher
        
        fetcher = WeChatContentFetcher(timeout=15, retry_times=2)
        content_data = fetcher.fetch_article_content(url)
        
        if not content_data:
            print("❌ 无法获取文章内容")
            return
        
        content = content_data['content']
        print(f"📝 文章内容长度: {len(content)} 字符")
        print(f"📄 内容预览: {content[:200]}...")
        
        # 2. 测试新的AI摘要
        test_new_summarizer(title, content)
        
    except Exception as e:
        print(f"❌ 文章处理失败: {e}")

def test_new_summarizer(title, content):
    """测试新的摘要生成器"""
    try:
        from wechat_rss.ai_summarizer import AISummarizer
        
        api_key = os.getenv('OPENROUTER_API_KEY')
        model = os.getenv('AI_MODEL', 'google/gemini-2.5-flash-lite-preview-09-2025')
        
        if not api_key:
            print("⚠️ 未配置OpenRouter API密钥，跳过AI摘要测试")
            return
        
        print(f"\n🤖 使用改进后的提示词生成摘要...")
        
        # 创建摘要生成器
        summarizer = AISummarizer(
            provider='openrouter',
            api_key=api_key,
            model=model,
            max_tokens=200  # 增加token数量以支持更长的摘要
        )
        
        # 生成摘要
        summary = summarizer.summarize(title, content)
        
        if summary:
            print(f"✅ 新摘要生成成功:")
            print(f"💡 摘要内容: {summary}")
            
            # 分析摘要质量
            analyze_summary_quality(summary, title, content)
        else:
            print(f"❌ 摘要生成失败")
            
    except Exception as e:
        print(f"❌ 摘要测试失败: {e}")

def analyze_summary_quality(summary, title, content):
    """分析摘要质量"""
    print(f"\n📊 摘要质量分析:")
    
    # 1. 长度分析
    summary_length = len(summary)
    if summary_length < 50:
        print(f"⚠️ 摘要偏短 ({summary_length} 字符)")
    elif summary_length > 150:
        print(f"⚠️ 摘要偏长 ({summary_length} 字符)")
    else:
        print(f"✅ 摘要长度适中 ({summary_length} 字符)")
    
    # 2. 内容质量分析
    quality_indicators = {
        "专业术语": check_professional_terms(summary),
        "具体数据": check_specific_data(summary),
        "分析深度": check_analysis_depth(summary),
        "商业洞察": check_business_insight(summary),
        "避免重复": not check_title_repetition(summary, title)
    }
    
    print(f"📈 质量指标:")
    for indicator, passed in quality_indicators.items():
        status = "✅" if passed else "⚠️"
        print(f"   {status} {indicator}: {'通过' if passed else '需改进'}")
    
    # 3. 整体评分
    score = sum(quality_indicators.values()) / len(quality_indicators) * 100
    print(f"🎯 整体质量评分: {score:.1f}%")
    
    if score >= 80:
        print(f"🎉 摘要质量优秀！")
    elif score >= 60:
        print(f"👍 摘要质量良好")
    else:
        print(f"🔧 摘要质量需要改进")

def check_professional_terms(summary):
    """检查是否包含专业术语"""
    professional_terms = [
        "技术", "创新", "突破", "优化", "提升", "解决方案", "平台", "系统",
        "模型", "算法", "框架", "工具", "应用", "场景", "价值", "影响",
        "市场", "行业", "竞争", "优势", "机会", "趋势", "发展", "增长"
    ]
    return any(term in summary for term in professional_terms)

def check_specific_data(summary):
    """检查是否包含具体数据或事实"""
    import re
    # 检查数字、百分比、具体名称等
    patterns = [
        r'\d+',  # 数字
        r'\d+%',  # 百分比
        r'\d+亿',  # 亿级数据
        r'\d+万',  # 万级数据
        r'[A-Z][a-zA-Z]+',  # 英文名称/品牌
    ]
    return any(re.search(pattern, summary) for pattern in patterns)

def check_analysis_depth(summary):
    """检查分析深度"""
    depth_indicators = [
        "分析", "评估", "预测", "影响", "意义", "价值", "优势", "挑战",
        "机会", "趋势", "变化", "发展", "提升", "改进", "突破", "创新"
    ]
    return any(indicator in summary for indicator in depth_indicators)

def check_business_insight(summary):
    """检查商业洞察"""
    business_terms = [
        "商业", "市场", "竞争", "优势", "机会", "价值", "收益", "效率",
        "成本", "投资", "回报", "增长", "规模", "份额", "领先", "布局"
    ]
    return any(term in summary for term in business_terms)

def check_title_repetition(summary, title):
    """检查是否简单重复标题"""
    # 如果摘要中包含标题的大部分内容，认为是重复
    title_words = set(title.replace('，', '').replace('。', '').replace('！', '').replace('？', ''))
    summary_words = set(summary.replace('，', '').replace('。', '').replace('！', '').replace('？', ''))
    
    if len(title_words) == 0:
        return False
    
    overlap_ratio = len(title_words & summary_words) / len(title_words)
    return overlap_ratio > 0.7  # 如果重叠度超过70%，认为是重复

def compare_with_old_prompts():
    """对比新旧提示词效果"""
    print(f"\n🔄 对比新旧提示词效果...")
    
    # 这里可以添加对比测试的逻辑
    # 由于旧版本已经被替换，这里主要是展示概念
    
    print(f"📊 预期改进:")
    print(f"   ✅ 摘要长度: 50-80字 → 80-120字")
    print(f"   ✅ 分析深度: 简单总结 → 专业洞察")
    print(f"   ✅ 内容类型: 通用模板 → 分类优化")
    print(f"   ✅ 专业程度: 基础描述 → 商业分析")

if __name__ == "__main__":
    print("🚀 开始测试改进后的AI摘要提示词\n")
    
    # 测试改进后的提示词
    test_improved_prompts()
    
    # 对比分析
    compare_with_old_prompts()
    
    print(f"\n🎉 测试完成！")
    print(f"💡 如果摘要质量有显著提升，说明新提示词生效")
    print(f"🔧 如果质量仍需改进，可以进一步调整提示词策略")
