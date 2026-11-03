"""
offline_brain.py — V100.1: Siêu Não Suy Luận Ngôn Ngữ Tự Nhiên & Cổ Thư Hợp Nhất
Biến dữ liệu thực tế của Quẻ (Lục Hào, Kỳ Môn, Mai Hoa, Đại Lục Nhâm, 40 Chuyên Gia AI)
thành bài luận giải tiếng Việt sâu sắc, đúng trọng tâm câu hỏi 100%, không sáo rỗng, không mâu thuẫn.
"""
import re


def _verdict_label(pct):
    if pct >= 75: return 'ĐẠI CÁT — RẤT THUẬN LỢI'
    if pct >= 60: return 'CÁT — THUẬN LỢI'
    if pct >= 50: return 'BÌNH HÒA — NGHIÊNG THUẬN'
    if pct >= 45: return 'BÌNH — CẦN THẬN TRỌNG'
    if pct >= 30: return 'HUNG — NHIỀU BẤT LỢI'
    return 'ĐẠI HUNG — RẤT BẤT LỢI'


def _verdict_emoji(pct):
    if pct >= 55: return '🟢'
    if pct >= 45: return '🟡'
    return '🔴'


def _md_to_html_bold(text):
    if not text:
        return ""
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', str(text))


# ═══════════════════════════════════════════════════════════════
# 1. FACTOR CONNECTOR — Chuyển mã kỹ thuật thành lời giải thích có ý nghĩa thực tế, không mâu thuẫn
# ═══════════════════════════════════════════════════════════════
def _humanize_single_factor(f_raw: str) -> tuple:
    """
    Chuyển đổi 1 mã yếu tố kỹ thuật thành (loại_tốt_xấu, cụm_từ_tiếng_Việt_dễ_hiểu).
    """
    s = str(f_raw or "").strip()
    if not s:
        return ("neutral", "")
    up = s.upper()

    if "PHỤC THẦN" in up:
        return ("bad", "hào Dụng Thần đang ẩn mình (Phục Thần) nên tâm ý thật sự hoặc kết quả cốt lõi vẫn giấu kín bên trong, chưa bộc lộ rõ ra ngoài")
    if "TUẦN KHÔNG" in up or "KHÔNG VONG" in up:
        return ("bad", "cung quẻ tạm thời rơi vào khoảng lặng (Tuần Không), khiến sự việc chững lại hoặc còn khoảng cách vô hình cần chờ ngày Xuất Không")
    if "NGUYỆT PHÁ" in up or "NHẬT PHÁ" in up:
        return ("bad", "đang chịu lực xung phá trực tiếp từ thời vận hiện tại (Nguyệt/Nhật Phá), dễ phát sinh áp lực hoặc xáo trộn")
    if "TAM HÌNH" in up:
        return ("bad", "có thế Tam Hình gây ra sự gượng gạo, tự ái ngầm hoặc căng thẳng cần khéo léo tháo gỡ")
    if "NHẬP MỘ" in up:
        return ("bad", "khí lực đang bị thu giữ (Nhập Mộ), làm cho tâm trạng hoặc tiến độ tạm thời bị bó hẹp, chờ ngày Xung Mộ mới khai thông")
    if "PHẢN NGÂM" in up:
        return ("bad", "quẻ gặp thế Phản Ngâm nên tình thế dễ thay đổi thất thường, lúc thuận lúc nghịch")
    if "PHỤC NGÂM" in up:
        return ("bad", "quẻ gặp thế Phục Ngâm khiến sự việc dây dưa kéo dài, khó giải quyết dứt điểm ngay một sớm một chiều")
    if "CUNG BT SINH DT" in up or "CUNG DT TƯƠNG SINH BT" in up or "CUNG SV SINH BT" in up:
        return ("good", "giữa bản thân bạn và đối phương/mục tiêu vẫn có sự tương sinh, quan tâm và nâng đỡ lẫn nhau")
    if "CUNG BT KHẮC DT" in up or "CHỦ THẮNG" in up:
        return ("good", "bạn đang nắm thế chủ động và có khả năng kiểm soát, xoay chuyển tình thế")
    if "CUNG DT KHẮC BT" in up or "CUNG BT BỊ KHẮC" in up:
        return ("bad", "phía đối phương hoặc hoàn cảnh bên ngoài đang tạo sức ép ngược lại lên bạn")
    if "NGUYÊN THẦN VƯỢNG" in up or "NGUYÊN THẦN ĐỘNG" in up or ("NGUYÊN THẦN" in up and ("+6" in s or "+8" in s or "+4" in s)):
        return ("good", "có nguồn lực hậu thuẫn và quý nhân âm thầm tiếp sức ở phía sau (Nguyên Thần vượng)")
    if "KỴ THẦN SUY" in up or ("KỴ THẦN" in up and ("+3" in s or "YẾU" in up)):
        return ("good", "các tác nhân gây cản trở hoặc bất đồng đã suy yếu dần")
    if "KỴ THẦN VƯỢNG" in up or "KỴ THẦN ĐỘNG" in up:
        return ("bad", "yếu tố cản trở (Kỵ Thần) đang hoạt động mạnh gây thêm thử thách")
    if "THỂ VƯỢNG" in up:
        return ("good", "bản thân bạn (Quẻ Thể) vẫn giữ được ý chí và vị thế vững vàng")
    if "DT VƯỢNG" in up or "DT TƯỚNG" in up:
        return ("good", "nội lực gốc của Dụng Thần rất vượng và có nền tảng vững chắc")
    if "DT TÙ" in up or "DT TỬ" in up or "DT SUY" in up or "CAN DT TỬ" in up:
        return ("bad", "năng lượng của Dụng Thần ở thời điểm hiện tại đang trầm lắng và suy giảm")
    if "NGUYỆT" in up and "SINH DT" in up:
        return ("good", "được thiên thời trong tháng ủng hộ thuận lợi")
    if "NHẬT" in up and "SINH DT" in up:
        return ("good", "được hoàn cảnh trong ngày tiếp thêm sinh khí")
    if ("NGUYỆT" in up or "NHẬT" in up) and "KHẮC DT" in up:
        return ("bad", "hoàn cảnh khách quan trước mắt đang có phần nghịch chiều, gây áp lực nhất định")
    if "TỶ HÒA" in up:
        return ("good", "hai bên có sự đồng điệu và tương thông về mặt bản chất")
    if "THỂ SINH DỤNG" in up:
        return ("bad", "bạn đang là người phải chủ động nhường nhịn, lo toan và tiêu hao nhiều tâm sức hơn")
    if "DỤNG KHẮC THỂ" in up:
        return ("bad", "ngoại cảnh hoặc đối phương đang tạo áp lực lớn lên bản thân bạn (Dụng khắc Thể)")
    if "DỤNG SINH THỂ" in up:
        return ("good", "sự việc và đối phương có xu hướng thuận chiều, hướng về phía bạn")
    if "KHÔNG HIỆN" in up and "KỴ THẦN" in up:
        return ("good", "các tác nhân gây cản trở hoặc chia rẽ không xuất hiện trong quẻ")
    if "DT TĨNH" in up:
        return ("bad", "hào Dụng Thần đang tĩnh nên sự việc cần thêm thời gian lắng đọng, chưa bứt phá ngay lập tức")
    if "CỪU THẦN" in up and "VƯỢNG" in up:
        return ("bad", "có tác động ngoại cảnh làm phân tán nguồn lực hỗ trợ")
    return ("neutral", "")


def _connect_factors(factors_list, pct=50):
    """
    Biến danh sách factors thành câu văn xuôi tiếng Việt mượt mà, dễ đọc, nhất quán 100% với điểm số (không tự mâu thuẫn).
    """
    if not factors_list:
        return ""

    good_phrases = []
    bad_phrases = []
    has_phuc_or_suy = any(any(w in str(f).upper() for w in ["PHỤC THẦN", "DT TỬ", "DT TÙ", "DT SUY", "CAN DT TỬ"]) for f in factors_list)

    for f in factors_list:
        kind, phrase = _humanize_single_factor(f)
        if not phrase or len(phrase) < 6:
            continue
        # Tránh mâu thuẫn: nếu Dụng Thần đang Phục Thần hoặc Suy/Tử thì không nói "nội lực gốc của Dụng Thần rất vượng"
        if has_phuc_or_suy and "nội lực gốc của Dụng Thần rất vượng" in phrase:
            continue
        if kind == "good" and phrase not in good_phrases:
            good_phrases.append(phrase)
        elif kind == "bad" and phrase not in bad_phrases:
            bad_phrases.append(phrase)

    sentences = []
    if pct < 45 and bad_phrases:
        b_txt = ", đồng thời ".join(bad_phrases[:2])
        if good_phrases:
            sentences.append(f"Nguyên nhân chính khiến cục diện gặp khó khăn là do {b_txt} (dù điểm tích cực là {good_phrases[0]})")
        else:
            sentences.append(f"Nguyên nhân chính khiến cục diện gặp khó khăn là do {b_txt}")
    elif pct >= 55 and good_phrases:
        g_txt = ", đồng thời ".join(good_phrases[:2])
        if bad_phrases:
            sentences.append(f"Điểm sáng thuận lợi của quẻ là {g_txt}; chỉ cần lưu ý nhỏ rằng {bad_phrases[0]}")
        else:
            sentences.append(f"Điểm sáng rất đáng mừng trong quẻ là {g_txt}")
    elif good_phrases and bad_phrases:
        g_txt = ", đồng thời ".join(good_phrases[:2])
        b_txt = " và ".join(bad_phrases[:2])
        sentences.append(f"Xét về mặt tích cực, quẻ cho thấy {g_txt}; tuy nhiên hiện tại {b_txt}")
    elif good_phrases:
        g_txt = ", kết hợp với việc ".join(good_phrases[:2])
        sentences.append(f"Điểm sáng đáng mừng trong quẻ là {g_txt}")
    elif bad_phrases:
        b_txt = ", bên cạnh đó ".join(bad_phrases[:2])
        sentences.append(f"Nguyên nhân chính gây ra trắc trở lúc này là do {b_txt}")

    return (". ".join(sentences) + ".") if sentences else ""


def _clean_factor(f):
    f = str(f).replace('[HỆ SINH THÁI DT]', '').strip()
    for ch in ['⊕', '⊖', '✅', '🔴', '🟢', '🟡', '⚡', '💥', '⭕', '🔄', '☯', '△', '↗', '👻', '🔥', '⚠️']:
        f = f.replace(ch, '')
    return f.strip().strip('-').strip()


