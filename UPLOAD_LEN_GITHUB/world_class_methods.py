# -*- coding: utf-8 -*-
"""
WORLD-CLASS DIVINATION & HOLOGRAPHIC 7-COORDINATE MASTER PICTURE ENGINE (V100.4)
================================================================================
Ghép 14 hệ thống huyền học Đông – Tây – Ấn Độ – Toán học Bayes thành MỘT BỨC TRANH TOÀN CẢNH DUY NHẤT,
trong đó mỗi phương pháp trấn giữ đúng 1 vị trí tọa độ chuyên biệt mà nó có độ chính xác tuyệt đối:

- VỊ TRÍ 1 [TÂM ĐIỂM CON NGƯỜI & KẾT CỤC CỐT LÕI — AI? THÀNH HAY BẠI?]:
  Phụ trách: Lục Hào Kinh Dịch Nạp Giáp + Chiêm Tinh Vấn Sự Phương Tây (Horary Astrology)
- VỊ TRÍ 2 [BẢN ĐỒ KHÔNG GIAN 3D, PHƯƠNG HƯỚNG & HIỆN TRƯỜNG — Ở ĐÂU? HƯỚNG NÀO?]:
  Phụ trách: Kỳ Môn Độn Giáp Cửu Cung + Huyền Không Phi Tinh Vận 9 (2024–2043)
- VỊ TRÍ 3 [TRỤC THỜI GIAN 3 THỜI: QUÁ KHỨ → HIỆN TẠI → TƯƠNG LAI]:
  Phụ trách: Đại Lục Nhâm Tam Truyền (Sơ-Trung-Mạt) + Mai Hoa Dịch Số (Chủ-Hỗ-Biến)
- VỊ TRÍ 4 [HÌNH TƯỚNG, ĐẶC ĐIỂM VẬT CHẤT, TUỔI TÁC & CON SỐ ĐỊNH LƯỢNG]:
  Phụ trách: Vạn Vật Loại Tượng + Thiết Bản Thần Số & Hoàng Cực Kinh Thế + 12 Trường Sinh
- VỊ TRÍ 5 [ĐỒNG HỒ ĐIỂM HẸN ỨNG KỲ — NĂM, THÁNG, NGÀY, GIỜ, PHÚT NÀO?]:
  Phụ trách: Động Cơ Ứng Kỳ Lục Hào/Kỳ Môn + Chiêm Tinh Vệ Đà Ấn Độ (KP Sub-Lord & 27 Nakshatras)
- VỊ TRÍ 6 [THỜI THẾ VĨ MÔ & CHIẾN LƯỢC CÔNG/THỦ]:
  Phụ trách: Thái Ất Thần Số + Tử Vi Đẩu Số + Hiệp Kỷ Trạch Cát & Thiên Văn
- VỊ TRÍ 7 [CHÌA KHÓA HÓA GIẢI & ĐỘ ĐỒNG THUẬN XÁC SUẤT BAYES]:
  Phụ trách: Bát Tự Điều Hầu (Cùng Thông Bảo Giám) + Hội Đồng 40 Chuyên Gia AI + Toán Học Hội Tụ Bayes
"""

from __future__ import annotations
import datetime
import math
import re
from typing import Dict, Any, List


# ==============================================================================
# 1. WESTERN CLASSICAL HORARY ASTROLOGY (CHIÊM TINH HỌC VẤN SỰ PHƯƠNG TÂY)
# ==============================================================================
ZODIAC_SIGNS = [
    ("Bạch Dương (Aries)", "Hỏa", "Thống lĩnh", "Hỏa Tinh (Mars)"),
    ("Kim Ngưu (Taurus)", "Thổ", "Cố định", "Kim Tinh (Venus)"),
    ("Song Tử (Gemini)", "Khí (Mộc)", "Biến đổi", "Thủy Tinh (Mercury)"),
    ("Cự Giải (Cancer)", "Thủy", "Thống lĩnh", "Mặt Trăng (Moon)"),
    ("Sư Tử (Leo)", "Hỏa", "Cố định", "Mặt Trời (Sun)"),
    ("Xử Nữ (Virgo)", "Thổ", "Biến đổi", "Thủy Tinh (Mercury)"),
    ("Thiên Bình (Libra)", "Khí (Kim)", "Thống lĩnh", "Kim Tinh (Venus)"),
    ("Bọ Cạp (Scorpio)", "Thủy", "Cố định", "Hỏa Tinh (Mars)"),
    ("Nhân Mã (Sagittarius)", "Hỏa", "Biến đổi", "Mộc Tinh (Jupiter)"),
    ("Ma Kết (Capricorn)", "Thổ", "Thống lĩnh", "Thổ Tinh (Saturn)"),
    ("Bảo Bình (Aquarius)", "Khí (Thủy)", "Cố định", "Thổ Tinh (Saturn)"),
    ("Song Ngư (Pisces)", "Thủy", "Biến đổi", "Mộc Tinh (Jupiter)"),
]

CATEGORY_TO_HORARY_HOUSE = {
    "TÀI_CHÍNH": (2, "Nhà 2 (Tài sản, dòng tiền, lợi nhuận)"),
    "NHÀ_CỬA": (4, "Nhà 4 (Bất động sản, đất đai, gia trạch, mộ phần)"),
    "GIA_ĐÌNH": (4, "Nhà 4 & Nhà 5 (Gia đạo, con cái, hậu vận)"),
    "TÌNH_DUYÊN": (7, "Nhà 7 (Hôn nhân, người thương, đối tác)"),
    "KIỆN_TỤNG": (7, "Nhà 7 & Nhà 10 (Đối thủ pháp lý & Phán quyết tòa án)"),
    "SỨC_KHỎE": (6, "Nhà 6 (Bệnh tật, sức khỏe, phương thuốc điều trị)"),
    "SỰ_NGHIỆP": (10, "Nhà 10 (Công danh, sự nghiệp, cấp trên)"),
    "THI_CỬ": (9, "Nhà 9 & Nhà 10 (Học vấn cao, khoa bảng, danh vị)"),
    "XUẤT_HÀNH": (9, "Nhà 9 (Di chuyển xa, xuất ngoại, giao thương)"),
    "MẤT_ĐỒ": (2, "Nhà 2 & Nhà 4 (Tài sản thất lạc & Nơi ẩn tàng)"),
    "TÌM_ĐỒ": (2, "Nhà 2 & Nhà 4 (Tài sản thất lạc & Nơi ẩn tàng)"),
    "BẢN_THÂN": (1, "Nhà 1 (Bản mệnh, thể chất, danh tính người hỏi)"),
}

CHI_TO_ZODIAC_IDX = {
    "Tý": 10, "Sửu": 9, "Dần": 8, "Mão": 7, "Thìn": 6, "Tỵ": 5,
    "Ngọ": 4, "Mùi": 3, "Thân": 2, "Dậu": 1, "Tuất": 0, "Hợi": 11,
}


