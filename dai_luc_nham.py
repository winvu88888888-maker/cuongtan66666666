# -*- coding: utf-8 -*-
"""
ĐẠI LỤC NHÂM (大六壬) — Tam Thức thứ 2
Module tính Đại Lục Nhâm cho QMDG App V14.0

Cấu trúc:
1. Nguyệt Tướng (theo Tiết Khí → vị trí Thái Dương trên Hoàng Đạo)
2. Thiên Địa Bàn (đặt Nguyệt Tướng lên giờ → xoay Thiên Bàn)
3. Tứ Khóa (4 khóa từ Can/Chi Ngày + Thiên/Địa bàn)
4. Tam Truyền (Sơ/Trung/Mạt truyền — Cửu Tông Môn)
5. Thập Nhị Thiên Tướng (12 Thiên Tướng do Quý Nhân dẫn đầu)
"""

# ============================================================
# HẰNG SỐ CƠ BẢN
# ============================================================

THIEN_CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
DIA_CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']

# Ngũ Hành của Thiên Can
CAN_NGU_HANH = {
    'Giáp': 'Mộc', 'Ất': 'Mộc',
    'Bính': 'Hỏa', 'Đinh': 'Hỏa',
    'Mậu': 'Thổ', 'Kỷ': 'Thổ',
    'Canh': 'Kim', 'Tân': 'Kim',
    'Nhâm': 'Thủy', 'Quý': 'Thủy'
}

# Ngũ Hành của Địa Chi
CHI_NGU_HANH = {
    'Tý': 'Thủy', 'Sửu': 'Thổ', 'Dần': 'Mộc', 'Mão': 'Mộc',
    'Thìn': 'Thổ', 'Tỵ': 'Hỏa', 'Ngọ': 'Hỏa', 'Mùi': 'Thổ',
    'Thân': 'Kim', 'Dậu': 'Kim', 'Tuất': 'Thổ', 'Hợi': 'Thủy'
}

# Âm Dương của Thiên Can
CAN_AM_DUONG = {
    'Giáp': 'Dương', 'Ất': 'Âm', 'Bính': 'Dương', 'Đinh': 'Âm',
    'Mậu': 'Dương', 'Kỷ': 'Âm', 'Canh': 'Dương', 'Tân': 'Âm',
    'Nhâm': 'Dương', 'Quý': 'Âm'
}

# Can ký tại Chi (Thiên Can ẩn trong Địa Chi)
CAN_KY_CHI = {
    'Giáp': 'Dần', 'Ất': 'Mão', 'Bính': 'Tỵ', 'Đinh': 'Ngọ',
    'Mậu': 'Tỵ', 'Kỷ': 'Ngọ', 'Canh': 'Thân', 'Tân': 'Dậu',
    'Nhâm': 'Hợi', 'Quý': 'Tý'
}

# ============================================================
# 1. NGUYỆT TƯỚNG (月将) — Theo Tiết Khí
# ============================================================
# Nguyệt Tướng = vị trí Thái Dương trên Hoàng Đạo
# Tính theo TRUNG KHÍ (không phải Tiết)

NGUYET_TUONG_MAP = {
    # Trung Khí → Nguyệt Tướng (Chi)
    'Vũ Thủy': 'Hợi',      # Đăng Minh
    'Xuân Phân': 'Tuất',    # Hà Khôi  
    'Cốc Vũ': 'Dậu',       # Tòng Khôi
    'Tiểu Mãn': 'Thân',    # Truyền Tống
    'Hạ Chí': 'Mùi',       # Tiểu Cát
    'Đại Thử': 'Ngọ',      # Thắng Quang
    'Xử Thử': 'Tỵ',       # Thái Ất
    'Thu Phân': 'Thìn',    # Thiên Cương
    'Sương Giáng': 'Mão',  # Thái Xung
    'Tiểu Tuyết': 'Dần',   # Công Tào
    'Đông Chí': 'Sửu',    # Đại Cát
    'Đại Hàn': 'Tý',      # Thần Hậu
}

# Tên gọi 12 Nguyệt Tướng
NGUYET_TUONG_TEN = {
    'Tý': 'Thần Hậu (神后)', 'Sửu': 'Đại Cát (大吉)',
    'Dần': 'Công Tào (功曹)', 'Mão': 'Thái Xung (太冲)',
    'Thìn': 'Thiên Cương (天罡)', 'Tỵ': 'Thái Ất (太乙)',
    'Ngọ': 'Thắng Quang (胜光)', 'Mùi': 'Tiểu Cát (小吉)',
    'Thân': 'Truyền Tống (传送)', 'Dậu': 'Tòng Khôi (从魁)',
    'Tuất': 'Hà Khôi (河魁)', 'Hợi': 'Đăng Minh (登明)'
}


