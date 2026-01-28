import json
import os
import sys
import re
from datetime import datetime

# Add paths for local import
base_dir = os.path.dirname(os.path.abspath(__file__))
ai_modules_dir = os.path.join(base_dir, "ai_modules")
if ai_modules_dir not in sys.path:
    sys.path.append(ai_modules_dir)
if base_dir not in sys.path:
    sys.path.append(base_dir)

from shard_manager import delete_entry, update_entry, BASE_HUB_DIR
from gemini_helper import GeminiQMDGHelper

def get_api_key():
    config_path = os.path.join(BASE_HUB_DIR, "factory_config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            return cfg.get("api_key")
    return None

def deep_ai_refinement():
    api_key = get_api_key()
    if not api_key:
        print("❌ No API Key found for AI cleanup.")
        return

    ai = GeminiQMDGHelper(api_key)
    index_path = os.path.join(BASE_HUB_DIR, "hub_index.json")
    
    with open(index_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    index = data.get("index", [])
    print(f"🔍 Analyzing {len(index)} entries...")

    removed_count = 0
    refined_count = 0

    # 1. First pass: Delete obvious errors without AI
    for entry in list(index):
        eid = entry["id"]
        shard_file = entry["shard"]
        shard_path = os.path.join(BASE_HUB_DIR, shard_file)
        
        try:
            with open(shard_path, 'r', encoding='utf-8') as f:
                s_data = json.load(f)
            
            e_data = s_data.get("entries", {}).get(eid)
            if not e_data: continue
            
            content = e_data.get("content", "")
            title = e_data.get("title", "")
            
            # Check for error indicators
            error_keywords = ["❌ Lỗi AI", "🛑 **Hết hạn mức AI**", "400 google_search", "quota", "API Key leaked"]
            if any(kw in content for kw in error_keywords):
                print(f"[-] Deleting error entry: {title}")
                delete_entry(eid)
                removed_count += 1
                index = [e for e in index if e["id"] != eid] # Keep local index in sync
                continue

            # 2. Check for technical junk in labels using AI for batches of 10
        except: continue

    # 2. Second pass: Refine titles in batches
    batch_size = 10
    for i in range(0, len(index), batch_size):
        batch = index[i:i+batch_size]
        titles_map = {e["id"]: e["title"] for e in batch}
        
        prompt = f"""
Bạn là chuyên gia biên tập nội dung. Hãy chuẩn hóa danh sách tiêu đề sau đây.
YÊU CẦU:
- Loại bỏ các tiền tố/hậu tố kỹ thuật: 'Ví dụ:', 'Nghiên cứu:', 'Case study:', 'Phần 1:', 'Ứng dụng:', 'Bí quyết:', 'Chi tiết:'...
- Giữ tên chủ đề NGẮN GỌN, SÚC TÍCH, CHUYÊN NGHIỆP.
- Ví dụ: 'Kỳ Môn Độn Giáp: Bí quyết thành công' -> 'Kỳ Môn Độn Giáp Thành Công'.
- Nếu tiêu đề đã chuẩn, giữ nguyên.

DANH SÁCH (JSON):
{json.dumps(titles_map, ensure_ascii=False, indent=2)}

TRẢ VỀ CHỈ MỘT KHỐI JSON DUY NHẤT VỚI CÂU TRẢ LỜI ĐÃ CHUẨN HÓA (tỉ lệ 1:1 với ID đầu vào).
"""
        try:
            response = ai._call_ai(prompt)
            # Find JSON in response
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            
            refined_titles = json.loads(response)
            
            for eid, new_title in refined_titles.items():
                old_title = titles_map.get(eid)
                if new_title and new_title != old_title:
                    print(f"[*] Refining: {old_title} -> {new_title}")
                    # Update in DB
                    update_entry(eid, title=new_title)
                    refined_count += 1
        except Exception as e:
            print(f"⚠️ Batch refinement failed: {e}")

    print(f"\n✨ Cleanup Complete!")
    print(f"🗑️ Removed (Errors): {removed_count}")
    print(f"🖋️ Refined (Titles): {refined_count}")

if __name__ == "__main__":
    deep_ai_refinement()
