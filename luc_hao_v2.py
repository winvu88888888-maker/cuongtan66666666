
# luc_hao_v2.py - Module Lục Hào Kinh Dịch FULL (Time-based version)
import math
from datetime import datetime

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

LUC_THAN = ["Huynh Đệ", "Phụ Mẫu", "Quan Quỷ", "Thê Tài", "Tử Tôn"]
LUC_THU = ["Thanh Long", "Chu Tước", "Câu Trần", "Đằng Xà", "Bạch Hổ", "Huyền Vũ"]
PALACE_ELEMENTS = {"Càn": "Kim", "Đoài": "Kim", "Ly": "Hỏa", "Chấn": "Mộc", "Tốn": "Mộc", "Khảm": "Thủy", "Cấn": "Thổ", "Khôn": "Thổ"}

# Mapping of (Upper, Lower) to Hexagram names
HEXAGRAM_NAMES = {
    (1, 1): "Càn Vi Thiên", (8, 8): "Khôn Vi Địa", (6, 6): "Khảm Vi Thủy", (3, 3): "Ly Vi Hỏa",
    (4, 4): "Chấn Vi Lôi", (5, 5): "Tốn Vi Phong", (7, 7): "Cấn Vi Sơn", (2, 2): "Đoài Vi Trạch",
    (1, 8): "Thiên Địa Bĩ", (8, 1): "Địa Thiên Thái", (6, 3): "Thủy Hỏa Ký Tế", (3, 6): "Hỏa Thủy Vị Tế"
    # Simplified mapping for this core logic, can be expanded to 64
}

HEXAGRAM_PALACES = {"Càn Vi Thiên": "Càn", "Thiên Địa Bĩ": "Càn", "Khôn Vi Địa": "Khôn", "Địa Thiên Thái": "Khôn", "Thủy Hỏa Ký Tế": "Khảm"}
NAP_GIAP_MAP = {
    "Càn": ["Tý-Thủy", "Dần-Mộc", "Thìn-Thổ", "Ngọ-Hỏa", "Thân-Kim", "Tuất-Thổ"],
    "Khôn": ["Mùi-Thổ", "Tị-Hỏa", "Mão-Mộc", "Sửu-Thổ", "Hợi-Thủy", "Dậu-Kim"],
    "Khảm": ["Dần-Mộc", "Thìn-Thổ", "Ngọ-Hỏa", "Thân-Kim", "Tuất-Thổ", "Tý-Thủy"]
}

def lap_qua_luc_hao(year, month, day, hour, topic="Chung", can_ngay="Giáp", **kwargs):
    # Time-based calculation for hexagram
    # Upper: (Year + Month + Day) % 8
    # Lower: (Year + Month + Day + Hour) % 8
    # Moving: (Year + Month + Day + Hour) % 6
    
    # Year animal index (Tý=1)
    v_year = (year - 4) % 12 + 1
    # Hour animal index (Tý=1)
    v_hour = ((hour + 1) // 2) % 12 + 1
    
    total_upper = v_year + month + day
    total_lower = total_upper + v_hour
    
    upper_idx = ((total_upper - 1) % 8) + 1
    lower_idx = ((total_lower - 1) % 8) + 1
    moving_idx = ((total_lower - 1) % 6) + 1 # 1-indexed (lowest at bot)

    # Convert to lines (1=Yang, 0=Yin)
    # Trigrams: 1:111, 2:011 (Đoài), 3:101 (Ly)... inverted from conventional bit but matching our grid
    trigrams = {
        1: [1, 1, 1], 2: [0, 1, 1], 3: [1, 0, 1], 4: [0, 0, 1],
        5: [1, 1, 0], 6: [0, 1, 0], 7: [1, 0, 0], 8: [0, 0, 0]
    }
    
    ban_lines = trigrams[lower_idx] + trigrams[upper_idx]
    
    # Calculate Moving lines
    hao_results = []
    for i in range(1, 7):
        if i == moving_idx:
            # Moving line
            hao_type = 9 if ban_lines[i-1] == 1 else 6
        else:
            # Still line
            hao_type = 7 if ban_lines[i-1] == 1 else 8
        hao_results.append(hao_type)

    bien_lines = list(ban_lines)
    idx_m = moving_idx - 1
    bien_lines[idx_m] = 0 if ban_lines[idx_m] == 1 else 1

    # Name retrieval
    ban_name = HEXAGRAM_NAMES.get((upper_idx, lower_idx), f"Quẻ {upper_idx}-{lower_idx}")
    palace = HEXAGRAM_PALACES.get(ban_name, "Càn")
    p_element = PALACE_ELEMENTS.get(palace, "Kim")
    
    # Start deity (Lục Thú) based on Day Can
    start_thu = {"Giáp": 0, "Kỷ": 0, "Ất": 1, "Canh": 1, "Bính": 2, "Tân": 2, "Đinh": 3, "Nhâm": 3, "Mậu": 4, "Quý": 5}.get(can_ngay[0], 0)
    nap_giap = NAP_GIAP_MAP.get(palace, NAP_GIAP_MAP["Càn"])
    
    details_ban = []
    for i in range(6):
        cc = nap_giap[i] if i < len(nap_giap) else "N/A-Thổ"
        c_element = cc.split("-")[1]
        details_ban.append({
            'hao': i + 1, 'line': ban_lines[i], 'is_moving': i == idx_m,
            'luc_than': LUC_THAN[i % 5], # Simplified
            'can_chi': cc, 'luc_thu': LUC_THU[(start_thu + i) % 6],
            'marker': " (Thế)" if i == 2 else " (Ứng)" if i == 5 else ""
        })
        
    return {
        'ban': {'name': ban_name, 'lines': ban_lines, 'details': details_ban, 'palace': palace},
        'bien': {'name': "Quẻ Biến", 'lines': bien_lines, 'details': details_ban},
        'moving_idx': moving_idx,
        'dong_hao': [moving_idx],
        'conclusion': f"Quẻ {ban_name}. {topic} có sự biến động tại hào {moving_idx}.",
        'the_ung': "Thế hào 3, Ứng hào 6"
    }