def get_nguyet_tuong(tiet_khi):
    """Xác định Nguyệt Tướng theo Tiết Khí."""
    # Mapping tiết khí → trung khí tương ứng
    TIET_TO_TRUNG = {
        'Lập Xuân': 'Đại Hàn', 'Vũ Thủy': 'Vũ Thủy',
        'Kinh Trập': 'Vũ Thủy', 'Xuân Phân': 'Xuân Phân',
        'Thanh Minh': 'Xuân Phân', 'Cốc Vũ': 'Cốc Vũ',
        'Lập Hạ': 'Cốc Vũ', 'Tiểu Mãn': 'Tiểu Mãn',
        'Mang Chủng': 'Tiểu Mãn', 'Hạ Chí': 'Hạ Chí',
        'Tiểu Thử': 'Hạ Chí', 'Đại Thử': 'Đại Thử',
        'Lập Thu': 'Đại Thử', 'Xử Thử': 'Xử Thử',
        'Bạch Lộ': 'Xử Thử', 'Thu Phân': 'Thu Phân',
        'Hàn Lộ': 'Thu Phân', 'Sương Giáng': 'Sương Giáng',
        'Lập Đông': 'Sương Giáng', 'Tiểu Tuyết': 'Tiểu Tuyết',
        'Đại Tuyết': 'Tiểu Tuyết', 'Đông Chí': 'Đông Chí',
        'Tiểu Hàn': 'Đông Chí', 'Đại Hàn': 'Đại Hàn',
    }
    trung_khi = TIET_TO_TRUNG.get(tiet_khi, 'Đông Chí')
    chi = NGUYET_TUONG_MAP.get(trung_khi, 'Sửu')
    ten = NGUYET_TUONG_TEN.get(chi, chi)
    return chi, ten


# ============================================================
# 2. THIÊN ĐỊA BÀN (天地盘) — Xoay theo Nguyệt Tướng + Giờ
# ============================================================

def tao_thien_dia_ban(nguyet_tuong_chi, chi_gio):
    """
    Tạo Thiên Địa Bàn.
    - Địa Bàn: cố định (Tý→Sửu→...→Hợi)
    - Thiên Bàn: đặt Nguyệt Tướng lên chi giờ, xoay thuận
    """
    dia_ban = list(DIA_CHI)  # Cố định
    
    # Tìm vị trí Nguyệt Tướng và chi giờ
    nt_idx = DIA_CHI.index(nguyet_tuong_chi) if nguyet_tuong_chi in DIA_CHI else 0
    gio_idx = DIA_CHI.index(chi_gio) if chi_gio in DIA_CHI else 0
    
    # Xoay Thiên Bàn: Nguyệt Tướng đặt lên vị trí chi giờ
    offset = gio_idx - nt_idx
    thien_ban = []
    for i in range(12):
        idx = (i + offset) % 12
        thien_ban.append(DIA_CHI[idx])
    
    # Trả về dict: Địa Chi → (Thiên bàn chi tại vị trí đó)
    result = {}
    for i, dia_chi in enumerate(dia_ban):
        result[dia_chi] = thien_ban[i]
    
    return result  # {Địa bàn chi: Thiên bàn chi}


def lay_thuong_than(thien_dia_ban, chi):
    """Lấy Thượng Thần (上神) = Thiên Bàn chi tại vị trí Địa Bàn chi."""
    return thien_dia_ban.get(chi, chi)


# ============================================================
# 3. TỨ KHÓA (四课) — 4 Khóa từ Can/Chi Ngày
# ============================================================

def tinh_tu_khoa(can_ngay, chi_ngay, thien_dia_ban):
    """
    Tính Tứ Khóa:
    - Khóa 1 (Nhật Can Dương Thần): Can Ngày → ký tại Chi → Thượng Thần
    - Khóa 2 (Nhật Can Âm Thần): Thượng Thần Khóa 1 → Thượng Thần tiếp
    - Khóa 3 (Nhật Chi Dương Thần): Chi Ngày → Thượng Thần
    - Khóa 4 (Nhật Chi Âm Thần): Thượng Thần Khóa 3 → Thượng Thần tiếp
    """
    # Can Ngày ký tại Chi nào
    can_ky = CAN_KY_CHI.get(can_ngay, 'Dần')
    
    # Khóa 1: Can ký tại Chi → lấy Thượng Thần
    k1_dia = can_ky
    k1_thien = lay_thuong_than(thien_dia_ban, k1_dia)
    
    # Khóa 2: Thượng Thần Khóa 1 → lấy Thượng Thần tiếp
    k2_dia = k1_thien
    k2_thien = lay_thuong_than(thien_dia_ban, k2_dia)
    
    # Khóa 3: Chi Ngày → lấy Thượng Thần
    k3_dia = chi_ngay
    k3_thien = lay_thuong_than(thien_dia_ban, k3_dia)
    
    # Khóa 4: Thượng Thần Khóa 3 → lấy Thượng Thần tiếp
    k4_dia = k3_thien
    k4_thien = lay_thuong_than(thien_dia_ban, k4_dia)
    
    return [
        {'ten': 'Khóa 1 (Nhật Can Dương)', 'thien': k1_thien, 'dia': k1_dia},
        {'ten': 'Khóa 2 (Nhật Can Âm)', 'thien': k2_thien, 'dia': k2_dia},
        {'ten': 'Khóa 3 (Nhật Chi Dương)', 'thien': k3_thien, 'dia': k3_dia},
        {'ten': 'Khóa 4 (Nhật Chi Âm)', 'thien': k4_thien, 'dia': k4_dia},
    ]


