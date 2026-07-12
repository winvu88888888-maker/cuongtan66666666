"""
km_luan_nang_cao.py — V42.9.42: Module Luận Kỳ Môn Nâng Cao
Bổ sung 6 logic chuyên sâu chưa có trong engine gốc:
1. Nhìn xa-gần (Timing) — Dương/Âm Độn + Phản/Phục Ngâm
2. Bốn cách nhìn (Ngang, Dọc, Xa-Gần, Toàn bàn) — với sinh/khắc thực tế
3. Vận hạn (Niên/Nguyệt/Nhật/Thời giá) — với vượng/suy theo mùa
4. Dụng Thần đặc thù KM — Thời tiết→Cửu Tinh, Phong thủy→Cửu Cung
5. Xem Tổng Quát nhanh — Thiên Can + Cửu Tinh + Trực Phù
6. Mở rộng Categories — Du lịch, Thời tiết, Pháp lý
"""

import datetime

# ═══════════════════════════════════════════════════════════════
# NGŨ HÀNH REFERENCE TABLES
# ═══════════════════════════════════════════════════════════════
SINH = {'Kim': 'Thủy', 'Thủy': 'Mộc', 'Mộc': 'Hỏa', 'Hỏa': 'Thổ', 'Thổ': 'Kim'}
KHAC = {'Kim': 'Mộc', 'Mộc': 'Thổ', 'Thổ': 'Thủy', 'Thủy': 'Hỏa', 'Hỏa': 'Kim'}

CUNG_NGU_HANH = {1: 'Thủy', 2: 'Thổ', 3: 'Mộc', 4: 'Mộc', 5: 'Thổ', 6: 'Kim', 7: 'Kim', 8: 'Thổ', 9: 'Hỏa'}

CAN_NGU_HANH = {
    'Giáp': 'Mộc', 'Ất': 'Mộc', 'Bính': 'Hỏa', 'Đinh': 'Hỏa',
    'Mậu': 'Thổ', 'Kỷ': 'Thổ', 'Canh': 'Kim', 'Tân': 'Kim',
    'Nhâm': 'Thủy', 'Quý': 'Thủy',
}

CHI_NGU_HANH = {
    'Tý': 'Thủy', 'Sửu': 'Thổ', 'Dần': 'Mộc', 'Mão': 'Mộc',
    'Thìn': 'Thổ', 'Tị': 'Hỏa', 'Ngọ': 'Hỏa', 'Mùi': 'Thổ',
    'Thân': 'Kim', 'Dậu': 'Kim', 'Tuất': 'Thổ', 'Hợi': 'Thủy',
}

# Mùa → Hành vượng
MUA_HANH_VUONG = {
    'Xuân': 'Mộc', 'Hạ': 'Hỏa', 'Thu': 'Kim', 'Đông': 'Thủy',
    'Tứ Quý': 'Thổ',  # Tháng chuyển mùa (3,6,9,12)
}

def _get_mua_hien_tai():
    """Xác định mùa hiện tại"""
    m = datetime.datetime.now().month
    if m in [2, 3, 4]: return 'Xuân'
    if m in [5, 6, 7]: return 'Hạ'
    if m in [8, 9, 10]: return 'Thu'
    return 'Đông'

def _xac_dinh_vuong_suy(hanh, hanh_vuong_mua):
    """Xác định trạng thái Vượng/Tướng/Hưu/Tù/Tử theo mùa"""
    if not hanh or not hanh_vuong_mua:
        return '?'
    if hanh == hanh_vuong_mua:
        return 'VƯỢNG (đương lệnh)'
    if SINH.get(hanh_vuong_mua) == hanh:
        return 'TƯỚNG (được sinh)'
    if SINH.get(hanh) == hanh_vuong_mua:
        return 'HƯU (tiết khí)'
    if KHAC.get(hanh) == hanh_vuong_mua:
        return 'TÙ (bị tiết)'
    if KHAC.get(hanh_vuong_mua) == hanh:
        return 'TỬ (bị khắc)'
    return 'BÌNH'

def _sinh_khac_label(hanh_a, hanh_b):
    """Trả về mối quan hệ sinh khắc giữa A và B"""
    if not hanh_a or not hanh_b or hanh_a == '?' or hanh_b == '?':
        return '?'
    if hanh_a == hanh_b:
        return 'tỷ hòa (cùng hành)'
    if SINH.get(hanh_a) == hanh_b:
        return f'{hanh_a} SINH {hanh_b} (CÁT)'
    if KHAC.get(hanh_a) == hanh_b:
        return f'{hanh_a} KHẮC {hanh_b}'
    if SINH.get(hanh_b) == hanh_a:
        return f'{hanh_b} sinh {hanh_a} (được sinh, CÁT)'
    if KHAC.get(hanh_b) == hanh_a:
        return f'{hanh_b} khắc {hanh_a} (bị khắc, HUNG)'
    return f'{hanh_a}↔{hanh_b}'


