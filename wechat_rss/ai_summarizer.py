#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 总结模块
支持多种 AI 服务: OpenRouter, DeepSeek, 通义千问, OpenAI
"""

import re
from typing import Optional


class AISummarizer:
    """AI 文章总结器"""

    def __init__(self, provider: str = "openrouter", api_key: str = "",
                 model: str = "meta-llama/llama-3.1-8b-instruct:free", max_tokens: int = 150):
        """
        初始化 AI 总结器

        Args:
            provider: AI 服务提供商 (openrouter, deepseek, qwen, openai)
            api_key: API Key
            model: 模型名称
            max_tokens: 最大 token 数
        """
        self.provider = provider.lower()
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens

        # 配置 API 端点
        self.api_configs = {
            'openrouter': {
                'base_url': 'https://openrouter.ai/api/v1',
                'default_model': 'meta-llama/llama-3.1-8b-instruct:free',
                'extra_headers': {
                    'HTTP-Referer': 'https://github.com/mathilda20011003/new',
                    'X-Title': 'WeChat RSS AI Assistant'
                }
            },
            'deepseek': {
                'base_url': 'https://api.deepseek.com/v1',
                'default_model': 'deepseek-chat',
                'extra_headers': {}
            },
            'qwen': {
                'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
                'default_model': 'qwen-turbo',
                'extra_headers': {}
            },
            'openai': {
                'base_url': 'https://api.openai.com/v1',
                'default_model': 'gpt-3.5-turbo',
                'extra_headers': {}
            }
        }

        if not self.api_key:
            print(f"⚠️  警告: 未设置 API Key，AI 总结功能将不可用")
    
    def clean_html(self, text: str) -> str:
        """
        清理 HTML 标签
        
        Args:
            text: 原始文本
        
        Returns:
            清理后的文本
        """
        # 移除 HTML 标签
        text = re.sub(r'<[^>]+>', '', text)
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff,.!?;:，。！？；：]', '', text)
        return text.strip()
    
    def truncate_content(self, content: str, max_length: int = 2000) -> str:
        """
        截断内容到指定长度
        
        Args:
            content: 原始内容
            max_length: 最大长度
        
        Returns:
            截断后的内容
        """
        if len(content) <= max_length:
            return content
        return content[:max_length] + "..."
    
    def summarize(self, title: str, content: str) -> Optional[str]:
        """
        生成文章摘要
        
        Args:
            title: 文章标题
            content: 文章内容
        
        Returns:
            摘要文本，失败返回 None
        """
        if not self.api_key:
            # 如果没有 API Key，返回简单摘要
            return self._simple_summary(title, content)
        
        try:
            # 清理内容
            clean_content = self.clean_html(content)
            clean_content = self.truncate_content(clean_content, 2000)
            
            # 根据内容长度和类型选择不同的提示词
            if len(clean_content.strip()) < 50:  # 内容很少，主要基于标题
                prompt = self._get_title_based_prompt(title)
            else:  # 有较多内容，基于完整内容分析
                prompt = self._get_content_based_prompt(title, clean_content)
            
            # 调用 AI API
            summary = self._call_ai_api(prompt)
            
            if summary:
                # 清理摘要
                summary = summary.strip()
                # 移除可能的引号
                summary = summary.strip('"\'')
                return summary
            else:
                return self._simple_summary(title, content)
                
        except Exception as e:
            print(f"   ⚠️  AI 总结失败: {e}")
            return self._simple_summary(title, content)
    
    def _call_ai_api(self, prompt: str) -> Optional[str]:
        """
        调用 AI API

        Args:
            prompt: 提示词

        Returns:
            AI 响应，失败返回 None
        """
        import requests

        try:
            # 获取配置
            config = self.api_configs.get(self.provider)
            if not config:
                print(f"   ⚠️  不支持的 AI 提供商: {self.provider}")
                return None

            base_url = config['base_url']
            model = self.model or config['default_model']
            extra_headers = config.get('extra_headers', {})

            # 构建请求
            url = f"{base_url}/chat/completions"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }

            # 添加额外的请求头（OpenRouter 需要）
            headers.update(extra_headers)

            data = {
                'model': model,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': self.max_tokens,
                'temperature': 0.7
            }

            # 发送请求
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()

            # 解析响应
            result = response.json()
            summary = result['choices'][0]['message']['content']

            return summary

        except Exception as e:
            print(f"   ⚠️  API 调用失败: {e}")
            return None

    def _get_title_based_prompt(self, title: str) -> str:
        """基于标题的提示词"""
        return f"""你是一位资深的商业分析师和科技记者。请基于以下标题，生成一个专业的商业洞察摘要（60-90字）：

标题：{title}

分析要求：
1. 识别核心商业价值和技术突破点
2. 分析对行业的潜在影响和意义
3. 使用专业但通俗易懂的语言
4. 避免使用"根据标题"、"可能"等不确定表述
5. 直接给出具体的分析结论
6. 突出创新点、市场机会或竞争优势