# ============================================================
# 4. TAM TRUYỀN (三传) — Cửu Tông Môn (9 phép)
# ============================================================

def _ngu_hanh_khac(h1, h2):
    """h1 khắc h2?"""
    KHAC = {'Mộc': 'Thổ', 'Thổ': 'Thủy', 'Thủy': 'Hỏa', 'Hỏa': 'Kim', 'Kim': 'Mộc'}
    return KHAC.get(h1) == h2


def tinh_tam_truyen(tu_khoa, thien_dia_ban):
    """
    Tính Tam Truyền theo Cửu Tông Môn (đơn giản hóa).
    
    Phép 1 — TẶC KHẮC (贼克): 
    Trong 4 khóa, tìm cặp Thiên khắc Địa (Thượng khắc Hạ = "tặc").
    Nếu có 1 → Sơ truyền = Thiên bàn chi khắc.
    Nếu có nhiều → chọn theo Nhật Can (phép Tỷ Dụng, Thiệp Hại...)
    
    Phép đơn giản: Lấy khóa có Thiên khắc Địa đầu tiên.
    """
    so_truyen = None
    
    # Phép 1: Tặc Khắc — tìm Thiên khắc Địa
    tac_khac_list = []
    for k in tu_khoa:
        h_thien = CHI_NGU_HANH.get(k['thien'], '')
        h_dia = CHI_NGU_HANH.get(k['dia'], '')
        if _ngu_hanh_khac(h_thien, h_dia):
            tac_khac_list.append(k)
    
    if len(tac_khac_list) == 1:
        so_truyen = tac_khac_list[0]['thien']
    elif len(tac_khac_list) > 1:
        # Nhiều tặc khắc → chọn cái cuối (phép Thiệp Hại đơn giản)
        so_truyen = tac_khac_list[-1]['thien']
    
    # Phép 2: Nếu không có tặc khắc → tìm Địa khắc Thiên
    if not so_truyen:
        for k in tu_khoa:
            h_thien = CHI_NGU_HANH.get(k['thien'], '')
            h_dia = CHI_NGU_HANH.get(k['dia'], '')
            if _ngu_hanh_khac(h_dia, h_thien):
                so_truyen = k['dia']
                break
    
    # Nếu vẫn không có → dùng Khóa 3 Thiên bàn (phép Dao Khắc đơn giản)
    if not so_truyen:
        so_truyen = tu_khoa[2]['thien']
    
    # Trung truyền = Thượng Thần của Sơ truyền
    trung_truyen = lay_thuong_than(thien_dia_ban, so_truyen)
    
    # Mạt truyền = Thượng Thần của Trung truyền  
    mat_truyen = lay_thuong_than(thien_dia_ban, trung_truyen)
    
    return {
        'so_truyen': so_truyen,
        'trung_truyen': trung_truyen,
        'mat_truyen': mat_truyen,
        'phuong_phap': 'Tặc Khắc' if tac_khac_list else 'Dao Khắc',
        'so_truyen_hanh': CHI_NGU_HANH.get(so_truyen, '?'),
        'trung_truyen_hanh': CHI_NGU_HANH.get(trung_truyen, '?'),
        'mat_truyen_hanh': CHI_NGU_HANH.get(mat_truyen, '?'),
    }


# ============================================================
# 5. THẬP NHỊ THIÊN TƯỚNG (十二天将) — 12 Thần Tướng
# ============================================================

