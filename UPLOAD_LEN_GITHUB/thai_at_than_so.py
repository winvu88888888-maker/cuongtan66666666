# -*- coding: utf-8 -*-
"""
THÁI ẤT THẦN SỐ (太乙神数) — Tam Thức thứ 3
Module tính Thái Ất Thần Số cho QMDG App V14.0

Cấu trúc:
1. Thái Ất Cửu Cung (9 cung theo Thái Ất — khác Kỳ Môn)
2. Thái Ất Tích Niên Số (tính từ Thượng Nguyên Giáp Tý)
3. Bát Tướng (8 tướng: Chủ/Khách Đại Tướng, Văn Xương, Thủy Kích...)
4. Thập Lục Thần (16 thần sát)
5. Cách Cục (Yểm, Bách, Kích, Cách, Đối, Đề Hiệp)
"""

# ============================================================
# HẰNG SỐ CƠ BẢN
# ============================================================

THIEN_CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
DIA_CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']

# Thái Ất Cửu Cung — KHÁC Kỳ Môn (xoay 45 độ)
# Càn=1, Ly=2, Cấn=3, Chấn=4, Trung=5, Đoài=6, Khôn=7, Khảm=8, Tốn=9
THAI_AT_CUU_CUNG = {
    1: {'ten': 'Càn', 'hanh': 'Kim', 'vi_tri': 'Tây Bắc', 'tuong': 'Trời, Cha, Vua'},
    2: {'ten': 'Ly', 'hanh': 'Hỏa', 'vi_tri': 'Nam', 'tuong': 'Lửa, Sáng, Văn minh'},
    3: {'ten': 'Cấn', 'hanh': 'Thổ', 'vi_tri': 'Đông Bắc', 'tuong': 'Núi, Dừng, Ổn định'},
    4: {'ten': 'Chấn', 'hanh': 'Mộc', 'vi_tri': 'Đông', 'tuong': 'Sấm, Động, Khởi đầu'},
    5: {'ten': 'Trung Cung', 'hanh': 'Thổ', 'vi_tri': 'Trung tâm', 'tuong': 'Trung tâm vũ trụ'},
    6: {'ten': 'Đoài', 'hanh': 'Kim', 'vi_tri': 'Tây', 'tuong': 'Đầm, Vui, Phá hủy'},
    7: {'ten': 'Khôn', 'hanh': 'Thổ', 'vi_tri': 'Tây Nam', 'tuong': 'Đất, Mẹ, Thuận'},
    8: {'ten': 'Khảm', 'hanh': 'Thủy', 'vi_tri': 'Bắc', 'tuong': 'Nước, Hiểm, Nguy'},
    9: {'ten': 'Tốn', 'hanh': 'Mộc', 'vi_tri': 'Đông Nam', 'tuong': 'Gió, Nhập, Thuận'},
}

# 16 Thần Sát Thái Ất
THAP_LUC_THAN = {
    'Thiên Mục': {'hanh': 'Mộc', 'cat_hung': 'Cát', 'tuong': 'Mắt trời, sáng suốt, minh bạch'},
    'Thiên Mã': {'hanh': 'Hỏa', 'cat_hung': 'Cát', 'tuong': 'Ngựa trời, di chuyển, thay đổi nhanh'},
    'Thiên Tài': {'hanh': 'Thổ', 'cat_hung': 'Cát', 'tuong': 'Tài lộc trời cho, phúc đức'},
    'Thiên Hỉ': {'hanh': 'Thổ', 'cat_hung': 'Đại Cát', 'tuong': 'Mừng vui, hỷ sự, tin tốt'},
    'Thiên Ấn': {'hanh': 'Kim', 'cat_hung': 'Cát', 'tuong': 'Ấn tín, quyền lực, danh vọng'},
    'Thiên Phúc': {'hanh': 'Thủy', 'cat_hung': 'Đại Cát', 'tuong': 'Phúc trời, may mắn, bảo hộ'},
    'Thiên Quan': {'hanh': 'Hỏa', 'cat_hung': 'Trung', 'tuong': 'Quan chức, kiện tụng, công việc'},
    'Thiên Đức': {'hanh': 'Thổ', 'cat_hung': 'Đại Cát', 'tuong': 'Đức trời, hóa giải hung, phù trợ'},
    'Địa Sát': {'hanh': 'Thổ', 'cat_hung': 'Hung', 'tuong': 'Sát đất, trì trệ, cản trở'},
    'Địa Hình': {'hanh': 'Kim', 'cat_hung': 'Hung', 'tuong': 'Hình phạt, kiện tụng, tù tội'},
    'Địa Binh': {'hanh': 'Mộc', 'cat_hung': 'Hung', 'tuong': 'Binh đao, chiến tranh, xung đột'},
    'Địa Hoàn': {'hanh': 'Hỏa', 'cat_hung': 'Hung', 'tuong': 'Tai hoàn, trở ngại, thất bại'},
    'Địa Tặc': {'hanh': 'Thủy', 'cat_hung': 'Hung', 'tuong': 'Trộm cướp, mất mát, lừa đảo'},
    'Địa Phá': {'hanh': 'Kim', 'cat_hung': 'Đại Hung', 'tuong': 'Phá hủy, tan hoang, thảm họa'},
    'Địa Kiếp': {'hanh': 'Hỏa', 'cat_hung': 'Đại Hung', 'tuong': 'Cướp bóc, tai kiếp, thiên tai'},
    'Địa Ách': {'hanh': 'Thổ', 'cat_hung': 'Hung', 'tuong': 'Tai ách, bệnh tật, nạn'},
}