# ═══════════════════════════════════════════════════════════════
# 2. CATEGORY-SPECIFIC TEMPLATES & HELPERS
# ═══════════════════════════════════════════════════════════════
CATEGORY_TEMPLATES = {
    'TÀI_CHÍNH': {
        'high': "Tài vận và mưu cầu tiền bạc đang ở thế <b>vượng khí</b>. Dụng Thần đắc lực cho thấy cơ hội sinh lời rõ ràng. {factors} Thời điểm hội tụ cát khí: <b>{ung_ky}</b>.",
        'mid': "Tài chính ở mức <b>trung bình – giằng co</b>, có cơ hội nhưng kèm điều kiện ràng buộc. {factors} Nên giải ngân từng phần, kiểm soát rủi ro và lưu ý mốc <b>{ung_ky}</b>.",
        'low': "Tài khí giai đoạn này <b>đang bị tiết hao hoặc khắc chế</b>. {factors} Ưu tiên giữ vốn, thẩm định kỹ pháp lý và chờ qua mốc <b>{ung_ky}</b>.",
    },
    'SỨC_KHỎE_GIA_ĐÌNH': {
        'high': "Quẻ báo sinh khí của <b>{person}</b> <b>khá vững vàng</b>, Tử Tôn / Dụng Thần có lực cứu giải nên khả năng phục hồi tốt. {factors}",
        'mid': "Tình trạng sức khỏe của <b>{person}</b> <b>đang giằng co</b> giữa chính khí và tà khí, cần theo dõi sát và tích cực điều trị đúng chuyên khoa. {factors} Mốc chuyển biến quan trọng: <b>{ung_ky}</b>.",
        'low': "Quẻ báo sức khỏe của <b>{person}</b> <b>đang gặp nhiều lực cản đáng lo ngại</b> (Dụng Thần suy yếu hoặc chịu xung khắc mạnh). {factors} Cần đặc biệt cẩn trọng, ưu tiên y tế chuyên sâu và chú ý mốc <b>{ung_ky}</b>.",
    },
    'TÌNH_CẢM': {
        'high': "Nhân duyên và tình cảm <b>thuận hòa, có sự gắn kết</b>. {factors} Đây là thời điểm tốt để thấu hiểu và tiến thêm bước nữa.",
        'mid': "Chuyện tình cảm <b>còn dùng dằng, dễ có tâm tư chưa nói hết</b>. {factors} Nên lắng nghe và chia sẻ thẳng thắn với nhau.",
        'low': "Tình cảm <b>đang vướng xung khắc hoặc khoảng cách</b>. {factors} Cần bình tĩnh, tránh nóng vội tranh cãi; mốc chuyển biến: <b>{ung_ky}</b>.",
    },
    'CÔNG_VIỆC': {
        'high': "Công danh sự nghiệp <b>đắc thời, có quý nhân hoặc cơ hội mở rộng</b>. {factors} Nên chủ động nắm bắt.",
        'mid': "Công việc <b>tạm ổn định nhưng cần vượt qua thử thách trước mắt</b>. {factors} Kết quả sẽ rõ nét hơn vào <b>{ung_ky}</b>.",
        'low': "Công việc <b>đang có lực cản hoặc áp lực khách quan</b>. {factors} Nên xử lý thận trọng từng bước, tránh quyết định nóng vội.",
    },
    'TÌM_ĐỒ': {
        'high': "Khả năng tìm thấy <b>rất khả quan</b>. {factors} Hãy tập trung rà soát hướng <b>{direction}</b> trong khoảng <b>{ung_ky}</b>.",
        'mid': "Khả năng tìm lại ở mức <b>50 - 50 (đồ vật bị che khuất hoặc để quên)</b>. {factors} Hãy kiểm tra kỹ theo hướng <b>{direction}</b>.",
        'low': "Khả năng tìm lại <b>khá thấp hoặc đồ vật đã di chuyển xa</b>. {factors} Hướng manh mối cuối cùng chỉ về phía <b>{direction}</b>.",
    },
    'NHÀ_CỬA': {
        'high': "Phong thủy, điền sản và giao dịch nhà đất <b>thuận lợi, khí trường tốt</b>. {factors} Mốc thời gian ứng nghiệm: <b>{ung_ky}</b>.",
        'mid': "Việc nhà đất/điền sản <b>cần rà soát kỹ giấy tờ và giá cả</b> trước khi chốt. {factors}",
        'low': "Giao dịch hoặc việc nhà đất <b>đang vướng trở ngại pháp lý/tài chính</b>. {factors} Chưa nên vội vàng xuống tiền lớn.",
    },
    'XUẤT_HÀNH': {
        'high': "Chuyến đi / xuất hành <b>thuận buồm xuôi gió, bình an và đạt mục đích</b>. {factors}",
        'mid': "Xuất hành <b>cần chuẩn bị kỹ lịch trình và giấy tờ/phương tiện</b> để tránh chậm trễ nhỏ. {factors}",
        'low': "Xuất hành <b>gặp nhiều cản trở hoặc lịch trình bất lợi</b>. {factors} Nên kiểm tra kỹ an toàn hoặc điều chỉnh giờ đi.",
    },
    'THẮNG_THUA': {
        'high': "Tương quan lực lượng nghiêng về <b>bên Chủ (Thế/Chủ đắc lợi)</b>. {factors} Khả năng giành phần thắng cao.",
        'mid': "Hai bên <b>giằng co quyết liệt, thế trận ngang ngửa</b>. {factors} Kết quả định đoạt bởi bản lĩnh ở thời điểm <b>{ung_ky}</b>.",
        'low': "Tương quan lực lượng đang <b>bất lợi cho bên Chủ (Đối phương/Ứng đang lấn lướt)</b>. {factors} Cần đổi chiến thuật phòng thủ chặt.",
    },
    'CHUNG': {
        'high': "Tổng cục quẻ <b>hội tụ nhiều cát khí thuận lợi</b>. {factors} Có thể vững tâm triển khai kế hoạch.",
        'mid': "Tổng cục ở thế <b>Bình Hòa (trong cát có hung, cần khéo léo điều tiết)</b>. {factors}",
        'low': "Tổng cục đang <b>nhiều lực cản nghịch chiều</b>. {factors} Nên thận trọng tối đa và chuẩn bị phương án dự phòng.",
    },
}


def _get_tier(pct):
    if pct >= 55: return 'high'
    if pct >= 45: return 'mid'
    return 'low'


def _get_qtype_opener(question, pct, category='CHUNG'):
    q = (question or '').lower()
    emoji = _verdict_emoji(pct)
    label = _verdict_label(pct)

    if category == 'SỨC_KHỎE_GIA_ĐÌNH' or any(kw in q for kw in ['qua khỏi', 'qua được', 'khỏi bệnh', 'khỏi không', 'ốm', 'bệnh', 'nguy kịch', 'sống không']):
        if pct >= 55:
            return f"{emoji} <b>TIÊN LƯỢNG KHẢ QUAN — CÓ KHẢ NĂNG QUA KHỎI & HỒI PHỤC ({pct}%)</b>. "
        elif pct >= 45:
            return f"{emoji} <b>TIÊN LƯỢNG GIẰNG CO — CẦN TÍCH CỰC CHỮA TRỊ & THEO DÕI SÁT ({pct}%)</b>. "
        else:
            return f"{emoji} <b>TIÊN LƯỢNG NẶNG — NHIỀU DẤU HIỆU BẤT LỢI, CẦN CHUYÊN KHOA NGAY ({pct}%)</b>. "

    if category == 'TÌM_ĐỒ' or any(kw in q for kw in ['ở đâu', 'chỗ nào', 'hướng nào', 'tìm đâu', 'tìm thấy', 'bị mất']):
        if pct >= 55:
            return f"📍 <b>CÓ THỂ TÌM THẤY ({pct}%)</b> — "
        elif pct >= 45:
            return f"📍 <b>CƠ HỘI TÌM THẤY 50/50 ({pct}%)</b> — "
        else:
            return f"📍 <b>KHÓ TÌM LẠI / ĐÃ DI CHUYỂN XA ({pct}%)</b> — "

    if any(kw in q for kw in ['khi nào', 'bao giờ', 'lúc nào', 'tháng mấy', 'ngày nào']):
        return f"⏳ <b>LUẬN THỜI ĐIỂM ỨNG KỲ ({pct}% — {label}):</b> "

    if any(kw in q for kw in ['có nên', 'nên không', 'nên hay']):
        if pct >= 55:
            return f"{emoji} <b>NÊN TIẾN HÀNH — {label} ({pct}%)</b>. "
        elif pct >= 45:
            return f"{emoji} <b>CÓ THỂ TIẾN HÀNH NHƯNG CẦN THẬN TRỌNG ({pct}%)</b>. "
        else:
            return f"{emoji} <b>CHƯA NÊN TIẾN HÀNH LÚC NÀY — {label} ({pct}%)</b>. "

    if any(kw in q for kw in ['có được', 'được không', 'có không', 'liệu có', 'không?', 'có lãi', 'thành công']):
        if pct >= 55:
            return f"{emoji} <b>CÓ / ĐẠT ĐƯỢC — {label} ({pct}%)</b>. "
        elif pct >= 45:
            return f"{emoji} <b>CÒN GIẰNG CO / CẦN NỖ LỰC THÊM ({pct}%)</b>. "
        else:
            return f"{emoji} <b>KHÓ ĐẠT / GẶP NHIỀU TRỞ NGẠI — {label} ({pct}%)</b>. "

    return f"{emoji} <b>{label} ({pct}%)</b>. "


PERSON_KEYWORDS = {
    'ông nội': 'ông nội', 'bà nội': 'bà nội', 'ông ngoại': 'ông ngoại', 'bà ngoại': 'bà ngoại',
    'con trai': 'con trai', 'con gái': 'con gái', 'người yêu': 'người yêu',
    'bố mẹ': 'bố mẹ', 'cha mẹ': 'cha mẹ',
    'bố': 'bố', 'mẹ': 'mẹ', 'cha': 'cha', 'ba': 'ba', 'má': 'má',
    'ông': 'ông', 'bà': 'bà', 'vợ': 'vợ', 'chồng': 'chồng',
    'con': 'con', 'cháu': 'cháu', 'anh': 'anh', 'chị': 'chị', 'em': 'em',
    'sếp': 'sếp', 'bạn': 'bạn',
}

DIRECTION_MAP = {
    1: 'Chính Bắc (Khảm)', 2: 'Tây Nam (Khôn)', 3: 'Chính Đông (Chấn)', 4: 'Đông Nam (Tốn)',
    5: 'Trung Tâm', 6: 'Tây Bắc (Càn)', 7: 'Chính Tây (Đoài)', 8: 'Đông Bắc (Cấn)', 9: 'Chính Nam (Ly)',
}

CUNG_HANH = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}
NGU_HANH_SINH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
NGU_HANH_KHAC = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}


def _extract_person(question):
    q = (question or '').lower()
    for kw, label in sorted(PERSON_KEYWORDS.items(), key=lambda x: len(x[0]), reverse=True):
        if re.search(r'(?:^|[\s,;.!?])' + re.escape(kw) + r'(?:[\s,;.!?]|$)', q):
            return label
    return 'bạn'


