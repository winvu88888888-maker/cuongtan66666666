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
        """Main entry point for the maintenance cycle."""
        print("🧹 Khởi chạy Quân đoàn Dọn dẹp (Cleanup Legion)...")
        
        # 1. Deduplication
        removed_count = self.remove_duplicates()
        
        # 2. Archiving (Bagging) if necessary
        bagged_count = self.archive_old_data(threshold_mb=100) # Archive if total hub > 100MB for web speed
        
        print(f"✨ Hoàn tất dọn dẹp: Đã xóa {removed_count} mục trùng, đóng gói {bagged_count} mục vào kho lưu trữ.")
        return {"removed": removed_count, "bagged": bagged_count}

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

    def archive_old_data(self, threshold_mb=50):
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