# ═══════════════════════════════════════════════════════════════
# 1. NHÌN XA-GẦN (TIMING)
# ═══════════════════════════════════════════════════════════════
def luan_nhin_xa_gan(is_duong_don, cung_dt, is_phan_ngam, is_phuc_ngam):
    """
    Dương Độn: cung 1,8,3,4 (Nội bàn) = gần/nhanh; cung 9,2,7,6 (Ngoại bàn) = xa/chậm
    Âm Độn: ngược lại
    Phản ngâm = nhanh, gấp gáp | Phục ngâm = chậm, đình trệ
    """
    if cung_dt is None or str(cung_dt) == '?':
        return "Không xác định cung DT."

    try:
        cung = int(cung_dt)
    except (ValueError, TypeError):
        return "Cung DT không hợp lệ."

    NOI_BAN = [1, 8, 3, 4]

    if is_duong_don:
        is_noi = cung in NOI_BAN
    else:
        is_noi = cung not in NOI_BAN and cung != 5

    khoang_cach = "Gần/Nhanh (Nội bàn)" if is_noi else "Xa/Chậm (Ngoại bàn)"
    don_type = "Dương Độn" if is_duong_don else "Âm Độn"

    res = f"{don_type} → Cung {cung} = {khoang_cach}"

    if is_phan_ngam:
        res += " ⚡ Phản Ngâm → sự việc NHANH, gấp gáp, đột biến, quay đầu"
    elif is_phuc_ngam:
        res += " 🐌 Phục Ngâm → sự việc CHẬM, đình trệ, dậm chân tại chỗ"

    return res


# ═══════════════════════════════════════════════════════════════
# 2. BỐN CÁCH NHÌN (Ngang, Dọc, Xa-Gần, Toàn bàn)
# ═══════════════════════════════════════════════════════════════
def luan_bon_cach_nhin(can_ngay, cua_dt, sao_dt, than_dt,
                       hanh_can, hanh_cua, hanh_sao, xa_gan_str,
                       tong_quan_9_cung=None):
    """
    1. Nhìn ngang: So sánh ngũ hành Can Ngày vs Cửa, Sao, Thần cùng cung
    2. Nhìn dọc: Thiên(Sao) - Địa(Cung) - Nhân(Cửa) - Thần(Bát Thần)
    3. Nhìn xa-gần: Timing (đã luận riêng)
    4. Nhìn toàn bàn: Đại cục + ngoại ứng
    """
    # --- Nhìn ngang: sinh khắc thực tế ---
    nhin_ngang_parts = []
    if hanh_can and hanh_cua and hanh_can != '?' and hanh_cua != '?':
        rel_cua = _sinh_khac_label(hanh_can, hanh_cua)
        nhin_ngang_parts.append(f"Can({hanh_can})↔Cửa {cua_dt}({hanh_cua}): {rel_cua}")
    if hanh_can and hanh_sao and hanh_can != '?' and hanh_sao != '?':
        rel_sao = _sinh_khac_label(hanh_can, hanh_sao)
        nhin_ngang_parts.append(f"Can({hanh_can})↔Sao {sao_dt}({hanh_sao}): {rel_sao}")
    nhin_ngang = "; ".join(nhin_ngang_parts) if nhin_ngang_parts else "Chưa đủ dữ liệu Ngũ Hành."

    # --- Nhìn dọc ---
    nhin_doc = (
        f"Thiên bàn (Sao {sao_dt}) — "
        f"Nhân bàn (Cửa {cua_dt}) — "
        f"Thần bàn ({than_dt}) → "
        f"Phối hợp 3 tầng để xét chiều sâu sự việc."
    )

    # --- Nhìn toàn bàn ---
    nhin_toan_ban = tong_quan_9_cung if tong_quan_9_cung else (
        "Xem đại cục 9 cung: tương tác tổng thể Sao-Cửa-Thần + ngoại ứng thực tế."
    )

    return {
        "nhin_ngang": nhin_ngang,
        "nhin_doc": nhin_doc,
        "nhin_xa_gan": xa_gan_str,
        "nhin_toan_ban": nhin_toan_ban,
    }


