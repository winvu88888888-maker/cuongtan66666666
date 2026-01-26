import random
from datetime import datetime

LUC_THAN = ["Huynh Đệ", "Phụ Mẫu", "Quan Quỷ", "Thê Tài", "Tử Tôn"]
LUC_THU = ["Thanh Long", "Chu Tước", "Câu Trần", "Đằng Xà", "Bạch Hổ", "Huyền Vũ"]
PALACE_ELEMENTS = {"Càn":"Kim", "Đoài":"Kim", "Ly":"Hỏa", "Chấn":"Mộc", "Tốn":"Mộc", "Khảm":"Thủy", "Cấn":"Thổ", "Khôn":"Thổ"}
HEXAGRAM_PALACES = {
    "Càn Vi Thiên":"Càn", "Thiên Địa Bĩ":"Càn", "Thiên Sơn Độn":"Càn", "Thiên Hỏa Đồng Nhân":"Càn",
    "Khôn Vi Địa":"Khôn", "Địa Thiên Thái":"Khôn", "Địa Trạch Lâm":"Khôn", "Địa Lôi Phục":"Khôn",
    "Khảm Vi Thủy":"Khảm", "Thủy Lôi Truân":"Khảm", "Thủy Trạch Tiết":"Khảm", "Thủy Sơn Kiển":"Khảm",
    "Ly Vi Hỏa":"Ly", "Hỏa Thiên Đại Hữu":"Ly", "Hỏa Phong Đỉnh":"Ly", "Hỏa Thủy Vị Tế":"Ly",
    "Chấn Vi Lôi":"Chấn", "Lôi Địa Dự":"Chấn", "Lôi Thủy Giải":"Chấn", "Lôi Phong Hằng":"Chấn",
    "Tốn Vi Phong":"Tốn", "Phong Thiên Tiểu Súc":"Tốn", "Phong Hỏa Gia Nhân":"Tốn", "Phong Lôi Ích":"Tốn",
    "Cấn Vi Sơn":"Cấn", "Sơn Hỏa Bí":"Cấn", "Sơn Thiên Đại Súc":"Cấn", "Sơn Trạch Tổn":"Cấn",
    "Đoài Vi Trạch":"Đoài", "Trạch Thủy Khốn":"Đoài", "Trạch Địa Tụy":"Đoài", "Trạch Sơn Hàm":"Đoài"
}
NAP_GIAP_MAP = {
    "Càn":["Tý-Thủy", "Dần-Mộc", "Thìn-Thổ", "Ngọ-Hỏa", "Thân-Kim", "Tuất-Thổ"], 
    "Khôn":["Mùi-Thổ", "Tị-Hỏa", "Mão-Mộc", "Sửu-Thổ", "Hợi-Thủy", "Dậu-Kim"],
    "Cấn":["Thìn-Thổ", "Ngọ-Hỏa", "Thân-Kim", "Tuất-Thổ", "Tý-Thủy", "Dần-Mộc"],
    "Đoài":["Tị-Hỏa", "Mão-Mộc", "Sửu-Thổ", "Hợi-Thủy", "Dậu-Kim", "Mùi-Thổ"],
    "Khảm":["Dần-Mộc", "Thìn-Thổ", "Ngọ-Hỏa", "Thân-Kim", "Tuất-Thổ", "Tý-Thủy"],
    "Ly":["Mão-Mộc", "Sửu-Thổ", "Hợi-Thủy", "Dậu-Kim", "Mùi-Thổ", "Tị-Hỏa"],
    "Chấn":["Tý-Thủy", "Dần-Mộc", "Thìn-Thổ", "Ngọ-Hỏa", "Thân-Kim", "Tuất-Thổ"],
    "Tốn":["Sửu-Thổ", "Hợi-Thủy", "Dậu-Kim", "Mùi-Thổ", "Tị-Hỏa", "Mão-Mộc"]
}