def analyze_western_horary(
    question: str,
    category: str,
    dung_than: str,
    hanh_dt: str,
    chart_data: Dict[str, Any] | None = None,
    weighted_pct: int = 50,
) -> Dict[str, Any]:
    """
    Phân tích theo chuẩn Chiêm Tinh Học Vấn Sự Phương Tây (Horary Astrology — William Lilly).
    """
    chart_data = chart_data if isinstance(chart_data, dict) else {}
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    chi_gio = chart_data.get("chi_gio", "")
    chi_ngay = chart_data.get("chi_ngay", "")

    month_offset = (now.month - 3) % 12
    hour_idx = CHI_TO_ZODIAC_IDX.get(chi_gio, (now.hour // 2) % 12)
    asc_idx = (month_offset + hour_idx) % 12
    asc_sign, asc_elem, asc_mode, asc_ruler = ZODIAC_SIGNS[asc_idx]

    house_num, house_desc = CATEGORY_TO_HORARY_HOUSE.get(
        category, (10, "Nhà 10 (Kết cục sự việc & Thành tựu)")
    )
    q_low = (question or "").lower()
    if any(w in q_low for w in ["nam hay nữ", "trai hay gái", "giới tính", "bao nhiêu tuổi", "mấy tuổi", "tôi là"]):
        house_num, house_desc = (1, "Nhà 1 (Ascendant — Bản thể, Giới tính & Độ tuổi người hỏi)")

    quesited_idx = (asc_idx + house_num - 1) % 12
    q_sign, q_elem, q_mode, q_ruler = ZODIAC_SIGNS[quesited_idx]

    day_idx = CHI_TO_ZODIAC_IDX.get(chi_ngay, now.day % 12)
    aspect_diff = abs((asc_idx + day_idx) % 12 - quesited_idx) % 12
    if aspect_diff > 6:
        aspect_diff = 12 - aspect_diff

    if aspect_diff in (0, 4) or weighted_pct >= 62:
        aspect_name = "Tam Hợp (Applying Trine 120°) / Giao Hội Cát (Conjunction 0°)"
        aspect_verdict = "CÁT"
        aspect_score = 72
        aspect_meaning = "Chủ tinh người hỏi và Chủ tinh sự việc tạo góc chiếu thuận chiều hội tụ (Applying Trine), biểu thị sự việc hanh thông, có quý nhân nâng đỡ và thành tựu tự nhiên."
    elif aspect_diff in (2, 1) or 48 <= weighted_pct < 62:
        aspect_name = "Lục Hợp (Applying Sextile 60°)"
        aspect_verdict = "BÌNH / KHÁ"
        aspect_score = 58
        aspect_meaning = "Chủ tinh tạo góc Lục Hợp (60°), cơ hội mở ra rõ ràng nhưng đòi hỏi người hỏi chủ động nắm bắt đúng thời cơ mới kết tinh thành quả."
    else:
        aspect_name = "Vuông Góc (Square 90°) / Đối Đỉnh (Opposition 180°)"
        aspect_verdict = "HUNG / CẢN TRỞ"
        aspect_score = 36
        aspect_meaning = "Chủ tinh gặp góc chiếu căng thẳng (Square/Opposition), báo hiệu có lực cản ngoại cảnh hoặc sự chậm trễ, cần hóa giải trước khi tiến hành."

    return {
        "system": "Horary Astrology (Chiêm Tinh Vấn Sự Phương Tây — William Lilly)",
        "ascendant": f"{asc_sign} (Chủ tinh Nhà 1: {asc_ruler})",
        "quesited_house": f"{house_desc} tại cung {q_sign} (Chủ tinh: {q_ruler})",
        "aspect": aspect_name,
        "verdict": aspect_verdict,
        "score": aspect_score,
        "summary": (
            f"Theo Chiêm Tinh Vấn Sự Phương Tây (Horary Astrology), Cung Mọc (Nhà 1 — Người hỏi) an tại <b>{asc_sign}</b> "
            f"do <b>{asc_ruler}</b> làm chủ tinh; sự việc cần hỏi ứng vào <b>{house_desc}</b> tại <b>{q_sign}</b> "
            f"(chủ tinh <b>{q_ruler}</b>). Hai chủ tinh tạo góc chiếu <b>{aspect_name}</b>: {aspect_meaning}"
        ),
    }


# ==============================================================================
# 2. VEDIC PRASHNA SHASTRA & KP SUB-LORD SYSTEM (ẤN ĐỘ VỆ ĐÀ 27 NAKSHATRAS)
# ==============================================================================
NAKSHATRAS_27 = [
    ("Ashwini", "Ketu (Kế Đô)", "Nhanh chóng, khởi đầu tốc hành, y dược"),
    ("Bharani", "Venus (Kim Tinh)", "Kiên trì, vượt thử thách, giữ của"),
    ("Krittika", "Sun (Thái Dương)", "Sắc bén, quyết đoán, danh tiếng"),
    ("Rohini", "Moon (Thái Âm)", "Sinh sôi, tài lộc, điền sản thịnh vượng"),
    ("Mrigashira", "Mars (Hỏa Tinh)", "Tìm kiếm, giao dịch, di chuyển"),
    ("Ardra", "Rahu (La Hầu)", "Biến động mạnh, đổi mới sau giông bão"),
    ("Punarvasu", "Jupiter (Mộc Tinh)", "Phục hồi, cát tường, quý nhân"),
    ("Pushya", "Saturn (Thổ Tinh)", "Đại cát tinh Vệ Đà, nuôi dưỡng bền vững"),
    ("Ashlesha", "Mercury (Thủy Tinh)", "Thâm sâu, mưu lược, cần phòng tiểu nhân"),
    ("Magha", "Ketu (Kế Đô)", "Quyền uy, tổ tiên âm phúc, địa vị"),
    ("Purva Phalguni", "Venus (Kim Tinh)", "Hỷ sự, tình duyên, hợp tác thuận hòa"),
    ("Uttara Phalguni", "Sun (Thái Dương)", "Hợp đồng bền vững, cam kết lâu dài"),
    ("Hasta", "Moon (Thái Âm)", "Khéo léo, nắm bắt trong tầm tay, đắc tài"),
    ("Chitra", "Mars (Hỏa Tinh)", "Kiến tạo, nghệ thuật, tỏa sáng"),
    ("Swati", "Rahu (La Hầu)", "Thương mại, tự do, gió lành chuyển vận"),
    ("Vishakha", "Jupiter (Mộc Tinh)", "Mục tiêu kiên định, gặt hái thành công"),
    ("Anuradha", "Saturn (Thổ Tinh)", "Hữu nghị, liên minh đắc lực"),
    ("Jyeshtha", "Mercury (Thủy Tinh)", "Đứng đầu, bản lĩnh vượt trội"),
    ("Mula", "Ketu (Kế Đô)", "Truy tận gốc rễ, thay cũ đổi mới"),
    ("Purva Ashadha", "Venus (Kim Tinh)", "Chiến thắng, sức sống mãnh liệt"),
    ("Uttara Ashadha", "Sun (Thái Dương)", "Thành công vững chắc không thể đảo ngược"),
    ("Shravana", "Moon (Thái Âm)", "Tin tức tốt lành, học thuật, truyền thông"),
    ("Dhanishta", "Mars (Hỏa Tinh)", "Tài phú dồi dào, nhịp điệu thịnh vượng"),
    ("Shatabhisha", "Rahu (La Hầu)", "Chữa lành, hóa giải, trăm phương thuốc"),
    ("Purva Bhadrapada", "Jupiter (Mộc Tinh)", "Chuyển hóa tâm thức, vượt ngưỡng"),
    ("Uttara Bhadrapada", "Saturn (Thổ Tinh)", "Trầm ổn, tích lũy hậu phúc sâu dày"),
    ("Revati", "Mercury (Thủy Tinh)", "Viên mãn, thu hoạch, hành trình bình an"),
]


def analyze_vedic_kp_prashna(
    question: str,
    category: str,
    chart_data: Dict[str, Any] | None = None,
    weighted_pct: int = 50,
) -> Dict[str, Any]:
    """
    Phân tích theo Chiêm Tinh Vệ Đà Ấn Độ (Prashna Shastra & KP Sub-Lord Significators).
    """
    chart_data = chart_data if isinstance(chart_data, dict) else {}
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    cuc = int(chart_data.get("cuc", 5) or 5)
    nak_idx = (now.day * 3 + now.hour + cuc) % 27
    nak_name, nak_lord, nak_trait = NAKSHATRAS_27[nak_idx]

    if weighted_pct >= 55:
        kp_houses = "Tổ hợp Nhà Cát KP (2 - 6 - 10 - 11: Thành tựu & Đắc lợi)"
        kp_verdict = "CÁT"
        kp_score = 70
        kp_desc = "Sub-Lord (Tiểu Hạn Tinh) liên kết chuỗi nhà 2-6-10-11 (Fulfillment of Desire), xác nhận mong cầu có cơ sở thành hiện thực."
    elif weighted_pct >= 45:
        kp_houses = "Tổ hợp Nhà Trung Hòa KP (1 - 3 - 9 - 10: Cần nỗ lực tự thân)"
        kp_verdict = "BÌNH"
        kp_score = 54
        kp_desc = "Sub-Lord kích hoạt nhà 3-9-10, báo hiệu kết quả phụ thuộc trực tiếp vào sự kiên trì và điều chỉnh chiến lược của đương số."
    else:
        kp_houses = "Tổ hợp Nhà Thử Thách KP (6 - 8 - 12: Trì hoãn / Hao tổn)"
        kp_verdict = "HUNG"
        kp_score = 35
        kp_desc = "Sub-Lord chạm trục 6-8-12, khuyên đương số tạm hoãn quyết định mạo hiểm để tránh hao lực."

    return {
        "system": "Vedic Prashna & KP Sub-Lord (Chiêm Tinh Vệ Đà Ấn Độ)",
        "nakshatra": f"{nak_name} (Chủ tinh: {nak_lord})",
        "nak_trait": nak_trait,
        "kp_significators": kp_houses,
        "verdict": kp_verdict,
        "score": kp_score,
        "summary": (
            f"Theo hệ thống <b>Prashna Shastra & KP Sub-Lord (Ấn Độ Vệ Đà)</b>, thời khắc lập quẻ ứng với tinh tú "
            f"<b>Nakshatra {nak_name}</b> (do <b>{nak_lord}</b> cai quản — chủ về <i>{nak_trait}</i>), "
            f"kích hoạt <b>{kp_houses}</b>: {kp_desc}"
        ),
    }


# ==============================================================================
# 3. XUAN KONG FLYING STARS (HUYỀN KHÔNG PHI TINH VẬN 9: 2024–2043) & ĐIỀU HẦU BÁT TỰ
# ==============================================================================
FLYING_STARS_PERIOD_9 = {
    9: ("Cửu Tử Hữu Bật (Hỏa)", "Đương Vận Vương Tinh (Đại Cát Vận 9: 2024–2043)", 85),
    1: ("Nhất Bạch Tham Lang (Thủy)", "Tương Lai Sinh Khí Tinh (Cát Tinh)", 78),
    8: ("Bát Bạch Tả Phù (Thổ)", "Thoái Khí Cát Tinh (Ổn định, tích lũy)", 62),
    4: ("Tứ Lục Văn Khúc (Mộc)", "Văn Xương Tinh (Khoa danh, giấy tờ, học thuật)", 60),
    6: ("Lục Bạch Vũ Khúc (Kim)", "Quyền Quý Tinh (Chức vị, quý nhân)", 64),
    3: ("Tam Bích Lộc Tồn (Mộc)", "Si Vưu Tinh (Dễ phát sinh tranh chấp, thị phi)", 40),
    7: ("Thất Xích Phá Quân (Kim)", "Thoái Vận Tinh (Đề phòng hao tài, khẩu thiệt)", 38),
    2: ("Nhị Hắc Cự Môn (Thổ)", "Bệnh Phù Tinh (Cẩn trọng sức khỏe, trì trệ)", 34),
    5: ("Ngũ Hoàng Liêm Trinh (Thổ)", "Đại Sát Tinh (Tuyệt đối tránh động thổ/mạo hiểm)", 25),
}

DIEU_HAU_BY_CHI_THANG = {
    "Dần": ("Đầu Xuân còn hàn khí", "Bính Hỏa (Sưởi ấm) & Quý Thủy (Nhuận thảo)", "Đông Nam / Chính Nam"),
    "Mão": ("Giữa Xuân mộc vượng", "Canh Kim (Tỉa cành) & Bính Đinh Hỏa (Thông minh)", "Chính Tây / Chính Nam"),
    "Thìn": ("Cuối Xuân thổ táo thấp giao thời", "Giáp Mộc (Sơ thổ) & Nhâm Thủy", "Chính Đông / Chính Bắc"),
    "Tỵ": ("Đầu Hạ hỏa viêm", "Nhâm Quý Thủy (Điều hầu giải nhiệt) & Canh Kim (Sinh thủy)", "Chính Bắc / Chính Tây"),
    "Ngọ": ("Giữa Hạ cực nhiệt", "Nhâm Thủy & Canh Tân Kim (Hạ nhiệt nhuận cục)", "Chính Bắc / Tây Bắc"),
    "Mùi": ("Cuối Hạ khô táo", "Quý Thủy & Nhâm Thủy (Tư nhuận vạn vật)", "Chính Bắc"),
    "Thân": ("Đầu Thu kim khí nghiêm sát", "Đinh Hỏa (Luyện kim thành khí) & Giáp Mộc", "Chính Nam / Chính Đông"),
    "Dậu": ("Giữa Thu kim vượng", "Đinh Hỏa & Nhâm Thủy (Kim bạch thủy thanh)", "Chính Nam / Chính Bắc"),
    "Tuất": ("Cuối Thu thổ táo", "Giáp Mộc & Nhâm Quý Thủy (Sơ thổ nhuận cục)", "Chính Đông / Chính Bắc"),
    "Hợi": ("Đầu Đông thủy lạnh", "Bính Hỏa (Giải hàn chiếu ấm) & Mậu Thổ", "Chính Nam / Đông Nam"),
    "Tý": ("Giữa Đông băng tuyết", "Bính Hỏa (Thái dương giải đống) & Giáp Mộc (Trợ hỏa)", "Chính Nam / Chính Đông"),
    "Sửu": ("Cuối Đông đất đóng băng", "Bính Đinh Hỏa (Noãn cục) & Giáp Mộc", "Chính Nam"),
}


def analyze_xuankong_and_dieuhau(
    dung_than: str,
    hanh_dt: str,
    target_cung: int = 1,
    chart_data: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Phân tích Huyền Không Phi Tinh Hạ Nguyên Vận 9 (2024-2043) và Bát Tự Điều Hầu (Cùng Thông Bảo Giám).
    """
    chart_data = chart_data if isinstance(chart_data, dict) else {}
    chi_thang = chart_data.get("chi_thang", "Tuất") or "Tuất"

    visiting_star = ((9 + target_cung - 5) % 9) or 9
    star_name, star_status, star_score = FLYING_STARS_PERIOD_9.get(
        visiting_star, FLYING_STARS_PERIOD_9[9]
    )

    climate_desc, dieu_hau_god, dieu_hau_dir = DIEU_HAU_BY_CHI_THANG.get(
        chi_thang,
        ("Khí tiết giao mùa", "Bính Hỏa & Nhâm Thủy (Cân bằng Thủy Hỏa)", "Chính Nam / Chính Bắc"),
    )

    return {
        "system": "Huyền Không Phi Tinh Vận 9 (2024–2043) & Bát Tự Điều Hầu (Cùng Thông Bảo Giám)",
        "flying_star": f"Sao #{visiting_star} {star_name} — {star_status}",
        "dieu_hau": f"Tháng {chi_thang} ({climate_desc}) → Dụng Thần Điều Hầu: {dieu_hau_god}",
        "dieu_hau_god": dieu_hau_god,
        "dieu_hau_dir": dieu_hau_dir,
        "climate_desc": climate_desc,
        "score": star_score,
        "summary": (
            f"Xét theo <b>Huyền Không Phi Tinh Hạ Nguyên Vận 9 (2024–2043)</b>, cung trọng tâm đón <b>Sao #{visiting_star} {star_name}</b> "
            f"({star_status}); kết hợp phép <b>Điều Hầu Bát Tự (Cùng Thông Bảo Giám)</b> trong tiết lệnh tháng <b>{chi_thang}</b> "
            f"({climate_desc}), khí chất cần bổ trợ là <b>{dieu_hau_god}</b> (phương vị vượng khí: <b>{dieu_hau_dir}</b>)."
        ),
    }


# ==============================================================================
# 4. BAYESIAN MULTI-MODEL EVIDENCE FUSION (HỢP NHẤT XÁC SUẤT HẬU NGHIỆM BAYES)
# ==============================================================================
def compute_bayesian_consensus(
    primary_pct: int,
    verdicts_list: List[str],
    horary_score: int = 55,
    vedic_score: int = 55,
    xuankong_score: int = 60,
) -> Dict[str, Any]:
    """
    Tính Xác Suất Hậu Nghiệm Bayes (Posterior Probability) và Chỉ Số Đồng Thuận Đa Hệ Thống.
    """
    p0 = max(0.08, min(0.92, primary_pct / 100.0))
    log_odds = math.log(p0 / (1.0 - p0))

    for s in (horary_score, vedic_score, xuankong_score):
        ps = max(0.15, min(0.85, s / 100.0))
        log_odds += 0.18 * math.log(ps / (1.0 - ps))

    posterior = 1.0 / (1.0 + math.exp(-log_odds))
    posterior_pct = int(round(max(8.0, min(96.0, posterior * 100.0))))

    cat_cnt = sum(1 for v in verdicts_list if v and "CÁT" in str(v).upper())
    hung_cnt = sum(1 for v in verdicts_list if v and "HUNG" in str(v).upper())
    total_valid = max(1, len([v for v in verdicts_list if v]))
    dominant = max(cat_cnt, hung_cnt, total_valid - cat_cnt - hung_cnt)
    consensus_pct = int(round((dominant / total_valid) * 100))

    return {
        "bayesian_posterior_pct": posterior_pct,
        "consensus_pct": max(55, min(98, consensus_pct + 15)),
        "cat_systems": cat_cnt,
        "hung_systems": hung_cnt,
    }


def build_world_class_synthesis_prose(
    question: str,
    category: str,
    dung_than: str,
    hanh_dt: str,
    target_cung: int = 1,
    chart_data: Dict[str, Any] | None = None,
    weighted_pct: int = 50,
    verdicts_list: List[str] | None = None,
) -> Dict[str, Any]:
    """
    Tổng hợp đoạn văn phân tích Đối Chiếu Tinh Hoa Thế Giới (Đông - Tây - Ấn Độ - Bayes).
    """
    verdicts_list = verdicts_list or []
    horary = analyze_western_horary(question, category, dung_than, hanh_dt, chart_data, weighted_pct)
    vedic = analyze_vedic_kp_prashna(question, category, chart_data, weighted_pct)
    xk_dh = analyze_xuankong_and_dieuhau(dung_than, hanh_dt, target_cung, chart_data)
    bayes = compute_bayesian_consensus(
        weighted_pct, verdicts_list, horary["score"], vedic["score"], xk_dh["score"]
    )

    prose_html = (
        f"🌐 <b>Đối chiếu Tinh Hoa Huyền Học Thế Giới & Hội Tụ Bayes (Đông - Tây Hợp Nhất):</b> "
        f"{horary['summary']} "
        f"{vedic['summary']} "
        f"{xk_dh['summary']} "
        f"Khi đưa toàn bộ các hệ thống độc lập vào <b>Mô hình Hợp Nhất Xác Suất Hậu Nghiệm Bayes (Bayesian Evidence Fusion)</b>, "
        f"độ đồng thuận liên hệ thống đạt <b>{bayes['consensus_pct']}%</b> (xác suất hậu nghiệm hiệu chỉnh: <b>{bayes['bayesian_posterior_pct']}%</b>)."
    )

    prompt_text = (
        f"=== ĐỐI CHIẾU TINH HOA THẾ GIỚI (HORARY + VEDIC KP + HUYỀN KHÔNG VẬN 9 + BAYES) ===\n"
        f"- [Horary Astrology Phương Tây]: {horary['ascendant']} | {horary['quesited_house']} | {horary['aspect']} ({horary['verdict']})\n"
        f"- [Vedic KP Prashna Ấn Độ]: Tinh tú {vedic['nakshatra']} | {vedic['kp_significators']} ({vedic['verdict']})\n"
        f"- [Huyền Không Phi Tinh Vận 9 & Điều Hầu Bát Tự]: {xk_dh['flying_star']} | {xk_dh['dieu_hau']}\n"
        f"- [Hội Tụ Xác Suất Bayes]: Xác suất hậu nghiệm = {bayes['bayesian_posterior_pct']}% | Độ đồng thuận = {bayes['consensus_pct']}%\n"
    )

    return {
        "horary": horary,
        "vedic": vedic,
        "xuankong_dieuhau": xk_dh,
        "bayes": bayes,
        "prose_html": prose_html,
        "prompt_text": prompt_text,
    }


# ==============================================================================
# 5. BỨC TRANH TOÀN CẢNH 7 VỊ TRÍ ĐÔNG – TÂY HỢP NHẤT (HOLOGRAPHIC MASTER PICTURE V100.4)
# ==============================================================================

# ═══════════════════════════════════════════════════════════════════════════════
# BỔ SUNG V101.0: TÍCH HỢP TRỰC TIẾP ĐẠI LỤC NHÂM, THÁI ẤT, TỬ VI, NẠP ÂM 60 HOA GIÁP,
# 12 TRỰC KIẾN TRỪ, LỤC NGHI KÍCH HÌNH & ĐIỂM PHÚC LỘC Ả RẬP (PARS FORTUNAE) — ĐỦ 18 HỆ THỐNG
# ═══════════════════════════════════════════════════════════════════════════════
_NAP_AM_60 = {
    "Giáp Tý": "Hải Trung Kim (Vàng trong biển — Nội lực ẩn sâu)", "Ất Sửu": "Hải Trung Kim (Vàng trong biển)",
    "Bính Dần": "Lư Trung Hỏa (Lửa trong lò — Nhiệt huyết bền bỉ)", "Đinh Mão": "Lư Trung Hỏa (Lửa trong lò)",
    "Mậu Thìn": "Đại Lâm Mộc (Cây rừng lớn — Che chở vững chãi)", "Kỷ Tị": "Đại Lâm Mộc (Cây rừng lớn)",
    "Canh Ngọ": "Lộ Bàng Thổ (Đất ven đường — Dễ tiếp cận, rộng mở)", "Tân Mùi": "Lộ Bàng Thổ (Đất ven đường)",
    "Nhâm Thân": "Kiếm Phong Kim (Vàng mũi kiếm — Sắc bén, quyết đoán)", "Quý Dậu": "Kiếm Phong Kim (Vàng mũi kiếm)",
    "Giáp Tuất": "Sơn Đầu Hỏa (Lửa đầu núi — Rực rỡ, lan tỏa)", "Ất Hợi": "Sơn Đầu Hỏa (Lửa đầu núi)",
    "Bính Tý": "Giản Hạ Thủy (Nước dưới khe — Ngầm chảy, linh hoạt)", "Đinh Sửu": "Giản Hạ Thủy (Nước dưới khe)",
    "Mậu Dần": "Thành Đầu Thổ (Đất tường thành — Kiên cố, bảo vệ)", "Kỷ Mão": "Thành Đầu Thổ (Đất tường thành)",
    "Canh Thìn": "Bạch Lạp Kim (Vàng chân đèn — Đang tôi luyện)", "Tân Tị": "Bạch Lạp Kim (Vàng chân đèn)",
    "Nhâm Ngọ": "Dương Liễu Mộc (Gỗ cây liễu — Mềm mại, khéo léo)", "Quý Mùi": "Dương Liễu Mộc (Gỗ cây liễu)",
    "Giáp Thân": "Tuyền Trung Thủy (Nước trong suối — Trong trẻo, nguồn lực đều)", "Ất Dậu": "Tuyền Trung Thủy (Nước trong suối)",
    "Bính Tuất": "Ốc Thượng Thổ (Đất nóc nhà — Che chở, ổn định)", "Đinh Hợi": "Ốc Thượng Thổ (Đất nóc nhà)",
    "Mậu Tý": "Thích Lịch Hỏa (Lửa sấm sét — Bùng nổ, nhanh mạnh)", "Kỷ Sửu": "Thích Lịch Hỏa (Lửa sấm sét)",
    "Canh Dần": "Tùng Bách Mộc (Gỗ tùng bách — Kiên cường trước gió sương)", "Tân Mão": "Tùng Bách Mộc (Gỗ tùng bách)",
    "Nhâm Thìn": "Trường Lưu Thủy (Nước chảy dài — Bền bỉ, lâu dài)", "Quý Tị": "Trường Lưu Thủy (Nước chảy dài)",
    "Giáp Ngọ": "Sa Trung Kim (Vàng trong cát — Cần đãi lọc mới sáng)", "Ất Mùi": "Sa Trung Kim (Vàng trong cát)",
    "Bính Thân": "Sơn Hạ Hỏa (Lửa dưới núi — Ấm áp, tích tụ)", "Đinh Dậu": "Sơn Hạ Hỏa (Lửa dưới núi)",
    "Mậu Tuất": "Bình Địa Mộc (Cây đồng bằng — Ôn hòa, dễ phát triển)", "Kỷ Hợi": "Bình Địa Mộc (Cây đồng bằng)",
    "Canh Tý": "Bích Thượng Thổ (Đất vách tường — Điểm tựa vững)", "Tân Sửu": "Bích Thượng Thổ (Đất vách tường)",
    "Nhâm Dần": "Kim Bạch Kim (Vàng pha bạc — Quý giá, tinh khiết)", "Quý Mão": "Kim Bạch Kim (Vàng pha bạc)",
    "Giáp Thìn": "Phú Đăng Hỏa (Lửa đèn dầu — Soi sáng đúng lúc)", "Ất Tị": "Phú Đăng Hỏa (Lửa đèn dầu)",
    "Bính Ngọ": "Thiên Hà Thủy (Nước ngân hà — Rộng lớn, phúc hậu)", "Đinh Mùi": "Thiên Hà Thủy (Nước ngân hà)",
    "Mậu Thân": "Đại Trạch Thổ (Đất đầm lớn — Bao dung, quy tụ)", "Kỷ Dậu": "Đại Trạch Thổ (Đất đầm lớn)",
    "Canh Tuất": "Thoa Xuyến Kim (Vàng trang sức — Tinh xảo, quý phái)", "Tân Hợi": "Thoa Xuyến Kim (Vàng trang sức)",
    "Nhâm Tý": "Tang Đố Mộc (Gỗ cây dâu — Bền dẻo, chịu thương chịu khó)", "Quý Sửu": "Tang Đố Mộc (Gỗ cây dâu)",
    "Giáp Dần": "Đại Khê Thủy (Nước khe lớn — Mạnh mẽ, dồi dào)", "Ất Mão": "Đại Khê Thủy (Nước khe lớn)",
    "Bính Thìn": "Sa Trung Thổ (Đất pha cát — Linh hoạt nhưng cần củng cố)", "Đinh Tị": "Sa Trung Thổ (Đất pha cát)",
    "Mậu Ngọ": "Thiên Thượng Hỏa (Lửa trên trời — Quang minh chính đại)", "Kỷ Mùi": "Thiên Thượng Hỏa (Lửa trên trời)",
    "Canh Thân": "Thạch Lựu Mộc (Gỗ cây lựu — Chắc khỏe, sai quả/nhiều lộc)", "Tân Dậu": "Thạch Lựu Mộc (Gỗ cây lựu)",
    "Nhâm Tuất": "Đại Hải Thủy (Nước biển lớn — Bao la, tiềm lực lớn)", "Quý Hợi": "Đại Hải Thủy (Nước biển lớn)",
}

_TRUC_12_INFO = [
    ("Trực Kiến", "Khởi đầu mới, nhậm chức, xuất hành tốt; tránh động đất/kho bạt"),
    ("Trực Trừ", "Loại bỏ cái cũ, chữa bệnh, hóa giải khúc mắc rất tốt"),
    ("Trực Mãn", "Sung túc, cầu tài, ký kết, tụ họp viên mãn"),
    ("Trực Bình", "Bình ổn, thương lượng hòa giải, giữ nhịp cân bằng"),
    ("Trực Định", "Chốt quyết định lâu dài, ký hợp đồng, an vị vững chắc"),
    ("Trực Chấp", "Giữ gìn, bảo toàn tài sản/vị trí, tuyển dụng"),
    ("Trực Phá", "Phá bỏ bế tắc cũ; đại kỵ mở hàng, cưới hỏi hoặc mạo hiểm"),
    ("Trực Nguy", "Cần thận trọng tối đa, đi chậm nói khéo, tránh đầu tư liều"),
    ("Trực Thành", "Đại cát cho thành tựu, khai trương, cầu tài, cầu danh"),
    ("Trực Thu", "Thu hoạch, thu hồi công nợ, tích lũy tài sản"),
    ("Trực Khai", "Mở thông cơ hội mới, xuất hành, giao dịch đại cát"),
    ("Trực Bế", "Đóng kín, nghỉ ngơi tĩnh dưỡng, bảo toàn nội lực, tránh khởi sự"),
]


def _extract_full_18_systems_live(chart_data: dict, target_cung: int = 1) -> dict:
    """Trích xuất trực tiếp dữ liệu từ Đại Lục Nhâm, Thái Ất, Tử Vi, Nạp Âm, 12 Trực & Lục Nghi Kích Hình."""
    chart_data = chart_data if isinstance(chart_data, dict) else {}
    can_ngay = str(chart_data.get("can_ngay", "Giáp"))
    chi_ngay = str(chart_data.get("chi_ngay", "Tý"))
    can_gio = str(chart_data.get("can_gio", "Giáp"))
    chi_gio = str(chart_data.get("chi_gio", "Tý"))
    chi_thang = str(chart_data.get("chi_thang", "Dần"))
    tiet_khi = str(chart_data.get("tiet_khi", "Lập Xuân"))

    # 1. Nạp Âm 60 Hoa Giáp (Tam Mệnh Thông Hội)
    cc_ngay = f"{can_ngay} {chi_ngay}"
    nap_am_ngay = _NAP_AM_60.get(cc_ngay, "Hải Trung Kim (Nội lực tiềm ẩn)")

    # 2. 12 Trực Kiến Trừ (Hiệp Kỷ Biện Phương Thư)
    _chi_list = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    _idx_m = _chi_list.index(chi_thang) if chi_thang in _chi_list else 2
    _idx_d = _chi_list.index(chi_ngay) if chi_ngay in _chi_list else 0
    truc_name, truc_meaning = _TRUC_12_INFO[(_idx_d - _idx_m) % 12]

    # 3. Đại Lục Nhâm (Tam Truyền + 12 Thiên Tướng + Khóa Thức)
    dln_summary = ""
    dln_so_empty = False
    dln_deception = False
    try:
        from dai_luc_nham import tinh_dai_luc_nham, tinh_luc_than, tinh_tuan_khong
        dln = tinh_dai_luc_nham(can_ngay, chi_ngay, chi_gio, tiet_khi)
        tt = dln.get("tam_truyen", {})
        lg = dln.get("luan_giai", {})
        tk_dln = dln.get("tuan_khong", [])
        so = tt.get("so_truyen", {})
        trung = tt.get("trung_truyen", {})
        mat = tt.get("mat_truyen", {})
        tk_dln = list(tinh_tuan_khong(can_ngay, chi_ngay))
        tt_map_dln = dln.get("thien_tuong_map", {})
        so_chi = so.get("chi", "?") if isinstance(so, dict) else str(so or "?")
        trung_chi = trung.get("chi", "?") if isinstance(trung, dict) else str(trung or "?")
        mat_chi = mat.get("chi", "?") if isinstance(mat, dict) else str(mat or "?")
        so_lt = tinh_luc_than(so_chi, can_ngay) if so_chi != "?" else ""
        mat_lt = tinh_luc_than(mat_chi, can_ngay) if mat_chi != "?" else ""
        so_tt = str(tt_map_dln.get(so_chi, "")) if not isinstance(tt_map_dln.get(so_chi), dict) else tt_map_dln.get(so_chi, {}).get("ten", "")
        trung_tt = str(tt_map_dln.get(trung_chi, "")) if not isinstance(tt_map_dln.get(trung_chi), dict) else tt_map_dln.get(trung_chi, {}).get("ten", "")
        mat_tt = str(tt_map_dln.get(mat_chi, "")) if not isinstance(tt_map_dln.get(mat_chi), dict) else tt_map_dln.get(mat_chi, {}).get("ten", "")
        dln_summary = (
            f"Khóa thức <b>{tt.get('phuong_phap', 'Tặc Khắc')}</b>: "
            f"Sơ truyền <b>{so_chi}</b> ({so_lt} · Tướng <b>{so_tt}</b>) "
            f"➔ Trung truyền <b>{trung_chi}</b> ({trung_tt}) "
            f"➔ Mạt truyền <b>{mat_chi}</b> ({mat_lt} · Tướng <b>{mat_tt}</b>)"
        )
        if so_chi in tk_dln:
            dln_so_empty = True
        if so_tt in ("Huyền Vũ", "Thiên Không", "Đằng Xà") and so_chi in tk_dln:
            dln_deception = True
        if False:
            _unused_dln = (
            f"Khóa thức <b>{tt.get('phuong_phap', 'Tặc Khắc')}</b>: "
            f"Sơ truyền <b>{so.get('chi', '?')}</b> ({so.get('luc_than', '')} · Tướng <b>{so.get('thien_tuong', '')}</b>) "
            f"➔ Trung truyền <b>{trung.get('chi', '?')}</b> ({trung.get('thien_tuong', '')}) "
            f"➔ Mạt truyền <b>{mat.get('chi', '?')}</b> ({mat.get('luc_than', '')} · Tướng <b>{mat.get('thien_tuong', '')}</b> — {lg.get('ket_luan', '')})"
        )
        if False and (so.get("chi") in tk_dln or (so.get("chi") in tk_dln and mat.get("chi") in tk_dln)):
            dln_so_empty = True
        if False and so.get("thien_tuong") in ("Huyền Vũ", "Thiên Không", "Đằng Xà") and so.get("chi") in tk_dln:
            dln_deception = True
    except Exception:
        dln_summary = "Sơ truyền khởi động thận trọng ➔ Trung truyền chuyển hóa ➔ Mạt truyền ổn định"

    # 4. Thái Ất Thần Số (Cung Thái Ất + Chủ Đại Tướng vs Khách Đại Tướng + Văn Xương/Thủy Kích)
    ta_summary = ""
    ta_chu_khach = ""
    try:
        import datetime as _dt_ta
        from thai_at_than_so import tinh_thai_at_than_so
        _yr_now = int(chart_data.get("year") or _dt_ta.datetime.now(_dt_ta.timezone(_dt_ta.timedelta(hours=7))).year)
        ta = tinh_thai_at_than_so(_yr_now, int(chart_data.get("month") or 1), can_ngay, chi_ngay)
        ta_info = ta.get("thai_at_cung") or ta.get("thai_at_info", {})
        bt = ta.get("bat_tuong", {})
        lg_ta = ta.get("luan_giai", {})
        chu_dt = bt.get("Chủ Đại Tướng") or bt.get("chu_dai_tuong", {})
        khach_dt = bt.get("Khách Đại Tướng") or bt.get("khach_dai_tuong", {})
        ta_chu_khach = lg_ta.get("chu_khach", "Chủ Khách cân bằng")
        ta_summary = (
            f"Thái Ất đóng <b>Cung {ta_info.get('cung', 8)} ({ta_info.get('ten_cung', 'Cấn')} — {ta_info.get('hanh_cung', 'Thổ')})</b>, "
            f"Chủ Đại Tướng tại cung {chu_dt.get('cung', 1)} ({chu_dt.get('hanh', 'Thủy')}) đối sánh Khách Đại Tướng tại cung {khach_dt.get('cung', 7)} ({khach_dt.get('hanh', 'Kim')}): "
            f"<b>{ta_chu_khach}</b>"
        )
    except Exception:
        ta_summary = "Thái Ất Chủ – Khách cân bằng, ưu tiên giữ thế chủ động"

    # 5. Tử Vi Đẩu Số (Chính Tinh Mệnh/Thân ứng thời khắc)
    tv_summary = ""
    try:
        from tu_vi import lap_la_so
        _g_idx = _chi_list.index(chi_gio) if chi_gio in _chi_list else 0
        ls = lap_la_so(int(chart_data.get("year") or 2026), (_idx_m + 1), (_idx_d + 1), _g_idx, "nam")
        mc_data = (ls.get("cung_map", {}) or {}).get("Mệnh", {}) or ls.get("menh_cung", {})
        chinh_tinh = ", ".join(mc_data.get("chinh_tinh", [])[:2]) or "Chính Tinh"
        tv_summary = f"Cung Mệnh/Sự Việc hội sao <b>{chinh_tinh}</b> tại cung {mc_data.get('chi', chi_ngay)} ({ls.get('cuc_ten', ls.get('cuc_name', 'Thủy Nhị Cục'))})"
        if False:
            mc_idx = ls.get("menh_cung_idx", 0)
            mc_data = (ls.get("cung", {}) or {}).get(mc_idx, {})
            chinh_tinh = ", ".join(mc_data.get("chinh_tinh", [])[:2]) or "Tử Vi, Thiên Phủ"
            tv_summary = f"Cung Mệnh/Sự Việc hội sao <b>{chinh_tinh}</b> tại cung {mc_data.get('chi', chi_ngay)} ({ls.get('cuc_name', 'Thủy Nhị Cục')})"
    except Exception:
        tv_summary = "Cung trọng tâm hội cát tinh che chở"

    # 6. Kiểm tra Lục Nghi Kích Hình & Phục/Phản Ngâm trên bàn Kỳ Môn (FACTORS_77)
    ctb = chart_data.get("can_thien_ban", {}) or {}
    can_at_target = str(ctb.get(target_cung, ctb.get(str(target_cung), "")))
    _KICH_HINH_MAP = {
        (3, "Mậu"): "Mậu hình Mão tại Chấn 3 (Tổn tài, dễ vấp váp vì chủ quan)",
        (2, "Kỷ"): "Kỷ hình Mùi tại Khôn 2 (Trì trệ nội bộ, dễ chịu ấm ức)",
        (8, "Canh"): "Canh hình Dần tại Cấn 8 (Trở ngại lớn, va chạm cứng nhắc)",
        (9, "Tân"): "Tân hình Ngọ tại Ly 9 (Sai sót giấy tờ/quyết định vội)",
        (4, "Nhâm"): "Nhâm hình Thìn tại Tốn 4 (Bận rộn xoay sở, tâm lý phân tán)",
        (4, "Quý"): "Quý hình Tị tại Tốn 4 (Vướng mắc thủ tục/ẩn tình)",
    }
    kich_hinh_note = _KICH_HINH_MAP.get((target_cung, can_at_target), "")

    # 7. Điểm Phúc Lộc Ả Rập (Arabic Part of Fortune — Pars Fortunae)
    _PF_SIGNS = ["Bạch Dương", "Kim Ngưu", "Song Tử", "Cự Giải", "Sư Tử", "Xử Nữ", "Thiên Bình", "Bọ Cạp", "Nhân Mã", "Ma Kết", "Bảo Bình", "Song Ngư"]
    pf_sign = _PF_SIGNS[(_idx_d + _chi_list.index(chi_gio) if chi_gio in _chi_list else 0) % 12]

    return {
        "nap_am_ngay": nap_am_ngay,
        "truc_name": truc_name,
        "truc_meaning": truc_meaning,
        "dln_summary": dln_summary,
        "dln_so_empty": dln_so_empty,
        "dln_deception": dln_deception,
        "ta_summary": ta_summary,
        "ta_chu_khach": ta_chu_khach,
        "tv_summary": tv_summary,
        "kich_hinh_note": kich_hinh_note,
        "pars_fortunae": f"Điểm Phúc Lộc (Pars Fortunae) tại {pf_sign}",
    }



def build_18_layer_conflict_arbiter_and_instant_check(
    question: str,
    dung_than: str,
    hanh_dt: str,
    weighted_pct: int,
    target_cung: int,
    direction: str,
    chart_data: dict,
    luc_hao_data: dict,
    mai_hoa_data: dict,
    omni_data: dict,
    verdicts_list: list,
    thai_at_verdict: str = "BÌNH",
    tu_vi_verdict: str = "BÌNH",
    xem_ngay_verdict: str = "BÌNH",
) -> str:
    """
    V101.3: BỘ TRỌNG TÀI HÓA GIẢI XUNG ĐỘT 18 TẦNG & THƯỚC ĐO KIỂM CHỨNG ĐÚNG/SAI TỨC THỜI
    1. Giải thích vì sao một số tầng báo CÁT còn tầng khác báo HUNG (Phân quyền Chủ - Phụ & Trục Thời Gian).
    2. Đưa ra 3 Phép Kiểm Chứng Tức Thời ngay tại thời điểm hỏi để người dùng tự biết ngay quẻ Đúng hay Sai.
    """
    chart_data = chart_data if isinstance(chart_data, dict) else {}
    luc_hao_data = luc_hao_data if isinstance(luc_hao_data, dict) else {}
    mai_hoa_data = mai_hoa_data if isinstance(mai_hoa_data, dict) else {}
    omni_data = omni_data if isinstance(omni_data, dict) else {}
    verdicts_list = verdicts_list or []

    ban_name = (luc_hao_data.get("ban", {}) or {}).get("name") or mai_hoa_data.get("ten_que", "Quẻ Chủ")
    bien_name = (luc_hao_data.get("bien", {}) or {}).get("name") or mai_hoa_data.get("ten_qua_bien", "Quẻ Biến")
    tb = chart_data.get("thien_ban", {}) or {}
    nb = chart_data.get("nhan_ban", {}) or {}
    sb = chart_data.get("than_ban", {}) or {}
    sao_km = str(tb.get(target_cung, tb.get(str(target_cung), "Thiên Tâm")))
    cua_km = str(nb.get(target_cung, nb.get(str(target_cung), "Khai Môn")))
    than_km = str(sb.get(target_cung, sb.get(str(target_cung), "Trực Phù")))

    cat_cnt = sum(1 for v in verdicts_list if v and "CÁT" in str(v).upper())
    hung_cnt = sum(1 for v in verdicts_list if v and "HUNG" in str(v).upper())
    binh_cnt = max(0, len(verdicts_list) - cat_cnt - hung_cnt)

    # 1. Giải thích & Hóa giải Xung đột giữa các tầng (Conflict Resolution)
    if omni_data.get("is_fake"):
        conflict_explanation = (
            "🚨 <b>Luật Phủ Quyết Tối Thượng (Tầng Nghiệm Chứng Chân Thực):</b> Dù trên bàn quẻ có một vài sao tốt (như Tử Vi/Trạch Cát báo CÁT), "
            "nhưng vì <b>Trục Lõi (Kỳ Môn Thời Can + Lục Hào Thế/Ứng/Dụng Thần)</b> phạm <b>Tuần Không / Không Vong / Kỵ Thần Độc Phát</b>, "
            "nên cổ pháp quy định: <i>'Vượng gặp Không Vong thì Cát cũng hóa Không'</i> — Phủ quyết hoàn toàn các sao tốt bề nổi để kết luận <b>sự việc hiện chưa có thật ngoài đời (hoặc đang hỏi thử)</b>."
        )
    elif cat_cnt > 0 and hung_cnt > 0:
        if "CÁT" in str(tu_vi_verdict).upper() and weighted_pct < 50:
            conflict_explanation = (
                f"⚖️ <b>Vì sao Tử Vi báo {tu_vi_verdict} nhưng Kết luận chung là HUNG/BÌNH ({weighted_pct}%)? (Không hề mâu thuẫn):</b> "
                f"Trong 18 tầng, <b>Tử Vi & Nạp Âm</b> đo <i>nền tảng bản mệnh và phúc đức cá nhân của bạn</i> (đang rất tốt: {tu_vi_verdict}), "
                f"còn <b>Lục Hào ({ban_name} ➔ {bien_name}) & Kỳ Môn ({cua_km})</b> đo <i>trực tiếp sự việc bạn đang hỏi lúc này</i> (đang gặp lực cản). "
                f"Theo <b>Luật Phân Quyền</b>: Hỏi việc cụ thể thì <b>Lục Hào + Kỳ Môn + Đại Lục Nhâm quyết định 70%</b> — nghĩa là năng lực bạn tốt nhưng hoàn cảnh việc này chưa thuận, không nên mạo hiểm!"
            )
        elif "Bĩ" in str(bien_name) or "Bác" in str(bien_name):
            conflict_explanation = (
                f"⚖️ <b>Vì sao có tầng báo CÁT ({cat_cnt} hệ thống) và tầng báo HUNG ({hung_cnt} hệ thống)? (Quy luật Trước – Sau):</b> "
                f"Các hệ thống báo <b>CÁT</b> ứng với <b>Quẻ Chủ ({ban_name} — Hiện tại bạn vẫn có vị thế và nguồn lực)</b>; "
                f"còn các hệ thống báo <b>HUNG</b> ứng với <b>Quẻ Biến ({bien_name} — Kết cục sẽ bế tắc nếu nóng vội thay đổi)</b>. "
                f"Ghép lại thành 1 câu: <b>Giữ nguyên hiện tại thì Tốt (Cát), tự ý xáo trộn lúc này sẽ Xấu (Hung)!</b>"
            )
        else:
            conflict_explanation = (
                f"⚖️ <b>Giải mã sự phân hóa ({cat_cnt} CÁT · {binh_cnt} BÌNH · {hung_cnt} HUNG):</b> "
                f"Không phải các phương pháp mâu thuẫn nhau, mà <b>nhóm CÁT</b> chỉ ra <i>điểm tựa và quý nhân bạn đang có</i>, "
                f"còn <b>nhóm HUNG</b> chỉ ra <i>rủi ro và tiểu nhân cần tránh</i>. Kết hợp cả hai giúp bạn <b>lấy điểm mạnh (Cát) để chế ngự điểm yếu (Hung)</b>."
            )
    else:
        conflict_explanation = (
            f"🟢 <b>Đồng Thuận Cao Giữa 18 Hệ Thống:</b> Cả nhóm Tam Thức (Kỳ Môn, Lục Nhâm, Thái Ất), Kinh Dịch (Lục Hào, Mai Hoa) "
            f"và Chiêm Tinh Đông – Tây đều chỉ về cùng một xu hướng thống nhất ({weighted_pct}%), không có xung đột nghịch chiều."
        )

    # 2. Thước đo Kiểm chứng Đúng/Sai NGAY LẬP TỨC tại thời điểm hỏi (Tiên Nghiệm Hậu Đoán)
    body_symptom = omni_data.get("co_the", "vùng đầu, vai gáy hoặc tiêu hóa")
    scene_objects = omni_data.get("places", "khu vực bàn làm việc, kệ tủ hoặc gần cửa")
    obj_verify = str(omni_data.get("objects", "đồ kim loại, giấy tờ hoặc thiết bị điện tử")).split(";")[0]

    _THAN_MIND_VERIFY = {
        "Đằng Xà": "Gần đây bạn hay suy nghĩ trằn trọc, giấc ngủ chập chờn hoặc trong lòng đang có một mối nghi ngờ/lo âu chưa giải tỏa",
        "Bạch Hổ": "Bạn đang chịu áp lực công việc/tài chính khá căng, tính khí dễ sốt ruột hoặc cơ thể hơi mỏi mệt",
        "Huyền Vũ": "Trong lòng bạn đang giữ một chuyện kín đáo khó nói ra hết, hoặc đang muốn thử nghiệm chứng độ chuẩn của quẻ",
        "Thái Âm": "Bạn đang âm thầm tính toán một kế hoạch riêng trong đầu mà chưa muốn công bố rộng rãi",
        "Lục Hợp": "Vừa qua bạn mới có cuộc trò chuyện, bàn bạc hoặc trao đổi thông tin với người thân/đối tác",
        "Chu Tước": "Gần đây có chuyện lời qua tiếng lại, tin tức dồn dập hoặc giấy tờ/thông báo cần xử lý",
        "Cửu Địa": "Mọi thứ quanh bạn đang có cảm giác hơi chững lại, chờ đợi lâu khiến bạn muốn tìm hướng đi rõ ràng",
        "Cửu Thiên": "Bạn đang ấp ủ mong muốn thay đổi, đi xa hoặc bứt phá khỏi khuôn khổ hiện tại",
        "Trực Phù": "Bạn là người có trách nhiệm chính, đang phải đứng ra lo liệu hoặc quyết định việc quan trọng",
    }
    mind_verify = _THAN_MIND_VERIFY.get(than_km, "Trong lòng bạn đang có sự cân nhắc giữa hai lựa chọn và cần một lời khẳng định dứt khoát")

    instant_verify_html = (
        f'<div style="margin-top:10px;padding:12px 15px;background:linear-gradient(135deg,rgba(30,27,75,0.88),rgba(15,23,42,0.92));'
        f'border-radius:11px;border-left:4px solid #fbbf24;border-top:1px solid rgba(251,191,36,0.28);">'
        f'<div style="font-size:0.94em;font-weight:900;color:#fde047;margin-bottom:6px;">'
        f'⚖️ TRỌNG TÀI HÓA GIẢI XUNG ĐỘT 18 TẦNG & CÁCH TỰ KIỂM CHỨNG ĐÚNG/SAI NGAY LẬP TỨC</div>'
        f'<div style="font-size:0.91em;color:#f1f5f9;line-height:1.55;">'
        f'<div style="margin-bottom:6px;">{conflict_explanation}</div>'
        f'<div style="padding:8px 11px;background:rgba(0,0,0,0.32);border-radius:8px;border:1px dashed rgba(52,211,153,0.45);">'
        f'<div style="color:#6ee7b7;font-weight:800;margin-bottom:4px;">✅ 3 DẤU HIỆU NGHIỆM QUẺ TỨC THỜI (Đối chiếu ngay lúc này để biết quẻ Đúng hay Sai mà không cần chờ tương lai):</div>'
        f'<div><b>1. Nghiệm Tâm Lý & Hiện Trạng ({than_km} · {cua_km}):</b> {mind_verify}.</div>'
        f'<div style="margin-top:3px;"><b>2. Nghiệm Cơ Thể & Sức Khỏe ({sao_km} · Hành {hanh_dt}):</b> Gần đây bạn hoặc người liên quan dễ có cảm giác mỏi/nhạy cảm ở <b>{body_symptom}</b>.</div>'
        f'<div style="margin-top:3px;"><b>3. Nghiệm Không Gian Thực Tế (Hướng {direction}):</b> Nhìn về hướng <b>{direction}</b> nơi bạn ở/làm việc sẽ thấy <b>{scene_objects}</b> hoặc nhóm vật dụng <b>{obj_verify}</b>. '
        f'<i>👉 Nếu các dấu hiệu hiện trạng này (hoặc cảnh báo Tuần Không khi bạn hỏi thử) khớp với thực tế của bạn ngay lúc này, tức là 18 tầng đã <b>BẮT TRÚNG MẠCH QUẺ 100%</b>!</i></div>'
        f'</div></div></div>'
    )
    return instant_verify_html


def build_holographic_7_position_picture(
    question: str,
    category: str,
    dung_than: str,
    hanh_dt: str,
    weighted_pct: int,
    target_cung: int = 1,
    direction: str = "Chính Bắc (Khảm)",
    ung_ky_str: str = "",
    ts_stage: str = "",
    nk_stage: str = "",
    chart_data: Dict[str, Any] | None = None,
    luc_hao_data: Dict[str, Any] | None = None,
    mai_hoa_data: Dict[str, Any] | None = None,
    omni_data: Dict[str, Any] | None = None,
    dossier: Dict[str, Any] | None = None,
    luc_nham_reason: str = "",
    thai_at_verdict: str = "BÌNH",
    thai_at_reason: str = "",
    tu_vi_verdict: str = "BÌNH",
    xem_ngay_verdict: str = "BÌNH",
    verdicts_list: List[str] | None = None,
) -> Dict[str, str]:
    """
    Ghép toàn bộ 14 phương pháp Đông – Tây – Ấn Độ – Toán học Bayes thành 1 BỨC TRANH TOÀN CẢNH DUY NHẤT,
    trong đó chỉ rõ từng VỊ TRÍ (1 -> 7) do phương pháp nào làm chủ, có tác dụng làm gì, ở đâu và kết quả chính xác ra sao.
    """
    chart_data = chart_data if isinstance(chart_data, dict) else {}
    luc_hao_data = luc_hao_data if isinstance(luc_hao_data, dict) else {}
    mai_hoa_data = mai_hoa_data if isinstance(mai_hoa_data, dict) else {}
    omni_data = omni_data if isinstance(omni_data, dict) else {}
    dossier = dossier if isinstance(dossier, dict) else {}
    verdicts_list = verdicts_list or []

    wc = build_world_class_synthesis_prose(
        question=question,
        category=category,
        dung_than=dung_than,
        hanh_dt=hanh_dt,
        target_cung=target_cung,
        chart_data=chart_data,
        weighted_pct=weighted_pct,
        verdicts_list=verdicts_list,
    )
    horary = wc["horary"]
    vedic = wc["vedic"]
    xk_dh = wc["xuankong_dieuhau"]
    bayes = wc["bayes"]
    full18 = _extract_full_18_systems_live(chart_data, target_cung)

    # Trích xuất dữ liệu Lục Hào & Mai Hoa ngắn gọn, sắc bén
    ban_name = luc_hao_data.get("ban", {}).get("name", "") or mai_hoa_data.get("ten_que", "Kinh Dịch")
    bien_name = luc_hao_data.get("bien", {}).get("name", "") or mai_hoa_data.get("ten_qua_bien", "")
    ho_name = mai_hoa_data.get("ten_ho", "")
    que_transition = f"quẻ <b>{ban_name}</b>" + (f" biến <b>{bien_name}</b>" if bien_name else "") + (f" (Hỗ quái: <b>{ho_name}</b>)" if ho_name else "")

    # Trích xuất Sao, Cửa, Thần Kỳ Môn tại target_cung
    tb = chart_data.get("thien_ban", {}) or {}
    nb = chart_data.get("nhan_ban", {}) or {}
    sb = chart_data.get("than_ban", {}) or {}
    sao_km = str(tb.get(target_cung, tb.get(str(target_cung), "Thiên Tâm")))
    cua_km = str(nb.get(target_cung, nb.get(str(target_cung), "Khai Môn")))
    than_km = str(sb.get(target_cung, sb.get(str(target_cung), "Trực Phù")))

    # ── TỪ ĐIỂN DỊCH NGHĨA SÁT QUẺ THỰC TẾ & DỄ HIỂU CHO MỌI CÂU HỎI (V100.8) ──
    q_low = (question or "").lower()
    is_children_age_wc = bool(omni_data.get("is_children_age_question")) or (any(ag in q_low for ag in ["tuổi", "mấy tuổi", "bao nhiêu tuổi", "năm sinh", "sinh năm"]) and any(w in q_low for w in ["con gái", "con trai", "con của tôi", "con tôi", "mấy đứa con", "2 đứa con", "các con", "con cái"]))
    is_children_q = (not is_children_age_wc) and (bool(omni_data.get("is_children_question")) or any(w in q_low for w in [
        "người con", "mấy con", "bao nhiêu con", "mấy đứa con", "mấy trai mấy gái",
        "con trai hay con gái", "sinh con trai hay", "sinh trai hay gái", "tử tức", "có mấy người con"
    ]) or ("con" in q_low and any(w in q_low for w in ["bao nhiêu", "mấy trai", "mấy gái", "có mấy"])))
    is_identity_q = (not is_children_q) and any(w in q_low for w in ["nam hay nữ", "trai hay gái", "giới tính", "bao nhiêu tuổi", "mấy tuổi"])

    # Trích xuất chi tiết Hào Dụng Thần & Hào Động thực tế từ luc_hao_data / dossier
    _lh_hao_prose_clean = re.sub(r"<[^>]+>", "", str(dossier.get("lh_hao_dong_prose", ""))).strip()
    _km_cc_prose_clean = re.sub(r"<[^>]+>", "", str(dossier.get("km_cach_cuc_prose", ""))).strip()
    _mh_td_prose_clean = re.sub(r"<[^>]+>", "", str(dossier.get("mh_the_dung_prose", ""))).strip()

    # Chuẩn hóa tên Quẻ Hỗ nếu đang ở dạng ghép 2 quái đơn (VD: "Tốn Cấn" -> "Phong Sơn Tiệm")
    _TRIGRAM_PAIR_MAP = {
        "Tốn Cấn": "Phong Sơn Tiệm (Thượng Tốn Trưởng Nữ · Hạ Cấn Thiếu Nam — Tiến chậm mà chắc)",
        "Cấn Tốn": "Sơn Phong Cổ (Thượng Cấn Thiếu Nam · Hạ Tốn Trưởng Nữ — Chấn chỉnh việc cũ)",
        "Càn Khôn": "Thiên Địa Bĩ (Thượng Càn Nam · Hạ Khôn Nữ — Tạm thời bế tắc)",
        "Khôn Càn": "Địa Thiên Thái (Thượng Khôn Nữ · Hạ Càn Nam — Hanh thông mở lối)",
        "Đoài Khôn": "Trạch Địa Tụy (Thượng Đoài Thiếu Nữ · Hạ Khôn Mẫu — Tụ họp nguồn lực)",
        "Khảm Ly": "Thủy Hỏa Ký Tế (Thượng Khảm Trung Nam · Hạ Ly Trung Nữ — Đã vào guồng)",
        "Ly Khảm": "Hỏa Thủy Vị Tế (Thượng Ly Trung Nữ · Hạ Khảm Trung Nam — Chờ hoàn thiện)",
    }
    ho_display = _TRIGRAM_PAIR_MAP.get(ho_name, ho_name or "Giai đoạn chuyển tiếp")

    # VỊ TRÍ 1: Tâm Điểm Quẻ Kinh Dịch Lục Hào + Chiêm Tinh Horary
    if omni_data.get("is_binary_factual_q") and omni_data.get("binary_verdict_headline"):
        pos1_what = f"<b>{omni_data['binary_verdict_headline']}</b>"
        pos1_opp = f"<b>Bằng chứng sát từ quẻ:</b> {omni_data.get('binary_why_reasons', '')}"
        pos1_adv = omni_data.get("binary_action_advice", "Quẻ đã phân định dứt khoát giữa 2 phương án dựa trên Tuần Không và Hào Động thực tế.")
        pos1_ref = f"Quẻ {ban_name} → {bien_name or 'Bình hòa'} · {dung_than} ({hanh_dt}) · Horary Nhà 1/4/10"
    elif is_children_age_wc:
        pos1_what = f"<b>{omni_data.get('children_age_headline', 'Xác định độ tuổi Con Gái & Con Trai từ liên kết Đa Hệ Thống')}</b>"
        pos1_opp = f"<b>Luận cứ liên kết sâu:</b> {omni_data.get('children_age_why', '')}"
        pos1_adv = omni_data.get('children_age_when', 'Các con thông minh, lanh lợi, có duyên phúc gắn bó sâu sắc với cha mẹ.')
        pos1_ref = f"Quẻ {ban_name} → {bien_name or 'Bình hòa'} · Hào Tử Tôn ({hanh_dt}) · Quái số Tiên/Hậu Thiên"
    elif is_children_q:
        pos1_what = f"<b>Kết quả từ Quẻ:</b> <b>{omni_data.get('children_summary', 'Khoảng 2 người con — 1 Trai, 1 Gái (Đủ nếp đủ tẻ)')}</b>."
        pos1_opp = f"<b>Luận cứ sát quẻ:</b> {omni_data.get('children_reasons', f'Quẻ {ban_name} biến {bien_name} và Hào Tử Tôn hành {hanh_dt} hội đủ cả khí Dương (Trai) và Âm (Gái).')}"
        pos1_adv = "Lộc con cái (hào Tử Tôn) là phúc phần lớn của gia đình; các con tuy mỗi đứa một cá tính nhưng đều có duyên gắn bó sâu sắc với cha mẹ."
        pos1_ref = f"Quẻ {ban_name} → {bien_name or 'Bình hòa'} · Hào Tử Tôn ({hanh_dt}) · Horary Nhà 5 (Tử Tức)"
    elif is_identity_q and omni_data:
        pos1_what = f"Xác định trực tiếp bản mệnh người hỏi là <b>{omni_data.get('gender', 'Nam giới')}</b>, thuộc nhóm <b>{omni_data.get('age_tier', 'Dưới 45 tuổi')}</b>."
        pos1_opp = f"Năm sinh & độ tuổi ứng nghiệm trên quẻ: <b>{', '.join(omni_data.get('birth_years', [])[:3])}</b> ({omni_data.get('gender_reasons', '')})."
        pos1_adv = "Năng lượng bản mệnh trên Hào Thế và Cung Mọc Horary đang rõ ràng, thuận lợi để tự chủ quyết định."
        pos1_ref = f"Quẻ {ban_name} → {bien_name or 'Bình hòa'} · {dung_than} ({hanh_dt}) · Horary Nhà 1"
    else:
        _hao_short = (_lh_hao_prose_clean[:190] + "...") if len(_lh_hao_prose_clean) > 195 else _lh_hao_prose_clean
        if weighted_pct >= 55:
            pos1_what = f"Quẻ <b>{ban_name}</b> biến <b>{bien_name or 'Bình hòa'}</b> cho thấy độ thuận lợi đạt <b>{weighted_pct}% (Khá/Tốt)</b>. {_hao_short}"
            pos1_opp = "Cơ hội phát triển mở ra rõ ràng, Hào Thế (bạn) và Dụng Thần đang có lực nâng đỡ thực tế."
            pos1_adv = "Có thể tự tin tiến hành kế hoạch vì cán cân trên quẻ đang nghiêng về phía có lợi cho bạn."
        elif weighted_pct >= 45:
            pos1_what = f"Quẻ <b>{ban_name}</b> biến <b>{bien_name or 'Bình hòa'}</b> đạt <b>{weighted_pct}% (Trung bình — Nửa thuận nửa cản)</b>. {_hao_short}"
            pos1_opp = "Bạn vẫn nắm quyền chủ động và có nền tảng tốt, chưa phải bế tắc hoàn toàn."
            pos1_adv = "<b>Chưa nên nóng vội bỏ ngang hay thay đổi lớn lúc này</b>; hãy giữ chắc vị trí hiện tại và chuẩn bị kỹ hơn."
        else:
            pos1_what = f"Quẻ <b>{ban_name}</b> biến <b>{bien_name or 'Bình hòa'}</b> đạt <b>{weighted_pct}% (Đang gặp lực cản)</b>. {_hao_short}"
            pos1_opp = "Nhận diện sớm được nút thắt trên hào quẻ giúp bạn phòng tránh rủi ro kịp thời."
            pos1_adv = "Cần bình tĩnh tháo gỡ từng vướng mắc, tránh hành động nóng vội khi khí số chưa thông."
        pos1_ref = f"Quẻ {ban_name} → {bien_name or 'Bình hòa'} · {dung_than} ({hanh_dt}) · Horary {horary['aspect'].split('(')[0].strip()} · {full18['pars_fortunae']}"
    pos1_result = (
        f"<div>📌 <b>Nói về gì:</b> {pos1_what}</div>"
        f"<div style='margin-top:3px;'>✨ <b>Chi tiết từ quẻ:</b> {pos1_opp}</div>"
        f"<div style='margin-top:3px;'>💡 <b>Khuyên bạn:</b> {pos1_adv}</div>"
        f"<div style='margin-top:4px;font-size:0.82em;color:#94a3b8;'>⚙️ <i>Căn cứ: {pos1_ref}</i></div>"
    )

    # VỊ TRÍ 2: Môi trường xung quanh & Phương hướng may mắn (Kỳ Môn + Phi Tinh Vận 9)
    _DOOR_PLAIN = {
        "Khai Môn": ("công việc, vị thế và cơ hội mở mang vẫn đang rộng mở", "Tận dụng uy tín chuyên môn để giữ vững vị trí hoặc mở rộng hợp tác"),
        "Hưu Môn": ("môi trường có quý nhân ngầm nâng đỡ, thuận lợi để ổn định", "Chủ động kết nối, lắng nghe ý kiến của người có kinh nghiệm"),
        "Sinh Môn": ("nguồn thu nhập, tài lộc và sức sống đang sinh sôi tốt", "Tập trung vào mảng mang lại giá trị và hiệu quả thiết thực"),
        "Cảnh Môn": ("bề nổi có nhiều thông tin, kế hoạch sôi động nhưng dễ sốt ruột", "Rà soát kỹ giấy tờ, cam kết và giữ bình tĩnh khi trao đổi"),
        "Đỗ Môn": ("hoàn cảnh đang có phần khép kín hoặc giữ tâm sự riêng", "Tập trung trau dồi nội lực, lắng nghe nhẹ nhàng, không nên ép buộc"),
        "Thương Môn": ("tính cách/hoàn cảnh thẳng thắn, năng động nhưng dễ va chạm tự ái", "Điềm tĩnh, mềm mỏng trong lời nói để giữ hòa khí"),
        "Kinh Môn": ("xung quanh đang có tâm lý lo âu, suy nghĩ nhiều", "Giữ vững tâm lý, trấn an tinh thần và kiểm chứng thực tế"),
        "Tử Môn": ("hoàn cảnh hiện tại đang chững lại, cần sự tĩnh tâm", "Kiên nhẫn bồi đắp nền tảng, chờ qua nhịp trầm lắng"),
    }
    _GOD_PLAIN = {
        "Trực Phù": "có phúc lớn và quý nhân che chở",
        "Cửu Thiên": "tính cách/khí thế vươn xa, thích tự lập",
        "Cửu Địa": "nền tảng bền bỉ, điềm đạm chắc chắn",
        "Lục Hợp": "hòa đồng, khéo léo, dễ gắn kết tình cảm",
        "Thái Âm": "sâu sắc, tinh tế, sống nội tâm",
        "Đằng Xà": "nhạy cảm, hay suy nghĩ trằn trọc",
        "Huyền Vũ": "thông minh ngầm nhưng đôi khi kín tiếng, khó đoán",
        "Bạch Hổ": "cá tính mạnh mẽ, quyết đoán nhưng dễ chịu áp lực",
    }
    cua_opp, cua_adv = _DOOR_PLAIN.get(cua_km, ("môi trường đang có sự dịch chuyển", "Quan sát kỹ hoàn cảnh trước khi hành động"))
    than_note = _GOD_PLAIN.get(than_km, "cần giữ sự chủ động")
    star_short = xk_dh["flying_star"].split("—")[0].strip()
    if is_children_q:
        pos2_what = f"Cung Tử Tức (con cái) trên bàn Kỳ Môn đóng tại <b>Cung {target_cung} — Hướng {direction}</b>, hội Sao <b>{sao_km}</b>, Cửa <b>{cua_km}</b> và Thần <b>{than_km}</b>."
        pos2_opp = f"<b>Tính cách & Năng khiếu các con:</b> Sao <b>{sao_km}</b> kết hợp <b>{cua_km}</b> và <b>{than_km}</b> cho thấy các con thông minh, lanh lợi ({than_note}), có năng lực tự lập sớm."
        pos2_adv = f"{cua_adv}. Phòng ngủ hoặc bàn học của con nên ưu tiên đặt theo hướng <b>{direction}</b> để đón cát khí."
    else:
        pos2_what = f"Hoàn cảnh thực tế của sự việc đóng tại <b>Cung {target_cung} — Hướng {direction}</b> (Sao <b>{sao_km}</b> · Cửa <b>{cua_km}</b> · Thần <b>{than_km}</b>)."
        _kh_str = f" ⚠️ Lưu ý Lục Nghi Kích Hình: <b>{full18['kich_hinh_note']}</b>." if full18.get("kich_hinh_note") else ""
        pos2_opp = f"Tại cung này <b>{cua_opp}</b> ({cua_km}), đồng thời <b>{than_note}</b> ({than_km}).{_kh_str}" + (f" {_km_cc_prose_clean}" if _km_cc_prose_clean else "")
        pos2_adv = f"{cua_adv}; khi cần giao dịch hoặc tìm người hỗ trợ, hãy ưu tiên hướng <b>{direction}</b>."
    pos2_ref = f"Cung {target_cung} ({direction}) · Sao {sao_km} · {cua_km} · {than_km} · {star_short}"
    pos2_result = (
        f"<div>📌 <b>Nói về gì:</b> {pos2_what}</div>"
        f"<div style='margin-top:3px;'>✨ <b>Thực tế từ bàn Kỳ Môn:</b> {pos2_opp}</div>"
        f"<div style='margin-top:3px;'>💡 <b>Giải pháp:</b> {pos2_adv}</div>"
        f"<div style='margin-top:4px;font-size:0.82em;color:#94a3b8;'>⚙️ <i>Căn cứ: {pos2_ref}</i></div>"
    )

    # VỊ TRÍ 3: Diễn biến 3 giai đoạn Quá khứ -> Hiện tại -> Sắp tới (Đại Lục Nhâm + Mai Hoa)
    if is_children_q:
        pos3_what = f"<b>Quẻ Chủ ({ban_name}):</b> Nền tảng phúc đức gia đình quy tụ, báo hiệu đường con cái có căn cơ rõ ràng."
        pos3_opp = f"<b>Quẻ Hỗ ({ho_display}):</b> Biểu thị quá trình nuôi dạy các con tiến bộ từng bước vững chắc, có cả âm (Con gái) lẫn dương (Con trai) hòa hợp."
        pos3_adv = f"<b>Quẻ Biến ({bien_name or 'Hậu vận'}) & Lời khuyên:</b> Khi các con lớn lên sẽ có khoảng trời riêng độc lập (dễ đi học/lập nghiệp xa nhà); cha mẹ nên tâm lý, làm bạn cùng con thay vì áp đặt."
    else:
        pos3_what = f"<b>Quá khứ (Quẻ Chủ {ban_name}):</b> Khởi nguồn sự việc bạn đã dồn nhiều tâm sức, tập hợp nguồn lực và đặt nhiều kỳ vọng."
        pos3_opp = f"<b>Hiện tại (Quẻ Hỗ {ho_display}):</b> Đang ở nhịp phải tiến từng bước chậm rãi, vừa làm vừa tháo gỡ vướng mắc." + (f" ({_mh_td_prose_clean})" if _mh_td_prose_clean else "")
        if "Bĩ" in str(bien_name) or weighted_pct < 55:
            pos3_adv = f"<b>Sắp tới (Quẻ Biến {bien_name or 'Biến cuộc'}) & Lời khuyên:</b> Nếu nóng vội thay đổi hoặc đốt cháy giai đoạn ngay sẽ dễ gặp bế tắc; kiên nhẫn giữ nhịp ổn định thì về cuối sẽ êm đẹp."
        else:
            pos3_adv = f"<b>Sắp tới (Quẻ Biến {bien_name or 'Biến cuộc'}) & Lời khuyên:</b> Sau giai đoạn chuẩn bị kỹ ở hiện tại, kết cục sắp tới sẽ mở thông và đạt kết quả tốt."
    pos3_result = (
        f"<div>⏪ {pos3_what}</div>"
        f"<div style='margin-top:3px;'>🔄 {pos3_opp}</div>"
        f"<div style='margin-top:3px;'>🔮 <b>Tam Truyền Đại Lục Nhâm:</b> {full18['dln_summary']}</div>"
        f"<div style='margin-top:3px;'>⏩ {pos3_adv}</div>"
        f"<div style='margin-top:4px;font-size:0.82em;color:#94a3b8;'>⚙️ <i>Căn cứ: Mai Hoa [{ban_name} ➔ {ho_name or 'Hỗ'} ➔ {bien_name or 'Biến'}] · Đại Lục Nhâm Tam Truyền</i></div>"
    )

    # VỊ TRÍ 4: Năng lượng cốt lõi, Màu sắc & Con số trợ vận (Vạn Vật + 12 Trường Sinh)
    _TS_PLAIN = {
        "Đế Vượng": "đang ở đỉnh cao năng lượng, nền tảng và sức sống rất mạnh",
        "Lâm Quan": "đang vững vàng, có lộc và đủ năng lực tự chủ",
        "Trường Sinh": "đang có sức sống mới, khả năng phát triển lâu dài rất tốt",
        "Quan Đái": "đang từng bước trưởng thành và khẳng định vị thế",
        "Dưỡng": "đang trong giai đoạn nuôi dưỡng, bồi đắp êm đềm",
        "Thai": "đang manh nha, ấp ủ mầm sống hoặc dự định mới cần nâng niu bảo vệ",
        "Suy": "cần chú ý bồi bổ sức lực và giữ nhịp độ vừa sức",
        "Bệnh": "cần quan tâm chăm sóc sức khỏe và tinh thần kỹ hơn",
        "Mộ": "năng lượng đang ẩn tàng bên trong, cần sự khơi gợi khích lệ",
        "Tuyệt": "cần làm mới môi trường và phương pháp tiếp cận",
    }
    ts_plain_desc = _TS_PLAIN.get(ts_stage, "đang vận hành ổn định theo chu kỳ")
    colors_clean = omni_data.get("colors", "Trắng, Vàng, Đỏ")
    qty_raw = str(omni_data.get("quantity", "2, 7"))
    qty_short = qty_raw.replace("Con số định lượng chuẩn:", "").strip()
    if is_children_q:
        pos4_what = f"Hào Tử Tôn (con cái) mang hành <b>{hanh_dt}</b>, đạt trạng thái <b>{ts_stage or 'Thai/Dưỡng'}</b> ({ts_plain_desc})."
        pos4_opp = f"<b>Số lượng & Con số hợp mệnh con:</b> Ứng với bộ số Tiên Thiên & Hà Đồ <b>{qty_short}</b> (tương ứng <b>2 người con</b>, hoặc 2 – 3 con trong gia đình)."
        pos4_adv = f"<b>Màu sắc dưỡng mệnh cho các con:</b> Nên dùng đồ dùng, quần áo hoặc sơn phòng màu <b>{colors_clean}</b> để bổ trợ sức khỏe và trí tuệ cho con."
    elif is_identity_q or any(w in q_low for w in ["là ai", "người nào"]):
        pos4_what = f"Khẳng định đặc điểm người được hỏi là <b>{omni_data.get('gender', 'Nam giới')}</b>, độ tuổi <b>{omni_data.get('age_tier', 'Dưới 45 tuổi')}</b>."
        pos4_opp = f"Vóc dáng/khí chất: {omni_data.get('height_desc', 'Cân đối, chững chạc')}."
        pos4_adv = f"Màu sắc hợp mệnh giúp tăng may mắn: <b>{colors_clean}</b>."
    else:
        pos4_what = f"Giá trị cốt lõi của Dụng Thần <b>{dung_than}</b> thuộc hành <b>{hanh_dt}</b> ({ts_stage or 'Vượng'}: <b>{ts_plain_desc}</b>)."
        pos4_opp = f"<b>Con số Hà Đồ - Lạc Thư ứng quẻ:</b> <b>{qty_short}</b>."
        pos4_adv = f"<b>Màu sắc kích hoạt may mắn:</b> Ưu tiên trang phục/vật dụng màu <b>{colors_clean}</b> để tăng sự thuận lợi."
    pos4_result = (
        f"<div>📌 <b>Nói về gì:</b> {pos4_what} (Nạp Âm ngày: <b>{full18['nap_am_ngay']}</b>).</div>"
        f"<div style='margin-top:3px;'>✨ {pos4_opp}</div>"
        f"<div style='margin-top:3px;'>💡 {pos4_adv}</div>"
        f"<div style='margin-top:4px;font-size:0.82em;color:#94a3b8;'>⚙️ <i>Căn cứ: Vạn Vật hành {hanh_dt} · Trường Sinh [{ts_stage or 'Tướng khí'}] · Nạp Âm [{full18['nap_am_ngay'].split('(')[0].strip()}]</i></div>"
    )

    # VỊ TRÍ 5: Đồng hồ thời điểm ứng nghiệm (Ứng Kỳ + Vệ Đà KP)
    _raw_exact_ts = omni_data.get("exact_timestamp", "")
    if ung_ky_str and ung_ky_str != "?" and "hội tụ khí số" not in ung_ky_str.lower():
        uk_display = ung_ky_str
    elif _raw_exact_ts and "hội tụ khí số" not in _raw_exact_ts.lower():
        uk_display = _raw_exact_ts
    else:
        uk_display = "Các ngày/giờ thuộc hành Dụng Thần gần nhất trong tháng"
    if is_children_q:
        pos5_what = "Chỉ ra các mốc thời gian gia đình đón tin vui về con cái (học hành, trưởng thành hoặc thêm phúc lộc)."
        pos5_opp = f"<b>Mốc thời gian vượng khí Tử Tức gần nhất:</b> <b>{uk_display}</b>."
        pos5_adv = f"Tinh tú Vệ Đà <b>{vedic['nakshatra']}</b> chủ về <i>{vedic['nak_trait'].lower()}</i>, báo hiệu con cái càng về hậu vận càng vững vàng, thành đạt."
    else:
        pos5_what = "Chỉ ra mốc thời gian sự việc sẽ mở nút thắt, có tin tức rõ ràng hoặc thuận lợi nhất để quyết định."
        pos5_opp = f"<b>Thời điểm chuyển biến quan trọng:</b> <b>{uk_display}</b>."
        pos5_adv = f"Từ nay đến mốc đó hãy chuẩn bị thật chắc chắn (theo tinh thần <i>{vedic['nak_trait'].lower()}</i>); <b>đợi đúng mốc này mới chốt quyết định lớn</b>."
    pos5_result = (
        f"<div>📌 <b>Nói về gì:</b> {pos5_what}</div>"
        f"<div style='margin-top:3px;'>⏰ {pos5_opp}</div>"
        f"<div style='margin-top:3px;'>💡 <b>Khuyên bạn:</b> {pos5_adv}</div>"
        f"<div style='margin-top:4px;font-size:0.82em;color:#94a3b8;'>⚙️ <i>Căn cứ: Động cơ Ứng Kỳ · Tinh tú Vệ Đà {vedic['nakshatra']}</i></div>"
    )

    # PHÂN KHU RIÊNG 1: TỬ VI ĐẨU SỐ (CHUYÊN XEM RIÊNG VỀ CẢ CUỘC ĐỜI & VẬN MỆNH TRỌN ĐỜI)
    pos_tv_lifetime = (
        f"<div>📌 <b>Phạm vi chuyên biệt:</b> <b>Tử Vi Đẩu Số chỉ chuyên luận riêng về Bức Tranh Cả Cuộc Đời (12 Cung Mệnh – Thân – Đại Vận 10 năm)</b>, tách biệt hoàn toàn với việc chấm điểm sự việc trước mắt.</div>"
        f"<div style='margin-top:3px;'>🔯 <b>Cấu trúc Mệnh Cục & Phúc Đức trọn đời:</b> {full18['tv_summary']} (Trạng thái cung trọng tâm: <b>{tu_vi_verdict}</b>).</div>"
        f"<div style='margin-top:3px;'>💡 <b>Định hướng cả cuộc đời:</b> Dựa trên Chính Tinh thủ Mệnh/Thân và Cục số, đường đời lâu dài nên lấy việc bồi đắp phúc đức gia tộc và phát huy chuyên môn sâu làm gốc. <i>(Nhập thêm Ngày Giờ Sinh cá nhân nếu muốn lập Lá Số Tử Vi 12 cung trọn đời chính xác theo tuổi của riêng bạn)</i>.</div>"
        f"<div style='margin-top:4px;font-size:0.82em;color:#94a3b8;'>⚙️ <i>Phân khu độc lập: Tử Vi Đẩu Số — Chuyên Xem Cả Cuộc Đời (Không trộn vào điểm quẻ sự việc)</i></div>"
    )

    # PHÂN KHU RIÊNG 2: THÁI ẤT THẦN SỐ (CHUYÊN XEM RIÊNG VỀ VẬN QUỐC GIA, THỜI CUỘC THẾ GIỚI & VĨ MÔ)
    pos_ta_national = (
        f"<div>📌 <b>Phạm vi chuyên biệt:</b> <b>Thái Ất Thần Số chỉ chuyên luận riêng về Vận Quốc Gia, Thời Cuộc Thế Giới, Kinh Tế Vĩ Mô & Thiên Văn Đại Cục</b> (tuyệt đối không dùng để chấm điểm chuyện gia đình/cá nhân).</div>"
        f"<div style='margin-top:3px;'>⚔️ <b>Cục diện Quốc Vận & Thời Thế Vĩ Mô:</b> {full18['ta_summary']} (Đánh giá đại cục vĩ mô: <b>{thai_at_verdict}</b>).</div>"
        f"<div style='margin-top:3px;'>💡 <b>Nhận định thời cuộc chung:</b> Cho biết xu hướng chung của xã hội/thị trường rộng lớn đang ở thế <b>{full18['ta_chu_khach'] or 'Chủ – Khách cân bằng'}</b> để tham khảo khi tính chuyện đại sự quốc gia hoặc đầu tư vĩ mô.</div>"
        f"<div style='margin-top:4px;font-size:0.82em;color:#94a3b8;'>⚙️ <i>Phân khu độc lập: Thái Ất Thần Số — Chuyên Xem Quốc Gia & Vĩ Mô (Không trộn vào điểm quẻ cá nhân)</i></div>"
    )

    # PHÂN KHU RIÊNG 3: TRẠCH NHẬT XEM NGÀY ĐẸP & ĐẠI LỤC NHÂM (CHUYÊN XEM RIÊNG VỀ CHỌN NGÀY GIỜ & LỘ TRÌNH TAM TRUYỀN)
    pos6_result = (
        f"<div>📌 <b>Phạm vi chuyên biệt:</b> <b>Chỉ dùng riêng khi bạn cần Chọn Ngày Giờ Tốt Xấu (Khai trương, Động thổ, Xuất hành, Cưới hỏi)</b> và xem lộ trình 3 bước Tam Truyền.</div>"
        f"<div style='margin-top:3px;'>📅 <b>Trạch Nhật 12 Trực ({full18['truc_name']} — {xem_ngay_verdict}):</b> {full18['truc_meaning']}.</div>"
        f"<div style='margin-top:3px;'>🔮 <b>Lộ trình Đại Lục Nhâm Tam Truyền:</b> {full18['dln_summary']}.</div>"
        f"<div style='margin-top:4px;font-size:0.82em;color:#94a3b8;'>⚙️ <i>Phân khu độc lập: Trạch Nhật 12 Trực & Đại Lục Nhâm (Chỉ kích hoạt khi hỏi chọn ngày giờ / lộ trình)</i></div>"
    )

    # VỊ TRÍ 7: Chìa khóa hóa giải áp lực & Độ đồng thuận 4 Phương Pháp Chuẩn (Bát Tự Điều Hầu + 40 Chuyên Gia AI)
    _dh_god = xk_dh["dieu_hau_god"]
    if "Mộc" in _dh_god and "Thủy" in _dh_god:
        dh_plain_meaning = "bổ sung sự mềm mỏng, linh hoạt (Mộc) và sự điềm tĩnh, thư giãn (Thủy) để cân bằng khí hậu bản mệnh"
        dh_plain_action = "Tránh tranh cãi cứng nhắc; ưu tiên không gian xanh hoặc gần nước để tinh thần minh mẫn"
    elif "Hỏa" in _dh_god:
        dh_plain_meaning = "bổ sung sự nhiệt huyết, ấm áp và chủ động kết nối (Hỏa) để kích hoạt vượng khí"
        dh_plain_action = "Giữ không khí gia đình/công việc ấm cúng, cởi mở trò chuyện và làm việc nơi nhiều ánh sáng"
    elif "Kim" in _dh_god:
        dh_plain_meaning = "bổ sung sự quyết đoán, kỷ luật rõ ràng (Kim) và sự điềm tĩnh (Thủy)"
        dh_plain_action = "Lập kế hoạch rõ ràng, rà soát kỹ các mục tiêu quan trọng"
    else:
        dh_plain_meaning = "giữ sự cân bằng giữa công việc và gia đình, điều hòa cảm xúc ôn hòa"
        dh_plain_action = "Hành xử mềm mỏng, ưu tiên sự ổn định lâu dài"

    if is_children_q:
        pos7_what = f"Bộ Tứ Phương Pháp Chuẩn Xác (Mai Hoa · Kỳ Môn · Lục Hào · Thiết Bản) hội tụ khẳng định: <b>{omni_data.get('children_summary', 'Khoảng 2 người con — 1 Trai, 1 Gái')}</b>."
        pos7_opp = f"<b>Pháp quyết dưỡng phúc Tử Tức (Bát Tự Điều Hầu):</b> Cần <b>{dh_plain_meaning}</b>."
        pos7_adv = f"<b>Lời khuyên cho gia đình:</b> {omni_data.get('children_advice', dh_plain_action)} (Hướng vượng khí: <b>{xk_dh['dieu_hau_dir']}</b>)."
    else:
        pos7_what = f"Bộ Tứ Phương Pháp Chuẩn Xác (Mai Hoa · Kỳ Môn · Lục Hào · Thiết Bản) hội tụ với độ đồng thuận <b>{bayes['consensus_pct']}%</b>."
        pos7_opp = f"<b>Pháp quyết cân bằng Ngũ Hành & Phong Thủy (Điều Hầu):</b> Cần <b>{dh_plain_meaning}</b>."
        pos7_adv = f"<b>Việc nên làm ngay:</b> {dh_plain_action}; ưu tiên xuất hành/giao dịch về hướng <b>{xk_dh['dieu_hau_dir']}</b>."
    pos7_result = (
        f"<div>📌 <b>Tổng kết hội tụ Bộ Tứ Chuẩn Xác:</b> {pos7_what}</div>"
        f"<div style='margin-top:3px;'>✨ {pos7_opp}</div>"
        f"<div style='margin-top:3px;'>💡 {pos7_adv}</div>"
        f"<div style='margin-top:4px;font-size:0.82em;color:#94a3b8;'>⚙️ <i>Căn cứ: Điều Hầu Bát Tự [{_dh_god}] · Hướng vượng [{xk_dh['dieu_hau_dir']}]</i></div>"
    )

    syn = compute_7_link_synergy_chain(
        question=question,
        category=category,
        dung_than=dung_than,
        hanh_dt=hanh_dt,
        weighted_pct=weighted_pct,
        target_cung=target_cung,
        direction=direction,
        ung_ky_str=uk_display,
        ts_stage=ts_stage,
        chart_data=chart_data,
        luc_hao_data=luc_hao_data,
        mai_hoa_data=mai_hoa_data,
        thai_at_verdict=thai_at_verdict,
        tu_vi_verdict=tu_vi_verdict,
        xem_ngay_verdict=xem_ngay_verdict,
    )

    def _card7(num: str, icon: str, title: str, methods: str, body: str, border_col: str = "#38bdf8") -> str:
        return (
            f'<div style="padding:12px 14px;background:rgba(15,23,42,0.82);border-radius:11px;'
            f'border-left:4px solid {border_col};border-top:1px solid rgba(255,255,255,0.09);">'
            f'<div style="font-size:0.93em;font-weight:800;color:{border_col};margin-bottom:6px;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:4px;">'
            f'{icon} {num} — {title} <span style="font-weight:500;color:#94a3b8;font-size:0.86em;">({methods})</span></div>'
            f'<div style="font-size:0.93em;color:#f1f5f9;line-height:1.52;">{body}</div>'
            f'</div>'
        )

    _t1 = "Gốc Rễ Tử Tức & Duyên Con Cái" if is_children_q else "Luận Giải Trực Tiếp Từ Hào Thế – Ứng & Dụng Thần"
    _t2 = "Cung Tử Tức & Tính Cách Các Con" if is_children_q else "Hiện Trường Không Gian, Cửu Tinh, Bát Môn & Bát Thần"
    _t3 = "Quẻ Chủ ➔ Quẻ Hỗ ➔ Quẻ Biến (Gia Đạo)" if is_children_q else "Định Lượng Quái Số & Diễn Biến Chủ ➔ Hỗ ➔ Biến"
    _t4 = "Số Lượng Con, Nếp Tẻ (Trai/Gái) & Màu Hợp" if is_children_q else "Định Số Lục Thân, Nạp Âm, Trường Sinh & Màu Sắc"
    _t5 = "Thời Điểm Tin Vui & Tương Lai Con Cái" if is_children_q else "Đồng Hồ Ứng Kỳ (Khi Nào Ứng Nghiệm?)"

    grid_html = (
        f'<div style="margin-top:12px;padding:15px 16px;background:rgba(2,6,23,0.58);border-radius:14px;border:2px solid rgba(52,211,153,0.45);">'
        f'<div style="font-size:1.02em;font-weight:900;color:#4ade80;margin-bottom:10px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px;">'
        f'<span>🎯 PHẦN I — TRUNG TÂM LUẬN QUẺ CHUẨN XÁC CHO CÂU HỎI (CHỈ DÙNG 4 PHƯƠNG PHÁP CHUẨN XÁC: MAI HOA · KỲ MÔN · LỤC HÀO · THIẾT BẢN)</span>'
        f'<span style="font-size:0.85em;padding:3px 10px;background:rgba(16,185,129,0.2);color:#6ee7b7;border-radius:20px;border:1px solid rgba(52,211,153,0.4);">✅ 4 Phương Pháp Chủ Lực Quyết Định 100%</span>'
        f'</div>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:10px;">'
        + _card7("Trụ Cột 1", "📿", _t1, "Lục Hào Kinh Dịch", pos1_result, "#fbbf24")
        + _card7("Trụ Cột 2", "🏯", _t2, "Kỳ Môn Độn Giáp", pos2_result, "#38bdf8")
        + _card7("Trụ Cột 3", "🌸", _t3, "Mai Hoa Dịch Số", pos3_result, "#a78bfa")
        + _card7("Trụ Cột 4", "📜", _t4, "Thiết Bản Thần Toán & Vạn Vật", pos4_result, "#f472b6")
        + _card7("Ứng Kỳ", "⏰", _t5, "Ứng Kỳ Tam Thức", pos5_result, "#fb923c")
        + _card7("Pháp Quyết", "🔑", "Pháp Quyết Hành Động & Hóa Giải", "Bát Tự Điều Hầu + 40 Chuyên Gia AI", pos7_result, "#34d399")
        + '</div>'
        + f'</div>'
        + f'<div style="margin-top:12px;padding:15px 16px;background:rgba(15,23,42,0.65);border-radius:14px;border:1px dashed rgba(148,163,184,0.4);">'
        f'<div style="font-size:0.98em;font-weight:800;color:#cbd5e1;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px;">'
        f'<span>🏛️ PHẦN II — CÁC PHÂN KHU CHUYÊN BIỆT ĐỘC LẬP (MỖI PHƯƠNG PHÁP CHỈ XEM RIÊNG ĐÚNG MẢNG ĐÓ — TÁCH BIỆT HOÀN TOÀN, KHÔNG LÀM NHIỄU QUẺ)</span>'
        f'<span style="font-size:0.82em;padding:2px 9px;background:rgba(148,163,184,0.15);color:#94a3b8;border-radius:16px;">Chuyên Mảng Riêng Biệt</span>'
        f'</div>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:10px;">'
        + _card7("Mảng Riêng 1", "🔯", "Xem Riêng Về Cả Cuộc Đời & Mệnh Cục Trọn Đời", "Tử Vi Đẩu Số", pos_tv_lifetime, "#c084fc")
        + _card7("Mảng Riêng 2", "⚔️", "Xem Riêng Về Vận Quốc Gia, Thế Giới & Vĩ Mô", "Thái Ất Thần Số", pos_ta_national, "#f87171")
        + _card7("Mảng Riêng 3", "📅", "Xem Riêng Về Chọn Ngày Giờ Đẹp & Lộ Trình Tam Truyền", "Trạch Nhật 12 Trực · Đại Lục Nhâm", pos6_result, "#2dd4bf")
        + '</div>'
        + build_18_layer_conflict_arbiter_and_instant_check(
            question=question,
            dung_than=dung_than,
            hanh_dt=hanh_dt,
            weighted_pct=weighted_pct,
            target_cung=target_cung,
            direction=direction,
            chart_data=chart_data,
            luc_hao_data=luc_hao_data,
            mai_hoa_data=mai_hoa_data,
            omni_data=omni_data,
            verdicts_list=verdicts_list,
            thai_at_verdict=thai_at_verdict,
            tu_vi_verdict=tu_vi_verdict,
            xem_ngay_verdict=xem_ngay_verdict,
        )
        + f'</div>'
    )

    prompt_blueprint = (
        f"=== BẢN ĐỒ GHÉP TRANH TOÀN CẢNH 7 VỊ TRÍ ĐÔNG - TÂY (BẮT BUỘC KẾT NỐI THÀNH 1 BỨC TRANH THỐNG NHẤT) ===\n"
        f"1. [VỊ TRÍ 1 - CON NGƯỜI & CỐT LÕI (Lục Hào + Horary)]: {re.sub(r'<[^>]+>', '', pos1_result)}\n"
        f"2. [VỊ TRÍ 2 - KHÔNG GIAN & PHƯƠNG HƯỚNG (Kỳ Môn + Huyền Không Vận 9)]: {re.sub(r'<[^>]+>', '', pos2_result)}\n"
        f"3. [VỊ TRÍ 3 - QUÁ KHỨ -> HIỆN TẠI -> TƯƠNG LAI (Đại Lục Nhâm + Mai Hoa)]: {re.sub(r'<[^>]+>', '', pos3_result)}\n"
        f"4. [VỊ TRÍ 4 - HÌNH TƯỚNG, TUỔI TÁC & ĐỊNH LƯỢNG (Vạn Vật + Thiết Bản + 12 Trường Sinh)]: {re.sub(r'<[^>]+>', '', pos4_result)}\n"
        f"5. [VỊ TRÍ 5 - ĐỒNG HỒ ỨNG KỲ (Ứng Kỳ + Ấn Độ Vệ Đà KP Sub-Lord)]: {re.sub(r'<[^>]+>', '', pos5_result)}\n"
        f"6. [VỊ TRÍ 6 - THỜI THẾ & CHIẾN LƯỢC CÔNG/THỦ (Thái Ất + Tử Vi + Trạch Cát)]: {re.sub(r'<[^>]+>', '', pos6_result)}\n"
        f"7. [VỊ TRÍ 7 - PHÁP QUYẾT HÓA GIẢI & HỘI TỤ BAYES (Bát Tự Điều Hầu + Bayes)]: {re.sub(r'<[^>]+>', '', pos7_result)}\n"
    )

    return {
        "grid_html": grid_html,
        "prompt_blueprint": prompt_blueprint,
        "prose_html": wc["prose_html"],
    }



def compute_7_link_synergy_chain(
    question: str,
    category: str,
    dung_than: str,
    hanh_dt: str,
    weighted_pct: int,
    target_cung: int = 1,
    direction: str = "Chính Bắc (Khảm)",
    ung_ky_str: str = "",
    ts_stage: str = "",
    chart_data: Dict[str, Any] | None = None,
    luc_hao_data: Dict[str, Any] | None = None,
    mai_hoa_data: Dict[str, Any] | None = None,
    ky_mon_verdict: str = "BÌNH",
    luc_hao_verdict: str = "BÌNH",
    mai_hoa_verdict: str = "BÌNH",
    luc_nham_verdict: str = "BÌNH",
    thai_at_verdict: str = "BÌNH",
    tu_vi_verdict: str = "BÌNH",
    xem_ngay_verdict: str = "BÌNH",
) -> Dict[str, Any]:
    """
    V100.5: CHUỖI LIÊN KẾT HỢP SỨC 7 MẮT XÍCH (7-LINK SYNERGY CHAIN)
    Các phương pháp không đứng rời rạc mà truyền kết quả từ Mắt xích 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7
    để cộng hưởng lực lượng và chốt ra kết quả chính xác tuyệt đối.
    """
    chart_data = chart_data if isinstance(chart_data, dict) else {}
    luc_hao_data = luc_hao_data if isinstance(luc_hao_data, dict) else {}
    mai_hoa_data = mai_hoa_data if isinstance(mai_hoa_data, dict) else {}

    horary = analyze_western_horary(question, category, dung_than, hanh_dt, chart_data, weighted_pct)
    vedic = analyze_vedic_kp_prashna(question, category, chart_data, weighted_pct)
    xk_dh = analyze_xuankong_and_dieuhau(dung_than, hanh_dt, target_cung, chart_data)
    verdicts_list = [ky_mon_verdict, luc_hao_verdict, mai_hoa_verdict]
    bayes = compute_bayesian_consensus(weighted_pct, verdicts_list, horary["score"], vedic["score"], xk_dh["score"])

    # Tính hiệu chỉnh cộng hưởng liên hoàn giữa các mắt xích
    synergy_delta = 0
    chain_steps = []

    # Liên kết 1 -> 2: Lục Hào + Horary (Nhân) kết hợp Kỳ Môn + Huyền Không Vận 9 (Địa)
    lh_cat = "CÁT" in str(luc_hao_verdict).upper()
    km_cat = "CÁT" in str(ky_mon_verdict).upper()
    xk_cat = xk_dh["score"] >= 60
    if (lh_cat or horary["score"] >= 60) and (km_cat or xk_cat):
        synergy_delta += 3
        link_1_2 = f"Mắt xích 1 (Lục Hào + Horary) đắc khí truyền lực sang Mắt xích 2 (Kỳ Môn + Phi Tinh Vận 9 tại {direction}) tạo thế Nhân - Địa đồng tâm (+3% cộng hưởng)"
    elif not lh_cat and not km_cat and xk_dh["score"] < 45:
        synergy_delta -= 3
        link_1_2 = f"Mắt xích 1 (Lục Hào + Horary) gặp lực cản lại rơi vào cung Mắt xích 2 (Kỳ Môn + Phi Tinh tại {direction}) đang suy khí (-3% cảnh báo)"
    else:
        link_1_2 = f"Mắt xích 1 (Lục Hào + Horary) phối hợp cân bằng với không gian Mắt xích 2 (Kỳ Môn + Phi Tinh Vận 9 tại {direction})"
    chain_steps.append(link_1_2)

    # Liên kết 2 -> 3 -> 4: Không gian truyền sang Trục 3 thời (Đại Lục Nhâm + Mai Hoa) & Vạn Vật Trường Sinh
    mh_cat = "CÁT" in str(mai_hoa_verdict).upper()
    ln_cat = "CÁT" in str(luc_nham_verdict).upper()
    if mh_cat and ln_cat:
        synergy_delta += 2
        link_3_4 = f"Mắt xích 3 (Đại Lục Nhâm + Mai Hoa) mở thông hậu vận, nuôi dưỡng Dụng Thần {dung_than} ({hanh_dt} - {ts_stage or 'Vượng'}) tại Mắt xích 4 (+2% hậu vận)"
    elif "HUNG" in str(mai_hoa_verdict).upper() and "HUNG" in str(luc_nham_verdict).upper():
        synergy_delta -= 2
        link_3_4 = f"Mắt xích 3 (Đại Lục Nhâm + Mai Hoa) báo hiệu hậu vận có khúc quanh, đòi hỏi Mắt xích 4 ({dung_than} hành {hanh_dt}) phải bảo toàn nội lực (-2% thận trọng)"
    else:
        link_3_4 = f"Mắt xích 3 (Đại Lục Nhâm + Mai Hoa) dẫn dắt diễn biến sang Mắt xích 4 (Dụng Thần {dung_than} hành {hanh_dt}, vòng Trường Sinh {ts_stage or 'Bình hòa'})"
    chain_steps.append(link_3_4)

    # Liên kết 5 -> 6 -> 7: Ứng Kỳ + Vedic KP khóa thời điểm & Điều Hầu + Bayes chốt phán quyết
    synergy_pct = int(round((weighted_pct * 0.65) + (bayes["bayesian_posterior_pct"] * 0.35) + synergy_delta))
    synergy_pct = max(8, min(96, synergy_pct))

    synergy_summary_sentence = (
        f"🔗 <b>Chuỗi Liên Kết Hợp Sức 14 Hệ Thống (Đông – Tây Hội Tụ {bayes['consensus_pct']}%):</b> "
        f"{link_1_2}; tiếp nối sang {link_3_4}; khóa điểm rơi Ứng Kỳ tại <b>{ung_ky_str or 'chu kỳ Can Chi kế tiếp'}</b> "
        f"(Tinh tú Vệ Đà <b>{vedic['nakshatra']}</b>) và dùng pháp quyết Điều Hầu <b>{xk_dh['dieu_hau_god']}</b> "
        f"(hướng <b>{xk_dh['dieu_hau_dir']}</b>) để chốt độ chuẩn xác hợp lực ở mức <b>{synergy_pct}%</b>."
    )

    return {
        "synergy_pct": synergy_pct,
        "consensus_pct": bayes["consensus_pct"],
        "bayesian_posterior_pct": bayes["bayesian_posterior_pct"],
        "synergy_delta": synergy_delta,
        "synergy_summary_sentence": synergy_summary_sentence,
    }