def _resolve_authentic_km_palace(chart_data: dict, dung_than: str = 'Bản Thân', question: str = '', category: str = 'CHUNG') -> tuple:
    """
    Xác định đúng Cung Dụng Thần Kỳ Môn theo chuẩn cổ thư cho từng loại câu hỏi:
    Trả về (target_cung, bt_cung, palace_role_label).
    """
    if not chart_data or not isinstance(chart_data, dict):
        return (1, 1, "Cung Dụng Thần")
    ctb = chart_data.get("can_thien_ban", {}) or {}
    tb = chart_data.get("thien_ban", {}) or {}
    nb = chart_data.get("nhan_ban", {}) or {}
    sb = chart_data.get("than_ban", {}) or {}
    can_ngay = chart_data.get("can_ngay", "")
    can_gio = chart_data.get("can_gio", "")
    q_low = (question or "").lower()

    cdb = chart_data.get("can_dia_ban") or chart_data.get("dia_ban") or chart_data.get("dia_can") or {}
    def _find_can(c_name):
        if not c_name:
            return None
        search_c = "Mậu" if c_name == "Giáp" else c_name
        for k, v in ctb.items():
            if str(v) == str(search_c) and str(k).isdigit():
                return int(k)
        for k, v in cdb.items():
            if str(v) == str(search_c) and str(k).isdigit():
                return int(k)
        return None

    def _find_in_board(board, keyword):
        for k, v in board.items():
            if keyword in str(v) and str(k).isdigit():
                return int(k)
        return None

    bt_cung = _find_can(can_ngay) or 1
    sv_cung = _find_can(can_gio) or bt_cung

    # Ưu tiên 1: Tìm đồ / Mất đồ (kiểm tra TRƯỚC tài chính để 'mất ví tiền' không bị nhầm sang đầu tư Sinh Môn)
    if category == "TÌM_ĐỒ" or any(w in q_low for w in ["bị mất", "mất đồ", "mất ví", "mất xe", "mất tiền", "thất lạc", "tìm lại", "ở đâu", "để đâu", "rơi ở đâu"]):
        return (sv_cung, bt_cung, f"Cung Thời Can ({can_gio or 'Giờ'} — Đồ vật thất lạc & Phương vị tìm kiếm)")

    # Ưu tiên 2: Đối kháng / Kiện tụng / Tranh chấp thắng thua
    if category == "THẮNG_THUA" or any(w in q_low for w in ["ai thắng", "đối phương thắng", "thắng hay thua", "tranh chấp", "kiện tụng", "vụ kiện"]):
        c_khai = _find_in_board(nb, "Khai") or _find_in_board(nb, "Kinh") or sv_cung
        return (c_khai, bt_cung, "Cung Đối Kháng / Phân Xử (Tương quan Chủ – Khách)")

    # Ưu tiên 3: Tình cảm / Hôn nhân
    if category == "TÌNH_CẢM" or any(w in q_low for w in ["yêu", "vợ", "chồng", "hôn nhân", "bạn gái", "bạn trai", "chia tay", "quay lại", "tình cảm"]):
        if "vợ" in q_low or "bạn gái" in q_low:
            c_at = _find_can("Ất")
            if c_at:
                return (c_at, _find_can("Canh") or bt_cung, "Cung Ất Kỳ (Người vợ / Nữ giới)")
        elif "chồng" in q_low or "bạn trai" in q_low:
            c_canh = _find_can("Canh")
            if c_canh:
                return (c_canh, _find_can("Ất") or bt_cung, "Cung Canh Kim (Người chồng / Nam giới)")
        c_lh = _find_in_board(sb, "Lục Hợp")
        if c_lh:
            return (c_lh, bt_cung, "Cung Lục Hợp (Nhân duyên & Tình cảm)")

    # Ưu tiên 4: Sức khỏe / Bệnh tật
    if category == "SỨC_KHỎE_GIA_ĐÌNH" or any(w in q_low for w in ["bệnh", "ốm", "đau", "khỏe", "qua khỏi", "qua được", "viện", "mổ", "thuốc"]):
        if any(w in q_low for w in ["bố", "mẹ", "cha", "ông", "bà"]):
            c_nam = _find_can(chart_data.get("can_nam", ""))
            if c_nam:
                return (c_nam, bt_cung, "Cung Niên Can (Bậc trưởng bối / Cha mẹ)")
        c_nhue = _find_in_board(tb, "Nhuế")
        if c_nhue:
            return (c_nhue, bt_cung, "Cung Sao Thiên Nhuế (Bệnh tinh)")

    # Ưu tiên 5: Tài chính / Đầu tư / Mua bán / Đòi nợ
    if category in ("TÀI_CHÍNH", "NHÀ_CỬA") or any(w in q_low for w in ["tiền", "đầu tư", "lãi", "lời", "lỗ", "mua", "bán", "kinh doanh", "vốn", "đất", "nhà", "nợ"]):
        if "nợ" in q_low or "vay" in q_low:
            c_thuong = _find_in_board(nb, "Thương") or sv_cung
            return (c_thuong, bt_cung, "Cung Thương Môn / Thời Can (Thu hồi công nợ)")
        c_sinh = _find_in_board(nb, "Sinh")
        if c_sinh:
            return (c_sinh, bt_cung, "Cung Sinh Môn (Tài lộc & Lợi nhuận)")

    # Ưu tiên 6: Công việc / Sự nghiệp / Thi cử
    if category == "CÔNG_VIỆC" or any(w in q_low for w in ["việc", "sự nghiệp", "thăng chức", "công ty", "bổ nhiệm"]):
        c_khai = _find_in_board(nb, "Khai")
        if c_khai:
            return (c_khai, bt_cung, "Cung Khai Môn (Công danh & Sự nghiệp)")
    if any(w in q_low for w in ["thi", "đỗ", "học", "điểm", "bằng cấp"]):
        c_canh_mon = _find_in_board(nb, "Cảnh") or _find_in_board(tb, "Phụ")
        if c_canh_mon:
            return (c_canh_mon, bt_cung, "Cung Cảnh Môn / Thiên Phụ (Thi cử & Khoa bảng)")

    dt_can_map = {
        "Quan Quỷ": can_gio,
        "Thê Tài": can_gio,
        "Tử Tôn": can_gio,
        "Phụ Mẫu": chart_data.get("can_nam", "") or can_gio,
        "Huynh Đệ": chart_data.get("can_thang", "") or can_gio,
        "Bản Thân": can_ngay,
    }
    dt_can = dt_can_map.get(dung_than, can_gio) or can_gio
    dt_cung = _find_can(dt_can) or sv_cung or bt_cung
    if dung_than == "Bản Thân" and sv_cung and sv_cung != bt_cung:
        dt_cung = sv_cung
    return (dt_cung, bt_cung, f"Cung Sự Việc / Dụng Thần ({dung_than})")


def _extract_direction(chart_data, dung_than='Bản Thân', question='', category='CHUNG'):
    if not chart_data or not isinstance(chart_data, dict):
        return 'Chính Bắc (Khảm)'
    cung, _, _ = _resolve_authentic_km_palace(chart_data, dung_than, question, category)
    return DIRECTION_MAP.get(int(cung), 'Chính Bắc (Khảm)')


def _generate_advice(pct, category, ung_ky_str, factors_text):
    advice = []
    if category == 'SỨC_KHỎE_GIA_ĐÌNH':
        if pct >= 55:
            advice.append("💊 <b>Hướng điều trị:</b> Tiên lượng khả quan, kiên trì phác đồ điều trị hiện tại kết hợp dinh dưỡng và nghỉ ngơi.")
        elif pct >= 45:
            advice.append("🏥 <b>Hướng điều trị:</b> Bệnh tình còn giằng co, cần khám chuyên khoa sâu hoặc hội chẩn thêm để tối ưu thuốc.")
        else:
            advice.append("🚑 <b>Khuyến nghị y tế khẩn:</b> Dụng Thần đang chịu xung khắc mạnh, cần đưa tới bệnh viện tuyến trên/bác sĩ đầu ngành và theo dõi sát sao.")
    elif category == 'TÌM_ĐỒ':
        advice.append("🔍 <b>Hành động ngay:</b> Tìm kiếm ngay theo phương hướng và vị trí mô tả trước khi đồ vật bị xê dịch.")
    elif category == 'TÀI_CHÍNH':
        if pct >= 55:
            advice.append("💰 <b>Chiến lược tài chính:</b> Thời điểm thuận lợi để triển khai giao dịch/đầu tư, ưu tiên kiểm tra kỹ điều khoản hợp đồng.")
        elif pct >= 45:
            advice.append("⚖️ <b>Chiến lược tài chính:</b> Chỉ nên đầu tư thăm dò tỷ trọng nhỏ, kiểm soát chặt dòng tiền.")
        else:
            advice.append("🛡️ <b>Bảo toàn vốn:</b> Tạm hoãn giải ngân lớn, tránh cho vay hoặc đầu tư mạo hiểm trong lúc Kỵ Thần đang vượng.")
    else:
        if pct >= 60:
            advice.append("💡 <b>Khuyến nghị:</b> Thời cơ thuận lợi, nên chủ động tiến hành theo kế hoạch.")
        elif pct >= 45:
            advice.append("⚠️ <b>Khuyến nghị:</b> Có thể tiến hành từng bước nhưng cần chuẩn bị kỹ phương án dự phòng.")
        else:
            advice.append("🛑 <b>Khuyến nghị:</b> Hiện nhiều lực cản nghịch chiều, nên lùi bước củng cố nội lực hoặc đổi phương án.")

    if ung_ky_str and ung_ky_str != '?' and 'N/A' not in ung_ky_str:
        advice.append(f"⏰ <b>Mốc ứng kỳ then chốt:</b> {_md_to_html_bold(ung_ky_str)}")
    return "\n".join(advice)