THAP_NHI_THIEN_TUONG = [
    {'ten': 'Quý Nhân (贵人)', 'hanh': 'Thổ', 'cat_hung': 'Đại Cát', 'tuong': 'Quý nhân phù trợ, quyền quý, văn thư'},
    {'ten': 'Đằng Xà (螣蛇)', 'hanh': 'Hỏa', 'cat_hung': 'Hung', 'tuong': 'Kinh sợ, quái dị, hỏa hoạn, lo âu'},
    {'ten': 'Chu Tước (朱雀)', 'hanh': 'Hỏa', 'cat_hung': 'Hung', 'tuong': 'Khẩu thiệt, kiện tụng, tin tức, thị phi'},
    {'ten': 'Lục Hợp (六合)', 'hanh': 'Mộc', 'cat_hung': 'Cát', 'tuong': 'Hôn nhân, hòa hợp, giao dịch, mua bán'},
    {'ten': 'Câu Trần (勾陈)', 'hanh': 'Thổ', 'cat_hung': 'Hung', 'tuong': 'Tranh đấu, kiện tụng, trì trệ, ruộng đất'},
    {'ten': 'Thanh Long (青龙)', 'hanh': 'Mộc', 'cat_hung': 'Đại Cát', 'tuong': 'Tiền tài, vui mừng, hỷ sự, quan chức'},
    {'ten': 'Thiên Không (天空)', 'hanh': 'Thổ', 'cat_hung': 'Hung', 'tuong': 'Lừa dối, hư không, nô bộc, mồ mả'},
    {'ten': 'Bạch Hổ (白虎)', 'hanh': 'Kim', 'cat_hung': 'Hung', 'tuong': 'Bệnh tật, tang sự, huyết quang, binh đao'},
    {'ten': 'Thái Thường (太常)', 'hanh': 'Thổ', 'cat_hung': 'Cát', 'tuong': 'Y phục, rượu thịt, tiệc tùng, tế lễ'},
    {'ten': 'Huyền Vũ (玄武)', 'hanh': 'Thủy', 'cat_hung': 'Hung', 'tuong': 'Đạo tặc, mất mát, ám muội, thủy tai'},
    {'ten': 'Thái Âm (太阴)', 'hanh': 'Kim', 'cat_hung': 'Cát', 'tuong': 'Âm mưu, ẩn giấu, mưu tính, nữ nhân, châu báu'},
    {'ten': 'Thiên Hậu (天后)', 'hanh': 'Thủy', 'cat_hung': 'Cát', 'tuong': 'Hậu cung, phụ nữ, hôn nhân, phúc đức'}
]

# Quý Nhân khởi cung theo Can Ngày (ban ngày/ban đêm)
QUY_NHAN_KHOI = {
    # Can: (Ngày-Quý Nhân Chi, Đêm-Quý Nhân Chi)
    'Giáp': ('Sửu', 'Mùi'), 'Mậu': ('Sửu', 'Mùi'),
    'Ất': ('Tý', 'Thân'), 'Kỷ': ('Tý', 'Thân'),
    'Bính': ('Hợi', 'Dậu'), 'Đinh': ('Hợi', 'Dậu'),
    'Canh': ('Dần', 'Ngọ'), 'Tân': ('Ngọ', 'Dần'),
    'Nhâm': ('Mão', 'Tỵ'), 'Quý': ('Tỵ', 'Mão'),
}


def tinh_thien_tuong(can_ngay, chi_gio, thien_dia_ban):
    """
    Tính 12 Thiên Tướng.
    Quý Nhân khởi đầu → các tướng khác xoay theo.
    Ban ngày (Mão→Thân) dùng Ngày Quý Nhân, thuận hành.
    Ban đêm (Dậu→Dần) dùng Đêm Quý Nhân, nghịch hành.
    """
    # Xác định ngày/đêm
    gio_idx = DIA_CHI.index(chi_gio) if chi_gio in DIA_CHI else 0
    is_ngay = 2 <= gio_idx <= 7  # Dần→Mùi = ngày
    
    # Quý Nhân khởi ở chi nào
    qn_ngay, qn_dem = QUY_NHAN_KHOI.get(can_ngay, ('Sửu', 'Mùi'))
    qn_chi = qn_ngay if is_ngay else qn_dem
    qn_idx = DIA_CHI.index(qn_chi) if qn_chi in DIA_CHI else 0
    
    # Xoay 12 Thiên Tướng theo chiều thuận (ngày) hoặc nghịch (đêm)
    result = {}
    for i in range(12):
        if is_ngay:
            chi_vi_tri = DIA_CHI[(qn_idx + i) % 12]
        else:
            chi_vi_tri = DIA_CHI[(qn_idx - i) % 12]
        
        tuong = THAP_NHI_THIEN_TUONG[i]
        result[chi_vi_tri] = tuong
    
    return result  # {Chi: {ten, hanh, cat_hung, tuong}}


# ============================================================
# 6. LUẬN GIẢI (断课) — Phân tích Cát/Hung
# ============================================================

