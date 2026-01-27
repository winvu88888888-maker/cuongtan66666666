
# phan_tich_da_tang.py
from database_tuong_tac import (
    LUC_THAN_MAPPING, 
    SINH_KHAC_MATRIX, 
    QUY_TAC_CHON_DUNG_THAN, 
    ANH_HUONG_MUA, 
    TRONG_SO_PHAN_TICH
)
from qmdg_data import KY_MON_DATA, CUNG_NGU_HANH

def chon_dung_than_theo_chu_de(topic):
    """Chọn dụng thần dựa trên chủ đề bí truyền."""
    return QUY_TAC_CHON_DUNG_THAN.get(topic, ["Can Ngày", "Trực Phù"])

def xac_dinh_luc_than(cung_hanh, chu_hanh):
    """Xác định Lục Thân của một cung so với cung chủ."""
    tuong_tac = SINH_KHAC_MATRIX.get(chu_hanh, {}).get(cung_hanh, "Bình")
    return LUC_THAN_MAPPING.get(tuong_tac, "Huynh Đệ")

def phan_tich_sinh_khac_hop(hanh1, hanh2):
    """Phân tích chi tiết mối quan hệ sinh khắc giữa 2 ngũ hành."""
    return SINH_KHAC_MATRIX.get(hanh1, {}).get(hanh2, "Bình Hòa")

def phan_tich_tuong_tac_trong_cung(sao, cua, than, cung_so):
    """Phân tích tương tác giữa các yếu tố trong cùng 1 cung."""
    cung_hanh = CUNG_NGU_HANH.get(cung_so)
    sao_hanh = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['CUU_TINH'].get(sao, {}).get('Hành')
    cua_hanh = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_MON'].get(cua + " Môn", {}).get('Hành', 'N/A')
    
    # Logic đơn giản: Sao/Cửa sinh cung = Cát, Khắc cung = Hung
    diem = 0
    if phan_tich_sinh_khac_hop(sao_hanh, cung_hanh) == "Sinh": diem += 10
    if phan_tich_sinh_khac_hop(cua_hanh, cung_hanh) == "Sinh": diem += 15
    
    return {"diem_noi_tai": diem, "chi_tiet": f"Sao {sao} ({sao_hanh}), Cửa {cua} ({cua_hanh}) tương tác với Cung {cung_so} ({cung_hanh})"}

def phan_tich_tuong_tac_giua_cac_cung(cung1_idx, cung2_idx):
    """Phân tích tương tác giữa 2 cung khác nhau."""
    h1 = CUNG_NGU_HANH.get(cung1_idx)
    h2 = CUNG_NGU_HANH.get(cung2_idx)
    return phan_tich_sinh_khac_hop(h1, h2)

def phan_tich_yeu_to_thoi_gian(hanh, mua):
    """Đánh giá ngũ hành theo mùa (Vượng, Tướng, Hưu, Tù, Tử)."""
    return ANH_HUONG_MUA.get(mua, {}).get(hanh, "Bình")

def tinh_diem_tong_hop(analysis_results):
    """Tính toán điểm số cuối cùng dựa trên trọng số."""
    total_score = 0
    # Giả sử analysis_results có các key tương ứng TRONG_SO_PHAN_TICH
    for key, weight in TRONG_SO_PHAN_TICH.items():
        score = analysis_results.get(key, 50) # Mặc định 50 nếu thiếu
        total_score += score * weight
    return round(total_score, 2)

def phan_tich_toan_dien(chart_data, topic, chu_cung_idx, khach_cung_idx, thoi_gian):
    """Hàm tổng lực phân tích toàn bộ bàn cờ."""
    # 1. Chọn Dụng Thần
    dung_than = chon_dung_than_theo_chu_de(topic)
    
    # 2. Phân tích Cung Chủ và Cung Khách
    chu_hanh = CUNG_NGU_HANH.get(chu_cung_idx)
    khach_hanh = CUNG_NGU_HANH.get(khach_cung_idx)
    mqh = phan_tich_sinh_khac_hop(chu_hanh, khach_hanh)
    
    # 3. Tính toán điểm số (Demo logic)
    ket_qua = {
        "dung_than": dung_than,
        "moi_quan_he": mqh,
        "diem_tong": 75, # Ví dụ
        "nhan_dinh": f"Chủ và Khách có mối quan hệ {mqh}. Chủ đề {topic} có triển vọng."
    }
    
    return ket_qua