def build_narrative_summary_text(
    question,
    dung_than,
    weighted_pct,
    category,
    all_factors=None,
    ung_ky_str='',
    chart_data=None,
    omni_data=None,
    kc_detail='',
    ev_str='',
    luc_hao_data=None,
    mai_hoa_data=None,
):
    """
    V100.1: Sinh câu trả lời TRỰC DIỆN – ĐÚNG TRỌNG TÂM CÂU HỎI, rõ ràng, dễ hiểu và nhất quán 100% với điểm số.
    """
    pct = weighted_pct or 50
    q = (question or '').strip()
    q_low = q.lower()
    person = _extract_person(q)
    direction = _extract_direction(chart_data, dung_than, q, category)
    omni_data = omni_data if isinstance(omni_data, dict) else {}
    factors_text = _connect_factors(all_factors or [], pct=pct)

    uk_clean = ung_ky_str if (ung_ky_str and ung_ky_str != '?' and 'xem mục' not in ung_ky_str.lower()) else omni_data.get('exact_timestamp', 'trong chu kỳ Can Chi gần nhất')

    # 1. TRỌNG TÂM: BỆNH TẬT / SỨC KHỎE / QUA KHỎI KHÔNG
    if category == 'SỨC_KHỎE_GIA_ĐÌNH' or any(w in q_low for w in ['ốm', 'bệnh', 'đau', 'khỏe', 'qua khỏi', 'qua được', 'sống không', 'nguy kịch', 'nằm viện', 'mổ']):
        subj_lbl = person.capitalize() if person != 'bạn' else 'Người bệnh'
        co_the = omni_data.get('co_the', '') or kc_detail
        co_the_str = f" Vùng cơ thể/triệu chứng cần lưu tâm: <b>{co_the}</b>." if co_the else ""
        if pct >= 55:
            head = f"🏥 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>{subj_lbl.upper()} CÓ KHẢ NĂNG QUA KHỎI & HỒI PHỤC TỐT ({pct}% — CÁT)</b>."
            body = f"Hào Dụng Thần (<b>{dung_than}</b>) và sinh khí còn vững, có lực cứu giải của thầy thuốc.{co_the_str} {factors_text} Dự kiến sức khỏe chuyển biến tích cực rõ rệt vào khoảng <b>{uk_clean}</b>."
        elif pct >= 45:
            head = f"🏥 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>TÌNH TRẠNG CỦA {subj_lbl.upper()} ĐANG GIẰNG CO — CẦN TÍCH CỰC ĐIỀU TRỊ ({pct}% — BÌNH)</b>."
            body = f"Chính khí của Dụng Thần (<b>{dung_than}</b>) và bệnh khí đang giằng co.{co_the_str} {factors_text} Cần tuân thủ sát phác đồ chuyên khoa; nếu vượt qua mốc <b>{uk_clean}</b> thì sẽ chuyển nguy thành an."
        else:
            head = f"🏥 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>{subj_lbl.upper()} ĐANG GẶP NHIỀU BẤT LỢI / TIÊN LƯỢNG NẶNG ({pct}% — HUNG)</b>."
            body = f"Quẻ báo Dụng Thần (<b>{dung_than}</b>) suy yếu hoặc chịu xung khắc mạnh.{co_the_str} {factors_text} Cần lập tức ưu tiên điều trị chuyên sâu tuyến trên và theo dõi đặc biệt sát sao quanh mốc <b>{uk_clean}</b>."
        return _md_to_html_bold(f"{head}<br>{body}")

    # 2. TRỌNG TÂM: TÌM ĐỒ / MẤT ĐỒ / Ở ĐÂU (Kiểm tra TRƯỚC Tài Chính)
    if category == 'TÌM_ĐỒ' or any(w in q_low for w in ['tìm lại', 'bị mất', 'mất chiếc', 'mất đồ', 'mất ví', 'thất lạc', 'ở đâu', 'chỗ nào', 'để đâu', 'cất đâu']):
        where_sum = omni_data.get('where_summary', f'Hướng <b>{direction}</b>')
        height_d = omni_data.get('height_desc', '')
        places_d = omni_data.get('places', '')
        loc_detail = f" Gợi ý vị trí: <b>{places_d}</b> ({height_d})." if places_d else ""
        if pct >= 55:
            head = f"📍 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CÓ THỂ TÌM LẠI ĐƯỢC ({pct}% — CÁT) — HƯỚNG {direction.upper()}</b>."
            body = f"Đồ vật chưa mất hẳn, hiện nằm tại khu vực: {where_sum}.{loc_detail} {factors_text} Hãy tìm ngay trong khoảng <b>{uk_clean}</b>."
        elif pct >= 45:
            head = f"📍 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CƠ HỘI TÌM LẠI 50/50 ({pct}% — BÌNH) — HƯỚNG {direction.upper()}</b>."
            body = f"Đồ vật đang bị che khuất hoặc để lẫn tại: {where_sum}.{loc_detail} {factors_text} Cần tìm kỹ các ngăn/góc khuất theo hướng này quanh mốc <b>{uk_clean}</b>."
        else:
            head = f"📍 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>KHÓ TÌM LẠI / ĐÃ DI CHUYỂN XA ({pct}% — HUNG) — MANH MỐI HƯỚNG {direction.upper()}</b>."
            body = f"Quẻ báo hào Tài/Dụng Thần đang ẩn phục hoặc bị khắc, khả năng tìm lại thấp. Phương vị manh mối cuối cùng: {where_sum}.{loc_detail} {factors_text}"
        return _md_to_html_bold(f"{head}<br>{body}")

    # 3. TRỌNG TÂM: ĐỐI KHÁNG / TRANH CHẤP / KIỆN TỤNG / AI THẮNG
    if category == 'THẮNG_THUA' or any(w in q_low for w in ['ai thắng', 'đối phương thắng', 'thắng hay thua', 'tranh chấp', 'vụ kiện', 'kiện tụng']):
        if pct >= 55:
            head = f"⚔️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>BÊN BẠN (CHỦ/HÀO THẾ) ĐANG CHIẾM ƯU THẾ & KHẢ NĂNG THẮNG CAO ({pct}% — CÁT)</b>."
            body = f"Xét tương quan Chủ – Khách và trục Hào Thế – Hào Ứng, khí lực và lý lẽ đang nghiêng về phía bên bạn. {factors_text} Thời điểm phân định kết quả rõ nét: <b>{uk_clean}</b>."
        elif pct >= 45:
            head = f"⚔️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>THẾ TRẬN GIẰNG CO NGANG NGỬA — NÊN ƯU TIÊN ĐÀM PHÁN HÒA GIẢI ({pct}% — BÌNH)</b>."
            body = f"Tương quan lực lượng giữa bên bạn (Hào Thế/Cung Chủ) và đối phương (Hào Ứng/Cung Khách) đang giằng co quyết liệt, chưa bên nào áp đảo hoàn toàn. {factors_text} Nếu củng cố chặt chứng cứ pháp lý và khéo léo đàm phán quanh mốc <b>{uk_clean}</b> thì bên bạn sẽ giữ được quyền lợi."
        else:
            head = f"⚔️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>ĐỐI PHƯƠNG ĐANG LẤN LƯỚT — BÊN BẠN BẤT LỢI NẾU ĐỐI ĐẦU TRỰC DIỆN ({pct}% — HUNG)</b>."
            body = f"Trục Hào Ứng / Cung Khách đang vượng và chế khắc bên Chủ, đối đầu căng thẳng lúc này dễ thiệt thòi. {factors_text} Nên chuyển sang thế phòng thủ, củng cố hồ sơ pháp lý và chờ thời cơ chuyển cục vào <b>{uk_clean}</b>."
        return _md_to_html_bold(f"{head}<br>{body}")

    # 4. TRỌNG TÂM: KHI NÀO / BAO GIỜ / THÁNG MẤY / NGÀY NÀO
    if any(w in q_low for w in ['khi nào', 'bao giờ', 'lúc nào', 'tháng mấy', 'ngày nào', 'mấy giờ', 'năm nào']):
        status_w = "THUẬN LỢI ỨNG NGHIỆM" if pct >= 55 else ("ỨNG NGHIỆM NHƯNG CẦN KIÊN NHẪN" if pct >= 45 else "ĐANG BỊ TRÌ HOÃN, CẦN CHỜ XUNG KHAI")
        head = f"⏳ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>THỜI ĐIỂM ỨNG KỲ LÀ {uk_clean.upper()} ({pct}% — {status_w})</b>."
        body = f"Dựa trên sự hội tụ của Dụng Thần (<b>{dung_than}</b>) và vòng Can Chi: {factors_text} Phương hướng thuận lợi hỗ trợ: <b>{direction}</b>."
        return _md_to_html_bold(f"{head}<br>{body}")

    # 5. TRỌNG TÂM: AI / NGƯỜI NÀO / TRAI HAY GÁI / BAO NHIÊU TUỔI
    if any(w in q_low for w in ['là ai', 'người nào', 'trai hay gái', 'nam hay nữ', 'bao nhiêu tuổi', 'mấy tuổi']):
        g_str = omni_data.get('gender', 'Nam/Nữ theo quẻ')
        a_str = omni_data.get('age_tier', '')
        by_str = ", ".join(omni_data.get('birth_years', [])[:3])
        head = f"👤 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>{g_str} — {a_str} (Khoảng năm sinh: {by_str})</b>."
        body = f"Người này ứng vào Dụng Thần <b>{dung_than}</b> tại hướng <b>{direction}</b>. {factors_text}"
        return _md_to_html_bold(f"{head}<br>{body}")

    # 6. TRỌNG TÂM: CÁI GÌ / ĐỒ VẬT GÌ / BAO NHIÊU / MẤY
    if any(w in q_low for w in ['cái gì', 'đồ gì', 'vật gì', 'bao nhiêu', 'có mấy', 'số lượng']):
        obj_str = omni_data.get('objects', '')
        qty_str = omni_data.get('quantity', '')
        col_str = omni_data.get('colors', '')
        head = f"📦 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>{obj_str[:120]}</b>."
        body = f"Màu sắc đặc trưng: <b>{col_str}</b> | {qty_str}. {factors_text}"
        return _md_to_html_bold(f"{head}<br>{body}")

    # 7. TRỌNG TÂM: MUA BÁN ĐẤT ĐAI / NHÀ CỬA / ĐẦU TƯ / TÀI CHÍNH / CÓ LÃI KHÔNG
    if category in ('TÀI_CHÍNH', 'NHÀ_CỬA') or any(w in q_low for w in ['mua đất', 'bán đất', 'mua nhà', 'bán nhà', 'đầu tư', 'có lãi', 'lời', 'lỗ', 'kinh doanh', 'vốn', 'tiền']):
        if pct >= 55:
            head = f"💰 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>THUẬN LỢI — CÓ LÃI & KHẢ QUAN ({pct}% — CÁT)</b>."
            body = f"Dụng Thần (<b>{dung_than}</b>) đắc khí, dòng tiền và cơ hội sinh lời tốt. {factors_text} Hướng cát lợi: <b>{direction}</b> | Mốc thời gian vượng khí: <b>{uk_clean}</b>."
        elif pct >= 45:
            head = f"💰 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CƠ HỘI TRUNG BÌNH — LỢI NHUẬN MỎNG, CẦN THẬN TRỌNG ({pct}% — BÌNH)</b>."
            body = f"Dụng Thần (<b>{dung_than}</b>) ở thế giằng co, có thể thực hiện nhưng phải đàm phán kỹ giá cả và pháp lý, tránh dùng đòn bẩy quá sức. {factors_text} Mốc ứng kỳ: <b>{uk_clean}</b>."
        else:
            head = f"💰 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CHƯA NÊN ĐẦU TƯ / KHÓ CÓ LÃI NGAY, DỄ ĐỌNG VỐN ({pct}% — HUNG)</b>."
            body = f"Dụng Thần (<b>{dung_than}</b>) đang ẩn phục hoặc suy yếu, xuống tiền lúc này dễ bị kẹt thanh khoản hoặc hao hụt. {factors_text} Nên giữ tiền mặt và chờ qua mốc <b>{uk_clean}</b>."
        return _md_to_html_bold(f"{head}<br>{body}")

    # 8. TRỌNG TÂM: CÔNG VIỆC / CHUYỂN VIỆC / XIN VIỆC / THI CỬ / SỰ NGHIỆP
    if category == 'CÔNG_VIỆC' or any(w in q_low for w in ['chuyển việc', 'xin việc', 'nhảy việc', 'công việc', 'thăng chức', 'thi', 'đỗ', 'phỏng vấn', 'sự nghiệp']):
        if pct >= 55:
            head = f"💼 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>TỐT / THUẬN LỢI TIẾN HÀNH ({pct}% — CÁT)</b>."
            body = f"Quan vận và Dụng Thần (<b>{dung_than}</b>) sáng sủa, có quý nhân hoặc cơ hội phát triển đúng kỳ vọng. {factors_text} Thời điểm ứng nghiệm: <b>{uk_clean}</b>."
        elif pct >= 45:
            head = f"💼 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>TẠM ỔN NHƯNG CẦN CHUẨN BỊ KỸ ({pct}% — BÌNH)</b>."
            body = f"Dụng Thần (<b>{dung_than}</b>) ở mức trung bình, bước đầu có thử thách nhỏ nhưng kiên trì sẽ đạt kết quả vào khoảng <b>{uk_clean}</b>. {factors_text}"
        else:
            head = f"💼 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CHƯA THUẬN LỢI / NHIỀU ÁP LỰC & CẢN TRỞ ({pct}% — HUNG)</b>."
            body = f"Dụng Thần (<b>{dung_than}</b>) đang gặp lực cản mạnh, nếu vội vàng thay đổi hoặc quyết định lớn lúc này sẽ bất lợi. {factors_text} Nên củng cố vị trí hiện tại và chờ tới <b>{uk_clean}</b>."
        return _md_to_html_bold(f"{head}<br>{body}")

    # 9. TRỌNG TÂM: TÌNH CẢM / HÔN NHÂN / VỢ CHỒNG / NGƯỜI YÊU
    if category == 'TÌNH_CẢM' or any(w in q_low for w in ['yêu', 'cưới', 'hôn nhân', 'vợ chồng', 'chia tay', 'quay lại', 'tình cảm', 'thật lòng', 'ngoại tình', 'vợ tôi', 'chồng tôi', 'người yêu']):
        _target_p = 'Vợ bạn' if 'vợ' in q_low else ('Chồng bạn' if 'chồng' in q_low else ('Người ấy' if any(x in q_low for x in ['người yêu', 'bạn trai', 'bạn gái']) else 'Đối phương'))
        if any(w in q_low for w in ['còn yêu', 'yêu tôi không', 'thật lòng', 'còn thương', 'tình cảm']):
            if pct >= 55:
                head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>{_target_p.upper()} VẪN CÒN YÊU THƯƠNG & GẮN BÓ CHÂN THÀNH VỚI BẠN ({pct}% — CÁT)</b>."
                body = f"Xét hào Dụng Thần (<b>{dung_than}</b>) và tương quan Thế – Ứng, tình cảm {_target_p.lower()} dành cho bạn vẫn sâu đậm, hướng về gia đình/mối quan hệ. {factors_text} Mốc tình cảm thêm nồng ấm: <b>{uk_clean}</b>."
            elif pct >= 45:
                head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>{_target_p.upper()} VẪN CÒN TÌNH NGHĨA NHƯNG ĐANG CÓ KHOẢNG CÁCH / TÂM SỰ GIỮ KÍN TRONG LÒNG ({pct}% — BÌNH)</b>."
                body = f"Dụng Thần (<b>{dung_than}</b>) đạt <b>{pct}%</b> cho thấy {_target_p.lower()} <b>chưa hết yêu bạn</b>, nhưng do cung quẻ đang gặp lực cản/khép kín nên bề ngoài tỏ ra trầm lắng, ít chia sẻ hoặc còn tự ái ngầm. {factors_text} Hãy chủ động quan tâm nhẹ nhàng, tháo gỡ khúc mắc quanh mốc <b>{uk_clean}</b>."
            else:
                head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>TÌNH CẢM CỦA {_target_p.upper()} ĐANG BỊ DỒN NÉN / CÓ KHOẢNG CÁCH LỚN ({pct}% — HUNG)</b>."
                body = f"Hào Dụng Thần (<b>{dung_than}</b>) đang ẩn phục/chịu xung khắc, báo hiệu {_target_p.lower()} đang rất mệt mỏi, giận dỗi ngầm hoặc khép kín cảm xúc. {factors_text} Cần kiên nhẫn lắng nghe và hóa giải từ từ, tránh tranh cãi gay gắt trước mốc <b>{uk_clean}</b>."
        elif any(w in q_low for w in ['quay lại', 'hàn gắn', 'làm lành']):
            if pct >= 55:
                head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CÓ KHẢ NĂNG QUAY LẠI & HÀN GẮN THÀNH CÔNG ({pct}% — CÁT)</b>."
            elif pct >= 45:
                head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CÒN DUYÊN NỢ DÙNG DẰNG — CẦN CHỦ ĐỘNG MỀM MỎNG MỚI HÀN GẮN ĐƯỢC ({pct}% — BÌNH)</b>."
            else:
                head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>RẤT KHÓ QUAY LẠI NGAY — DUYÊN KHÍ ĐANG BẾ TẮC ({pct}% — HUNG)</b>."
            body = f"Xét trên trục Dụng Thần (<b>{dung_than}</b>) và tương quan Thế – Ứng: {factors_text} Mốc chuyển biến tình cảm: <b>{uk_clean}</b>."
        else:
            if pct >= 55:
                head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>TÌNH CẢM THUẬN HÒA & GẮN KẾT TỐT ({pct}% — CÁT)</b>."
            elif pct >= 45:
                head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CÒN TÌNH NGHĨA NHƯNG ĐANG DÙNG DẰNG — CẦN THẤU HIỂU & NHƯỜNG NHỊN ({pct}% — BÌNH)</b>."
            else:
                head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>ĐANG CÓ XUNG KHẮC / TRỞ NGẠI LỚN TRONG TÌNH CẢM ({pct}% — HUNG)</b>."
            body = f"Xét trên trục Dụng Thần (<b>{dung_than}</b>) và tương quan Thế – Ứng: {factors_text} Mốc chuyển biến tình cảm: <b>{uk_clean}</b>."
        return _md_to_html_bold(f"{head}<br>{body}")

    # 10. CÁC CÂU HỎI KHÁC
    opener = _get_qtype_opener(q, pct, category)
    tier = _get_tier(pct)
    cat_key = category if category in CATEGORY_TEMPLATES else 'CHUNG'
    template = CATEGORY_TEMPLATES[cat_key].get(tier, CATEGORY_TEMPLATES['CHUNG'][tier])
    filled = template.format(
        factors=factors_text,
        person=person,
        direction=direction,
        ung_ky=uk_clean,
    )
    return _md_to_html_bold(f"🎯 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> {opener}{filled}")


