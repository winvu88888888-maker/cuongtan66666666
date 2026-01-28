import json
import os
import sys

# Add the directory to path so we can import shard_manager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ai_modules.shard_manager import delete_entry

def cleanup_technical_titles():
    index_path = os.path.join("data_hub", "hub_index.json")
    
    # 1. EMERGENY REBUILD: If index is empty but shards exist, rebuild it!
    from shard_manager import BASE_HUB_DIR, add_entry
    
    print("🔍 Checking data consistency...")
    shards = [f for f in os.listdir(BASE_HUB_DIR) if f.startswith("shard_") and f.endswith(".json")]
    
    # If index is empty or very small, let's scan shards to be sure
    with open(index_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if len(data.get("index", [])) == 0 and shards:
        print("⚠️ Local index is empty but shards found. RESTORING index first...")
        for shard_file in shards:
            shard_path = os.path.join(BASE_HUB_DIR, shard_file)
            with open(shard_path, 'r', encoding='utf-8') as f:
                shard_data = json.load(f)
                for eid, entry in shard_data.get("entries", {}).items():
                    # Manually add back to index data structure
                    data["index"].append({
                        "id": eid,
                        "shard": shard_file,
                        "title": entry["title"],
                        "category": entry.get("category", "Kiến Thức"),
                        "tags": entry.get("tags", []),
                        "created_at": entry.get("created_at", datetime.now().isoformat())
                    })
        data["stats"]["total"] = len(data["index"])
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Restored {len(data['index'])} entries into index.")

    index = data.get("index", [])
    if not index:
        print("Hub index is still empty. Nothing to clean.")
        return

    to_delete = []
    # Identify titles with colons OR technical keywords
    technical_keywords = [
        "Ví dụ thực tế", "Ứng dụng sâu", "Case study", 
        "Hướng dẫn chi thực", "Phân tích rủi ro", "Giải pháp tối ưu",
        "Bí quyết thực thi nhanh", "Dữ liệu gốc từ cổ tịch", "papers",
        "Nghiên cứu", "Ví dụ", "Hướng dẫn", "Giải pháp", "Bí quyết", "Thực hành",
        "Chuyên sâu", "Chi tiết", "Tổng hợp", "Ayurveda và Y học Ấn Độ:"
    ]
    
    for entry in index:
        title = entry.get("title", "")
        should_delete = False
        
        # 1. Any title with a colon is likely a technical/draft title
        if ":" in title:
            should_delete = True
            
        # 2. Any title containing these "filler" keywords
        if any(kw.lower() in title.lower() for kw in technical_keywords):
            should_delete = True
            
        # 3. Titles that are too long
        if len(title) > 60:
            should_delete = True
            
        if should_delete:
            to_delete.append(entry["id"])
            print(f"[-] Marking for deletion: {title}")

    print(f"\nTargeting {len(to_delete)} messy entries for deletion.")

    count = 0
    for entry_id in to_delete:
        if delete_entry(entry_id):
            count += 1

    print(f"✅ Successfully cleaned up {count} entries.")

if __name__ == "__main__":
    cleanup_technical_titles()
