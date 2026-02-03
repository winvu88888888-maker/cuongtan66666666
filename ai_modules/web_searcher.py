"""
Web Search Module for 50 AI Agents
Tìm kiếm và thu thập dữ liệu từ Google/Internet
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict

class WebSearcher:
    """Advanced web searcher for AI agents."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.search_engines = [
            'https://www.google.com/search?q=',
            'https://duckduckgo.com/html/?q='
        ]
    
    def search_google(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Tìm kiếm trên Google và trả về danh sách URLs + snippets.
        
        Args:
            query: Từ khóa tìm kiếm
            num_results: Số kết quả cần lấy
            
        Returns:
            List of dicts with 'title', 'url', 'snippet'
        """
        results = []
        
        try:
            # Format query
            search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}&num={num_results}"
            
            # Add random delay to avoid rate limiting
            time.sleep(random.uniform(1, 3))
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Parse search results
                for g in soup.find_all('div', class_='g')[:num_results]:
                    try:
                        title_elem = g.find('h3')
                        link_elem = g.find('a')
                        snippet_elem = g.find('div', class_='VwiC3b')
                        
                        if title_elem and link_elem:
                            title = title_elem.get_text()
                            url = link_elem.get('href', '')
                            snippet = snippet_elem.get_text() if snippet_elem else ""
                            
                            if url.startswith('http'):
                                results.append({
                                    'title': title,
                                    'url': url,
                                    'snippet': snippet
                                })
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"⚠️ Search error: {e}")
            
        return results
    
    def extract_content(self, url: str, max_length: int = 5000) -> str:
        """
        Trích xuất nội dung văn bản từ URL.
        
        Args:
            url: URL cần crawl
            max_length: Độ dài tối đa của nội dung
            
        Returns:
            Cleaned text content
        """
        try:
            time.sleep(random.uniform(0.5, 2))
            
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                # Get text
                text = soup.get_text()
                
                # Clean up
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                # Truncate if too long
                if len(text) > max_length:
                    text = text[:max_length] + "..."
                
                return text
                
        except Exception as e:
            print(f"⚠️ Extract error for {url}: {e}")
            return ""
    
    def deep_research(self, topic: str, num_sources: int = 3) -> str:
        """
        Nghiên cứu sâu một chủ đề từ nhiều nguồn.
        
        Args:
            topic: Chủ đề cần nghiên cứu
            num_sources: Số nguồn cần crawl
            
        Returns:
            Synthesized content from multiple sources
        """
        print(f"🔍 Đang nghiên cứu: {topic}")
        
        # Search
        search_results = self.search_google(topic, num_results=num_sources)
        
        if not search_results:
            return f"Không tìm thấy kết quả cho: {topic}"
        
        # Collect content from sources
        collected_data = []
        collected_data.append(f"# Nghiên cứu chuyên sâu: {topic}\n\n")
        
        for idx, result in enumerate(search_results, 1):
            collected_data.append(f"## Nguồn {idx}: {result['title']}\n")
            collected_data.append(f"**URL**: {result['url']}\n\n")
            
            if result['snippet']:
                collected_data.append(f"**Tóm tắt**: {result['snippet']}\n\n")
            
            # Extract full content
            content = self.extract_content(result['url'], max_length=2000)
            if content:
                collected_data.append(f"**Nội dung chi tiết**:\n{content}\n\n")
                collected_data.append("---\n\n")
        
        return ''.join(collected_data)
    
    def quick_search(self, query: str) -> str:
        """
        Tìm kiếm nhanh và trả về tóm tắt.
        
        Args:
            query: Câu hỏi/từ khóa
            
        Returns:
            Quick summary from search results
        """
        results = self.search_google(query, num_results=3)
        
        if not results:
            return "Không tìm thấy thông tin."
        
        summary = f"**Kết quả tìm kiếm: {query}**\n\n"
        
        for idx, r in enumerate(results, 1):
            summary += f"{idx}. **{r['title']}**\n"
            if r['snippet']:
                summary += f"   {r['snippet']}\n"
            summary += f"   🔗 {r['url']}\n\n"
        
        return summary


# Singleton instance
_searcher_instance = None

def get_web_searcher() -> WebSearcher:
    """Get or create web searcher instance."""
    global _searcher_instance
    if _searcher_instance is None:
        _searcher_instance = WebSearcher()
    return _searcher_instance