# 8 Tướng Thái Ất
BAT_TUONG = {
    'Văn Xương': {'hanh': 'Thổ', 'cat_hung': 'Đại Cát', 'tuong': 'Văn minh, học vấn, thông minh, giao tiếp Thiên-Địa-Nhân'},
    'Thủy Kích': {'hanh': 'Hỏa', 'cat_hung': 'Hung', 'tuong': 'Binh đao, xung đột, chiến tranh, bất ổn'},
    'Chủ Đại Tướng': {'hanh': 'Kim', 'cat_hung': 'Trung', 'tuong': 'Bản thân, chủ nhân, sức mạnh nội tại'},
    'Khách Đại Tướng': {'hanh': 'Thủy', 'cat_hung': 'Trung', 'tuong': 'Đối phương, ngoại lực, sức mạnh đến'},
    'Chủ Tham Tướng': {'hanh': 'Mộc', 'cat_hung': 'Trung', 'tuong': 'Tham mưu bên ta, cố vấn, hỗ trợ'},
    'Khách Tham Tướng': {'hanh': 'Hỏa', 'cat_hung': 'Trung', 'tuong': 'Tham mưu đối phương'},
    'Kế Thần': {'hanh': 'Thổ', 'cat_hung': 'Trung', 'tuong': 'Kế hoạch, mưu tính, chiến lược'},
    'Hợp Thần': {'hanh': 'Mộc', 'cat_hung': 'Cát', 'tuong': 'Hòa hợp, liên kết, đồng minh'},
}


# ============================================================
# 1. TÍNH THÁI ẤT TÍCH NIÊN SỐ
# ============================================================

def tinh_tich_nien(nam):
    """
    Tính Thái Ất Tích Niên Số.
    Thượng Nguyên Giáp Tý = năm 2697 TCN (theo truyền thống).
    Tích Niên = năm hiện tại + 2696 (offset).
    """
    return nam + 2696


# ============================================================
# 2. TÍNH THÁI ẤT NHẬP CUNG
# ============================================================

def tinh_thai_at_cung(tich_nien, is_duong_don=True):
    """
    Tính Thái Ất đang ở Cung nào.
    - Thái Ất mỗi cung ở 3 năm
    - Năm 1 = Lý Thiên, Năm 2 = Lý Địa, Năm 3 = Lý Nhân
    - KHÔNG VÀO TRUNG CUNG (5)
    - Dương Độn: Càn(1)→Ly(2)→Cấn(3)→Chấn(4)→Đoài(6)→Khôn(7)→Khảm(8)→Tốn(9) thuận
    - Âm Độn: Tốn(9)→Khảm(8)→Khôn(7)→Đoài(6)→Chấn(4)→Cấn(3)→Ly(2)→Càn(1) nghịch
    """
    DUONG_DON_ORDER = [1, 2, 3, 4, 6, 7, 8, 9]  # 8 cung, bỏ 5
    
    # Mỗi cung 3 năm, 8 cung = 24 năm 1 vòng
    du = tich_nien % 24
    if du == 0:
        du = 24
    
    cung_idx = (du - 1) // 3  # 0-7
    nam_trong_cung = ((du - 1) % 3) + 1  # 1-3
    
    ly_map = {1: 'Lý Thiên', 2: 'Lý Địa', 3: 'Lý Nhân'}
    
    if is_duong_don:
        cung = DUONG_DON_ORDER[cung_idx % 8]
    else:
        cung = DUONG_DON_ORDER[-(cung_idx % 8) - 1]
    
    return {
        'cung': cung,
        'ten_cung': THAI_AT_CUU_CUNG[cung]['ten'],
        'hanh_cung': THAI_AT_CUU_CUNG[cung]['hanh'],
        'ly': ly_map.get(nam_trong_cung, '?'),
        'nam_trong_cung': nam_trong_cung,
        'tich_nien': tich_nien,
    }