def luan_giai(tam_truyen, tu_khoa, thien_tuong, can_ngay):
    """Tổng hợp luận giải Đại Lục Nhâm."""
    result = []
    
    can_hanh = CAN_NGU_HANH.get(can_ngay, '?')
    
    # Phân tích Sơ Truyền
    so = tam_truyen['so_truyen']
    so_hanh = tam_truyen['so_truyen_hanh']
    tuong_so = thien_tuong.get(so, {})
    
    # Quan hệ Sơ Truyền với Can Ngày
    SINH = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
    
    if so_hanh == can_hanh:
        quan_he = "Tỷ Hòa (ngang sức)"
        verdict = "BÌNH"
    elif SINH.get(so_hanh) == can_hanh:
        quan_he = f"{so_hanh} sinh {can_hanh} → Sơ Truyền SINH Can Ngày"
        verdict = "CÁT"
    elif SINH.get(can_hanh) == so_hanh:
        quan_he = f"{can_hanh} sinh {so_hanh} → Can Ngày BỎ SỨC"
        verdict = "BÌNH HUNG"
    elif _ngu_hanh_khac(can_hanh, so_hanh):
        quan_he = f"{can_hanh} khắc {so_hanh} → Can Ngày KHẮC Sơ Truyền"
        verdict = "CÁT (có thể chế phục)"
    elif _ngu_hanh_khac(so_hanh, can_hanh):
        quan_he = f"{so_hanh} khắc {can_hanh} → Sơ Truyền KHẮC Can Ngày"
        verdict = "HUNG"
    else:
        quan_he = "?"
        verdict = "BÌNH"
    
    result.append(f"Sơ Truyền: {so} ({so_hanh}) — {quan_he} → {verdict}")
    
    if tuong_so:
        result.append(f"  Thiên Tướng: {tuong_so.get('ten', '?')} ({tuong_so.get('cat_hung', '?')}) — {tuong_so.get('tuong', '')}")
    
    # Trung Truyền = quá trình
    trung = tam_truyen['trung_truyen']
    trung_hanh = tam_truyen['trung_truyen_hanh']
    result.append(f"Trung Truyền: {trung} ({trung_hanh}) — Diễn biến giữa chừng")
    
    # Mạt Truyền = kết quả
    mat = tam_truyen['mat_truyen']
    mat_hanh = tam_truyen['mat_truyen_hanh']
    if SINH.get(mat_hanh) == can_hanh:
        mat_verdict = "CÁT — Kết quả TỐT"
    elif _ngu_hanh_khac(mat_hanh, can_hanh):
        mat_verdict = "HUNG — Kết quả XẤU"
    else:
        mat_verdict = "BÌNH — Kết quả TRUNG BÌNH"
    result.append(f"Mạt Truyền: {mat} ({mat_hanh}) — {mat_verdict}")
    
    return {
        'verdict': verdict,
        'details': result,
        'so_truyen': so,
        'trung_truyen': trung,
        'mat_truyen': mat,
    }


# ============================================================
# 7. HÀM CHÍNH — Tính toàn bộ Đại Lục Nhâm
# ============================================================

def tinh_dai_luc_nham(can_ngay, chi_ngay, chi_gio, tiet_khi='Đông Chí'):
    """
    Tính toàn bộ bảng Đại Lục Nhâm.
    
    Args:
        can_ngay: Thiên Can ngày (VD: 'Giáp')
        chi_ngay: Địa Chi ngày (VD: 'Tý')
        chi_gio: Địa Chi giờ (VD: 'Ngọ')
        tiet_khi: Tiết Khí hiện tại (VD: 'Đông Chí')
    
    Returns:
        dict chứa toàn bộ kết quả Đại Lục Nhâm
    """
    # 1. Nguyệt Tướng
    nt_chi, nt_ten = get_nguyet_tuong(tiet_khi)
    
    # 2. Thiên Địa Bàn
    thien_dia_ban = tao_thien_dia_ban(nt_chi, chi_gio)
    
    # 3. Tứ Khóa
    tu_khoa = tinh_tu_khoa(can_ngay, chi_ngay, thien_dia_ban)
    
    # 4. Tam Truyền
    tam_truyen = tinh_tam_truyen(tu_khoa, thien_dia_ban)
    
    # 5. Thập Nhị Thiên Tướng
    thien_tuong = tinh_thien_tuong(can_ngay, chi_gio, thien_dia_ban)
    
    # 6. Luận Giải
    luan_giai_kq = luan_giai(tam_truyen, tu_khoa, thien_tuong, can_ngay)
    
    return {
        'phuong_phap': 'Đại Lục Nhâm (大六壬)',
        'nguyet_tuong': {'chi': nt_chi, 'ten': nt_ten},
        'thien_dia_ban': thien_dia_ban,
        'tu_khoa': tu_khoa,
        'tam_truyen': tam_truyen,
        'thien_tuong_map': {k: v.get('ten', '?') for k, v in thien_tuong.items()},
        'thien_tuong_full': thien_tuong,
        'luan_giai': luan_giai_kq,
        'can_ngay': can_ngay,
        'chi_ngay': chi_ngay,
        'chi_gio': chi_gio,
        'tiet_khi': tiet_khi,
    }


