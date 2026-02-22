
# database_tuong_tac.py

LUC_THAN_MAPPING = {
    "Sinh": "Phụ Mẫu", # Thủy sinh Mộc
    "Khắc": "Quan Quỷ", # Kim khắc Mộc
    "Được Sinh": "Tử Tôn", # Mộc sinh Hỏa
    "Bị Khắc": "Thê Tài", # Mộc khắc Thổ
    "Bình": "Huynh Đệ"  # Mộc - Mộc
}

SINH_KHAC_MATRIX = {
    "Kim": {"Kim": "Bình", "Thủy": "Sinh", "Mộc": "Khắc", "Hỏa": "Bị Khắc", "Thổ": "Được Sinh"},
    "Thủy": {"Kim": "Được Sinh", "Thủy": "Bình", "Mộc": "Sinh", "Hỏa": "Khắc", "Thổ": "Bị Khắc"},
    "Mộc": {"Kim": "Bị Khắc", "Thủy": "Được Sinh", "Mộc": "Bình", "Hỏa": "Sinh", "Thổ": "Khắc"},
    "Hỏa": {"Kim": "Khắc", "Thủy": "Bị Khắc", "Mộc": "Được Sinh", "Hỏa": "Bình", "Thổ": "Sinh"},
    "Thổ": {"Kim": "Sinh", "Thủy": "Khắc", "Mộc": "Bị Khắc", "Hỏa": "Được Sinh", "Thổ": "Bình"}
}

# Tương tác giữa Sao và Môn
TUONG_TAC_SAO_MON = {
    # Cát: Sao sinh Môn hoặc Môn sinh Sao
    # Hung: Sao khắc Môn hoặc Môn khắc Sao
    ("Thiên Phụ", "Đỗ Môn"): "Cát (Đồng hành Mộc)",
    ("Thiên Tâm", "Khai Môn"): "Cát (Đồng hành Kim)",
    ("Thiên Nhuế", "Tử Môn"): "Cát (Đồng hành Thổ)",
    ("Thiên Bồng", "Hưu Môn"): "Cát (Đồng hành Thủy)",
    ("Thiên Anh", "Cảnh Môn"): "Cát (Đồng hành Hỏa)",
    ("Thiên Nhậm", "Sinh Môn"): "Cát (Đồng hành Thổ)",
}

QUY_TAC_CHON_DUNG_THAN = {
    "Kinh Doanh": ["Sinh Môn", "Mậu"],
    "Hôn Nhân": ["Ất", "Canh", "Lục Hợp"],
    "Bệnh Tật": ["Thiên Nhuế", "Thiên Tâm", "Ất"],
    "Công Việc": ["Khai Môn", "Trực Phù"]
}

ANH_HUONG_MUA = {
    "Xuân": {"Mộc": "Vượng", "Hỏa": "Tướng", "Thủy": "Hưu", "Kim": "Tù", "Thổ": "Tử"},
    "Hạ": {"Hỏa": "Vượng", "Thổ": "Tướng", "Mộc": "Hưu", "Thủy": "Tù", "Kim": "Tử"},
    "Thu": {"Kim": "Vượng", "Thủy": "Tướng", "Thổ": "Hưu", "Hỏa": "Tù", "Mộc": "Tử"},
    "Đông": {"Thủy": "Vượng", "Mộc": "Tướng", "Kim": "Hưu", "Thổ": "Tù", "Hỏa": "Tử"}
}

TRONG_SO_PHAN_TICH = {
    "Dụng Thần": 0.4,
    "Cung Mệnh": 0.3,
    "Thời Gian": 0.2,
    "Cách Cục": 0.1
}

TRONG_SO_YEU_TO = {
    "Cửa": 0.35,
    "Sao": 0.25,
    "Thần": 0.15,
    "Can": 0.25
}

LUC_THAN_THEO_CHU_DE = {
    "Kinh Doanh": "Thê Tài",
    "Công Việc": "Quan Quỷ",
    "Học Tập": "Phụ Mẫu",
    "Sức Khỏe": "Tử Tôn"
}

def goi_y_doi_tuong_theo_chu_de(topic):
    for key, value in LUC_THAN_THEO_CHU_DE.items():
        if key in topic:
            return value
    return "Huynh Đệ"