# ============================================================
# 3. TÍNH BÁT TƯỚNG — 8 Tướng Thái Ất
# ============================================================

def tinh_bat_tuong(tich_nien, thai_at_cung):
    """
    Tính vị trí 8 Tướng Thái Ất trong Cửu Cung.
    Đơn giản hóa: Phân bổ 8 tướng dựa trên tích niên và Thái Ất cung.
    """
    DUONG_ORDER = [1, 2, 3, 4, 6, 7, 8, 9]
    tuong_names = list(BAT_TUONG.keys())
    
    result = {}
    base = thai_at_cung % 8
    
    for i, name in enumerate(tuong_names):
        cung = DUONG_ORDER[(base + i) % 8]
        result[name] = {
            'cung': cung,
            'ten_cung': THAI_AT_CUU_CUNG[cung]['ten'],
            'hanh_cung': THAI_AT_CUU_CUNG[cung]['hanh'],
            **BAT_TUONG[name]
        }
    
    return result


# ============================================================
# 4. TÍNH CÁCH CỤC — Yểm/Bách/Kích/Cách/Đối
# ============================================================

def _ngu_hanh_khac(h1, h2):
    """h1 khắc h2?"""
    KHAC = {'Mộc': 'Thổ', 'Thổ': 'Thủy', 'Thủy': 'Hỏa', 'Hỏa': 'Kim', 'Kim': 'Mộc'}
    return KHAC.get(h1) == h2

def _ngu_hanh_sinh(h1, h2):
    """h1 sinh h2?"""
    SINH = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
    return SINH.get(h1) == h2


def tinh_cach_cuc(bat_tuong_data, thai_at_info):
    """
    Phân tích Cách Cục Thái Ất:
    - Yểm (掩): Chủ Đại Tướng cùng cung Thái Ất → bị yểm
    - Bách (迫): Cung của Tướng bị khắc bởi Thái Ất
    - Kích (击): Thái Ất cung khắc Tướng cung
    - Cách (格): Tướng cung khắc Thái Ất cung
    - Đối (对): Thái Ất và Tướng đối xung
    """
    cach_cuc_list = []
    thai_at_cung = thai_at_info['cung']
    thai_at_hanh = thai_at_info['hanh_cung']
    
    for tuong_name, tuong_info in bat_tuong_data.items():
        tuong_cung = tuong_info['cung']
        tuong_hanh = tuong_info['hanh_cung']
        
        if tuong_cung == thai_at_cung:
            cach_cuc_list.append(f"YỂM (掩): {tuong_name} cùng cung Thái Ất → bị che đậy, khó triển khai")
        
        if _ngu_hanh_khac(thai_at_hanh, tuong_hanh):
            cach_cuc_list.append(f"KÍCH (击): Thái Ất ({thai_at_hanh}) khắc {tuong_name} ({tuong_hanh}) → áp chế mạnh")
        
        if _ngu_hanh_khac(tuong_hanh, thai_at_hanh):
            cach_cuc_list.append(f"CÁCH (格): {tuong_name} ({tuong_hanh}) khắc Thái Ất ({thai_at_hanh}) → chống đối, trở ngại")
        
        # Đối xung: cung cách 4
        if abs(tuong_cung - thai_at_cung) == 4 or abs(tuong_cung - thai_at_cung) == 5:
            cach_cuc_list.append(f"ĐỐI (对): {tuong_name} (Cung {tuong_cung}) đối xung Thái Ất (Cung {thai_at_cung})")
    
    return cach_cuc_list


# ============================================================
# 5. LUẬN GIẢI TỔNG HỢP
# ============================================================