# ═══════════════════════════════════════════════════════════════
# 3. VẬN HẠN (Niên/Nguyệt/Nhật/Thời giá)
# ═══════════════════════════════════════════════════════════════
def luan_van_han(tu_tru_dict):
    """
    Phân tích vận hạn 4 tầng: Niên giá (năm), Nguyệt giá (tháng),
    Nhật giá (ngày), Thời giá (giờ).
    Kèm vượng/suy theo mùa hiện tại.
    """
    if not tu_tru_dict:
        return "Chưa có Tứ Trụ."

    mua = _get_mua_hien_tai()
    hanh_vuong = MUA_HANH_VUONG.get(mua, '')

    parts = []
    mapping = [
        ('Niên giá', 'can_nam', 'chi_nam', 'xu hướng NĂM'),
        ('Nguyệt giá', 'can_thang', 'chi_thang', 'trạng thái THÁNG'),
        ('Nhật giá', 'can_ngay', 'chi_ngay', 'trạng thái NGÀY'),
        ('Thời giá', 'can_gio', 'chi_gio', 'biến động tức thời'),
    ]

    for label, can_key, chi_key, desc in mapping:
        can = tu_tru_dict.get(can_key, '')
        chi = tu_tru_dict.get(chi_key, '')
        if can and chi:
            hanh_can = CAN_NGU_HANH.get(can, '?')
            vs = _xac_dinh_vuong_suy(hanh_can, hanh_vuong)
            parts.append(f"{label}({can}{chi}/{hanh_can} {vs}): {desc}")
        elif can or chi:
            parts.append(f"{label}({can}{chi}): {desc}")

    if not parts:
        return "Thiếu dữ liệu Tứ Trụ."

    return " | ".join(parts)


# ═══════════════════════════════════════════════════════════════
# 4. DỤNG THẦN ĐẶC THÙ KỲ MÔN
# ═══════════════════════════════════════════════════════════════
KM_DUNG_THAN_DAC_THU = {
    # Thời tiết → Cửu Tinh
    'thời tiết': {'dung_than_km': 'Cửu Tinh', 'ghi_chu': 'Xem sao trực (Trực Phù) để đoán thời tiết'},
    'mưa': {'dung_than_km': 'Cửu Tinh', 'ghi_chu': 'Thiên Bồng (Thủy)=mưa, Thiên Anh (Hỏa)=nắng'},
    'nắng': {'dung_than_km': 'Cửu Tinh', 'ghi_chu': 'Thiên Anh (Hỏa)=nắng to'},
    'bão': {'dung_than_km': 'Cửu Tinh', 'ghi_chu': 'Thiên Xung (Mộc)=gió, Thiên Bồng (Thủy)=mưa lớn'},
    # Phong thủy → Cửu Cung
    'phong thủy': {'dung_than_km': 'Cửu Cung (Địa Bàn)', 'ghi_chu': 'Xem cung Địa Bàn, hướng nhà'},
    'nhà': {'dung_than_km': 'Cửu Cung (Địa Bàn)', 'ghi_chu': 'Cung DT trên Địa Bàn = hướng/vị trí nhà'},
    'đất': {'dung_than_km': 'Cửu Cung (Địa Bàn)', 'ghi_chu': 'Địa Bàn + Cung = vị trí đất'},
    'hướng': {'dung_than_km': 'Cửu Cung (Địa Bàn)', 'ghi_chu': 'Cung số → hướng (1=Bắc, 9=Nam...)'},
    # Sự việc con người → Bát Môn
    'người': {'dung_than_km': 'Bát Môn', 'ghi_chu': 'Cửa DT phản ánh tình trạng con người'},
    'quan hệ': {'dung_than_km': 'Bát Môn', 'ghi_chu': 'Cửa phản ánh mối quan hệ'},
}

def luan_dung_than_dac_thu_km(question):
    """
    Xác định Dụng Thần đặc thù KM dựa trên câu hỏi.
    Returns: dict {dung_than_km, ghi_chu} hoặc None
    """
    if not question:
        return None
    q = question.lower()
    for keyword, info in KM_DUNG_THAN_DAC_THU.items():
        if keyword in q:
            return info
    return None


# ═══════════════════════════════════════════════════════════════
# 5. XEM TỔNG QUÁT NHANH
# ═══════════════════════════════════════════════════════════════
CUU_TINH_CAT_HUNG = {
    'Thiên Bồng': ('HUNG', 'Thủy'), 'Thiên Nhậm': ('CÁT', 'Thổ'),
    'Thiên Xung': ('CÁT', 'Mộc'), 'Thiên Phụ': ('CÁT', 'Mộc'),
    'Thiên Anh': ('BÌNH', 'Hỏa'), 'Thiên Nhuế': ('HUNG', 'Thổ'),
    'Thiên Cầm': ('CÁT', 'Thổ'), 'Thiên Trụ': ('HUNG', 'Kim'),
    'Thiên Tâm': ('CÁT', 'Kim'),
}

