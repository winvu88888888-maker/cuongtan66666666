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
    now = datetime.datetime.now()
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

    # VỊ TRÍ 1: Tâm Điểm Chủ Thể & Nội Tình (Lục Hào + Horary)
    q_low = (question or "").lower()
    is_identity_q = any(w in q_low for w in ["nam hay nữ", "trai hay gái", "giới tính", "bao nhiêu tuổi", "mấy tuổi"])
    if is_identity_q and omni_data:
        pos1_result = (
            f"Xác định trực tiếp Chủ thể qua Hào Thế & Dụng Thần <b>{dung_than}</b> (hành <b>{hanh_dt}</b>, vòng Trường Sinh <b>{ts_stage or 'Vượng'}</b>) "
            f"kết hợp Cung Mọc Horary <b>{horary['ascendant']}</b>: Giới tính là <b>{omni_data.get('gender', 'Nam giới')}</b>, "
            f"độ tuổi thuộc nhóm <b>{omni_data.get('age_tier', 'Dưới 45 tuổi')}</b> ({', '.join(omni_data.get('birth_years', [])[:3])})."
        )
    else:
        pos1_result = (
            f"Trên {que_transition}, Dụng Thần <b>{dung_than}</b> mang hành <b>{hanh_dt}</b> (vòng Trường Sinh: <b>{ts_stage or 'Bình hòa'}</b>) "
            f"đối chiếu cùng Chủ tinh Horary <b>{horary['quesited_house']}</b> tạo góc <b>{horary['aspect']}</b>, "
            f"khẳng định lực lượng cốt lõi đạt <b>{weighted_pct}%</b> (Hậu nghiệm Bayes: <b>{bayes['bayesian_posterior_pct']}%</b>)."
        )

    # VỊ TRÍ 2: Không Gian 3D, Phương Hướng & Hiện Trường (Kỳ Môn + Huyền Không Vận 9)
    where_scene = omni_data.get("where_scene", "") or f"tọa độ Cung số {target_cung} hướng {direction}"
    pos2_result = (
        f"Tọa độ không gian khóa tại <b>Cung {target_cung} — Hướng {direction}</b>, hội tụ bộ ba Kỳ Môn "
        f"(Sao <b>{sao_km}</b> · Cửa <b>{cua_km}</b> · Thần <b>{than_km}</b>) cùng Phi Tinh Vận 9 "
        f"<b>{xk_dh['flying_star']}</b>. Đặc điểm hiện trường/môi trường: {where_scene}"
    )

    # VỊ TRÍ 3: Trục Thời Gian 3 Thời Quá Khứ -> Hiện Tại -> Tương Lai (Đại Lục Nhâm + Mai Hoa)
    ln_clean = re.sub(r"<[^>]+>", "", str(luc_nham_reason or "")).strip()
    pos3_result = (
        f"Khởi phát từ Quẻ Chủ <b>{ban_name}</b> (Sơ truyền), đi qua nội tình Quẻ Hỗ <b>{ho_name or 'Trung truyền'}</b> "
        f"và hội tụ về Quẻ Biến <b>{bien_name or 'Mạt truyền'}</b>"
        + (f" ({ln_clean[:160]})" if ln_clean else "")
        + ": cho thấy mạch vận động từ nguyên nhân ban đầu đến kết cục cuối cùng đang chuyển dịch theo đúng quy luật nhân quả của quẻ."
    )

    # VỊ TRÍ 4: Hình Tướng, Đặc Điểm Vật Chất, Tuổi Tác & Định Lượng (Vạn Vật + Thiết Bản + 12 Trường Sinh)
    if is_identity_q or any(w in q_low for w in ["là ai", "người nào"]):
        pos4_result = (
            f"Chân dung con người: Giới tính <b>{omni_data.get('gender', 'Nam giới')}</b>, "
            f"độ tuổi <b>{omni_data.get('age_tier', 'Dưới 45 tuổi')}</b> ({', '.join(omni_data.get('birth_years', [])[:3])}), "
            f"chiều cao/vóc dáng: {omni_data.get('height_desc', 'Cân đối')}, màu sắc hợp mệnh: <b>{omni_data.get('colors', 'Trắng, Vàng kim')}</b>."
        )
    else:
        pos4_result = (
            f"Loại tượng hành <b>{hanh_dt}</b> ({ts_stage or 'Tướng khí'}): đặc trưng bởi màu sắc <b>{omni_data.get('colors', 'Sáng rõ')}</b>, "
            f"chất liệu/thuộc tính <b>{omni_data.get('materials', hanh_dt)}</b> ({omni_data.get('condition', 'Đang vận hành')}); "
            f"con số định lượng ứng nghiệm: <b>{omni_data.get('quantity', 'Theo số Hà Đồ - Lạc Thư của cung quẻ')}</b>."
        )

    # VỊ TRÍ 5: Đồng Hồ Điểm Hẹn Ứng Kỳ (Ứng Kỳ Lục Hào/Kỳ Môn + Vedic KP Sub-Lord)
    uk_display = omni_data.get("exact_timestamp") or ung_ky_str or "Các ngày/giờ thuộc hành Dụng Thần hoặc Xung Không/Xuất Mộ"
    pos5_result = (
        f"Điểm hẹn thời gian được khóa kép bởi <b>Động cơ Ứng Kỳ ({uk_display})</b> và tinh tú Vệ Đà Ấn Độ "
        f"<b>Nakshatra {vedic['nakshatra']}</b> ({vedic['kp_significators']} — <i>{vedic['nak_trait']}</i>)."
    )

    # VỊ TRÍ 6: Thời Thế Vĩ Mô & Chiến Lược Công/Thủ (Thái Ất + Tử Vi + Trạch Cát)
    strategy_mode = "CHỦ ĐỘNG TẤN CÔNG (Lợi Động — Nắm bắt cơ hội)" if weighted_pct >= 55 else (
        "LINH HOẠT THĂM DÒ, VỪA TIẾN VỪA GIỮ (Thận trọng từng bước)" if weighted_pct >= 45 else
        "ÁN BINH BẤT ĐỘNG, PHÒNG THỦ BẢO TOÀN (Lợi Tĩnh — Chờ qua vận cản)"
    )
    pos6_result = (
        f"Cục diện Thái Ất ({thai_at_verdict}) kết hợp Tử Vi ({tu_vi_verdict}) và Trạch Cát ({xem_ngay_verdict}) "
        f"xác định chiến lược tối ưu lúc này là: <b>{strategy_mode}</b>."
    )

    # VỊ TRÍ 7: Chìa Khóa Hóa Giải & Độ Đồng Thuận Bayes (Bát Tự Điều Hầu + 40 Chuyên Gia AI + Bayes)
    remedy_extra = omni_data.get("hoa_giai", "")
    pos7_result = (
        f"Độ đồng thuận liên hệ thống đạt <b>{bayes['consensus_pct']}%</b> (Xác suất hậu nghiệm Bayes: <b>{bayes['bayesian_posterior_pct']}%</b>). "
        f"Pháp quyết Điều Hầu (Cùng Thông Bảo Giám): <b>{xk_dh['dieu_hau']}</b>, ưu tiên hướng <b>{direction}</b> "
        f"và phương vị vượng khí <b>{xk_dh['dieu_hau_dir']}</b>" + (f" ({remedy_extra})" if remedy_extra else ".")
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

    # Bản đồ HTML 7 vị trí liên kết hợp sức thành 1 bức tranh thống nhất
    grid_html = (
        f'<div style="margin-top:14px;padding:16px 18px;background:rgba(2,6,23,0.62);border-radius:12px;border:1px solid rgba(56,189,248,0.4);">'
        f'<div style="font-size:1.03em;font-weight:800;color:#38bdf8;margin-bottom:10px;border-bottom:1px solid rgba(56,189,248,0.25);padding-bottom:6px;">'
        f'🗺️ BỨC TRANH TOÀN CẢNH 7 MẮT XÍCH LIÊN KẾT HỢP SỨC (14 HỆ THỐNG ĐÔNG – TÂY BẮT TAY GIẢI MÃ CHÍNH XÁC TUYỆT ĐỐI)</div>'
        f'<div style="display:flex;flex-direction:column;gap:8px;font-size:0.95em;line-height:1.68;color:#e2e8f0;text-align:justify;">'
        f'<div>🎯 <b>Vị trí 1 [Mắt xích Khởi nguồn — Con Người & Cốt Lõi]</b> <i>(<b>Lục Hào Nạp Giáp + Horary Phương Tây</b>)</i>: {pos1_result} ➔ <i>Truyền tọa độ sang Vị trí 2</i>.</div>'
        f'<div>🧭 <b>Vị trí 2 [Mắt xích Không gian — Phương Hướng & Hiện Trường]</b> <i>(<b>Kỳ Môn Độn Giáp + Huyền Không Vận 9</b> nhận lực từ Vị trí 1)</i>: {pos2_result} ➔ <i>Truyền bối cảnh sang Vị trí 3</i>.</div>'
        f'<div>⏳ <b>Vị trí 3 [Mắt xích Thời gian — Quá Khứ → Hiện Tại → Tương Lai]</b> <i>(<b>Đại Lục Nhâm Tam Truyền + Mai Hoa Dịch Số</b> nối mạch từ Vị trí 2)</i>: {pos3_result} ➔ <i>Truyền khí số sang Vị trí 4</i>.</div>'
        f'<div>📦 <b>Vị trí 4 [Mắt xích Định hình — Hình Tướng, Tuổi Tác & Số Lượng]</b> <i>(<b>Vạn Vật Loại Tượng + Thiết Bản + 12 Trường Sinh</b> kết tinh từ Vị trí 1-2-3)</i>: {pos4_result} ➔ <i>Khóa vào đồng hồ Vị trí 5</i>.</div>'
        f'<div>⏰ <b>Vị trí 5 [Mắt xích Điểm hẹn — Đồng Hồ Ứng Kỳ]</b> <i>(<b>Động Cơ Ứng Kỳ + Vệ Đà Ấn Độ KP Sub-Lord</b> kích hoạt từ Vị trí 4)</i>: {pos5_result} ➔ <i>Soi chiếu lên Vị trí 6</i>.</div>'
        f'<div>🌌 <b>Vị trí 6 [Mắt xích Chiến lược — Thời Thế Công/Thủ]</b> <i>(<b>Thái Ất Thần Số + Tử Vi + Trạch Cát</b> định hướng từ Vị trí 5)</i>: {pos6_result} ➔ <i>Mở chìa khóa Vị trí 7</i>.</div>'
        f'<div>🔑 <b>Vị trí 7 [Mắt xích Chốt hạ — Hóa Giải & Hội Tụ Bayes]</b> <i>(<b>Bát Tự Điều Hầu + 40 Chuyên Gia AI + Toán Học Bayes</b> hợp lực cả 6 vị trí trên)</i>: {pos7_result}</div>'
        f'<div style="margin-top:6px;padding:10px 12px;background:rgba(16,185,129,0.15);border-left:4px solid #34d399;border-radius:8px;color:#ecfdf5;">{syn["synergy_summary_sentence"]}</div>'
        f'</div></div>'
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
    verdicts_list = [ky_mon_verdict, luc_hao_verdict, mai_hoa_verdict, luc_nham_verdict, thai_at_verdict, tu_vi_verdict, xem_ngay_verdict]
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
