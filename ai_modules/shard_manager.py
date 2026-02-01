import os
import json
import uuid
from datetime import datetime
from pathlib import Path

# Configuration
BASE_HUB_DIR = "data_hub"
INDEX_FILE = os.path.join(BASE_HUB_DIR, "hub_index.json")
MAX_ENTRIES_PER_SHARD = 500  # Increased from 100 for better efficiency

def initialize_hub():
    """Initialize the directory and index if they don't exist."""
    if not os.path.exists(BASE_HUB_DIR):
        os.makedirs(BASE_HUB_DIR)
    
    if not os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump({"index": [], "stats": {"total": 0, "categories": {}}}, f, indent=2)

def _check_duplicate(title, index_data):
    """Check if an entry with similar title already exists.
    Returns the duplicate entry if found, None otherwise."""
    title_lower = title.lower().strip()
    for entry in index_data.get("index", []):
        if entry.get("title", "").lower().strip() == title_lower:
            return entry
    return None

def add_entry(title, content, category="Kiến Thức", source="AI Miner", tags=None, allow_duplicate=False):
    """Add a new entry into a shard and update the index.
    
    Args:
        title: Title of the entry
        content: Full content
        category: Category (default: "Kiến Thức")
        source: Source of the entry (default: "AI Miner")
        tags: List of tags (optional)
        allow_duplicate: If False, skip adding if duplicate title exists
        
    Returns:
        entry_id if added, None if skipped due to duplicate
    """
    initialize_hub()
    
    # Load index
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
    
    # Check for duplicates unless explicitly allowed
    if not allow_duplicate:
        duplicate = _check_duplicate(title, index_data)
        if duplicate:
            print(f"⚠️ Skipped duplicate: '{title}' (existing ID: {duplicate['id']})")
            return None
    
    entry_id = str(uuid.uuid4())[:8] + datetime.now().strftime("%Y%m%d%H%M%S")
    timestamp = datetime.now().isoformat()
    tags = tags or []
    
    # 1. Determine Shard
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
    
    # Atomic Write to Shard
    temp_shard_path = f"{shard_path}.tmp"
    with open(temp_shard_path, 'w', encoding='utf-8') as f:
        json.dump(shard_data, f, indent=2, ensure_ascii=False)
    os.replace(temp_shard_path, shard_path)
        
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
    
    # Atomic Write to Index
    temp_index_path = f"{INDEX_FILE}.tmp"
    with open(temp_index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    os.replace(temp_index_path, INDEX_FILE)
        
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
            # Atomic Write to Shard
            temp_shard_path = f"{shard_path}.tmp"
            with open(temp_shard_path, 'w', encoding='utf-8') as f:
                json.dump(shard_data, f, indent=2, ensure_ascii=False)
            os.replace(temp_shard_path, shard_path)
                
    # 2. Remove from Index
    index_data["index"] = [e for e in index_data["index"] if e["id"] != entry_id]
    index_data["stats"]["total"] -= 1
    cat = entry_ref["category"]
    index_data["stats"]["categories"][cat] = max(0, index_data["stats"]["categories"].get(cat, 0) - 1)
    
    # Atomic Write to Index
    temp_index_path = f"{INDEX_FILE}.tmp"
    with open(temp_index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    os.replace(temp_index_path, INDEX_FILE)
    
    return True

def update_entry(entry_id, title=None, category=None, tags=None, content=None):
    """Update an existing entry in both index and shard."""
    if not os.path.exists(INDEX_FILE): return False
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_data = json.load(f)
        
    # Find in index
    entry_idx = next((i for i, e in enumerate(index_data["index"]) if e["id"] == entry_id), -1)
    if entry_idx == -1: return False
    
    entry_ref = index_data["index"][entry_idx]
    old_cat = entry_ref["category"]
    
    # 1. Update Shard
    shard_path = os.path.join(BASE_HUB_DIR, entry_ref["shard"])
    if os.path.exists(shard_path):
        with open(shard_path, 'r', encoding='utf-8') as f:
            shard_data = json.load(f)
        
        if entry_id in shard_data["entries"]:
            e = shard_data["entries"][entry_id]
            if title: e["title"] = title
            if category: e["category"] = category
            if tags: e["tags"] = tags
            if content: e["content"] = content
            
            # Atomic Write to Shard
            temp_shard_path = f"{shard_path}.tmp"
            with open(temp_shard_path, 'w', encoding='utf-8') as f:
                json.dump(shard_data, f, indent=2, ensure_ascii=False)
            os.replace(temp_shard_path, shard_path)
                
    # 2. Update Index
    if title: entry_ref["title"] = title
    if category: entry_ref["category"] = category
    if tags: entry_ref["tags"] = tags
    
    # Update Stats if category changed
    if category and category != old_cat:
        index_data["stats"]["categories"][old_cat] = max(0, index_data["stats"]["categories"].get(old_cat, 0) - 1)
        index_data["stats"]["categories"][category] = index_data["stats"]["categories"].get(category, 0) + 1
    
    # Atomic Write to Index
    temp_index_path = f"{INDEX_FILE}.tmp"
    with open(temp_index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    os.replace(temp_index_path, INDEX_FILE)
    
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

def cleanup_duplicates():
    """Remove duplicate entries from the data hub.
    Keeps the oldest entry and removes newer duplicates.
    
    Returns:
        dict: Stats about cleanup operation
    """
    if not os.path.exists(INDEX_FILE):
        return {"removed": 0, "error": "No index file"}
    
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        seen_titles = {}
        duplicates = []
        
        for entry in index_data.get("index", []):
            title_key = entry.get("title", "").lower().strip()
            if title_key in seen_titles:
                duplicates.append(entry["id"])
            else:
                seen_titles[title_key] = entry["id"]
        
        # Remove duplicates
        removed_count = 0
        for dup_id in duplicates:
            if delete_entry(dup_id):
                removed_count += 1
        
        return {
            "removed": removed_count,
            "total_checked": len(index_data.get("index", [])),
            "unique_entries": len(seen_titles)
        }
    except Exception as e:
        return {"removed": 0, "error": str(e)}

def find_similar_entries(query, threshold=0.8, max_results=10):
    """Find entries with similar titles using simple matching.
    
    Args:
        query: Search query string
        threshold: Minimum similarity ratio (0.0 to 1.0)
        max_results: Maximum number of results to return
        
    Returns:
        List of similar entries with similarity scores
    """
    if not os.path.exists(INDEX_FILE):
        return []
    
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        query_lower = query.lower().strip()
        query_words = set(query_lower.split())
        results = []
        
        for entry in index_data.get("index", []):
            title = entry.get("title", "").lower().strip()
            title_words = set(title.split())
            
            # Calculate Jaccard similarity
            if title_words or query_words:
                intersection = len(query_words & title_words)
                union = len(query_words | title_words)
                similarity = intersection / union if union > 0 else 0
                
                if similarity >= threshold:
                    results.append({
                        **entry,
                        "similarity": round(similarity, 2)
                    })
        
        # Sort by similarity, descending
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:max_results]
    except:
        return []

