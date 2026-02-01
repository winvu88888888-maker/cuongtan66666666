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
from gemini_expert_v172 import GeminiQMDGHelper

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
            error_keywords = ["❌ Lỗi AI", "🛑 **Hết hạn mức AI**", "400 google_search", "google_search_retrieval", "quota", "API Key leaked"]
            if any(kw in content for kw in error_keywords):
                print(f"[-] Deleting error entry: {title}")
                delete_entry(eid)
                removed_count += 1
                index = [e for e in index if e["id"] != eid] # Keep local index in sync
                continue

            # 2. Check for technical junk in labels using AI for batches of 10
        except: continue

    # 2. Second pass: Refine titles and CATEGORY in batches
    batch_size = 10
    from ai_modules.mining_strategist import MiningStrategist
    categories = list(MiningStrategist().categories.keys()) + ["Kiến Thức", "Lưu Trữ (Sách)", "Khác"]
    
    for i in range(0, len(index), batch_size):
        batch = index[i:i+batch_size]
        entries_data = []
        for e in batch:
            # Try to get a snippet of content for better classification
            snippet = ""
            full_e = get_full_entry(e["id"], e["shard"])
            if full_e:
                snippet = full_e.get("content", "")[:300]
            
            entries_data.append({
                "id": e["id"],
                "title": e["title"],
                "content_snippet": snippet
            })
        
        prompt = f"""
Bạn là chuyên gia phân loại nội dung cho hệ thống Kỳ Môn Độn Giáp.
Hãy phân loại và chuẩn hóa danh sách sau đây.

MỤC TIÊU:
- Nhận diện các tiêu đề là "Tên sách", "Kiến thức lý thuyết suông" hoặc "Nội dung không dùng để gieo quẻ/xem bói".
- Những nội dung đó hãy chuyển vào phân loại: 'Lưu Trữ (Sách)'.
- Những nội dung thực tiễn (Ví dụ: 'Đầu tư 2026', 'Sức khỏe', 'Tình duyên'...) hãy giữ ở phân loại phù hợp.
- Chuẩn hóa tiêu đề: Loại bỏ tiền tố rác (Ví dụ:, Nghiên cứu:, ...).

PHÂN LOẠI CHO PHÉP: {categories}

DANH SÁCH (JSON):
{json.dumps(entries_data, ensure_ascii=False, indent=2)}

TRẢ VỀ JSON DUY NHẤT:
{{
  "id_cần_xử_lý": {{
    "title": "Tiêu đề mới",
    "category": "Phân loại mới"
  }}
}}
"""
        prompt = f"""
Bạn là chuyên gia phân loại và tối ưu hóa nội dung cho hệ thống Kỳ Môn Độn Giáp & Kinh Dịch.
Hãy phân loại và chuẩn hóa danh sách sau đây để Kho dữ liệu trở nên ngăn nắp và chuyên nghiệp hơn.

MỤC TIÊU:
- **PHÂN LOẠI CHÍNH XÁC**: Đưa nội dung vào đúng danh mục phù hợp nhất.
- **BẢO TỒN DỮ LIỆU**: KHÔNG ĐƯỢC xóa bỏ nội dung. Nếu nội dung không thuộc các chuyên ngành chính, hãy đưa vào mục 'Khác'.
- **DỌN DẸP TIÊU ĐỀ**: Loại bỏ các tiền tố rác (Ví dụ: 'Nghiên cứu:', 'AI Summary:', ...), giữ tiêu đề ngắn gọn, súc tích và đúng trọng tâm.

PHÂN LOẠI CHO PHÉP: {categories}

DANH SÁCH (JSON):
{json.dumps(entries_data, ensure_ascii=False, indent=2)}

TRẢ VỀ JSON DUY NHẤT:
{{
  "id_cần_xử_lý": {{
    "title": "Tiêu đề mới chuẩn hóa",
    "category": "Phân loại mới (Dùng 'Khác' nếu không thuộc chuyên mục nào)"
  }}
}}
"""
        try:
            from ai_modules.shard_manager import get_full_entry, delete_entry
            response = ai._call_ai(prompt)
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            
            refinements = json.loads(response)
            
            for eid, ref in refinements.items():
                new_title = ref.get("title")
                new_cat = ref.get("category")
                
                # KHÔNG XÓA DỮ LIỆU CỦA NGƯỜI DÙNG - CHỈ PHÂN LOẠI LẠI
                if new_cat == "DELETE" or not new_cat:
                    new_cat = "Khác"
                
                print(f"[*] Updating {eid}: Category -> {new_cat}")
                update_entry(eid, title=new_title, category=new_cat)
                refined_count += 1
        except Exception as e:
            print(f"⚠️ Batch refinement failed: {e}")

    print(f"\n✨ Cleanup Complete!")
    print(f"🗑️ Removed (Errors/Off-topic): {removed_count}")
    print(f"🖋️ Processed (AI): {refined_count}")

if __name__ == "__main__":
    deep_ai_refinement()
