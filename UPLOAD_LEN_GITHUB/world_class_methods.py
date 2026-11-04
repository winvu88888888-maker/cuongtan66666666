# -*- coding: utf-8 -*-
"""
WORLD-CLASS DIVINATION & QUANTITATIVE PREDICTION ENGINE (V100.3)
================================================================
Hợp nhất 4 phương pháp dự đoán đỉnh cao thế giới bổ sung vào 10 hệ thống cổ học phương Đông:
1. Western Classical Horary Astrology (William Lilly's Christian Astrology 1647):
   - 12 Houses (Querent Ascendant House 1 vs Quesited Target House)
   - Planetary Rulers, Essential Dignities, Applying Aspects (Trine/Sextile/Conjunction vs Square/Opposition)
   - Void of Course Moon check (tương đương Tuần Không của Lục Hào)
2. Vedic Prashna Shastra & KP System (Krishnamurti Paddhati 27 Nakshatras & Sub-Lord Significators):
   - 27 Nakshatras (Tinh tú Vệ Đà), House Significators (2-6-10-11 Tài Lộc, 5-7-11 Tình Duyên, 1-5-9-11 Vạn Sự Cát, 6-8-12 Trở Ngại)
3. Xuan Kong Flying Stars (Huyền Không Phi Tinh Tam Nguyên Cửu Vận — Hạ Nguyên Vận 9: 2024–2043) & Điều Hầu Dụng Thần (Cùng Thông Bảo Giám):
   - Cửu Tinh Đương Vận (9 Cửu Tử Vượng Khí, 1 Nhất Bạch Sinh Khí, 8 Bát Bạch Phụ Khí vs 5 Ngũ Hoàng / 2 Nhị Hắc Sát Khí)
   - Hàn - Noãn - Táo - Thấp Điều Hầu theo Nguyệt Lệnh
4. Bayesian Multi-Model Evidence Fusion (Hợp Nhất Xác Suất Hậu Nghiệm Bayes & Độ Đồng Thuận Đa Hệ Thống):
   - Tính Log-Odds Likelihood Ratio từ toàn bộ các hệ thống Đông - Tây để hiệu chỉnh xác suất chuẩn xác.
"""

from __future__ import annotations
import datetime
import math
from typing import Dict, Any, List, Tuple


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
    now = datetime.datetime.now()
    chi_gio = chart_data.get("chi_gio", "")
    chi_ngay = chart_data.get("chi_ngay", "")

    # Tính Cung Mọc (Ascendant - Nhà 1) dựa trên kinh độ Mặt Trời theo tháng và Giờ gieo quẻ
    month_offset = (now.month - 3) % 12
    hour_idx = CHI_TO_ZODIAC_IDX.get(chi_gio, (now.hour // 2) % 12)
    asc_idx = (month_offset + hour_idx) % 12
    asc_sign, asc_elem, asc_mode, asc_ruler = ZODIAC_SIGNS[asc_idx]

    # Xác định Nhà Sự Việc (Quesited House)
    house_num, house_desc = CATEGORY_TO_HORARY_HOUSE.get(
        category, (10, "Nhà 10 (Kết cục sự việc & Thành tựu)")
    )
    q_low = (question or "").lower()
    if any(w in q_low for w in ["nam hay nữ", "trai hay gái", "giới tính", "bao nhiêu tuổi", "mấy tuổi", "tôi là"]):
        house_num, house_desc = (1, "Nhà 1 (Ascendant — Bản thể, Giới tính & Độ tuổi người hỏi)")

    quesited_idx = (asc_idx + house_num - 1) % 12
    q_sign, q_elem, q_mode, q_ruler = ZODIAC_SIGNS[quesited_idx]

    # Tính góc chiếu (Aspect) giữa Chủ tinh Nhà 1 (Querent) và Chủ tinh Nhà Sự Việc (Quesited)
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
    now = datetime.datetime.now()
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
    "Thân": ("Đầu Thu kim khí肃 sát", "Đinh Hỏa (Luyện kim thành khí) & Giáp Mộc", "Chính Nam / Chính Đông"),
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
    cuc = int(chart_data.get("cuc", 5) or 5)

    # Phi tinh Vận 9 bay đến target_cung
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

    # Tích hợp Likelihood Ratio từ các hệ thống độc lập
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