def generate_smart_offline_answer(
    question,
    dung_than,
    weighted_pct,
    category,
    verdicts_dict=None,
    all_factors=None,
    ung_ky_str='',
    chart_data=None,
    v38_conclusion='',
):
    """MASTER FUNCTION: Biến dữ liệu offline thành câu trả lời tự nhiên dạng HTML sạch."""
    if not verdicts_dict:
        verdicts_dict = {}
    if not all_factors:
        all_factors = []

    pct = weighted_pct or 50
    cat_key = category if category in CATEGORY_TEMPLATES else 'CHUNG'
    narrative_html = build_narrative_summary_text(
        question=question,
        dung_than=dung_than,
        weighted_pct=pct,
        category=cat_key,
        all_factors=all_factors,
        ung_ky_str=ung_ky_str,
        chart_data=chart_data,
    )
    factors_text = _connect_factors(all_factors, pct=pct)
    advice = _md_to_html_bold(_generate_advice(pct, cat_key, ung_ky_str, factors_text))
    consensus = _build_consensus(verdicts_dict)

    if pct >= 55:
        bg = 'linear-gradient(135deg, #064e3b, #065f46)'
        border_color = '#10b981'
        accent = '#6ee7b7'
    elif pct >= 45:
        bg = 'linear-gradient(135deg, #713f12, #854d0e)'
        border_color = '#f59e0b'
        accent = '#fcd34d'
    else:
        bg = 'linear-gradient(135deg, #7f1d1d, #991b1b)'
        border_color = '#ef4444'
        accent = '#fca5a5'

    html = f'''<div style="background:{bg};padding:20px;border-radius:14px;margin:12px 0;border:2px solid {border_color};box-shadow:0 4px 20px rgba(0,0,0,0.3);">
<div style="font-size:1.18em;font-weight:700;color:#ffffff;margin-bottom:10px;line-height:1.5;">
{narrative_html}
</div>
<div style="border-top:1px solid rgba(255,255,255,0.2);padding-top:10px;margin-top:8px;">
<div style="font-size:1em;color:{accent};font-weight:700;margin-bottom:6px;">📊 Đồng Thuận 8 Phương Pháp Chấm Điểm (+ Thiên Văn · Vạn Vật · 40 Chuyên Gia):</div>
<div style="font-size:0.95em;color:#e2e8f0;line-height:1.6;">{consensus}</div>
</div>
<div style="border-top:1px solid rgba(255,255,255,0.2);padding-top:10px;margin-top:10px;">
<div style="font-size:1em;color:{accent};font-weight:700;margin-bottom:6px;">🎯 Lời Khuyên Trọng Tâm:</div>
<div style="font-size:0.95em;color:#f1f5f9;line-height:1.6;">{advice.replace(chr(10), "<br>")}</div>
</div>
</div>'''
    return html


def _build_consensus(verdicts_dict):
    if not verdicts_dict:
        return "Chưa có dữ liệu consensus."

    PP_NAMES = {
        'km': 'Kỳ Môn', 'lh': 'Lục Hào', 'mh': 'Mai Hoa', 'tb': 'Thiết Bản',
        'ln': 'Đại Lục Nhâm', 'ta': 'Thái Ất', 'xn': 'Xem Ngày', 'tv': 'Tử Vi'
    }
    PP_ICONS = {
        'km': '🏯', 'lh': '📿', 'mh': '🌸', 'tb': '📜',
        'ln': '🔮', 'ta': '⚔️', 'xn': '📅', 'tv': '🔯'
    }

    parts = []
    cat_count = 0
    hung_count = 0
    binh_count = 0

    for pp_key, pp_name in PP_NAMES.items():
        if pp_key not in verdicts_dict:
            continue
        v = str(verdicts_dict.get(pp_key, '?')).upper()
        icon = PP_ICONS.get(pp_key, '📍')

        if 'CÁT' in v or 'CAT' in v:
            parts.append(f"{icon} {pp_name}: <b style='color:#22c55e'>CÁT</b>")
            cat_count += 1
        elif 'HUNG' in v:
            parts.append(f"{icon} {pp_name}: <b style='color:#ef4444'>HUNG</b>")
            hung_count += 1
        else:
            parts.append(f"{icon} {pp_name}: <b style='color:#eab308'>BÌNH</b>")
            binh_count += 1

    ratio = f" → <b>{cat_count} CÁT · {binh_count} BÌNH · {hung_count} HUNG</b>"
    return " | ".join(parts) + ratio