def format_display(data):
    """Format kết quả Đại Lục Nhâm để hiển thị trên web."""
    lines = []
    lines.append("═══ ĐẠI LỤC NHÂM (大六壬) ═══")
    lines.append(f"Can Ngày: {data['can_ngay']} | Chi Ngày: {data['chi_ngay']} | Chi Giờ: {data['chi_gio']}")
    lines.append(f"Tiết Khí: {data['tiet_khi']}")
    lines.append(f"Nguyệt Tướng: {data['nguyet_tuong']['ten']} ({data['nguyet_tuong']['chi']})")
    
    lines.append("\n── TỨ KHÓA ──")
    for k in data['tu_khoa']:
        lines.append(f"  {k['ten']}: {k['thien']}/{k['dia']}")
    
    lines.append("\n── TAM TRUYỀN ──")
    tt = data['tam_truyen']
    lines.append(f"  Sơ Truyền (Phát): {tt['so_truyen']} ({tt['so_truyen_hanh']}) — Phương pháp: {tt['phuong_phap']}")
    lines.append(f"  Trung Truyền (Diễn): {tt['trung_truyen']} ({tt['trung_truyen_hanh']})")
    lines.append(f"  Mạt Truyền (Quả): {tt['mat_truyen']} ({tt['mat_truyen_hanh']})")
    
    lines.append("\n── LUẬN GIẢI ──")
    for d in data['luan_giai']['details']:
        lines.append(f"  {d}")
    
    return "\n".join(lines)


# ============================================================
# 8. LỤC THÂN (六亲) — Hệ thống Quan hệ Ngũ Hành
# ============================================================

def tinh_luc_than(chi, can_ngay):
    """
    Tính Lục Thân của 1 chi so với Can Ngày.
    Sinh Ta = Phụ Mẫu | Ta Sinh = Tử Tôn | Khắc Ta = Quan Quỷ
    Ta Khắc = Thê Tài | Đồng = Huynh Đệ
    """
    can_h = CAN_NGU_HANH.get(can_ngay, '')
    chi_h = CHI_NGU_HANH.get(chi, '')
    SINH = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
    
    if can_h == chi_h:
        return 'Huynh Đệ'
    elif SINH.get(chi_h) == can_h:
        return 'Phụ Mẫu'  # Chi sinh Can
    elif SINH.get(can_h) == chi_h:
        return 'Tử Tôn'   # Can sinh Chi
    elif _ngu_hanh_khac(chi_h, can_h):
        return 'Quan Quỷ'  # Chi khắc Can
    elif _ngu_hanh_khac(can_h, chi_h):
        return 'Thê Tài'   # Can khắc Chi
    return '?'


# ============================================================
# 9. DỤNG THẦN MAPPING — Theo loại câu hỏi
# ============================================================

DUNG_THAN_MAP = {
    'tài_lộc': {'dung_than': 'Thê Tài', 'thien_tuong': 'Thanh Long', 'giai_thich': 'Hỏi tiền bạc → xem Thê Tài + Thanh Long'},
    'sự_nghiệp': {'dung_than': 'Quan Quỷ', 'thien_tuong': 'Câu Trần', 'giai_thich': 'Hỏi công việc → xem Quan Quỷ + Câu Trần'},
    'hôn_nhân': {'dung_than': 'Thê Tài', 'thien_tuong': 'Lục Hợp', 'giai_thich': 'Hỏi tình duyên → xem Thê Tài + Lục Hợp + Thiên Hậu'},
    'sức_khỏe': {'dung_than': 'Quan Quỷ', 'thien_tuong': 'Bạch Hổ', 'giai_thich': 'Hỏi bệnh tật → xem Quan Quỷ + Bạch Hổ (bệnh = quỷ hại thân)'},
    'tìm_đồ': {'dung_than': 'Thê Tài', 'thien_tuong': 'Huyền Vũ', 'giai_thich': 'Hỏi mất đồ → xem Thê Tài + Huyền Vũ (đạo tặc)'},
    'kiện_tụng': {'dung_than': 'Quan Quỷ', 'thien_tuong': 'Chu Tước', 'giai_thich': 'Hỏi kiện → xem Quan Quỷ + Chu Tước (khẩu thiệt)'},
    'đi_xa': {'dung_than': 'Phụ Mẫu', 'thien_tuong': 'Đằng Xà', 'giai_thich': 'Hỏi đi xa → xem Dịch Mã + đường sá'},
    'mua_bán': {'dung_than': 'Thê Tài', 'thien_tuong': 'Lục Hợp', 'giai_thich': 'Hỏi giao dịch → xem Thê Tài + Lục Hợp'},
    'con_cái': {'dung_than': 'Tử Tôn', 'thien_tuong': 'Thiên Hậu', 'giai_thich': 'Hỏi con → xem Tử Tôn + Thiên Hậu'},
    'cha_mẹ': {'dung_than': 'Phụ Mẫu', 'thien_tuong': 'Thái Thường', 'giai_thich': 'Hỏi cha mẹ → xem Phụ Mẫu'},
    'học_hành': {'dung_than': 'Phụ Mẫu', 'thien_tuong': 'Quý Nhân', 'giai_thich': 'Hỏi thi cử → xem Phụ Mẫu + Quý Nhân'},
    'nhà_đất': {'dung_than': 'Phụ Mẫu', 'thien_tuong': 'Câu Trần', 'giai_thich': 'Hỏi nhà → Phụ Mẫu + Câu Trần (ruộng đất)'},
    'xe_cộ': {'dung_than': 'Phụ Mẫu', 'thien_tuong': 'Bạch Hổ', 'giai_thich': 'Xe = Phụ Mẫu (phương tiện che chở)'},
    'thời_tiết': {'dung_than': 'Phụ Mẫu', 'thien_tuong': 'Đằng Xà', 'giai_thich': 'Mưa = Thủy vượng, Nắng = Hỏa vượng'},
    'chung': {'dung_than': 'Quan Quỷ', 'thien_tuong': 'Quý Nhân', 'giai_thich': 'Câu hỏi tổng quát → xem Sơ Truyền + Quý Nhân'},
}