BAT_MON_CAT_HUNG = {
    'Khai Môn': ('ĐẠI CÁT', 'Kim'), 'Hưu Môn': ('CÁT', 'Thủy'),
    'Sinh Môn': ('ĐẠI CÁT', 'Thổ'), 'Thương Môn': ('TIỂU CÁT', 'Mộc'),
    'Đỗ Môn': ('BÌNH', 'Mộc'), 'Cảnh Môn': ('BÌNH', 'Hỏa'),
    'Tử Môn': ('ĐẠI HUNG', 'Thổ'), 'Kinh Môn': ('HUNG', 'Kim'),
}

def luan_xem_tong_quat_nhanh(can_gio, truc_phu_sao, truc_su_cua):
    """
    Phương pháp Xem Tổng Quát nhanh:
    Chỉ cần Thiên Can Giờ + Trực Phù (Cửu Tinh) + Trực Sử (Bát Môn)
    → Đưa ra phán đoán nhanh cát/hung tổng thể.
    """
    if not can_gio or not truc_phu_sao or not truc_su_cua:
        return "Thiếu dữ liệu Thiên Can/Trực Phù/Trực Sử."

    hanh_can = CAN_NGU_HANH.get(can_gio, '?')

    sao_info = CUU_TINH_CAT_HUNG.get(truc_phu_sao, ('?', '?'))
    sao_cat_hung, sao_hanh = sao_info

    cua_info = BAT_MON_CAT_HUNG.get(truc_su_cua, ('?', '?'))
    cua_cat_hung, cua_hanh = cua_info

    # Đánh giá tổng
    cat_count = sum(1 for x in [sao_cat_hung, cua_cat_hung] if 'CÁT' in str(x))
    hung_count = sum(1 for x in [sao_cat_hung, cua_cat_hung] if 'HUNG' in str(x))

    # Sao vượng + Cửa cát = ĐẠI CÁT
    sao_cua_rel = _sinh_khac_label(sao_hanh, cua_hanh)

    if cat_count >= 2:
        tong_ket = "ĐẠI CÁT — Sao cát + Cửa cát, thuận lợi mọi việc"
    elif cat_count == 1 and hung_count == 0:
        tong_ket = "CÁT — Nghiêng thuận, cần xem thêm chi tiết"
    elif hung_count >= 2:
        tong_ket = "ĐẠI HUNG — Sao hung + Cửa hung, nên tránh"
    elif hung_count == 1 and cat_count == 0:
        tong_ket = "HUNG — Bất lợi, cẩn thận"
    else:
        tong_ket = "BÌNH — Cần xem kỹ các yếu tố khác"

    return (
        f"Can Giờ: {can_gio}({hanh_can}) | "
        f"Trực Phù: {truc_phu_sao}({sao_hanh}/{sao_cat_hung}) | "
        f"Trực Sử: {truc_su_cua}({cua_hanh}/{cua_cat_hung}) | "
        f"Sao↔Cửa: {sao_cua_rel} → {tong_ket}"
    )


# ═══════════════════════════════════════════════════════════════
# 6. MỞ RỘNG CATEGORIES
# ═══════════════════════════════════════════════════════════════
EXTRA_CATEGORIES = {
    'du_lich': {
        'keywords': ['du lịch', 'đi chơi', 'xuất hành', 'di chuyển', 'chuyến đi',
                     'bay', 'về quê', 'đi xa', 'đi nước ngoài', 'visa'],
        'dung_than': 'Bản Thân',
        'hanh_dt_key': 'can_ngay',
        'ghi_chu': 'Xem Cửa DT: Khai/Hưu/Sinh=NÊN ĐI, Tử/Kinh=KHÔNG NÊN. Dịch Mã động=SẼ ĐI.',
    },
    'thoi_tiet': {
        'keywords': ['thời tiết', 'mưa', 'nắng', 'bão', 'lũ', 'sấm', 'sét', 'gió'],
        'dung_than': 'Cửu Tinh',
        'hanh_dt_key': 'truc_phu',
        'ghi_chu': 'DT=Cửu Tinh. Thiên Bồng=mưa, Thiên Anh=nắng, Thiên Xung=gió.',
    },
    'phap_ly': {
        'keywords': ['kiện', 'tòa án', 'luật', 'pháp lý', 'hợp đồng', 'ký kết',
                     'giấy tờ', 'tranh chấp', 'bồi thường'],
        'dung_than': 'Quan Quỷ',
        'hanh_dt_key': 'can_gio',
        'ghi_chu': 'DT=Quan Quỷ. Cảnh Môn=kiện cáo. Thế vượng Ứng suy=thắng.',
    },
}

def detect_extra_category(question):
    """
    Phát hiện câu hỏi thuộc category mở rộng.
    Returns: (category_key, category_info) hoặc (None, None)
    """
    if not question:
        return None, None
    q = question.lower()
    for cat_key, cat_info in EXTRA_CATEGORIES.items():
        for kw in cat_info['keywords']:
            if kw in q:
                return cat_key, cat_info
    return None, None