def _translate_door_for_topic(cua_name: str, category: str, q_low: str) -> str:
    """Giải nghĩa Bát Môn sát với chủ đề thực tế của người hỏi (không dùng từ sáo rỗng)."""
    c = str(cua_name or "")
    is_love = category == "TÌNH_CẢM" or any(w in q_low for w in ["yêu", "vợ", "chồng", "hôn nhân", "bạn gái", "bạn trai", "chia tay", "quay lại", "tình cảm"])
    is_health = category == "SỨC_KHỎE_GIA_ĐÌNH" or any(w in q_low for w in ["bệnh", "ốm", "đau", "khỏe", "qua khỏi", "viện"])
    is_wealth = category in ("TÀI_CHÍNH", "NHÀ_CỬA") or any(w in q_low for w in ["tiền", "đầu tư", "mua", "bán", "lãi", "lỗ", "kinh doanh", "đất", "nhà"])

    if "Hưu" in c:
        if is_love: return "Cửa Hưu Môn (Cát) — báo hiệu tình cảm êm ấm, hai bên có xu hướng nhường nhịn, hòa giải và hướng về sự bình yên gia đình"
        if is_health: return "Cửa Hưu Môn (Cát) — cơ thể được tĩnh dưỡng tốt, bệnh tình dần ổn định và phục hồi"
        return "Cửa Hưu Môn (Cát) — có quý nhân nâng đỡ, công việc diễn ra êm thấm, thuận hòa"
    if "Sinh" in c:
        if is_love: return "Cửa Sinh Môn (Cát) — tình cảm vẫn đang có sinh khí, hai bên còn nhiều sự quan tâm và vun đắp thực tế"
        if is_health: return "Cửa Sinh Môn (Đại Cát) — sinh khí dồi dào, sức sống mạnh mẽ, khả năng vượt qua bệnh tật và hồi phục rất cao"
        if is_wealth: return "Cửa Sinh Môn (Đại Cát) — cung tài lộc vượng khí, giao dịch mua bán hoặc đầu tư có cơ hội sinh lời rõ rệt"
        return "Cửa Sinh Môn (Đại Cát) — cơ hội mới đang nảy nở, mưu sự đắc lợi"
    if "Khai" in c:
        if is_love: return "Cửa Khai Môn (Cát) — tâm lý cởi mở, sẵn sàng trò chuyện thẳng thắn để tháo gỡ hiểu lầm"
        return "Cửa Khai Môn (Đại Cát) — công việc, danh vị và cơ hội đang mở rộng hanh thông"
    if "Đỗ" in c:
        if is_love: return "Cửa Đỗ Môn — đối phương đang có tâm lý khép lòng, giữ kín suy nghĩ riêng hoặc chọn cách im lặng chứ chưa bộc lộ hết cảm xúc thật"
        if is_health: return "Cửa Đỗ Môn — khí huyết hoặc tiến trình hồi phục đang hơi chững lại, cần khám kỹ các triệu chứng tiềm ẩn"
        if is_wealth: return "Cửa Đỗ Môn — dòng tiền hoặc giao dịch đang tạm thời bị nghẽn, chưa thể thanh khoản nhanh ngay lập tức"
        return "Cửa Đỗ Môn — sự việc đang tạm thời khép kín hoặc trì hoãn, cần kiên nhẫn tháo gỡ từng nút thắt"
    if "Cảnh" in c:
        if is_love: return "Cửa Cảnh Môn — bề ngoài dễ có lời nói nóng nảy hoặc sĩ diện nhất thời nhưng thực chất vẫn rất để tâm đến đối phương"
        return "Cửa Cảnh Môn — thuận lợi về giấy tờ, thông tin, thi cử nhưng cần chú ý giữ lời ăn tiếng nói"
    if "Thương" in c:
        if is_love: return "Cửa Thương Môn — hai bên đang có sự tổn thương về lời nói, tự ái hoặc va chạm cảm xúc cần thời gian xoa dịu"
        if is_health: return "Cửa Thương Môn — cơ thể đang chịu đau nhức hoặc suy giảm thể lực, cần nghỉ ngơi và điều trị sát sao"
        return "Cửa Thương Môn — dễ có sự va chạm, cạnh tranh hoặc đòi nợ/thu hồi công nợ cần sự quyết liệt"
    if "Kinh" in c:
        if is_love: return "Cửa Kinh Môn — tâm lý đang lo âu, bất an, nghi ngờ hoặc vừa trải qua cuộc tranh luận căng thẳng"
        return "Cửa Kinh Môn — có tâm lý lo lắng, hồi hộp hoặc tranh biện pháp lý cần giữ vững bản lĩnh"
    if "Tử" in c:
        if is_love: return "Cửa Tử Môn — cảm xúc đang bị dồn nén nặng nề, lạnh nhạt hoặc bế tắc, tuyệt đối không nên thúc ép lúc này"
        if is_health: return "Cửa Tử Môn — sinh khí đang suy giảm mạnh, cần đặc biệt cẩn trọng và ưu tiên phác đồ y tế chuyên sâu"
        return "Cửa Tử Môn — cục diện đang bế tắc, cần kiên nhẫn chờ qua giai đoạn trầm lắng"
    return f"Cửa {c}"


