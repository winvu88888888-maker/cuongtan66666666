"""
XEM NGÀY ĐẸP — Module tổng hợp từ 5 sách chuẩn:
1. Hiệp Kỷ Biện Phương Thư
2. Ngọc Hạp Thông Thư
3. Đổng Công Trạch Nhật
4. Thọ Mai Gia Lễ
5. Tam Giáo Chính Hội
"""
import datetime

# ══════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════
CHI_12 = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CAN_10 = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]

# ── 12 TRỰC (Đổng Công Trạch Nhật) ──
TRUC_12 = ["Kiến", "Trừ", "Mãn", "Bình", "Định", "Chấp", "Phá", "Nguy", "Thành", "Thu", "Khai", "Bế"]

TRUC_TINH_CHAT = {
    "Kiến": {"cat_hung": "Cát", "icon": "🟢", "mo_ta": "Khởi đầu, sinh sôi",
             "nen": ["Nhậm chức", "Xuất hành", "Cưới hỏi", "Động thổ", "Cầu tài"],
             "ky": ["Lợp nhà", "Đào ao", "Chôn cất"]},
    "Trừ": {"cat_hung": "Bình", "icon": "🟡", "mo_ta": "Loại bỏ cái xấu",
            "nen": ["Chữa bệnh", "Quét dọn", "Cúng tế", "Cầu an"],
            "ky": ["Ký kết", "Giao dịch", "Mở kho"]},
    "Mãn": {"cat_hung": "Cát", "icon": "🟢", "mo_ta": "Đầy đủ, viên mãn",
            "nen": ["Cầu phúc", "Khai trương", "Nhập kho", "Cưới hỏi"],
            "ky": ["Chôn cất", "Kiện tụng"]},
    "Bình": {"cat_hung": "Cát", "icon": "🟢", "mo_ta": "Bình yên, ổn định",
             "nen": ["Sửa sang", "Chăn nuôi", "Di chuyển", "Xây bếp"],
             "ky": ["Động thổ lớn", "Khai trương"]},
    "Định": {"cat_hung": "Cát", "icon": "🟢", "mo_ta": "Cố định, vẹn toàn",
             "nen": ["Giao dịch", "Ký kết", "Cưới hỏi", "Xây chuồng"],
             "ky": ["Kiện tụng", "Xuất hành", "Chữa bệnh"]},
    "Chấp": {"cat_hung": "Bình", "icon": "🟡", "mo_ta": "Giữ gìn, duy trì",
             "nen": ["Thu nhận", "Học tập", "Xây dựng"],
             "ky": ["Đầu tư lớn", "Cho vay", "Mở kho"]},
    "Phá":  {"cat_hung": "Hung", "icon": "🔴", "mo_ta": "Phá bỏ, dỡ bỏ",
             "nen": ["Tháo dỡ", "Chữa bệnh", "Dọn dẹp"],
             "ky": ["Cưới hỏi", "Khai trương", "Ký kết", "Động thổ"]},
    "Nguy": {"cat_hung": "Hung", "icon": "🔴", "mo_ta": "Nguy hiểm, rủi ro",
             "nen": ["Việc nhỏ", "Cầu an"],
             "ky": ["Xuất hành", "Động thổ", "Di chuyển", "Leo trèo"]},
    "Thành": {"cat_hung": "Cát", "icon": "🟢", "mo_ta": "Thành công, viên mãn",
              "nen": ["Cưới hỏi", "Khai trương", "Nhập học", "Ký kết"],
              "ky": ["Kiện tụng"]},
    "Thu":  {"cat_hung": "Hung", "icon": "🔴", "mo_ta": "Thu hoạch, kết thúc",
             "nen": ["Thu hoạch", "Mua bán", "Nhập kho"],
             "ky": ["Động thổ", "Chôn cất", "Đi xa"]},
    "Khai": {"cat_hung": "Cát", "icon": "🟢", "mo_ta": "Mở mang, bắt đầu",
             "nen": ["Khai trương", "Khởi nghiệp", "Xây dựng", "Cưới hỏi"],
             "ky": ["An táng", "Cho vay"]},
    "Bế":  {"cat_hung": "Bình", "icon": "🟡", "mo_ta": "Bế tắc, kín đáo",
            "nen": ["Đóng kho", "Sửa chữa", "Nghỉ ngơi"],
            "ky": ["Khai trương", "Động thổ", "Việc lớn"]},
}