def luan_giai_thai_at(thai_at_info, bat_tuong_data, cach_cuc):
    """Tổng hợp luận giải Thái Ất Thần Số."""
    details = []
    
    # Phân tích Thái Ất cung
    details.append(f"Thái Ất ở Cung {thai_at_info['cung']} ({thai_at_info['ten_cung']}) — {thai_at_info['ly']}")
    details.append(f"Ngũ Hành: {thai_at_info['hanh_cung']} — Vị trí: {THAI_AT_CUU_CUNG[thai_at_info['cung']]['vi_tri']}")
    
    # Phân tích Văn Xương (quan trọng nhất)
    van_xuong = bat_tuong_data.get('Văn Xương', {})
    if van_xuong:
        vx_hanh = van_xuong.get('hanh_cung', '?')
        ta_hanh = thai_at_info['hanh_cung']
        if _ngu_hanh_sinh(vx_hanh, ta_hanh):
            details.append(f"✅ Văn Xương (Cung {van_xuong['ten_cung']}) SINH Thái Ất → VĂN MINH XƯƠNG THỊNH, CÁT")
        elif _ngu_hanh_khac(vx_hanh, ta_hanh):
            details.append(f"❌ Văn Xương KHẮC Thái Ất → VĂN VẬN BẤT LỢI, HUNG")
        else:
            details.append(f"📌 Văn Xương tại Cung {van_xuong['ten_cung']} — BÌNH")
    
    # Phân tích Chủ/Khách
    chu = bat_tuong_data.get('Chủ Đại Tướng', {})
    khach = bat_tuong_data.get('Khách Đại Tướng', {})
    if chu and khach:
        chu_hanh = chu.get('hanh_cung', '?')
        khach_hanh = khach.get('hanh_cung', '?')
        if _ngu_hanh_khac(chu_hanh, khach_hanh):
            details.append(f"✅ Chủ Đại Tướng ({chu_hanh}) KHẮC Khách ({khach_hanh}) → BẢN THÂN THẮNG = CÁT")
            verdict = "CÁT"
        elif _ngu_hanh_khac(khach_hanh, chu_hanh):
            details.append(f"❌ Khách Đại Tướng ({khach_hanh}) KHẮC Chủ ({chu_hanh}) → BẢN THÂN THUA = HUNG")
            verdict = "HUNG"
        elif _ngu_hanh_sinh(chu_hanh, khach_hanh):
            details.append(f"⚠️ Chủ SINH Khách → Bỏ sức cho đối phương = BÌNH HUNG")
            verdict = "BÌNH"
        else:
            details.append(f"📌 Chủ và Khách — quan hệ BÌNH")
            verdict = "BÌNH"
    else:
        verdict = "BÌNH"
    
    # Cách cục
    if cach_cuc:
        details.append("\n── CÁCH CỤC ──")
        for cc in cach_cuc[:5]:
            details.append(f"  {cc}")
    
    return {
        'verdict': verdict,
        'details': details,
    }


# ============================================================
# 6. HÀM CHÍNH — Tính toàn bộ Thái Ất
# ============================================================

def tinh_thai_at_than_so(nam, thang=1, can_ngay='Giáp', chi_ngay='Tý'):
    """
    Tính toàn bộ Thái Ất Thần Số.
    
    Args:
        nam: Năm dương lịch (VD: 2026)
        thang: Tháng (1-12)
        can_ngay: Can ngày
        chi_ngay: Chi ngày
    
    Returns:
        dict chứa toàn bộ kết quả Thái Ất
    """
    # 1. Tích Niên
    tich_nien = tinh_tich_nien(nam)
    
    # 2. Dương/Âm Độn (trước Hạ Chí = Dương, sau = Âm)
    is_duong = thang <= 6
    
    # 3. Thái Ất nhập cung
    thai_at_info = tinh_thai_at_cung(tich_nien, is_duong)
    
    # 4. Bát Tướng
    bat_tuong_data = tinh_bat_tuong(tich_nien, thai_at_info['cung'])
    
    # 5. Cách Cục
    cach_cuc = tinh_cach_cuc(bat_tuong_data, thai_at_info)
    
    # 6. Luận Giải
    luan_giai_kq = luan_giai_thai_at(thai_at_info, bat_tuong_data, cach_cuc)
    
    return {
        'phuong_phap': 'Thái Ất Thần Số (太乙神数)',
        'nam': nam,
        'tich_nien': tich_nien,
        'thai_at_cung': thai_at_info,
        'bat_tuong': bat_tuong_data,
        'cach_cuc': cach_cuc,
        'luan_giai': luan_giai_kq,
    }


def format_display(data):
    """Format kết quả Thái Ất để hiển thị trên web."""
    lines = []
    lines.append("═══ THÁI ẤT THẦN SỐ (太乙神数) ═══")
    lines.append(f"Năm: {data['nam']} | Tích Niên: {data['tich_nien']}")
    
    ta = data['thai_at_cung']
    lines.append(f"Thái Ất: Cung {ta['cung']} ({ta['ten_cung']}) — {ta['hanh_cung']} — {ta['ly']}")
    
    lines.append("\n── BÁT TƯỚNG ──")
    for name, info in data['bat_tuong'].items():
        lines.append(f"  {name}: Cung {info['cung']} ({info['ten_cung']}) — {info['cat_hung']}")
    
    lines.append("\n── LUẬN GIẢI ──")
    for d in data['luan_giai']['details']:
        lines.append(f"  {d}")
    
    lines.append(f"\n── VERDICT: {data['luan_giai']['verdict']} ──")
    
    return "\n".join(lines)
