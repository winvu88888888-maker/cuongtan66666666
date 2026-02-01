import json
import os
import sys
from datetime import datetime

# Add the directory to path so we can import shard_manager
base_dir = os.path.dirname(os.path.abspath(__file__))
ai_modules_dir = os.path.join(base_dir, "ai_modules")
if ai_modules_dir not in sys.path:
    sys.path.append(ai_modules_dir)

from shard_manager import delete_entry

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

    from shard_manager import update_entry
    
    # Identify titles with colons OR technical keywords
    technical_keywords = [
        "Ví dụ thực tế", "Ứng dụng sâu", "Case study", 
        "Hướng dẫn chi thực", "Phân tích rủi ro", "Giải pháp tối ưu",
        "Bí quyết thực thi nhanh", "Dữ liệu gốc từ cổ tịch", "papers",
        "Nghiên cứu", "Ví dụ", "Hướng dẫn", "Giải pháp", "Bí quyết", "Thực hành",
        "Chuyên sâu", "Chi tiết", "Tổng hợp", "Ayurveda và Y học Ấn Độ:"
    ]
    
    modified_count = 0
    for entry in index:
        eid = entry.get("id")
        title = entry.get("title", "")
        new_title = title
        
        # 1. Formatting: Remove parts after colon if it looks like technical junk
        if ":" in title:
            # Keep the main part before the colon as the title
            new_title = title.split(":")[0].strip()
            
        # 2. Formatting: Remove technical keywords from title
        for kw in technical_keywords:
            if kw.lower() in new_title.lower():
                new_title = new_title.replace(kw, "").replace(kw.lower(), "").strip()
                
        # 3. Truncate if still too long (but keep the entry!)
        if len(new_title) > 60:
            new_title = new_title[:57] + "..."
            
        # Only update if title actually changed
        if new_title and new_title != title:
            print(f"[*] Formatting title: '{title}' -> '{new_title}'")
            if update_entry(eid, title=new_title):
                modified_count += 1

    print(f"✅ Successfully formatted {modified_count} titles. NO DATA WAS DELETED.")

if __name__ == "__main__":
    cleanup_technical_titles()