请用简洁有力的语言，提供有价值的商业洞察。"""

    def _get_content_based_prompt(self, title: str, content: str) -> str:
        """基于完整内容的提示词"""
        # 检测内容类型
        content_type = self._detect_content_type(title, content)

        if content_type == "tech":
            return self._get_tech_prompt(title, content)
        elif content_type == "business":
            return self._get_business_prompt(title, content)
        elif content_type == "industry":
            return self._get_industry_prompt(title, content)
        else:
            return self._get_general_prompt(title, content)

    def _detect_content_type(self, title: str, content: str) -> str:
        """检测内容类型"""
        text = (title + " " + content).lower()

        # 技术类关键词
        tech_keywords = ["ai", "人工智能", "模型", "算法", "技术", "开源", "api", "框架", "工具", "平台", "系统"]
        # 商业类关键词
        business_keywords = ["融资", "投资", "估值", "上市", "收购", "合作", "战略", "商业", "市场", "营收", "盈利"]
        # 行业类关键词
        industry_keywords = ["行业", "市场", "趋势", "报告", "数据", "分析", "增长", "规模", "份额", "竞争"]

        tech_score = sum(1 for keyword in tech_keywords if keyword in text)
        business_score = sum(1 for keyword in business_keywords if keyword in text)
        industry_score = sum(1 for keyword in industry_keywords if keyword in text)

        if tech_score >= max(business_score, industry_score):
            return "tech"
        elif business_score >= industry_score:
            return "business"
        elif industry_score > 0:
            return "industry"
        else:
            return "general"

    def _get_tech_prompt(self, title: str, content: str) -> str:
        """技术类文章提示词"""
        return f"""你是一位资深的技术分析师。请基于以下技术文章，生成一个专业的技术洞察摘要（严格控制在60-90字）：

标题：{title}

内容：{content}

分析要求：
1. 突出核心技术创新点和突破
2. 分析技术的实际应用价值和场景
3. 评估对开发者和行业的影响
4. 识别技术优势、性能提升或解决的痛点
5. 使用准确的技术术语但保持可读性
6. 避免过度技术化，确保商业人士也能理解

请提供有深度的技术商业分析。"""

    def _get_business_prompt(self, title: str, content: str) -> str:
        """商业类文章提示词"""
        return f"""你是一位资深的商业分析师。请基于以下商业文章，生成一个专业的商业洞察摘要（严格控制在60-90字）：

标题：{title}

内容：{content}

分析要求：
1. 识别关键商业动态和战略意图
2. 分析对市场格局和竞争的影响
3. 评估商业模式创新或变化
4. 突出投资价值和市场机会
5. 分析对相关行业和生态的影响
6. 提供前瞻性的商业判断

请提供有价值的商业洞察和趋势分析。"""

    def _get_industry_prompt(self, title: str, content: str) -> str:
        """行业类文章提示词"""
        return f"""你是一位资深的行业研究分析师。请基于以下行业文章，生成一个专业的行业洞察摘要（严格控制在60-90字）：

标题：{title}

内容：{content}

分析要求：
1. 提炼关键行业数据和趋势
2. 分析市场规模、增长驱动因素
3. 识别行业变化和发展机会
4. 评估主要玩家的竞争态势
5. 预测行业发展方向和影响
6. 突出对投资者和从业者的价值

请提供专业的行业分析和市场洞察。"""

    def _get_general_prompt(self, title: str, content: str) -> str:
        """通用文章提示词"""
        return f"""你是一位资深的内容分析师。请基于以下文章，生成一个专业的内容摘要（严格控制在60-90字）：

标题：{title}

内容：{content}

分析要求：
1. 提炼文章的核心观点和价值
2. 突出最重要的信息和洞察
3. 分析内容的实际意义和影响
4. 使用清晰、专业的表达方式
5. 确保摘要具有独立的阅读价值
6. 避免简单复述，提供深度分析

请提供有价值的内容洞察。"""

    def _simple_summary(self, title: str, content: str) -> str:
        """
        简单摘要（不使用 AI）
        
        Args:
            title: 文章标题
            content: 文章内容
        
        Returns:
            简单摘要
        """
        # 清理内容
        clean_content = self.clean_html(content)
        
        # 取前 100 个字符作为摘要
        if len(clean_content) > 100:
            summary = clean_content[:100] + "..."
        else:
            summary = clean_content or "暂无摘要"
        
        return summary


# 测试代码
if __name__ == "__main__":
    import os

    # 测试 OpenRouter
    api_key = os.getenv('OPENROUTER_API_KEY') or os.getenv('DEEPSEEK_API_KEY')
    if api_key:
        # 优先使用 OpenRouter
        if os.getenv('OPENROUTER_API_KEY'):
            summarizer = AISummarizer(
                provider='openrouter',
                api_key=api_key,
                model='meta-llama/llama-3.1-8b-instruct:free'
            )
        else:
            summarizer = AISummarizer(provider='deepseek', api_key=api_key)

        test_title = "OpenAI 发布 Sora 视频生成模型"
        test_content = """
        <p>OpenAI 今天发布了全新的视频生成模型 Sora，能够根据文本描述生成高质量的视频内容。</p>
        <p>Sora 可以生成长达 60 秒的视频，包含复杂的场景、多个角色和精确的动作。</p>
        <p>这标志着 AI 视频生成技术的重大突破。</p>
        """

        summary = summarizer.summarize(test_title, test_content)
        print(f"标题: {test_title}")
        print(f"摘要: {summary}")
    else:
        print("请设置 OPENROUTER_API_KEY 或 DEEPSEEK_API_KEY 环境变量")

