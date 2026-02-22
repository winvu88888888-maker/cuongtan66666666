import os
import json
from pathlib import Path
import re

class HubSearcher:
    """Intelligent search across the infinite knowledge hub for evidence-based AI reasoning."""
    
    def __init__(self, hub_dir="data_hub"):
        self.hub_dir = Path(hub_dir)
        self.index_path = self.hub_dir / "hub_index.json"
    
    def search(self, query, category=None, max_results=5):
        """
        Search the knowledge hub for relevant entries.
        
        Args:
            query: Search query (e.g., "đánh đỏ đen Kỳ Môn")
            category: Optional category filter
            max_results: Maximum number of results to return
            
        Returns:
            List of matching entries with title, content snippet, and relevance score
        """
        if not self.index_path.exists():
            return []
        
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            index = data.get("index", [])
            
            # Filter by category if specified
            if category:
                index = [e for e in index if e.get("category") == category]
            
            # Score and rank results
            results = []
            query_terms = self._tokenize(query)
            
            for entry in index:
                score = self._calculate_relevance(entry, query_terms)
                if score > 0:
                    results.append({
                        "id": entry["id"],
                        "shard": entry["shard"],
                        "title": entry["title"],
                        "category": entry.get("category", "Khác"),
                        "score": score
                    })
            
            # Sort by relevance and limit
            results.sort(key=lambda x: x["score"], reverse=True)
            results = results[:max_results]
            
            # Load full content for top results
            enriched_results = []
            for r in results:
                full_entry = self._load_full_entry(r["id"], r["shard"])
                if full_entry:
                    enriched_results.append({
                        "title": r["title"],
                        "category": r["category"],
                        "content_snippet": full_entry.get("content", "")[:500],
                        "full_content": full_entry.get("content", ""),
                        "score": r["score"]
                    })
            
            return enriched_results
            
        except Exception as e:
            print(f"Hub search error: {e}")
            return []
    
    def _tokenize(self, text):
        """Simple tokenization for Vietnamese text."""
        text = text.lower()
        # Remove punctuation but keep Vietnamese characters
        text = re.sub(r'[^\w\s]', ' ', text)
        return set(text.split())
    
    def _calculate_relevance(self, entry, query_terms):
        """Calculate relevance score based on term matching."""
        title_terms = self._tokenize(entry.get("title", ""))
        tags = entry.get("tags", [])
        tag_terms = set(" ".join(tags).lower().split())
        
        # Title matches are worth more
        title_score = len(query_terms & title_terms) * 3
        tag_score = len(query_terms & tag_terms) * 2
        
        return title_score + tag_score
    
    def _load_full_entry(self, entry_id, shard_filename):
        """Load full entry content from shard."""
        shard_path = self.hub_dir / shard_filename
        if not shard_path.exists():
            return None
        
        try:
            with open(shard_path, 'r', encoding='utf-8') as f:
                shard_data = json.load(f)
            return shard_data.get("entries", {}).get(entry_id)
        except:
            return None
    
    def find_case_studies(self, topic_keywords, palace_config=None):
        """
        Find relevant case studies for a specific divination topic.
        
        Args:
            topic_keywords: List of keywords (e.g., ["đánh", "đỏ", "đen", "cá cược"])
            palace_config: Optional dict with palace elements (sao, mon, than)
            
        Returns:
            List of case studies with outcomes
        """
        query = " ".join(topic_keywords)
        results = self.search(query, category="Kỳ Môn Độn Giáp", max_results=3)
        
        # Filter for case studies (entries with outcome indicators)
        case_studies = []
        outcome_keywords = ["kết quả", "thành công", "thất bại", "thắng", "thua", "lời", "lỗ"]
        
        for r in results:
            content = r["full_content"].lower()
            if any(kw in content for kw in outcome_keywords):
                case_studies.append(r)
        
        return case_studies

def get_hub_searcher():
    """Factory function to get hub searcher instance."""
    return HubSearcher()
