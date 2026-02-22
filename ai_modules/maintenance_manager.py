import os
import json
import time
import gzip
from pathlib import Path

class MaintenanceManager:
    """The Cleanup Legion: Decides what stays, what merges, and what goes to the Archive Bag."""
    
    def __init__(self, data_hub_dir="data_hub"):
        self.data_hub_dir = Path(data_hub_dir)
        self.archive_dir = self.data_hub_dir / "archive"
        self.index_path = self.data_hub_dir / "hub_index.json"
        
        self.data_hub_dir.mkdir(exist_ok=True)
        self.archive_dir.mkdir(exist_ok=True)

    def run_cleanup_cycle(self):
        """Main entry point for the maintenance cycle. DISABLED - Không xóa bất kỳ dữ liệu nào."""
        print("🛡️ Bảo trì: Chế độ BẢO TỒN 100% - Không xóa dữ liệu.")
        # TẤT CẢ CHỨC NĂNG XÓA ĐÃ BỊ VÔ HIỆU HÓA VĨNH VIỄN
        # để bảo vệ toàn bộ chủ đề khỏi bị mất
        return {"removed": 0, "bagged": 0}

    def purge_ai_errors(self):
        """Removes entries containing AI error messages."""
        if not self.index_path.exists(): return 0
        
        with open(self.index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        index = data.get("index", [])
        to_remove = []
        
        error_keywords = ["❌ Lỗi AI", "🛑 **Hết hạn mức AI**", "400 google_search", "google_search_retrieval", "quota", "limit"]
        
        for entry in index:
            shard_file = self.data_hub_dir / entry['shard']
            if shard_file.exists():
                try:
                    with open(shard_file, 'r', encoding='utf-8') as f:
                        s_data = json.load(f)
                    e_data = s_data.get("entries", {}).get(entry['id'], {})
                    content = e_data.get("content", "")
                    if any(kw in content for kw in error_keywords):
                        to_remove.append(entry['id'])
                except: pass
        
        if to_remove:
            from shard_manager import delete_entry
            for eid in to_remove:
                delete_entry(eid)
        
        return len(to_remove)

    def remove_duplicates(self):
        """Removes entries with identical or nearly identical titles/content."""
        if not self.index_path.exists():
            return 0
            
        with open(self.index_path, 'r', encoding='utf-8') as f:
            full_data = json.load(f)
            
        index = full_data.get("index", [])
        stats = full_data.get("stats", {"total": 0, "categories": {}})
        
        seen_titles = set()
        to_remove = []
        unique_index = []
        
        for entry in index:
            title_clean = entry['title'].strip().lower()
            # Simple fuzzy check: ignore small variations in punctuation/spacing
            title_clean = "".join(e for e in title_clean if e.isalnum())
            
            if title_clean in seen_titles:
                to_remove.append(entry)
            else:
                seen_titles.add(title_clean)
                unique_index.append(entry)
        
        if to_remove:
            # Update Stats
            for entry in to_remove:
                cat = entry.get('category', 'Khác')
                stats["total"] -= 1
                stats["categories"][cat] = max(0, stats["categories"].get(cat, 0) - 1)

            # Update Index Data
            full_data["index"] = unique_index
            full_data["stats"] = stats
            
            with open(self.index_path, 'w', encoding='utf-8') as f:
                json.dump(full_data, f, ensure_ascii=False, indent=2)
            
            # Physically remove shard files if they are empty or orphaned
            for entry in to_remove:
                shard_file = self.data_hub_dir / entry['shard']
                if shard_file.exists():
                    try:
                        with open(shard_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        if entry['id'] in data.get("entries", {}):
                            del data["entries"][entry['id']]
                            with open(shard_file, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=2)
                    except Exception: pass
                    
        return len(to_remove)

    def archive_old_data(self, threshold_mb=10000000): # Huge threshold to prevent automatic archiving
        """Moves oldest 20% of data to compressed Bags if hub directory is too large."""
        # Calculate size of data_hub
        total_size = sum(f.stat().st_size for f in self.data_hub_dir.glob('**/*') if f.is_file())
        size_mb = total_size / (1024 * 1024)
        
        if size_mb < threshold_mb:
            return 0
            
        print(f"📦 Hệ thống quá đầy ({size_mb:.1f}MB). Đang đóng gói dữ liệu cũ...")
        
        with open(self.index_path, 'r', encoding='utf-8') as f:
            full_data = json.load(f)
            
        index = full_data.get("index", [])
        stats = full_data.get("stats", {"total": 0, "categories": {}})
            
        # Sort by date
        index.sort(key=lambda x: x['created_at'])
        
        # Take oldest 20 entries or 10%
        archive_batch = index[:max(10, len(index)//10)]
        remaining_index = index[len(archive_batch):]
        
        bag_id = int(time.time())
        bag_path = self.archive_dir / f"bag_{bag_id}.json.gz"
        
        bag_content = {}
        for entry in archive_batch:
            shard_file = self.data_hub_dir / entry['shard']
            if shard_file.exists():
                with open(shard_file, 'r', encoding='utf-8') as f:
                    shard_data = json.load(f)
                if entry['id'] in shard_data.get("entries", {}):
                    bag_content[entry['id']] = shard_data["entries"][entry['id']]
                    
                    # Update Stats for archived items
                    cat = entry.get('category', 'Khác')
                    stats["total"] -= 1
                    stats["categories"][cat] = max(0, stats["categories"].get(cat, 0) - 1)
        
        # Save compressed bag
        if bag_content:
            with gzip.open(bag_path, 'wt', encoding='utf-8') as f:
                json.dump(bag_content, f, ensure_ascii=False)
            
        # Update Index Data
        full_data["index"] = remaining_index
        full_data["stats"] = stats
            
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)
            
        return len(archive_batch)