# 64 Hexagrams Database for Naming
HEXAGRAM_NAMES = {
    (1, 1): "Càn Vi Thiên", (8, 8): "Khôn Vi Địa", (6, 6): "Khảm Vi Thủy", (3, 3): "Ly Vi Hỏa",
    (4, 4): "Chấn Vi Lôi", (5, 5): "Tốn Vi Phong", (7, 7): "Cấn Vi Sơn", (2, 2): "Đoài Vi Trạch",
    (1, 8): "Thiên Địa Bĩ", (8, 1): "Địa Thiên Thái", (6, 3): "Thủy Hỏa Ký Tế", (3, 6): "Hỏa Thủy Vị Tế",
    (2, 1): "Trạch Thiên Quải", (1, 2): "Thiên Trạch Lý", (3, 1): "Hỏa Thiên Đại Hữu", (1, 3): "Thiên Hỏa Đồng Nhân",
    (4, 1): "Lôi Thiên Đại Tráng", (1, 4): "Thiên Lôi Vô Vọng", (5, 1): "Phong Thiên Tiểu Súc", (1, 5): "Thiên Phong Cấu",
    (7, 1): "Sơn Thiên Đại Súc", (1, 7): "Thiên Sơn Độn", (8, 2): "Địa Trạch Lâm", (2, 8): "Trạch Địa Tụy",
    (3, 2): "Hỏa Trạch Khuê", (2, 3): "Trạch Hỏa Cách", (4, 2): "Lôi Trạch Quy Muội", (2, 4): "Trạch Lôi Tùy",
    (5, 2): "Phong Trạch Trung Phu", (2, 5): "Trạch Phong Đại Quá", (6, 2): "Thủy Trạch Tiết", (2, 6): "Trạch Thủy Khốn",
    (7, 2): "Sơn Trạch Tổn", (2, 7): "Trạch Sơn Hàm", (4, 3): "Lôi Hỏa Phong", (3, 4): "Hỏa Lôi Phệ Hạp",
    (5, 3): "Phong Hỏa Gia Nhân", (3, 5): "Hỏa Phong Đỉnh", (6, 4): "Thủy Lôi Truân", (4, 6): "Lôi Thủy Giải",
    # ... can add more as needed, or use a helper to derive from lines
}

def lines_to_quai_num(lines):
    m = {(1,1,1):1, (1,1,0):2, (1,0,1):3, (1,0,0):4, (0,1,1):5, (0,1,0):6, (0,0,1):7, (0,0,0):8}
    return m.get(tuple(lines), 1)

def get_hex_name(lines):
    # lines: 0,1,2 (lower), 3,4,5 (upper)
    lower = lines_to_quai_num(lines[:3])
    upper = lines_to_quai_num(lines[3:])
    return HEXAGRAM_NAMES.get((upper, lower), f"Quẻ {upper}-{lower}")

def get_element_strength(h_element, month):
    # month is 1-12
    # Simple mapping: 1,2: Mộc, 4,5: Hỏa, 7,8: Kim, 10,11: Thủy, 3,6,9,12: Thổ
    month_element_map = {
        1: "Mộc", 2: "Mộc", 4: "Hỏa", 5: "Hỏa", 7: "Kim", 8: "Kim", 10: "Thủy", 11: "Thủy",
        3: "Thổ", 6: "Thổ", 9: "Thổ", 12: "Thổ"
    }
    m_el = month_element_map.get(month, "Thổ")
    
    strengths = {
        "Mộc": {"Mộc": "Vượng", "Hỏa": "Tướng", "Thủy": "Hưu", "Thổ": "Tù", "Kim": "Tử"},
        "Hỏa": {"Hỏa": "Vượng", "Thổ": "Tướng", "Mộc": "Hưu", "Kim": "Tù", "Thủy": "Tử"},
        "Thổ": {"Thổ": "Vượng", "Kim": "Tướng", "Hỏa": "Hưu", "Thủy": "Tù", "Mộc": "Tử"},
        "Kim": {"Kim": "Vượng", "Thủy": "Tướng", "Thổ": "Hưu", "Mộc": "Tù", "Hỏa": "Tử"},
        "Thủy": {"Thủy": "Vượng", "Mộc": "Tướng", "Kim": "Hưu", "Hỏa": "Tù", "Thổ": "Tử"},
    }
    return strengths.get(m_el, {}).get(h_element, "Bình")

def get_tuan_khong(can_ngay, chi_ngay):
    # Simplified Tuan Khong
    can_map = {"Giáp":1, "Ất":2, "Bính":3, "Đinh":4, "Mậu":5, "Kỷ":6, "Canh":7, "Tân":8, "Nhâm":9, "Quý":10}
    chi_map = {"Tý":1, "Sửu":2, "Dần":3, "Mão":4, "Thìn":5, "Tị":6, "Ngọ":7, "Mùi":8, "Thân":9, "Dậu":10, "Tuất":11, "Hợi":12}
    
    c_idx = can_map.get(can_ngay, 1)
    ch_idx = chi_map.get(chi_ngay, 1)
    
    # Tuan Khong branches (2 branches after the 10th stem in the current 12 branch cycle)
    start_phi = (ch_idx - c_idx + 1)
    if start_phi <= 0: start_phi += 12
    
    void_indices = [(start_phi + 10 - 1) % 12 + 1, (start_phi + 11 - 1) % 12 + 1]
    inv_chi_map = {v: k for k, v in chi_map.items()}
    return [inv_chi_map.get(idx) for idx in void_indices]

def get_dich_ma(chi_ngay):
    map_ma = {
        "Thân": "Dần", "Tý": "Dần", "Thìn": "Dần",
        "Dần": "Thân", "Ngọ": "Thân", "Tuất": "Thân",
        "Tị": "Hợi", "Dậu": "Hợi", "Sửu": "Hợi",
        "Hợi": "Tị", "Mão": "Tị", "Mùi": "Tị"
    }
    return map_ma.get(chi_ngay, "")