# ── HOÀNG ĐẠO / HẮC ĐẠO (12 SAO) ──
SAO_12 = [
    ("Thanh Long",  "Hoàng Đạo", "🐉", "Cát — thích hợp mọi việc lớn"),
    ("Minh Đường",  "Hoàng Đạo", "🏛️", "Cát — thuận lợi cầu tài, cưới hỏi"),
    ("Thiên Hình",  "Hắc Đạo",   "⚔️", "Hung — dễ gặp hình phạt, kiện tụng"),
    ("Chu Tước",    "Hắc Đạo",   "🐦", "Hung — thị phi, tranh cãi"),
    ("Kim Quỹ",     "Hoàng Đạo", "💰", "Cát — có lợi tiền bạc, kinh doanh"),
    ("Kim Đường",   "Hoàng Đạo", "🏆", "Cát — quý nhân phù trợ"),
    ("Bạch Hổ",     "Hắc Đạo",   "🐅", "Hung — tang tóc, thương tích"),
    ("Ngọc Đường",  "Hoàng Đạo", "🏯", "Cát — xây dựng, khởi nghiệp"),
    ("Thiên Lao",   "Hắc Đạo",   "🔒", "Hung — tù tội, trở ngại"),
    ("Nguyên Vũ",   "Hắc Đạo",   "🐢", "Hung — mất mát, trộm cắp"),
    ("Tư Mệnh",    "Hoàng Đạo", "📜", "Cát — làm ăn, thăng tiến"),
    ("Câu Trận",    "Hắc Đạo",   "🕸️", "Hung — vướng mắc, trì trệ"),
]

# Bảng khởi điểm Hoàng Đạo theo tháng âm (tháng 1-12)
# Tháng 1 khởi Thanh Long ở Tý, tháng 2 ở Dần, tháng 3 ở Thìn...
HD_KHOI_DIEM = {1: 0, 2: 2, 3: 4, 4: 6, 5: 8, 6: 10, 7: 0, 8: 2, 9: 4, 10: 6, 11: 8, 12: 10}

# ── TAM NƯƠNG (ngày âm lịch) ──
TAM_NUONG = [3, 7, 13, 18, 22, 27]

# ── SAO TỐT / SAO XẤU THEO CAN-CHI NGÀY ──
# Thiên Đức theo tháng âm
THIEN_DUC = {1: "Đinh", 2: "Khôn", 3: "Nhâm", 4: "Tân",
             5: "Càn", 6: "Giáp", 7: "Quý", 8: "Cấn",
             9: "Bính", 10: "Ất", 11: "Tốn", 12: "Canh"}

# Nguyệt Đức theo tháng âm (Can ngày)
NGUYET_DUC = {1: "Bính", 2: "Giáp", 3: "Nhâm", 4: "Canh",
              5: "Bính", 6: "Giáp", 7: "Nhâm", 8: "Canh",
              9: "Bính", 10: "Giáp", 11: "Nhâm", 12: "Canh"}

# ── TRÙNG TANG (Thọ Mai Gia Lễ) ──
# Kết quả cung: Dần/Thân/Tỵ/Hợi = Trùng Tang, Tý/Ngọ/Mão/Dậu = Thiên Di, Thìn/Tuất/Sửu/Mùi = Nhập Mộ
TRUNG_TANG_CUNG = {
    "Dần": "TRÙNG TANG", "Thân": "TRÙNG TANG", "Tỵ": "TRÙNG TANG", "Hợi": "TRÙNG TANG",
    "Tý": "THIÊN DI", "Ngọ": "THIÊN DI", "Mão": "THIÊN DI", "Dậu": "THIÊN DI",
    "Thìn": "NHẬP MỘ", "Tuất": "NHẬP MỘ", "Sửu": "NHẬP MỘ", "Mùi": "NHẬP MỘ",
}