# ============================================================
# 10. TUẦN KHÔNG (旬空) — Rất quan trọng trong Lục Nhâm
# ============================================================

def tinh_tuan_khong(can_ngay, chi_ngay):
    """
    Tính 2 chi Tuần Không từ Can Chi ngày.
    Tìm đầu tuần (Giáp) → 2 chi cuối = Tuần Không.
    """
    can_idx = THIEN_CAN.index(can_ngay) if can_ngay in THIEN_CAN else 0
    chi_idx = DIA_CHI.index(chi_ngay) if chi_ngay in DIA_CHI else 0
    
    # Lùi về đầu tuần (Giáp)
    offset = can_idx  # Từ Giáp đến Can hiện tại
    giap_chi_idx = (chi_idx - offset) % 12  # Chi đầu tuần
    
    # 2 chi cuối (vị trí 10, 11 kể từ đầu tuần)
    k1 = DIA_CHI[(giap_chi_idx + 10) % 12]
    k2 = DIA_CHI[(giap_chi_idx + 11) % 12]
    
    return [k1, k2]


# ============================================================
# 11. QUÁ KHỨ / HIỆN TẠI / TƯƠNG LAI — Tam Truyền Timeline
# ============================================================

def phan_tich_thoi_gian(tam_truyen, tu_khoa, can_ngay, thien_tuong, tuan_khong):
    """
    Phân tích Quá Khứ / Hiện Tại / Tương Lai dựa trên Tam Truyền.
    - Sơ Truyền = KHỞI ĐẦU (quá khứ gần / nguyên nhân)
    - Trung Truyền = HIỆN TẠI (đang diễn ra)
    - Mạt Truyền = TƯƠNG LAI (kết quả cuối cùng)
    
    Kết hợp Lục Thân + Thiên Tướng + Tuần Không.
    """
    SINH = {'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim', 'Kim': 'Thủy', 'Thủy': 'Mộc'}
    can_h = CAN_NGU_HANH.get(can_ngay, '')
    
    timeline = {}
    
    for phase, chi_key, label in [
        ('qua_khu', 'so_truyen', 'QUÁ KHỨ / NGUYÊN NHÂN'),
        ('hien_tai', 'trung_truyen', 'HIỆN TẠI / DIỄN BIẾN'),
        ('tuong_lai', 'mat_truyen', 'TƯƠNG LAI / KẾT QUẢ')
    ]:
        chi = tam_truyen[chi_key]
        chi_h = CHI_NGU_HANH.get(chi, '?')
        luc_than = tinh_luc_than(chi, can_ngay)
        tuong = thien_tuong.get(chi, {})
        is_khong = chi in tuan_khong
        
        # Phân tích Ngũ Hành
        if chi_h == can_h:
            ngu_hanh_str = f"{chi_h} Tỷ Hòa {can_h} → ngang sức"
        elif SINH.get(chi_h) == can_h:
            ngu_hanh_str = f"{chi_h} sinh {can_h} → ĐƯỢC HỖ TRỢ"
        elif SINH.get(can_h) == chi_h:
            ngu_hanh_str = f"{can_h} sinh {chi_h} → BỎ SỨC"
        elif _ngu_hanh_khac(can_h, chi_h):
            ngu_hanh_str = f"{can_h} khắc {chi_h} → KIỂM SOÁT"
        elif _ngu_hanh_khac(chi_h, can_h):
            ngu_hanh_str = f"{chi_h} khắc {can_h} → BỊ HẠI"
        else:
            ngu_hanh_str = "?"
        
        timeline[phase] = {
            'label': label,
            'chi': chi,
            'hanh': chi_h,
            'luc_than': luc_than,
            'thien_tuong': tuong.get('ten', '?') if tuong else '?',
            'cat_hung': tuong.get('cat_hung', '?') if tuong else '?',
            'tuong_y': tuong.get('tuong', '') if tuong else '',
            'ngu_hanh': ngu_hanh_str,
            'tuan_khong': is_khong,
            'tuan_khong_str': '⚠️ LÂM TUẦN KHÔNG — sự việc HƯ, chưa thành' if is_khong else '',
        }
    
    return timeline


