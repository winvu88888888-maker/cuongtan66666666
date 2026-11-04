"""
TEMPLATE TRẢ LỜI CHUẨN - Ngắn Gọn, Chính Xác, Có Căn Cứ
NGUYÊN TẮC: KHÔNG GIẢI THÍCH DÀI - CHỈ TRẢ LỜI THẲNG VÀO CÂU HỎI
"""

# ============================================================
# TEMPLATE TRẢ LỜI CHO CÂU HỎI TÌM ĐỒ MẤT
# ============================================================

TEMPLATE_TIM_DO_MAT = """
**📍 KẾT QUẢ PHÂN TÍCH:**

| Câu hỏi | Trả lời | Căn cứ |
|---------|---------|--------|
| 👤 Ai lấy? | {gioi_tinh}, {tuoi} tuổi | {can_than} |
| 🎨 Màu sắc? | {mau_sac} | {hanh_cung} |
| 💰 Giá trị? | {gia_tri} | Cung {cung_so} |
| 📏 Khoảng cách? | {khoang_cach} | {huong} |
| 🔗 Quen/Lạ? | {quen_la} | {than} |
| 🔄 Lấy lại được? | {kha_nang_lay_lai} | {mon} |
| 👮 Bị bắt? | {kha_nang_bi_bat} | {mon_than} |

**💡 LỜI KHUYÊN:** {loi_khuyen}
"""

# ============================================================
# HÀM TẠO CÂU TRẢ LỜI NGẮN GỌN
# ============================================================

def tao_tra_loi_ngan_gon(cung_so, can, mon, than):
    """
    Tạo câu trả lời NGẮN GỌN, CHÍNH XÁC
    Không giải thích dài dòng - chỉ trả lời thẳng
    """
    
    # Import dữ liệu
    from qmdg_inference_rules import (
        tinh_mau_sac_vat, tinh_gia_tri_vat, tinh_khoang_cach,
        tinh_kha_nang_bi_bat, xac_dinh_ke_lay
    )
    
    # 1. Màu sắc
    mau = tinh_mau_sac_vat(cung_so)
    
    # 2. Giá trị
    gia = tinh_gia_tri_vat(cung_so)
    
    # 3. Khoảng cách
    kc = tinh_khoang_cach(cung_so)
    
    # 4. Kẻ lấy
    ke_lay = xac_dinh_ke_lay(can, than, cung_so)
    
    # 5. Quen/Lạ
    quen_la = _xac_dinh_quen_la_ngan(than)
    
    # 6. Khả năng lấy lại
    kha_nang = _tinh_kha_nang_lay_lai_ngan(mon)
    
    # 7. Bị bắt
    bi_bat = tinh_kha_nang_bi_bat(mon, than)
    
    # Format kết quả
    ket_qua = {
        "gioi_tinh": ke_lay["gioi_tinh"],
        "tuoi": ke_lay["tuoi"],
        "can_than": f"{can} + {than}",
        "mau_sac": mau["mau_chinh"],
        "hanh_cung": f"Cung {cung_so} ({_lay_hanh_cung(cung_so)})",
        "gia_tri": gia["gia_tri"],
        "cung_so": cung_so,
        "khoang_cach": kc["met"],
        "huong": kc["mo_ta"],
        "quen_la": quen_la,
        "than": than,
        "kha_nang_lay_lai": kha_nang["ty_le"],
        "mon": mon,
        "kha_nang_bi_bat": bi_bat["ket_luan_chung"],
        "mon_than": f"{mon} + {than}",
        "loi_khuyen": _tao_loi_khuyen(kha_nang["ty_le"], quen_la)
    }
    
    return TEMPLATE_TIM_DO_MAT.format(**ket_qua)

def _lay_hanh_cung(cung_so):
    """Lấy Ngũ Hành của cung"""
    hanh_map = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}
    return hanh_map.get(cung_so, "Thổ")

def _xac_dinh_quen_la_ngan(than):
    """Xác định quen/lạ ngắn gọn"""
    if than in ["Huyền Vũ", "Bạch Hổ"]:
        return "NGƯỜI LẠ (90%)"
    elif than in ["Thái Âm", "Lục Hợp", "Cửu Địa"]:
        return "NGƯỜI QUEN (75%)"
    else:
        return "50/50"