# ── CATEGORIES VIỆC XEM NGÀY ──
VIEC_XEM_NGAY = {
    "cuoi_hoi": {"ten": "💒 Cưới Hỏi", "truc_tot": ["Kiến", "Mãn", "Định", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Thu", "Bế"]},
    "lam_nha": {"ten": "🏠 Làm Nhà / Động Thổ", "truc_tot": ["Kiến", "Mãn", "Bình", "Định", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Bế"]},
    "xuat_hanh": {"ten": "🚀 Xuất Hành", "truc_tot": ["Kiến", "Mãn", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Định", "Bế"]},
    "an_tang": {"ten": "⚰️ An Táng / Chôn Cất", "truc_tot": ["Mãn", "Bình", "Định", "Thành"], "truc_xau": ["Kiến", "Phá", "Thu", "Khai"]},
    "tao_mo": {"ten": "🪦 Tảo Mộ / Sửa Mộ", "truc_tot": ["Mãn", "Bình", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy"]},
    "boc_mo": {"ten": "🏺 Bốc Mộ / Cải Táng", "truc_tot": ["Mãn", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Bế", "Thu"]},
    "khai_truong": {"ten": "🏪 Khai Trương", "truc_tot": ["Kiến", "Mãn", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Bế"]},
    "ky_ket": {"ten": "📝 Ký Kết / Giao Dịch", "truc_tot": ["Định", "Thành", "Khai", "Mãn"], "truc_xau": ["Phá", "Nguy", "Trừ"]},
    "cung_te": {"ten": "🙏 Cúng Tế / Lễ Bái", "truc_tot": ["Kiến", "Trừ", "Mãn", "Bình", "Định", "Thành", "Khai"], "truc_xau": ["Phá"]},
    "cau_tai": {"ten": "💰 Cầu Tài / Xin Việc", "truc_tot": ["Kiến", "Mãn", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Bế"]},
    "don_nha": {"ten": "🔀 Dọn Nhà / Nhập Trạch", "truc_tot": ["Kiến", "Mãn", "Bình", "Thành", "Khai"], "truc_xau": ["Phá", "Nguy", "Bế"]},
    "chua_benh": {"ten": "⚕️ Chữa Bệnh / Phẫu Thuật", "truc_tot": ["Trừ", "Phá", "Khai"], "truc_xau": ["Nguy", "Bế", "Định"]},
}


# ══════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ══════════════════════════════════════════════════════════════

def tinh_truc(thang_am, chi_ngay):
    """Tính Trực theo tháng âm + chi ngày (Đổng Công Trạch Nhật).
    Quy tắc: Tháng 1 khởi Kiến ở Dần, Tháng 2 khởi Kiến ở Mão...
    """
    chi_idx = CHI_12.index(chi_ngay) if chi_ngay in CHI_12 else 0
    # Tháng 1: Kiến ở Dần (index 2), Tháng 2: Kiến ở Mão (index 3)...
    khoi = (thang_am + 1) % 12  # Tháng 1 -> khởi ở chi index 2 (Dần)
    offset = (chi_idx - khoi) % 12
    truc = TRUC_12[offset]
    return truc


def tinh_hoang_dao(thang_am, chi_ngay):
    """Tính sao Hoàng Đạo/Hắc Đạo theo tháng âm + chi ngày.
    Returns: (tên sao, loại HD/HĐ, icon, mô tả)
    """
    chi_idx = CHI_12.index(chi_ngay) if chi_ngay in CHI_12 else 0
    khoi = HD_KHOI_DIEM.get(thang_am, 0)
    sao_idx = (chi_idx - khoi) % 12
    return SAO_12[sao_idx]


def kiem_tra_tam_nuong(ngay_am):
    """Kiểm tra ngày Tam Nương (3, 7, 13, 18, 22, 27 âm lịch)."""
    return ngay_am in TAM_NUONG


def kiem_tra_nguyet_pha(thang_am, chi_ngay):
    """Nguyệt Phá: Chi ngày XUNG Chi tháng.
    Tháng 1=Dần, Chi xung: cách 6 vị trí.
    """
    chi_thang_idx = (thang_am + 1) % 12  # Tháng 1 = Dần (idx 2)
    chi_ngay_idx = CHI_12.index(chi_ngay) if chi_ngay in CHI_12 else -1
    return (chi_ngay_idx - chi_thang_idx) % 12 == 6


def kiem_tra_thien_duc(thang_am, can_ngay):
    """Kiểm tra ngày có Thiên Đức không."""
    td = THIEN_DUC.get(thang_am, "")
    return can_ngay == td


def kiem_tra_nguyet_duc(thang_am, can_ngay):
    """Kiểm tra ngày có Nguyệt Đức không."""
    nd = NGUYET_DUC.get(thang_am, "")
    return can_ngay == nd


def tinh_trung_tang(tuoi_mat, gioi_tinh, nam_mat, thang_mat, ngay_mat, gio_mat):
    """Tính Trùng Tang theo Thọ Mai Gia Lễ.
    tuoi_mat: tuổi âm lịch (số)
    gioi_tinh: 'nam' hoặc 'nu'
    Returns: dict với kết quả từng trụ
    """
    if gioi_tinh == 'nam':
        khoi = CHI_12.index("Dần")  # 2
        huong = 1  # thuận
    else:
        khoi = CHI_12.index("Thân")  # 8
        huong = -1  # nghịch

    ket_qua = {}
    # Đếm theo tuổi qua 4 trụ: Năm -> Tháng -> Ngày -> Giờ
    tru_values = [nam_mat, thang_mat, ngay_mat, gio_mat]
    tru_names = ["Năm", "Tháng", "Ngày", "Giờ"]

    pos = khoi
    for i, (val, name) in enumerate(zip(tru_values, tru_names)):
        # Đếm val bước
        steps = (val - 1) if val > 0 else 0
        pos = (pos + huong * steps) % 12
        cung = CHI_12[pos]
        loai = TRUNG_TANG_CUNG.get(cung, "KHÔNG RÕ")
        ket_qua[name] = {"cung": cung, "loai": loai}

    # Kết luận tổng
    trung_count = sum(1 for v in ket_qua.values() if v["loai"] == "TRÙNG TANG")
    if trung_count >= 2:
        ket_qua["ket_luan"] = "🔴 TRÙNG TANG NẶNG — Cần hóa giải!"
    elif trung_count == 1:
        ket_qua["ket_luan"] = "🟡 CÓ TRÙNG TANG — Nên cẩn trọng"
    else:
        nhap_mo = sum(1 for v in ket_qua.values() if isinstance(v, dict) and v.get("loai") == "NHẬP MỘ")
        if nhap_mo >= 2:
            ket_qua["ket_luan"] = "🟢 NHẬP MỘ — An nghỉ vĩnh viễn, tốt"
        else:
            ket_qua["ket_luan"] = "🟢 KHÔNG TRÙNG TANG — An toàn"

    return ket_qua


def danh_gia_ngay(thang_am, ngay_am, can_ngay, chi_ngay, loai_viec="cuoi_hoi"):
    """Đánh giá tổng hợp một ngày cho một loại việc cụ thể.
    Returns: dict với tất cả thông tin
    """
    truc = tinh_truc(thang_am, chi_ngay)
    truc_info = TRUC_TINH_CHAT.get(truc, {})
    sao = tinh_hoang_dao(thang_am, chi_ngay)
    is_hoang_dao = sao[1] == "Hoàng Đạo"
    is_tam_nuong = kiem_tra_tam_nuong(ngay_am)
    is_nguyet_pha = kiem_tra_nguyet_pha(thang_am, chi_ngay)
    has_thien_duc = kiem_tra_thien_duc(thang_am, can_ngay)
    has_nguyet_duc = kiem_tra_nguyet_duc(thang_am, can_ngay)

    viec = VIEC_XEM_NGAY.get(loai_viec, VIEC_XEM_NGAY["cuoi_hoi"])
    truc_tot_cho_viec = truc in viec["truc_tot"]
    truc_xau_cho_viec = truc in viec["truc_xau"]

    # ── TÍNH ĐIỂM ──
    diem = 50  # Baseline
    ly_do_tot = []
    ly_do_xau = []

    # Hoàng Đạo
    if is_hoang_dao:
        diem += 20
        ly_do_tot.append(f"✅ Ngày Hoàng Đạo — {sao[0]} {sao[2]}")
    else:
        diem -= 15
        ly_do_xau.append(f"❌ Ngày Hắc Đạo — {sao[0]} {sao[2]}")

    # 12 Trực
    if truc_tot_cho_viec:
        diem += 20
        ly_do_tot.append(f"✅ Trực {truc} — {truc_info.get('mo_ta', '')} — TỐT cho {viec['ten']}")
    elif truc_xau_cho_viec:
        diem -= 25
        ly_do_xau.append(f"❌ Trực {truc} — {truc_info.get('mo_ta', '')} — XẤU cho {viec['ten']}")

    # Tam Nương
    if is_tam_nuong:
        diem -= 20
        ly_do_xau.append(f"❌ Ngày Tam Nương (ngày {ngay_am} âm lịch) — Kiêng kỵ việc lớn")

    # Nguyệt Phá
    if is_nguyet_pha:
        diem -= 30
        ly_do_xau.append("❌ Ngày NGUYỆT PHÁ — Xung tháng, mọi việc dễ đổ vỡ!")

    # Thiên Đức / Nguyệt Đức
    if has_thien_duc:
        diem += 15
        ly_do_tot.append("✅ Có sao THIÊN ĐỨC — Hóa giải hung, đại cát!")
    if has_nguyet_duc:
        diem += 15
        ly_do_tot.append("✅ Có sao NGUYỆT ĐỨC — May mắn, thuận lợi!")

    # Clamp
    diem = max(0, min(100, diem))

    # Verdict
    if diem >= 80:
        verdict = "🟢 NGÀY RẤT ĐẸP"
        verdict_color = "#22c55e"
    elif diem >= 60:
        verdict = "🟢 NGÀY TỐT"
        verdict_color = "#86efac"
    elif diem >= 40:
        verdict = "🟡 NGÀY BÌNH THƯỜNG"
        verdict_color = "#fbbf24"
    elif diem >= 20:
        verdict = "🟠 NGÀY XẤU"
        verdict_color = "#f97316"
    else:
        verdict = "🔴 NGÀY RẤT XẤU"
        verdict_color = "#ef4444"

    return {
        "diem": diem,
        "verdict": verdict,
        "verdict_color": verdict_color,
        "truc": truc,
        "truc_info": truc_info,
        "sao_hoang_dao": sao,
        "is_hoang_dao": is_hoang_dao,
        "is_tam_nuong": is_tam_nuong,
        "is_nguyet_pha": is_nguyet_pha,
        "has_thien_duc": has_thien_duc,
        "has_nguyet_duc": has_nguyet_duc,
        "truc_tot_cho_viec": truc_tot_cho_viec,
        "truc_xau_cho_viec": truc_xau_cho_viec,
        "ly_do_tot": ly_do_tot,
        "ly_do_xau": ly_do_xau,
        "loai_viec": viec["ten"],
        "can_ngay": can_ngay,
        "chi_ngay": chi_ngay,
        "thang_am": thang_am,
        "ngay_am": ngay_am,
    }


def tim_ngay_dep(thang_am, can_chi_list, loai_viec="cuoi_hoi", top_n=5):
    """Tìm N ngày đẹp nhất từ danh sách can-chi.
    can_chi_list: [(ngay_am, can, chi), ...]
    Returns: sorted list of results
    """
    results = []
    for ngay_am, can, chi in can_chi_list:
        r = danh_gia_ngay(thang_am, ngay_am, can, chi, loai_viec)
        results.append(r)
    results.sort(key=lambda x: x["diem"], reverse=True)
    return results[:top_n]
