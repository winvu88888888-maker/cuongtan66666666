"""
AUTO KNOWLEDGE UPDATER - Hệ Thống Tự Động Học & Cập Nhật Dữ Liệu
Mỗi khi AI trả lời, nếu phát hiện thông tin mới sẽ tự động lưu vào kho
"""

import json
import os
from datetime import datetime

# Đường dẫn kho dữ liệu
KNOWLEDGE_STORE_PATH = os.path.join(os.path.dirname(__file__), 'knowledge_store.json')

def load_knowledge_store():
    """Tải kho dữ liệu đã học"""
    if os.path.exists(KNOWLEDGE_STORE_PATH):
        try:
            with open(KNOWLEDGE_STORE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"topics": {}, "last_updated": None}
    return {"topics": {}, "last_updated": None}

def save_knowledge_store(data):
    """Lưu kho dữ liệu"""
    data["last_updated"] = datetime.now().isoformat()
    try:
        with open(KNOWLEDGE_STORE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def auto_learn_from_question(topic, question, answer):
    """
    Tự động học từ câu hỏi và câu trả lời
    Lưu các pattern mới vào kho dữ liệu
    """
    store = load_knowledge_store()
    
    # Chuẩn hóa topic
    topic_key = topic.lower().strip()
    
    if topic_key not in store["topics"]:
        store["topics"][topic_key] = {
            "count": 0,
            "patterns": [],
            "keywords": [],
            "sample_qa": []
        }
    
    topic_data = store["topics"][topic_key]
    topic_data["count"] += 1
    
    # Trích xuất keywords từ câu hỏi
    keywords = extract_keywords(question)
    for kw in keywords:
        if kw not in topic_data["keywords"]:
            topic_data["keywords"].append(kw)
    
    # Lưu sample Q&A (tối đa 10)
    if len(topic_data["sample_qa"]) < 10:
        topic_data["sample_qa"].append({
            "q": question[:200],  # Giới hạn độ dài
            "a": answer[:500] if answer else "",
            "time": datetime.now().isoformat()
        })
    
    save_knowledge_store(store)
    return True

def extract_keywords(text):
    """Trích xuất keywords từ văn bản"""
    # Các từ khóa quan trọng trong QMDG
    important_terms = [
        "hướng", "khoảng cách", "nam", "nữ", "đàn ông", "phụ nữ",
        "quen", "lạ", "người thân", "trộm", "mất", "tìm", "lấy lại",
        "màu", "đỏ", "xanh", "vàng", "trắng", "đen",
        "gần", "xa", "bắc", "nam", "đông", "tây",
        "sinh môn", "tử môn", "khai môn", "hưu môn",
        "huyền vũ", "bạch hổ", "thiên bồng", "trực phù",
        "cung 1", "cung 2", "cung 3", "cung 4", "cung 5",
        "cung 6", "cung 7", "cung 8", "cung 9",
        "kinh doanh", "hôn nhân", "sức khỏe", "công việc", "tài lộc"
    ]
    
    text_lower = text.lower()
    found = []
    for term in important_terms:
        if term in text_lower:
            found.append(term)
    return found

def get_learned_knowledge(topic):
    """Lấy kiến thức đã học về một chủ đề"""
    store = load_knowledge_store()
    topic_key = topic.lower().strip()
    
    if topic_key in store["topics"]:
        topic_data = store["topics"][topic_key]
        return {
            "has_data": True,
            "count": topic_data["count"],
            "keywords": topic_data["keywords"][:20],  # Top 20 keywords
            "sample_qa": topic_data["sample_qa"][-3:]  # 3 Q&A gần nhất
        }
    return {"has_data": False}

def get_all_learned_topics():
    """Lấy danh sách tất cả chủ đề đã học"""
    store = load_knowledge_store()
    topics = []
    for key, data in store["topics"].items():
        topics.append({
            "topic": key,
            "count": data["count"],
            "keywords_count": len(data["keywords"])
        })
    return sorted(topics, key=lambda x: x["count"], reverse=True)

# ============================================================
# LĨNH VỰC ĐÃ CÓ SẴN DỮ LIỆU CHI TIẾT
# ============================================================

LINH_VUC_CO_SAN = {
    "Tìm Đồ Mất": {
        "Dung_Than": ["Can Giờ", "Huyền Vũ"],
        "Yeu_To_Phan_Tich": ["hướng", "khoảng cách", "giới tính", "quen/lạ", "màu sắc", "khả năng tìm"],
        "Do_Chi_Tiet": "★★★★★ (5/5)",
        "File_Du_Lieu": ["qmdg_knowledge_complete.py", "qmdg_advanced_rules.py", "qmdg_data.py"]
    },
    "Kinh Doanh": {
        "Dung_Than": ["Sinh Môn", "Mậu", "Can Ngày"],
        "Yeu_To_Phan_Tich": ["lợi nhuận", "thời điểm", "đối tác", "rủi ro"],
        "Do_Chi_Tiet": "★★★★☆ (4/5)",
        "File_Du_Lieu": ["qmdg_data.py"]
    },
    "Hôn Nhân": {
        "Dung_Than": ["Ất", "Canh", "Lục Hợp"],
        "Yeu_To_Phan_Tich": ["tương hợp", "thời điểm", "người thứ ba", "hạnh phúc"],
        "Do_Chi_Tiet": "★★★★☆ (4/5)",
        "File_Du_Lieu": ["qmdg_data.py"]
    },
    "Bệnh Tật": {
        "Dung_Than": ["Thiên Nhuế", "Thiên Tâm", "Ất"],
        "Yeu_To_Phan_Tich": ["bệnh gì", "có khỏi không", "thầy thuốc"],
        "Do_Chi_Tiet": "★★★☆☆ (3/5)",
        "File_Du_Lieu": ["qmdg_data.py"]
    },
    "Công Việc": {
        "Dung_Than": ["Khai Môn", "Trực Phù"],
        "Yeu_To_Phan_Tich": ["thăng tiến", "đổi việc", "sếp", "đồng nghiệp"],
        "Do_Chi_Tiet": "★★★★☆ (4/5)",
        "File_Du_Lieu": ["qmdg_data.py"]
    },
    "Thi Cử": {
        "Dung_Than": ["Cảnh Môn", "Đinh", "Thiên Phụ"],
        "Yeu_To_Phan_Tich": ["đỗ/trượt", "điểm số", "trường"],
        "Do_Chi_Tiet": "★★★☆☆ (3/5)",
        "File_Du_Lieu": ["qmdg_data.py"]
    },
    "Xuất Hành": {
        "Dung_Than": ["Mã Tinh", "Khai Môn", "Can Ngày"],
        "Yeu_To_Phan_Tich": ["an toàn", "hướng đi", "thời điểm"],
        "Do_Chi_Tiet": "★★★☆☆ (3/5)",
        "File_Du_Lieu": ["qmdg_data.py"]
    },
    "Kiện Tụng": {
        "Dung_Than": ["Khai Môn", "Trực Phù", "Canh"],
        "Yeu_To_Phan_Tich": ["thắng/thua", "luật sư", "thời gian"],
        "Do_Chi_Tiet": "★★★☆☆ (3/5)",
        "File_Du_Lieu": ["qmdg_data.py"]
    }
}

def get_field_detail_level(topic):
    """Kiểm tra mức độ chi tiết của dữ liệu theo lĩnh vực"""
    for field, info in LINH_VUC_CO_SAN.items():
        if field.lower() in topic.lower():
            return info
    return None

# Export
__all__ = [
    'auto_learn_from_question', 'get_learned_knowledge', 
    'get_all_learned_topics', 'LINH_VUC_CO_SAN', 'get_field_detail_level'
]
