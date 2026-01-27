import os
import json
import uuid
from datetime import datetime
from pathlib import Path

# Configuration
BASE_HUB_DIR = "data_hub"
INDEX_FILE = os.path.join(BASE_HUB_DIR, "hub_index.json")
MAX_ENTRIES_PER_SHARD = 100 # Adjust based on performance needs

def initialize_hub():
    """Initialize the directory and index if they don't exist."""
    if not os.path.exists(BASE_HUB_DIR):
        os.makedirs(BASE_HUB_DIR)
    
    if not os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump({"index": [], "stats": {"total": 0, "categories": {}}}, f, indent=2)

def add_entry(title, content, category="Kiến Thức", source="AI Miner", tags=None):
    """Add a new entry into a shard and update the index."""
    initialize_hub()
    
    entry_id = str(uuid.uuid4())[:8] + datetime.now().strftime("%Y%m%d%H%M%S")
    timestamp = datetime.now().isoformat()
    tags = tags or []
    
    # 1. Determine Shard
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
        
    total_entries = index_data['stats']['total']
    shard_id = (total_entries // MAX_ENTRIES_PER_SHARD) + 1
    shard_filename = f"shard_{shard_id}.json"
    shard_path = os.path.join(BASE_HUB_DIR, shard_filename)
    
    # 2. Save Full Content to Shard
    shard_data = {"entries": {}}
    if os.path.exists(shard_path):
        with open(shard_path, 'r', encoding='utf-8') as f:
            shard_data = json.load(f)
            
    shard_data["entries"][entry_id] = {
        "id": entry_id,
        "title": title,
        "content": content,
        "category": category,
        "source": source,
        "tags": tags,
        "created_at": timestamp
    }
    
    with open(shard_path, 'w', encoding='utf-8') as f:
        json.dump(shard_data, f, indent=2, ensure_ascii=False)
        
    # 3. Update Index (Lightweight Info)
    index_data["index"].append({
        "id": entry_id,
        "shard": shard_filename,
        "title": title,
        "category": category,
        "tags": tags,
        "created_at": timestamp
    })
    
    # Update Stats
    index_data["stats"]["total"] += 1
    index_data["stats"]["categories"][category] = index_data["stats"]["categories"].get(category, 0) + 1
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
        
    return entry_id

def search_index(query="", category="Tất cả"):
    """Search the lightweight index for matches."""
    if not os.path.exists(INDEX_FILE):
        return []
        
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
        
    results = index_data["index"]
    
    if category != "Tất cả":
        results = [e for e in results if e["category"] == category]
        
    if query:
        query = query.lower()
        results = [e for e in results if query in e["title"].lower() or any(query in t.lower() for t in e["tags"])]
        
    return sorted(results, key=lambda x: x["created_at"], reverse=True)

def get_full_entry(entry_id, shard_filename):
    """Lazy load only the specific shard needed for full content."""
    shard_path = os.path.join(BASE_HUB_DIR, shard_filename)
    if not os.path.exists(shard_path):
        return None
        
    try:
        with open(shard_path, 'r', encoding='utf-8') as f:
            shard_data = json.load(f)
            return shard_data["entries"].get(entry_id)
    except:
        return None

def delete_entry(entry_id):
    """Remove entry from index and shard."""
    if not os.path.exists(INDEX_FILE): return False
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
        
    # Find entry in index
    entry_ref = next((e for e in index_data["index"] if e["id"] == entry_id), None)
    if not entry_ref: return False
    
    # 1. Remove from Shard
    shard_path = os.path.join(BASE_HUB_DIR, entry_ref["shard"])
    if os.path.exists(shard_path):
        with open(shard_path, 'r', encoding='utf-8') as f:
            shard_data = json.load(f)
        if entry_id in shard_data["entries"]:
            del shard_data["entries"][entry_id]
            with open(shard_path, 'w', encoding='utf-8') as f:
                json.dump(shard_data, f, indent=2, ensure_ascii=False)
                
    # 2. Remove from Index
    index_data["index"] = [e for e in index_data["index"] if e["id"] != entry_id]
    index_data["stats"]["total"] -= 1
    cat = entry_ref["category"]
    index_data["stats"]["categories"][cat] = max(0, index_data["stats"]["categories"].get(cat, 0) - 1)
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    return True

def get_hub_stats():
    """Get statistics about the entire data hub (Total, Categories, Disk Size)."""
    if not os.path.exists(INDEX_FILE):
        return {"total": 0, "categories": {}, "size_mb": 0.0}
    
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        stats = index_data.get("stats", {"total": 0, "categories": {}})
        
        # Calculate total disk size
        total_bytes = 0
        for f in os.listdir(BASE_HUB_DIR):
            fp = os.path.join(BASE_HUB_DIR, f)
            if os.path.isfile(fp):
                total_bytes += os.path.getsize(fp)
                
        stats["size_mb"] = round(total_bytes / (1024 * 1024), 2)
        return stats
    except:
        return {"total": 0, "categories": {}, "size_mb": 0.0}