# ============================================================
# 12. PHÂN TÍCH CHUYÊN SÂU — Tổng hợp mọi thông tin
# ============================================================

def phan_tich_chuyen_sau(data, question='', topic='chung'):
    """
    Phân tích chuyên sâu Đại Lục Nhâm.
    Bao gồm: Dụng Thần, Lục Thân, Timeline, Tuần Không, Thiên Tướng.
    
    Returns: dict với đầy đủ thông tin để AI hoặc người đọc.
    """
    can_ngay = data['can_ngay']
    chi_ngay = data['chi_ngay']
    tam_truyen = data['tam_truyen']
    tu_khoa = data['tu_khoa']
    thien_tuong = data.get('thien_tuong_full', {})
    
    # Tuần Không
    tuan_khong = tinh_tuan_khong(can_ngay, chi_ngay)
    
    # Dụng Thần theo loại câu hỏi
    dt_info = DUNG_THAN_MAP.get(topic, DUNG_THAN_MAP['chung'])
    
    # Lục Thân cho mỗi khóa
    khoa_luc_than = []
    for k in tu_khoa:
        lt = tinh_luc_than(k['thien'], can_ngay)
        k_tuong = thien_tuong.get(k['thien'], {})
        khoa_luc_than.append({
            **k,
            'luc_than': lt,
            'thien_tuong': k_tuong.get('ten', '?') if k_tuong else '?',
            'is_dung_than': lt == dt_info['dung_than'],
            'tuan_khong': k['thien'] in tuan_khong,
        })
    
    # Timeline phân tích
    timeline = phan_tich_thoi_gian(tam_truyen, tu_khoa, can_ngay, thien_tuong, tuan_khong)
    
    # Tìm Dụng Thần trong Tứ Khóa
    dung_than_found = [k for k in khoa_luc_than if k['is_dung_than']]
    
    # Verdict tổng hợp
    details = []
    details.append(f"=== ĐẠI LỤC NHÂM — PHÂN TÍCH CHUYÊN SÂU ===")
    details.append(f"Dụng Thần: {dt_info['dung_than']} — {dt_info['giai_thich']}")
    details.append(f"Tuần Không: {tuan_khong[0]}, {tuan_khong[1]}")
    
    if dung_than_found:
        dk = dung_than_found[0]
        if dk['tuan_khong']:
            details.append(f"⚠️ Dụng Thần {dk['thien']} LÂM TUẦN KHÔNG → sự việc chưa thành, phải chờ!")
        else:
            details.append(f"✅ Dụng Thần tại Khóa: {dk['ten']} — {dk['thien']}/{dk['dia']}")
    else:
        details.append(f"❌ Dụng Thần KHÔNG HIỆN trong Tứ Khóa → khó thành")
    
    # Timeline
    for phase in ['qua_khu', 'hien_tai', 'tuong_lai']:
        t = timeline[phase]
        details.append(f"\n── {t['label']} ──")
        details.append(f"  Chi: {t['chi']} ({t['hanh']}) | Lục Thân: {t['luc_than']}")
        details.append(f"  Thiên Tướng: {t['thien_tuong']} ({t['cat_hung']})")
        details.append(f"  Ngũ Hành: {t['ngu_hanh']}")
        if t['tuan_khong']:
            details.append(f"  {t['tuan_khong_str']}")
        if t['tuong_y']:
            details.append(f"  Tượng ý: {t['tuong_y']}")
    
    # Verdict cuối
    mat = timeline['tuong_lai']
    if mat['cat_hung'] in ('Cát', 'Đại Cát') and not mat['tuan_khong']:
        verdict = 'CÁT'
    elif mat['cat_hung'] in ('Hung', 'Đại Hung') or mat['tuan_khong']:
        verdict = 'HUNG'
    else:
        verdict = 'BÌNH'
    
    return {
        'verdict': verdict,
        'dung_than': dt_info,
        'tuan_khong': tuan_khong,
        'tu_khoa_luc_than': khoa_luc_than,
        'timeline': timeline,
        'details': details,
        'dung_than_found': len(dung_than_found) > 0,
    }

