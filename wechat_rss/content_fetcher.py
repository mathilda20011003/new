#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章内容获取模块
从微信公众号文章链接获取完整的文章内容
"""

import re
import time
import requests
from typing import Optional, Dict
from bs4 import BeautifulSoup


class WeChatContentFetcher:
    """微信公众号文章内容获取器"""
    
    def __init__(self, timeout: int = 30, retry_times: int = 3):
        """
        初始化内容获取器
        
        Args:
            timeout: 请求超时时间
            retry_times: 重试次数
        """
        self.timeout = timeout
        self.retry_times = retry_times
        
        # 设置请求头，模拟浏览器访问
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def fetch_article_content(self, url: str) -> Optional[Dict[str, str]]:
        """
        获取微信公众号文章内容
        
        Args:
            url: 文章链接
            
        Returns:
            包含标题和内容的字典，失败返回None
        """
        if not self._is_wechat_article_url(url):
            print(f"⚠️ 不是有效的微信公众号文章链接: {url}")
            return None
        
        for attempt in range(self.retry_times):
            try:
                print(f"🔍 获取文章内容 (尝试 {attempt + 1}/{self.retry_times}): {url[:50]}...")
                
                # 发送请求
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.raise_for_status()
                
                # 检查是否被重定向到错误页面
                if '该内容已被发布者删除' in response.text or '此内容因违规无法查看' in response.text:
                    print(f"⚠️ 文章已被删除或违规")
                    return None
                
                # 解析HTML内容
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 提取文章内容
                content_data = self._extract_content(soup)
                
                if content_data and content_data.get('content'):
                    print(f"✅ 成功获取文章内容: {len(content_data['content'])} 字符")
                    return content_data
                else:
                    print(f"⚠️ 未能提取到文章内容")
                    
            except requests.exceptions.Timeout:
                print(f"⏰ 请求超时 (尝试 {attempt + 1}/{self.retry_times})")
            except requests.exceptions.RequestException as e:
                print(f"❌ 请求失败 (尝试 {attempt + 1}/{self.retry_times}): {e}")
            except Exception as e:
                print(f"❌ 解析失败 (尝试 {attempt + 1}/{self.retry_times}): {e}")
            
            # 重试前等待
            if attempt < self.retry_times - 1:
                time.sleep(2)
        
        print(f"❌ 获取文章内容失败，已重试 {self.retry_times} 次")
        return None
    
    def _is_wechat_article_url(self, url: str) -> bool:
        """
        检查是否是微信公众号文章链接
        
        Args:
            url: 链接地址
            
        Returns:
            是否是微信文章链接
        """
        wechat_patterns = [
            r'mp\.weixin\.qq\.com/s/',
            r'mp\.weixin\.qq\.com/s\?',
        ]
        
        return any(re.search(pattern, url) for pattern in wechat_patterns)
    
    def _extract_content(self, soup: BeautifulSoup) -> Optional[Dict[str, str]]:
        """
        从BeautifulSoup对象中提取文章内容
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            包含标题和内容的字典
        """
        try:
            # 提取标题
            title = self._extract_title(soup)
            
            # 提取正文内容
            content = self._extract_main_content(soup)
            
            if not content:
                return None
            
            return {
                'title': title or '无标题',
                'content': content,
                'length': len(content)
            }
            
        except Exception as e:
            print(f"❌ 内容提取失败: {e}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """提取文章标题"""
        # 尝试多种标题选择器
        title_selectors = [
            '#activity-name',
            '.rich_media_title',
            'h1.rich_media_title',
            'h2.rich_media_title',
            '.wx_article_title',
            'title'
        ]
        
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True)
                if title and len(title) > 3:  # 过滤太短的标题
                    return title
        
        return None
    
    def _extract_main_content(self, soup: BeautifulSoup) -> Optional[str]:
        """提取文章正文内容"""
        # 尝试多种内容选择器
        content_selectors = [
            '#js_content',
            '.rich_media_content',
            '.wx_article_content',
            '#img-content',
            '.article_content'
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # 清理内容
                content = self._clean_content(content_elem)
                if content and len(content) > 100:  # 过滤太短的内容
                    return content
        
        return None
    
    def _clean_content(self, content_elem) -> str:
        """
        清理文章内容
        
        Args:
            content_elem: 内容元素
            
        Returns:
            清理后的文本内容
        """
        # 移除不需要的元素
        for elem in content_elem.find_all(['script', 'style', 'noscript']):
            elem.decompose()
        
        # 移除广告和推广相关的元素
        ad_classes = ['ad', 'advertisement', 'promotion', 'sponsor']
        for ad_class in ad_classes:
            for elem in content_elem.find_all(class_=re.compile(ad_class, re.I)):
                elem.decompose()
        
        # 获取文本内容
        text = content_elem.get_text(separator='\n', strip=True)
        
        # 清理文本
        text = re.sub(r'\n\s*\n', '\n\n', text)  # 合并多个空行
        text = re.sub(r'[ \t]+', ' ', text)      # 合并多个空格
        text = text.strip()
        
        return text
    
    def batch_fetch_contents(self, articles: list) -> list:
        """
        批量获取文章内容
        
        Args:
            articles: 文章列表，每个文章应包含'link'字段
            
        Returns:
            更新后的文章列表，添加了'full_content'字段
        """
        updated_articles = []
        
        for i, article in enumerate(articles, 1):
            print(f"\n📖 处理文章 {i}/{len(articles)}")
            
            link = article.get('link', '')
            if not link:
                print(f"⚠️ 文章缺少链接")
                updated_articles.append(article)
                continue
            
            # 获取完整内容
            content_data = self.fetch_article_content(link)
            
            if content_data:
                article['full_content'] = content_data['content']
                article['content_length'] = content_data['length']
                print(f"✅ 获取成功: {content_data['length']} 字符")
            else:
                article['full_content'] = article.get('summary', '') or article.get('title', '')
                article['content_length'] = len(article['full_content'])
                print(f"⚠️ 使用备用内容: {article['content_length']} 字符")
            
            updated_articles.append(article)
            
            # 避免请求过于频繁
            if i < len(articles):
                time.sleep(1)
        
        return updated_articles


# 测试代码
if __name__ == "__main__":
    fetcher = WeChatContentFetcher()
    
    # 测试文章链接
    test_url = "https://mp.weixin.qq.com/s/test_article_id"
    
    content = fetcher.fetch_article_content(test_url)
    if content:
        print(f"标题: {content['title']}")
        print(f"内容长度: {content['length']} 字符")
        print(f"内容预览: {content['content'][:200]}...")
    else:
        print("获取内容失败")
