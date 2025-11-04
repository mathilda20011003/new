#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 总结模块
支持多种 AI 服务: DeepSeek, 通义千问, OpenAI
"""

import re
from typing import Optional


class AISummarizer:
    """AI 文章总结器"""
    
    def __init__(self, provider: str = "deepseek", api_key: str = "", 
                 model: str = "deepseek-chat", max_tokens: int = 150):
        """
        初始化 AI 总结器
        
        Args:
            provider: AI 服务提供商 (deepseek, qwen, openai)
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
            'deepseek': {
                'base_url': 'https://api.deepseek.com/v1',
                'default_model': 'deepseek-chat'
            },
            'qwen': {
                'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
                'default_model': 'qwen-turbo'
            },
            'openai': {
                'base_url': 'https://api.openai.com/v1',
                'default_model': 'gpt-3.5-turbo'
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
            
            # 构建提示词
            prompt = f"""请用1-2句话总结以下文章的核心内容（不超过100字）：

标题：{title}

内容：{clean_content}

要求：
1. 简洁明了，突出重点
2. 使用中文
3. 不要包含"本文"、"文章"等词汇
4. 直接说明文章讲了什么"""
            
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
            
            # 构建请求
            url = f"{base_url}/chat/completions"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
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
    
    # 测试 DeepSeek
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if api_key:
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
        print("请设置 DEEPSEEK_API_KEY 环境变量")