def _tinh_kha_nang_lay_lai_ngan(mon):
    """Tính khả năng lấy lại ngắn gọn"""
    mon_key = mon.replace(" Môn", "") + " Môn" if " Môn" not in mon else mon
    ty_le = {
        "Sinh Môn": {"ty_le": "85% - RẤT CAO", "loi_khuyen": "Tìm ngay"},
        "Hưu Môn": {"ty_le": "80% - CAO", "loi_khuyen": "Chờ 1-2 ngày"},
        "Khai Môn": {"ty_le": "70% - KHÁ CAO", "loi_khuyen": "Báo công an"},
        "Cảnh Môn": {"ty_le": "50% - TRUNG BÌNH", "loi_khuyen": "Tìm nhanh"},
        "Đỗ Môn": {"ty_le": "40% - THẤP", "loi_khuyen": "Tìm kỹ góc khuất"},
        "Thương Môn": {"ty_le": "25% - RẤT THẤP", "loi_khuyen": "Có thể đã bán"},
        "Kinh Môn": {"ty_le": "15% - CỰC THẤP", "loi_khuyen": "Báo công an"},
        "Tử Môn": {"ty_le": "5% - GẦN NHƯ KHÔNG", "loi_khuyen": "Chuẩn bị mất"}
    }
    return ty_le.get(mon_key, {"ty_le": "50% - TRUNG BÌNH", "loi_khuyen": "Cần xem thêm"})

def _tao_loi_khuyen(kha_nang, quen_la):
    """Tạo lời khuyên ngắn gọn"""
    if "CAO" in kha_nang:
        return "Nên tìm ngay, khả năng lấy lại cao"
    elif "QUEN" in quen_la:
        return "Hỏi người xung quanh, có thể ai đó biết"
    elif "LẠ" in quen_la:
        return "Báo công an, kẻ trộm chuyên nghiệp"
    else:
        return "Tìm kiếm xung quanh, kiên nhẫn"

# ============================================================
# VÍ DỤ CÂU TRẢ LỜI CHUẨN
# ============================================================

VI_DU_TRA_LOI = """
**📍 KẾT QUẢ PHÂN TÍCH XE ĐẠP BỊ MẤT:**

| Câu hỏi | Trả lời | Căn cứ |
|---------|---------|--------|
| 👤 Ai lấy? | **NAM**, 25-45 tuổi | Thiên Bồng (Dương) + Huyền Vũ |
| 🎨 Màu sắc? | **TRẮNG/BẠC** | Cung 6 (Kim) |
| 💰 Giá trị? | **6-15 triệu** | Cung 6 = xe tốt |
| 📏 Khoảng cách? | **600-6000m** | Hướng Tây Bắc |
| 🔗 Quen/Lạ? | **NGƯỜI LẠ (90%)** | Huyền Vũ = trộm chuyên |
| 🔄 Lấy lại được? | **50% - TRUNG BÌNH** | Cảnh Môn |
| 👮 Bị bắt? | **KHẢ NĂNG THẤP (40%)** | Cảnh + Huyền Vũ |

**💡 LỜI KHUYÊN:** Báo công an ngay, kẻ trộm là NAM chuyên nghiệp. Tìm hướng Tây Bắc, cách 600m-6km.
"""

# ============================================================
# PROMPT CHO AI - BẮT BUỘC TRẢ LỜI NGẮN GỌN
# ============================================================

PROMPT_TRA_LOI_NGAN = """
**NGUYÊN TẮC BẮT BUỘC:**
1. KHÔNG giải thích dài dòng
2. KHÔNG nói "không có thông tin"
3. CHỈ trả lời theo BẢNG
4. MỖI câu trả lời = 1-2 từ + căn cứ
5. LUÔN có % và số liệu cụ thể

**FORMAT BẮT BUỘC:**
| Câu hỏi | Trả lời | Căn cứ |
|---------|---------|--------|
| Ai lấy? | NAM/NỮ, X tuổi | Can + Thần |
| Màu sắc? | MÀU X | Ngũ Hành |
| Khoảng cách? | X-Y mét | Cung |
| Quen/Lạ? | QUEN/LẠ (X%) | Thần |
| Lấy lại? | X% | Môn |
| Bị bắt? | X% | Môn + Thần |

**LỜI KHUYÊN:** 1 câu ngắn gọn, hành động cụ thể.
"""

# Export
__all__ = ['TEMPLATE_TIM_DO_MAT', 'tao_tra_loi_ngan_gon', 'VI_DU_TRA_LOI', 'PROMPT_TRA_LOI_NGAN']