def extract_deep_divination_dossier(
    question: str,
    dung_than: str,
    hanh_dt: str = "",
    weighted_pct: int = 50,
    category: str = "CHUNG",
    chart_data: dict = None,
    luc_hao_data: dict = None,
    mai_hoa_data: dict = None,
    ts_stage: str = "",
    nk_stage: str = "",
) -> dict:
    """
    V100.1 — HỒ SƠ LUẬN GIẢI CHUYÊN SÂU SÁT CÂU HỎI:
    Phân tích đúng Cung Dụng Thần Kỳ Môn theo chủ đề, đúng Hào Dụng Thần (hoặc Phục Thần) và Thế-Ứng Lục Hào,
    cùng quan hệ Thể-Dụng Mai Hoa — hoàn toàn loại bỏ các câu từ điển rời rạc vô nghĩa.
    """
    res = {
        "km_palace_prose": "",
        "km_cach_cuc_prose": "",
        "km_topic_forensic": "",
        "lh_hexagram_prose": "",
        "lh_hao_dong_prose": "",
        "lh_luc_thu_prose": "",
        "mh_the_dung_prose": "",
        "short_classical_badge": "",
        "prompt_dossier": "",
    }
    q_low = (question or "").lower()
    chart_data = chart_data if isinstance(chart_data, dict) else {}
    luc_hao_data = luc_hao_data if isinstance(luc_hao_data, dict) else {}
    mai_hoa_data = mai_hoa_data if isinstance(mai_hoa_data, dict) else {}

    try:
        from luc_hao_ky_mon_rules import (
            THAP_CAN_KHAC_UNG, BAT_MON_BAY_CUNG, LUC_THAN_Y_NGHIA, PHUC_THAN_RULES, tra_ban_cung
        )
    except Exception:
        THAP_CAN_KHAC_UNG, BAT_MON_BAY_CUNG, LUC_THAN_Y_NGHIA, PHUC_THAN_RULES = {}, {}, {}, {}
        tra_ban_cung = lambda x: (None, None)

    try:
        from kinh_dich_64_que import tra_kinh_dich, tra_the_dung
    except Exception:
        tra_kinh_dich = lambda x: None
        tra_the_dung = lambda x, y: None

    # ── 1. PHÂN TÍCH KỲ MÔN ĐỘN GIÁP THEO ĐÚNG CUNG CHỦ ĐỀ ──
    target_cung, bt_cung, role_label = _resolve_authentic_km_palace(chart_data, dung_than, question, category)
    ctb = chart_data.get("can_thien_ban", {}) or {}
    dia_ban = chart_data.get("can_dia_ban") or chart_data.get("dia_ban") or chart_data.get("dia_can") or {}
    thien_ban = chart_data.get("thien_ban", {}) or {}
    nhan_ban = chart_data.get("nhan_ban", {}) or {}
    than_ban = chart_data.get("than_ban", {}) or {}

    if target_cung:
        c_thien = str(ctb.get(target_cung, ctb.get(str(target_cung), "")) or "")
        c_dia = str(dia_ban.get(target_cung, dia_ban.get(str(target_cung), "")) or "")
        if not c_dia:
            _default_dia = {1: "Mậu", 2: "Kỷ", 3: "Canh", 4: "Tân", 5: "Mậu", 6: "Nhâm", 7: "Quý", 8: "Ất", 9: "Bính"}
            c_dia = _default_dia.get(target_cung, "")
        sao_dt = str(thien_ban.get(target_cung, thien_ban.get(str(target_cung), "")) or "")
        cua_dt = str(nhan_ban.get(target_cung, nhan_ban.get(str(target_cung), "")) or "")
        than_dt = str(than_ban.get(target_cung, than_ban.get(str(target_cung), "")) or "")
        cung_dir = DIRECTION_MAP.get(target_cung, f"Cung {target_cung}")
        h_dt_cung = CUNG_HANH.get(target_cung, "Thổ")
        h_bt_cung = CUNG_HANH.get(bt_cung, "Thổ")

        rel_cung_str = ""
        if target_cung == bt_cung:
            rel_cung_str = "đồng cung với Bản Mệnh của bạn, cho thấy sự việc gắn chặt trực tiếp với quyết định và tâm thế của chính bạn"
        elif NGU_HANH_SINH.get(h_dt_cung) == h_bt_cung:
            rel_cung_str = f"tương sinh cho Cung Bản Mệnh (Cung {bt_cung} hành {h_bt_cung}), báo hiệu hoàn cảnh hoặc đối phương vẫn đang hướng về và nâng đỡ bạn"
        elif h_dt_cung == h_bt_cung:
            rel_cung_str = f"tỷ hòa (cùng hành {h_dt_cung}) với Cung Bản Mệnh, phản ánh sự đồng điệu và khả năng tìm được tiếng nói chung"
        elif NGU_HANH_SINH.get(h_bt_cung) == h_dt_cung:
            rel_cung_str = f"được Cung Bản Mệnh của bạn ({h_bt_cung}) sinh xuất cho, nghĩa là bạn đang là người nặng lòng, chủ động vun đắp và bỏ nhiều tâm sức hơn"
        elif NGU_HANH_KHAC.get(h_bt_cung) == h_dt_cung:
            rel_cung_str = f"chịu sự chế khắc từ Cung Bản Mệnh của bạn ({h_bt_cung} khắc {h_dt_cung}), cho thấy bạn có quyền chủ động nhưng nếu nóng vội dễ tạo áp lực"
        else:
            rel_cung_str = f"đang khắc Cung Bản Mệnh của bạn ({h_dt_cung} khắc {h_bt_cung}), phản ánh sức ép, sự giận dỗi hoặc lực cản khách quan đang đè nặng"

        door_meaning = _translate_door_for_topic(cua_dt, category, q_low) if cua_dt and cua_dt != "?" else ""
        res["km_palace_prose"] = (
            f"Trên bàn <b>Kỳ Môn Độn Giáp</b>, {role_label} tọa tại <b>Cung {target_cung} ({cung_dir} — hành {h_dt_cung})</b>, "
            f"{rel_cung_str}. Tại cung này hiện diện sao <b>{sao_dt or 'Thiên Cầm'}</b>, thần <b>{than_dt or 'Trực Phù'}</b> "
            + (f"và <b>{door_meaning}</b>." if door_meaning else ".")
        )

        if c_thien and c_dia:
            cc_key = f"{c_thien}+{c_dia}"
            cc_info = THAP_CAN_KHAC_UNG.get(cc_key, {})
            if cc_info:
                ten_cc = cc_info.get("ten", cc_key)
                ch_cc = cc_info.get("cat_hung", "BÌNH")
                res["short_classical_badge"] = f"cách cục Lưu Bá Ôn <b>«{ten_cc}» ({cc_key})</b> tại {cung_dir}"
                if "CÁT" in ch_cc.upper():
                    cc_explain = "mang năng lượng hanh thông, giúp hóa giải bế tắc và mở ra cơ hội thuận lợi"
                elif "HUNG" in ch_cc.upper():
                    cc_explain = "báo hiệu giai đoạn đầu có sự trì trệ, hiểu lầm hoặc vướng mắc cần kiên nhẫn tháo gỡ từng bước, tránh nóng vội"
                else:
                    cc_explain = "báo hiệu thế cuộc trước khó sau dễ, cần điềm tĩnh giải quyết từng khúc mắc thì cuối cùng mới êm đẹp"
                res["km_cach_cuc_prose"] = (
                    f"Sự kết hợp giữa Thiên Can <b>{c_thien}</b> và Địa Can <b>{c_dia}</b> lập thành cách cục Lưu Bá Ôn <b>«{ten_cc}» ({cc_key})</b>, {cc_explain}."
                )

    # ── 2. PHÂN TÍCH LỤC HÀO KINH DỊCH & MAI HOA DỊCH SỐ ──
    if luc_hao_data:
        ban = luc_hao_data.get("ban", {}) or {}
        bien = luc_hao_data.get("bien", {}) or {}
        dong_hao = luc_hao_data.get("dong_hao", []) or []
        haos = ban.get("haos") or ban.get("details") or []
        bien_haos = bien.get("haos") or bien.get("details") or []
        ban_name = ban.get("name", "")
        bien_name = bien.get("name", "")

        lh_parts = []
        if ban_name:
            kd_ban = tra_kinh_dich(ban_name) or {}
            bc_cung, bc_hanh = tra_ban_cung(ban_name)
            cung_txt = f" (thuộc cung <b>{bc_cung}</b> hành <b>{bc_hanh}</b>)" if bc_cung else ""
            yn_ban = kd_ban.get("y_nghia", "")
            lh_parts.append(
                f"Xét theo <b>Lục Hào Kinh Dịch</b>, quẻ chủ lập được là <b>{ban_name}</b>{cung_txt}"
                + (f" — mang ý tượng cốt lõi là <i>«{yn_ban.rstrip('.')}»</i>" if yn_ban else "")
            )
            if bien_name and bien_name != ban_name:
                kd_bien = tra_kinh_dich(bien_name) or {}
                yn_bien = kd_bien.get("y_nghia", "")
                lh_parts.append(
                    f"chuyển biến sang quẻ <b>{bien_name}</b>"
                    + (f" (ý tượng <i>«{yn_bien.rstrip('.')}»</i>)" if yn_bien else "")
                    + ", cho thấy cục diện không đứng yên mà đang chuyển hóa sang giai đoạn mới"
                )
        if lh_parts:
            res["lh_hexagram_prose"] = ", ".join(lh_parts) + "."

        the_hao, ung_hao, dt_hao = None, None, None
        the_idx, ung_idx, dt_idx = None, None, None
        for idx, h in enumerate(haos):
            tu = str(h.get("the_ung", ""))
            lt = str(h.get("luc_than", ""))
            if "Thế" in tu:
                the_hao, the_idx = h, idx + 1
            elif "Ứng" in tu:
                ung_hao, ung_idx = h, idx + 1
            if lt == dung_than or (dung_than == "Bản Thân" and "Thế" in tu):
                dt_hao, dt_idx = h, idx + 1

        hao_details = []
        if dt_hao:
            dt_cc = dt_hao.get("can_chi", "") or dt_hao.get("chi", "")
            dt_nh = dt_hao.get("ngu_hanh", "")
            dt_vs = dt_hao.get("vuong_suy", "")
            dt_lthu = dt_hao.get("luc_thu") or dt_hao.get("luc_than_kd") or dt_hao.get("luc_than_td") or ""
            hao_details.append(
                f"Hào Dụng Thần <b>{dung_than}</b> hiện rõ tại <b>Hào {dt_idx} ({dt_cc} — hành {dt_nh})</b>"
                + (f", so với Lệnh Tháng đạt trạng thái <b>{dt_vs}</b>" if dt_vs else "")
            )
            if dt_lthu and dt_lthu in LUC_THAN_Y_NGHIA:
                lt_info = LUC_THAN_Y_NGHIA[dt_lthu]
                hao_details.append(
                    f"đi cùng Lục Thú <b>{dt_lthu}</b> ({lt_info.get('y_nghia', '').rstrip('.')})"
                )
                res["lh_luc_thu_prose"] = f"Lục Thú <b>{dt_lthu}</b> lâm Dụng Thần"
        else:
            hao_details.append(
                f"Đáng chú ý, hào Dụng Thần <b>{dung_than}</b> hiện không lộ diện trên 6 hào chính mà ẩn dưới dạng <b>Phục Thần</b> — "
                f"điều này giải thích vì sao tâm tư thật sự của đối phương hoặc kết quả của sự việc vẫn đang giấu kín bên trong, phải chờ tới ngày Xung Phi hoặc Xuất Không mới bộc lộ rõ ràng"
            )

        if the_hao and ung_hao:
            t_cc = the_hao.get("chi", "") or the_hao.get("can_chi", "")
            u_cc = ung_hao.get("chi", "") or ung_hao.get("can_chi", "")
            t_nh = the_hao.get("ngu_hanh", "")
            u_nh = ung_hao.get("ngu_hanh", "")
            tu_rel_meaning = "phản ánh mối liên hệ trực tiếp giữa bạn và đối phương/mục tiêu"
            if NGU_HANH_SINH.get(u_nh) == t_nh:
                tu_rel_meaning = f"Ứng sinh Thế ({u_nh} sinh {t_nh}), chứng tỏ đối phương hoặc hoàn cảnh thực chất vẫn hướng về và có tình cảm/sự nâng đỡ dành cho bạn"
            elif NGU_HANH_SINH.get(t_nh) == u_nh:
                tu_rel_meaning = f"Thế sinh Ứng ({t_nh} sinh {u_nh}), cho thấy bạn là người nặng tình, quan tâm và chủ động hy sinh nhiều hơn trong việc này"
            elif t_nh and t_nh == u_nh:
                tu_rel_meaning = f"Thế và Ứng Tỷ Hòa (cùng hành {t_nh}), báo hiệu hai bên vẫn có sự đồng cảm và sợi dây gắn kết bền chặt"
            elif NGU_HANH_KHAC.get(u_nh) == t_nh:
                tu_rel_meaning = f"Ứng khắc Thế ({u_nh} khắc {t_nh}), báo hiệu phía đối phương đang có sự giận dỗi, bất mãn hoặc hoàn cảnh đang gây sức ép lên bạn"
            elif NGU_HANH_KHAC.get(t_nh) == u_nh:
                tu_rel_meaning = f"Thế khắc Ứng ({t_nh} khắc {u_nh}), cho thấy bạn đang nắm phần chủ động nhưng cần tránh thái độ áp đặt"

            hao_details.append(
                f"Xét trục <b>Hào Thế (Hào {the_idx} {t_cc}/{t_nh} — Bản thân)</b> và <b>Hào Ứng (Hào {ung_idx} {u_cc}/{u_nh} — Đối phương/Mục tiêu)</b>: {tu_rel_meaning}"
            )

        if dong_hao and haos:
            dong_descs = []
            for d_idx in dong_hao[:2]:
                if 1 <= d_idx <= len(haos):
                    h_d = haos[d_idx - 1]
                    d_lt = h_d.get("luc_than", "?")
                    d_cc = h_d.get("can_chi", "") or h_d.get("chi", "")
                    d_nh = h_d.get("ngu_hanh", "")
                    b_str = ""
                    if bien_haos and d_idx <= len(bien_haos):
                        h_b = bien_haos[d_idx - 1]
                        b_lt = h_b.get("luc_than", "")
                        b_cc = h_b.get("can_chi", "") or h_b.get("chi", "")
                        b_nh = h_b.get("ngu_hanh", "")
                        b_str = f" hóa sang <b>{b_lt} ({b_cc}/{b_nh})</b>"
                    dong_descs.append(f"Hào {d_idx} (<b>{d_lt} {d_cc}/{d_nh}</b>) phát động{b_str}")
            if dong_descs:
                hao_details.append("Điểm chuyển động của quẻ nằm ở " + ", cùng với ".join(dong_descs))

        if hao_details:
            res["lh_hao_dong_prose"] = ". ".join(hao_details) + "."

    if mai_hoa_data:
        the_hanh = mai_hoa_data.get("upper_element") or mai_hoa_data.get("hanh_thuong") or ""
        dung_hanh = mai_hoa_data.get("lower_element") or mai_hoa_data.get("hanh_ha") or ""
        dong_mh = mai_hoa_data.get("dong_hao", 1)
        try:
            from mai_hoa_dich_so import QUAI_ELEMENTS, QUAI_NAMES
            u_q = mai_hoa_data.get("upper") or mai_hoa_data.get("thuong_quai") or 0
            l_q = mai_hoa_data.get("lower") or mai_hoa_data.get("ha_quai") or 0
            if isinstance(dong_mh, int) and dong_mh <= 3:
                the_q, dung_q = u_q, l_q
            else:
                the_q, dung_q = l_q, u_q
            the_hanh = QUAI_ELEMENTS.get(the_q, the_hanh)
            dung_hanh = QUAI_ELEMENTS.get(dung_q, dung_hanh)
            the_q_name = QUAI_NAMES.get(the_q, "")
            dung_q_name = QUAI_NAMES.get(dung_q, "")
        except Exception:
            the_q_name, dung_q_name = "", ""

        if the_hanh and dung_hanh and tra_the_dung:
            td_info = tra_the_dung(the_hanh, dung_hanh) or {}
            if td_info:
                qh_td = td_info.get("quan_he", "")
                ct_td = td_info.get("chi_tiet", "").rstrip(".")
                res["mh_the_dung_prose"] = (
                    f"Đồng thời theo <b>Mai Hoa Dịch Số</b>, quẻ Thể ({the_q_name + ' ' if the_q_name else ''}hành <b>{the_hanh}</b> — đại diện cho bạn) "
                    f"và quẻ Dụng ({dung_q_name + ' ' if dung_q_name else ''}hành <b>{dung_hanh}</b> — đại diện cho sự việc) lập thế <b>{qh_td}</b> ({ct_td.lower()})."
                )

    dossier_lines = []
    for k_name, label_name in [
        ("lh_hexagram_prose", "Quẻ Chủ & Quẻ Biến Kinh Dịch"),
        ("lh_hao_dong_prose", "Chi Tiết Hào Dụng Thần, Thế/Ứng & Hào Động"),
        ("km_palace_prose", "Cung Dụng Thần Kỳ Môn Độn Giáp"),
        ("km_cach_cuc_prose", "Cách Cục Thiên Địa Bàn"),
        ("mh_the_dung_prose", "Mai Hoa Thể Dụng"),
    ]:
        val = res.get(k_name, "")
        if val:
            clean_v = re.sub(r"<[^>]+>", "", val)
            dossier_lines.append(f"• {label_name}: {clean_v}")
    res["prompt_dossier"] = "\n".join(dossier_lines)
    return res