def get_luc_than(h_element, p_element):
    relations = {
        "Kim": {"Kim": "Huynh Đệ", "Mộc": "Thê Tài", "Hỏa": "Quan Quỷ", "Thủy": "Tử Tôn", "Thổ": "Phụ Mẫu"},
        "Mộc": {"Mộc": "Huynh Đệ", "Thổ": "Thê Tài", "Kim": "Quan Quỷ", "Hỏa": "Tử Tôn", "Thủy": "Phụ Mẫu"},
        "Thủy": {"Thủy": "Huynh Đệ", "Hỏa": "Thê Tài", "Thổ": "Quan Quỷ", "Mộc": "Tử Tôn", "Kim": "Phụ Mẫu"},
        "Hỏa": {"Hỏa": "Huynh Đệ", "Kim": "Thê Tài", "Thủy": "Quan Quỷ", "Thổ": "Tử Tôn", "Mộc": "Phụ Mẫu"},
        "Thổ": {"Thổ": "Huynh Đệ", "Thủy": "Thê Tài", "Mộc": "Quan Quỷ", "Kim": "Tử Tôn", "Hỏa": "Phụ Mẫu"},
    }
    return relations.get(p_element, {}).get(h_element, "Huynh Đệ")

def lap_qua_luc_hao(year, month, day, hour, topic="Chung", can_ngay="Giáp", chi_ngay="Tý", **kwargs):
    hao_results = [random.randint(6, 9) for _ in range(6)]
    ban_lines = [1 if h in [7, 9] else 0 for h in hao_results]
    bien_lines = [ (0 if h==9 else 1 if h==6 else (1 if h==7 else 0)) for h in hao_results ]
    
    ban_name = get_hex_name(ban_lines)
    bien_name = get_hex_name(bien_lines)
    
    palace = HEXAGRAM_PALACES.get(ban_name, "Càn")
    p_element = PALACE_ELEMENTS.get(palace, "Kim")
    
    start_thu = {"Giáp":0, "Ất":0, "Bính":1, "Đinh":1, "Mậu":2, "Kỷ":3, "Canh":4, "Tân":4, "Nhâm":5, "Quý":5}.get(can_ngay[0], 0)
    nap_giap = NAP_GIAP_MAP.get(palace, NAP_GIAP_MAP["Càn"])
    
    # Advanced markers
    void_branches = get_tuan_khong(can_ngay, chi_ngay)
    ma_branch = get_dich_ma(chi_ngay)
    
    # Simple The/Ung logic (Hào 3/6 as common default in simplified apps, but let's vary it)
    the_pos = random.choice([1, 2, 3, 4, 5, 6])
    ung_pos = (the_pos + 2) % 6 + 1
    
    details_ban = []
    for i in range(6):
        cc = nap_giap[i]; c_branch = cc.split("-")[0]; c_element = cc.split("-")[1]
        lt = get_luc_than(c_element, p_element)
        strength = get_element_strength(c_element, month)
        
        markers = []
        if (i+1)==the_pos: markers.append("(T)")
        if (i+1)==ung_pos: markers.append("(Ứ)")
        if c_branch in void_branches: markers.append("(○)") # Void
        if c_branch == ma_branch: markers.append("(🐎)") # Traveling Horse
        
        details_ban.append({
            'hao': i+1, 'line': ban_lines[i], 'is_moving': hao_results[i] in [6, 9],
            'luc_than': lt, 'can_chi': cc, 'luc_thu': LUC_THU[(start_thu+i)%6],
            'strength': strength,
            'marker': " ".join(markers)
        })
        
    details_bien = []
    for i in range(6):
        # Biến hexagram Can Chi usually depends on its own quái
        # For simplicity, we use same palace's nap giap but can be improved
        cc = nap_giap[i]; c_branch = cc.split("-")[0]; c_element = cc.split("-")[1]
        lt = get_luc_than(c_element, p_element)
        strength = get_element_strength(c_element, month)
        
        markers_b = []
        if c_branch in void_branches: markers_b.append("(○)")
        if c_branch == ma_branch: markers_b.append("(🐎)")
        
        details_bien.append({
            'hao': i+1, 'line': bien_lines[i], 'is_moving': False,
            'luc_than': lt, 'can_chi': cc, 'luc_thu': LUC_THU[(start_thu+i)%6],
            'strength': strength,
            'marker': " ".join(markers_b)
        })
        
    return {
        'ban': {'name': ban_name, 'lines': ban_lines, 'details': details_ban, 'palace': palace},
        'bien': {'name': bien_name, 'lines': bien_lines, 'details': details_bien},
        'dong_hao': [i+1 for i, h in enumerate(hao_results) if h in [6, 9]],
        'conclusion': f"Quẻ {ban_name} biến {bien_name}. {topic} tốt lành.",
        'the_ung': f"Thế hào {the_pos}, Ứng hào {ung_pos}"
    }

# 64 Hexagrams Database for Naming remains unchanged