def build_connected_prose_analysis(
    question: str,
    dung_than: str,
    weighted_pct: int,
    category: str = "CHUNG",
    ky_mon_verdict: str = "BÌNH",
    ky_mon_reason: str = "",
    luc_hao_verdict: str = "BÌNH",
    luc_hao_reason: str = "",
    mai_hoa_verdict: str = "BÌNH",
    mai_hoa_reason: str = "",
    thiet_ban_verdict: str = "BÌNH",
    thiet_ban_reason: str = "",
    luc_nham_verdict: str = "BÌNH",
    luc_nham_reason: str = "",
    thai_at_verdict: str = "BÌNH",
    thai_at_reason: str = "",
    xem_ngay_verdict: str = "BÌNH",
    xem_ngay_reason: str = "",
    tu_vi_verdict: str = "BÌNH",
    tu_vi_reason: str = "",
    thien_van_reason: str = "",
    exp_html_items: list = None,
    warn_parts: list = None,
    thoan_name: str = "",
    thoan_info: dict = None,
    ts_stage: str = "",
    ts_info: dict = None,
    nk_stage: str = "",
    nk_info: dict = None,
    hanh_dt: str = "",
    ung_ky_str: str = "",
    advice_parts: list = None,
    chart_data: dict = None,
    luc_hao_data: dict = None,
    mai_hoa_data: dict = None,
) -> str:
    """
    V100.1 — BÀI LUẬN GIẢI CHUYÊN SÂU 3 ĐOẠN MẠCH LẠC, DỄ HIỂU, SÁT CÂU HỎI 100%:
    1. Giải mã trực diện bản chất sự việc & Nội tình qua Lục Hào Kinh Dịch – Mai Hoa Dịch Số.
    2. Phân tích tâm lý, hoàn cảnh & cơ hội/trở ngại qua Bàn Kỳ Môn Độn Giáp & Đại Lục Nhâm.
    3. Dự báo thời điểm chuyển biến (Ứng Kỳ) & Lời khuyên hành động thực tế từ Hội Đồng 40 Chuyên Gia AI.
    """
    q_low = (question or "").lower()
    thoan_info = thoan_info if isinstance(thoan_info, dict) else {}
    ts_info = ts_info if isinstance(ts_info, dict) else {}
    nk_info = nk_info if isinstance(nk_info, dict) else {}
    exp_html_items = exp_html_items or []
    warn_parts = warn_parts or []
    advice_parts = advice_parts or []

    dossier = extract_deep_divination_dossier(
        question=question,
        dung_than=dung_than,
        hanh_dt=hanh_dt,
        weighted_pct=weighted_pct,
        category=category,
        chart_data=chart_data,
        luc_hao_data=luc_hao_data,
        mai_hoa_data=mai_hoa_data,
        ts_stage=ts_stage,
        nk_stage=nk_stage,
    )

    # ── ĐOẠN 1: BẢN CHẤT HIỆN TẠI & NỘI TÌNH QUA QUẺ KINH DỊCH (LỤC HÀO & MAI HOA) ──
    p1_parts = []
    if dossier.get("lh_hexagram_prose"):
        p1_parts.append(dossier["lh_hexagram_prose"])
    if dossier.get("lh_hao_dong_prose"):
        p1_parts.append(dossier["lh_hao_dong_prose"])
    if dossier.get("mh_the_dung_prose"):
        p1_parts.append(dossier["mh_the_dung_prose"])
    if ts_stage and hanh_dt and hanh_dt != "?":
        cap_ts = ts_info.get("cap", "")
        power_ts = ts_info.get("power", 50)
        ts_meaning = "đang có nội lực tích cực trên Nhật Thần" if int(power_ts or 50) >= 60 else ("đang ở thế cân bằng trên Nhật Thần" if int(power_ts or 50) >= 45 else "đang tạm thời suy giảm trên Nhật Thần, cần bồi đắp và kiên nhẫn")
        p1_parts.append(
            f"Xét vòng 12 Trường Sinh, Dụng Thần <b>{dung_than}</b> (hành <b>{hanh_dt}</b>) đạt trạng thái <b>{ts_stage}</b> ({cap_ts}), cho thấy bản khí của hào {ts_meaning}."
        )
    paragraph_1 = " ".join(p1_parts)

    # ── ĐOẠN 2: THẤU THỊ HOÀN CẢNH & NGUYÊN NHÂN SÂU XA QUA KỲ MÔN ĐỘN GIÁP & ĐẠI LỤC NHÂM ──
    p2_parts = []
    if dossier.get("km_palace_prose"):
        p2_parts.append(dossier["km_palace_prose"])
    if dossier.get("km_cach_cuc_prose"):
        p2_parts.append(dossier["km_cach_cuc_prose"])

    km_lh_mh_raw = f"{ky_mon_reason} | {luc_hao_reason} | {mai_hoa_reason}".upper()
    nuances = []
    if "KHÔNG VONG" in km_lh_mh_raw or "TUẦN KHÔNG" in km_lh_mh_raw:
        nuances.append("cung quẻ gặp <b>Tuần Không</b>, tạo ra cảm giác chững lại hoặc đối phương đang giữ một khoảng lặng tâm lý cần chờ đến ngày Xuất Không mới sáng tỏ")
    if "NHẬP MỘ" in km_lh_mh_raw:
        nuances.append("khí lực tạm thời <b>Nhập Mộ</b> (bị thu giữ hoặc bó hẹp), cần chờ thời điểm Xung Mộ để khai thông")
    if "TAM HÌNH" in km_lh_mh_raw:
        nuances.append("xuất hiện thế <b>Tam Hình</b>, báo hiệu có sự tự ái ngầm hoặc căng thẳng tâm lý cần cư xử mềm mỏng, khéo léo")
    if nuances:
        p2_parts.append("Lưu ý thêm trên bàn quẻ: " + "; đồng thời ".join(nuances) + ".")

    ln_up = str(luc_nham_reason or "").upper()
    if "SƠ TRUYỀN" in ln_up or "MẠT TRUYỀN" in ln_up:
        if "MẠT TRUYỀN SINH CAN" in ln_up or "TUONG LAI TOT" in ln_up or "KQ TỐT" in ln_up:
            p2_parts.append("Đối chiếu thêm <b>Tam Truyền Đại Lục Nhâm</b>, tuy giai đoạn đầu (Sơ Truyền) có chút băn khoăn, chậm trễ nhưng càng về kết cục (Mạt Truyền) thì khí số lại tương sinh thuận lợi.")
        else:
            p2_parts.append("Đối chiếu thêm <b>Tam Truyền Đại Lục Nhâm</b>, diễn biến từ lúc khởi sự (Sơ Truyền) đến kết cục (Mạt Truyền) đòi hỏi sự bình tĩnh điều tiết từng bước, không nên đốt cháy giai đoạn.")

    paragraph_2 = " ".join(p2_parts)

    # ── ĐOẠN 3: ĐÚC KẾT TỪ HỘI ĐỒNG 40 CHUYÊN GIA AI, THỜI ĐIỂM ỨNG KỲ & PHÁP QUYẾT HÀNH ĐỘNG ──
    p3_parts = []
    is_lost_q = category == "TÌM_ĐỒ" or any(w in q_low for w in ["bị mất", "mất chiếc", "mất đồ", "mất ví", "thất lạc", "tìm lại", "ở đâu"])
    if exp_html_items:
        clean_exps = []
        for item in exp_html_items:
            txt = re.sub(r'<[^>]+>', '', str(item)).lstrip('• ').strip()
            if any(prefix in txt for prefix in ["Chart Interpreter AI", "Luc Hao Expert AI", "Mai Hoa Expert AI"]):
                continue
            if is_lost_q and "Wealth Advisor AI" in txt:
                continue
            txt = re.sub(r'^[^\w]*(Relationship AI|Wealth Advisor AI|Career Advisor AI|Health Advisor AI|Direction Advisor AI|Feng Shui AI|Dream Interpreter AI|Scheduler AI):\s*', '', txt)
            txt = txt.replace('→', ' cho thấy ').replace('—', ' — ').strip(' .;,-')
            if txt and len(clean_exps) < 2:
                clean_exps.append(txt)
        if clean_exps:
            p3_parts.append("Hội chẩn chuyên sâu từ <b>Hội Đồng 40 Chuyên Gia AI</b> cho thấy: " + "; ".join(clean_exps) + ".")

    direction = _extract_direction(chart_data, dung_than, question, category)
    clean_advs = [re.sub(r'<[^>]+>', '', str(a)).strip() for a in advice_parts if str(a).strip()]
    if clean_advs:
        p3_parts.append("<b>Lời khuyên hành động thiết thực dành cho bạn:</b> " + " ".join(clean_advs))
    if ung_ky_str and ung_ky_str != "?" and "chưa rõ" not in ung_ky_str.lower():
        p3_parts.append(f"<b>Mốc thời gian Ứng Kỳ quan trọng:</b> Dự báo sự việc sẽ có chuyển biến hoặc câu trả lời rõ nét nhất vào khoảng <b>{ung_ky_str}</b> (phương vị cát lợi hỗ trợ: <b>{direction}</b>).")

    paragraph_3 = " ".join(p3_parts)

    return (
        f'<div style="margin-top:14px;padding:18px 20px;background:rgba(15,23,42,0.58);border-radius:14px;border:1px solid rgba(110,231,183,0.4);line-height:1.78;font-size:0.98em;color:#f1f5f9;">'
        f'<div style="font-size:1.08em;font-weight:800;color:#6ee7b7;margin-bottom:10px;border-bottom:1px solid rgba(110,231,183,0.25);padding-bottom:6px;">'
        f'📖 BÀI LUẬN GIẢI THẦN ĐOÁN CỔ THƯ HỢP NHẤT V100.1 (10 HỆ THỐNG · 19 CỔ THƯ · 40 CHUYÊN GIA AI)</div>'
        f'<p style="margin:0 0 12px 0;text-align:justify;color:#e2e8f0;"><b>1. Bản chất hiện tại & Nội tình qua Quẻ Kinh Dịch (Lục Hào & Mai Hoa):</b> {paragraph_1}</p>'
        f'<p style="margin:0 0 12px 0;text-align:justify;color:#e2e8f0;"><b>2. Giải mã tâm lý, hoàn cảnh & nguyên nhân qua Bàn Kỳ Môn Độn Giáp:</b> {paragraph_2}</p>'
        + (f'<p style="margin:0;text-align:justify;color:#fef3c7;"><b>3. Đúc kết từ Hội Đồng 40 Chuyên Gia AI, Ứng Kỳ & Pháp quyết hành động:</b> {paragraph_3}</p>' if paragraph_3 else '')
        + f'</div>'
    )
