"""
offline_brain.py — V99.7: Não Suy Luận Ngôn Ngữ Tự Nhiên AI Nội Bộ
Biến dữ liệu thô (verdicts, factors, %) thành câu trả lời ngôn ngữ tự nhiên chuẩn xác,
nhất quán 100% với phân tích học thuật và không lộ ký tự Markdown thô trong HTML.
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
# 1. FACTOR CONNECTOR — Phân loại chuẩn xác theo dấu điểm (+N/-N) & ngữ nghĩa
# ═══════════════════════════════════════════════════════════════
def _humanize_single_factor(f_raw: str) -> tuple:
    """
    Chuyển đổi 1 mã yếu tố kỹ thuật (VD: 'DT Vượng +10', 'PHỤC THẦN: DT ẩn -10')
    thành (loại_tốt_xấu, cụm_từ_tiếng_Việt_tự_nhiên_dễ_hiểu).
    """
    s = str(f_raw or "").strip()
    if not s:
        return ("neutral", "")
    up = s.upper()

    # Nhận diện các yếu tố cốt lõi bằng ngôn ngữ đời thường dễ hiểu
    if "PHỤC THẦN" in up:
        return ("bad", "yếu tố chính đang ẩn mình (Phục Thần) nên tâm ý hoặc kết quả thật sự vẫn giấu kín bên trong, chưa bộc lộ rõ ra ngoài")
    if "TUẦN KHÔNG" in up or "KHÔNG VONG" in up:
        return ("bad", "cung quẻ tạm thời rơi vào khoảng lặng (Tuần Không), khiến sự việc có cảm giác chững lại hoặc còn khoảng cách vô hình")
    if "NGUYỆT PHÁ" in up or "NHẬT PHÁ" in up:
        return ("bad", "đang chịu lực xung phá trực tiếp từ thời vận hiện tại (Nguyệt/Nhật Phá), dễ phát sinh xáo trộn hoặc áp lực")
    if "TAM HÌNH" in up:
        return ("bad", "có thế Tam Hình gây ra sự gượng gạo, tự ái ngầm hoặc căng thẳng tâm lý cần khéo léo tháo gỡ")
    if "NHẬP MỘ" in up:
        return ("bad", "khí lực đang bị thu giữ (Nhập Mộ), làm cho tâm trạng hoặc tiến độ bị bó hẹp, bế tắc tạm thời")
    if "PHẢN NGÂM" in up:
        return ("bad", "quẻ gặp thế Phản Ngâm nên tình thế dễ thay đổi thất thường, lúc nóng lúc lạnh")
    if "PHỤC NGÂM" in up:
        return ("bad", "quẻ gặp thế Phục Ngâm khiến sự việc dây dưa kéo dài, khó giải quyết dứt điểm ngay một sớm một chiều")
    if "CUNG BT SINH DT" in up or "CUNG DT TƯƠNG SINH BT" in up or "CUNG SV SINH BT" in up:
        return ("good", "giữa bản thân bạn và đối phương/mục tiêu vẫn có sự tương sinh, quan tâm và nâng đỡ lẫn nhau")
    if "CUNG BT KHẮC DT" in up or "CHỦ THẮNG" in up:
        return ("good", "bạn đang nắm thế chủ động và có khả năng xoay chuyển tình thế")
    if "CUNG DT KHẮC BT" in up:
        return ("bad", "phía đối phương hoặc hoàn cảnh bên ngoài đang tạo sức ép ngược lại lên bạn")
    if "NGUYÊN THẦN VƯỢNG" in up or "NGUYÊN THẦN ĐỘNG" in up or ("NGUYÊN THẦN" in up and ("+6" in s or "+8" in s or "+4" in s)):
        return ("good", "có nguồn lực hậu thuẫn và quý nhân âm thầm tiếp sức ở phía sau (Nguyên Thần vượng)")
    if "KỴ THẦN SUY" in up or ("KỴ THẦN" in up and ("+3" in s or "YẾU" in up)):
        return ("good", "các tác nhân gây cản trở hoặc bất đồng đã suy yếu dần")
    if "KỴ THẦN VƯỢNG" in up or "KỴ THẦN ĐỘNG" in up:
        return ("bad", "yếu tố cản trở (Kỵ Thần) đang hoạt động mạnh gây thêm thử thách")
    if "DT VƯỢNG" in up or "DT TƯỚNG" in up or "THỂ VƯỢNG" in up:
        return ("good", "nội lực gốc của sự việc rất vượng và có nền tảng vững chắc")
    if "DT TÙ" in up or "DT TỬ" in up or "DT SUY" in up or "CAN DT TỬ" in up:
        return ("bad", "năng lượng ở thời điểm hiện tại đang hơi trầm lắng và suy giảm")
    if "NGUYỆT" in up and "SINH DT" in up:
        return ("good", "được thiên thời trong tháng ủng hộ thuận lợi")
    if "NHẬT" in up and "SINH DT" in up:
        return ("good", "được hoàn cảnh trong ngày tiếp thêm sinh khí")
    if ("NGUYỆT" in up or "NHẬT" in up) and "KHẮC DT" in up:
        return ("bad", "hoàn cảnh khách quan trước mắt đang có chút nghịch chiều, gây áp lực nhất định")
    if "TỶ HÒA" in up:
        return ("good", "hai bên có sự đồng điệu và tương thông về mặt bản chất")
    if "THỂ SINH DỤNG" in up:
        return ("bad", "bạn đang là người phải chủ động nhường nhịn, lo toan và tiêu hao nhiều tâm sức hơn")
    if "DỤNG SINH THỂ" in up:
        return ("good", "sự việc và đối phương có xu hướng thuận chiều, hướng về phía bạn")
    if "KHÔNG HIỆN" in up and "KỴ THẦN" in up:
        return ("good", "các tác nhân gây cản trở hoặc chia rẽ không xuất hiện trong quẻ")
    if "CỪU THẦN" in up and ("RẤT YẾU" in up or "KHÔNG ĐỦ SỨC" in up):
        return ("good", "các yếu tố gây nhiễu bên ngoài rất yếu, không đủ sức làm suy giảm phúc khí")
    if "DT TĨNH" in up:
        return ("bad", "hào Dụng Thần đang tĩnh nên sự việc cần thêm thời gian lắng đọng, chưa bứt phá ngay lập tức")
    if "CỪU THẦN" in up and "VƯỢNG" in up:
        return ("bad", "có chút tác động ngoại cảnh làm phân tán nguồn lực hỗ trợ")
    if any(k in up for k in ["KHÔNG TÁC ĐỘNG", "NGUYÊN THẦN ẨN", "KỴ THẦN ẨN", "NT(ẨN)", "KT(ẨN)"]):
        return ("neutral", "")

    # Nếu là chuỗi khác, chỉ lấy khi điểm số khác 0 và không phải mã kỹ thuật thô
    m_score = re.search(r'([+-]\d+)\s*$', s)
    if m_score:
        sc = int(m_score.group(1))
        if sc == 0:
            return ("neutral", "")
        cleaned = _clean_factor(s)
        cleaned = re.sub(r'[+-]\d+\b', '', cleaned)
        cleaned = re.sub(r'\b(DT|BT|SV|NT|KT|TB-\d+|LH-B\d+|KM-B\d+)\b', '', cleaned).strip(' ,;:-')
        if '(' in cleaned or '/' in cleaned or len(cleaned) < 8:
            return ("neutral", "")
        return ("good" if sc > 0 else "bad", cleaned.lower())
    return ("neutral", "")


def _connect_factors(factors_list):
    """
    V99.9.7: Biến danh sách factors thành câu văn xuôi tiếng Việt mượt mà, dễ đọc, dễ hiểu (không còn mã +10, -8 khô khan).
    """
    if not factors_list:
        return ""

    good_phrases = []
    bad_phrases = []

    for f in factors_list:
        kind, phrase = _humanize_single_factor(f)
        if not phrase or len(phrase) < 6:
            continue
        if kind == "good" and phrase not in good_phrases:
            good_phrases.append(phrase)
        elif kind == "bad" and phrase not in bad_phrases:
            bad_phrases.append(phrase)

    sentences = []
    if good_phrases and bad_phrases:
        g_txt = ", đồng thời ".join(good_phrases[:2])
        b_txt = " và ".join(bad_phrases[:2])
        sentences.append(f"Xét về mặt tích cực, quẻ cho thấy {g_txt}; tuy nhiên bạn cũng cần lưu ý rằng hiện tại {b_txt}")
    elif good_phrases:
        g_txt = ", kết hợp với việc ".join(good_phrases[:3])
        sentences.append(f"Điểm sáng rất đáng mừng trong quẻ là {g_txt}")
    elif bad_phrases:
        b_txt = ", bên cạnh đó ".join(bad_phrases[:2])
        sentences.append(f"Nguyên nhân chính gây ra trắc trở lúc này là do {b_txt}")

    return (". ".join(sentences) + ".") if sentences else ""


def _clean_factor(f):
    """Bỏ emoji thừa và ký hiệu nội bộ, giữ nội dung sạch"""
    f = str(f).replace('[HỆ SINH THÁI DT]', '').strip()
    for ch in ['⊕', '⊖', '✅', '🔴', '🟢', '🟡', '⚡', '💥', '⭕', '🔄', '☯', '△', '↗', '👻', '🔥', '⚠️']:
        f = f.replace(ch, '')
    return f.strip().strip('-').strip()


# ═══════════════════════════════════════════════════════════════
# 2. CATEGORY-SPECIFIC TEMPLATES
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
        'low': "Công việc <b>đang có lực cản hoặc tiểu nhân/áp lực</b>. {factors} Nên xử lý thận trọng từng bước, tránh quyết định nóng vội.",
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
        'low': "Xuất hành <b>gặp nhiều cản trở hoặc thời tiết/lịch trình bất lợi</b>. {factors} Nên kiểm tra kỹ an toàn hoặc điều chỉnh giờ đi.",
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


# ═══════════════════════════════════════════════════════════════
# 3. QUESTION-TYPE SPECIFIC OPENERS
# ═══════════════════════════════════════════════════════════════
def _get_qtype_opener(question, pct, category='CHUNG'):
    """Sinh câu mở đầu đúng ngữ pháp và sát bản chất câu hỏi"""
    q = (question or '').lower()
    emoji = _verdict_emoji(pct)
    label = _verdict_label(pct)

    # Nhóm 1: Câu hỏi SỨC KHỎE / BỆNH TẬT / QUA KHỎI KHÔNG
    if category == 'SỨC_KHỎE_GIA_ĐÌNH' or any(kw in q for kw in ['qua khỏi', 'qua được', 'khỏi bệnh', 'khỏi không', 'ốm', 'bệnh', 'nguy kịch', 'sống không']):
        if pct >= 55:
            return f"{emoji} <b>TIÊN LƯỢNG KHẢ QUAN — CÓ KHẢ NĂNG QUA KHỎI & HỒI PHỤC ({pct}%)</b>. "
        elif pct >= 45:
            return f"{emoji} <b>TIÊN LƯỢNG GIẰNG CO — CẦN TÍCH CỰC CHỮA TRỊ & THEO DÕI SÁT ({pct}%)</b>. "
        else:
            return f"{emoji} <b>TIÊN LƯỢNG NẶNG — NHIỀU DẤU HIỆU BẤT LỢI, CẦN CẤP CỨU/CHUYÊN KHOA NGAY ({pct}%)</b>. "

    # Nhóm 2: Câu hỏi TÌM ĐỒ / Ở ĐÂU
    if category == 'TÌM_ĐỒ' or any(kw in q for kw in ['ở đâu', 'chỗ nào', 'hướng nào', 'tìm đâu', 'tìm thấy']):
        if pct >= 55:
            return f"📍 <b>CÓ THỂ TÌM THẤY ({pct}%)</b> — "
        elif pct >= 45:
            return f"📍 <b>CƠ HỘI TÌM THẤY 50/50 ({pct}%)</b> — "
        else:
            return f"📍 <b>KHÓ TÌM LẠI / ĐÃ DI CHUYỂN XA ({pct}%)</b> — "

    # Nhóm 3: Câu hỏi KHI NÀO / BAO GIỜ
    if any(kw in q for kw in ['khi nào', 'bao giờ', 'lúc nào', 'tháng mấy', 'ngày nào']):
        return f"⏳ <b>LUẬN THỜI ĐIỂM ỨNG KỲ ({pct}% — {label}):</b> "

    # Nhóm 4: Câu hỏi CÓ NÊN HAY KHÔNG (Lời khuyên hành động)
    if any(kw in q for kw in ['có nên', 'nên không', 'nên hay']):
        if pct >= 55:
            return f"{emoji} <b>NÊN TIẾN HÀNH — {label} ({pct}%)</b>. "
        elif pct >= 45:
            return f"{emoji} <b>CÓ THỂ TIẾN HÀNH NHƯNG CẦN THẬN TRỌNG ({pct}%)</b>. "
        else:
            return f"{emoji} <b>CHƯA NÊN TIẾN HÀNH LÚC NÀY — {label} ({pct}%)</b>. "

    # Nhóm 5: Câu hỏi CÓ ĐƯỢC KHÔNG / THÀNH BẠI
    if any(kw in q for kw in ['có được', 'được không', 'có không', 'liệu có', 'không?', 'có lãi', 'thành công']):
        if pct >= 55:
            return f"{emoji} <b>CÓ / ĐẠT ĐƯỢC — {label} ({pct}%)</b>. "
        elif pct >= 45:
            return f"{emoji} <b>CÒN GIẰNG CO / CẦN NỖ LỰC THÊM ({pct}%)</b>. "
        else:
            return f"{emoji} <b>KHÓ ĐẠT / GẶP NHIỀU TRỞ NGẠI — {label} ({pct}%)</b>. "

    return f"{emoji} <b>{label} ({pct}%)</b>. "


# ═══════════════════════════════════════════════════════════════
# 4. CONTEXT INJECTOR
# ═══════════════════════════════════════════════════════════════
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


def _extract_person(question):
    q = (question or '').lower()
    for kw, label in sorted(PERSON_KEYWORDS.items(), key=lambda x: len(x[0]), reverse=True):
        if re.search(r'(?:^|[\s,;.!?])' + re.escape(kw) + r'(?:[\s,;.!?]|$)', q):
            return label
    return 'bạn'


def _extract_direction(chart_data, dung_than='Bản Thân'):
    if not chart_data or not isinstance(chart_data, dict):
        return 'Chính Bắc (Khảm)'
    cung = chart_data.get('cung_dung_than') or chart_data.get('cung_dt')
    if not cung:
        try:
            from omniscient_prophecy import _find_target_palace
            c_dt, c_sv, _, _ = _find_target_palace(dung_than, chart_data)
            cung = c_sv if (dung_than == 'Bản Thân' and c_sv != c_dt) else c_dt
        except Exception:
            cung = 1
    try:
        return DIRECTION_MAP.get(int(cung), 'Chính Bắc (Khảm)')
    except (ValueError, TypeError):
        return 'Chính Bắc (Khảm)'


# ═══════════════════════════════════════════════════════════════
# 5. ACTIONABLE ADVICE — Sinh lời khuyên chuẩn theo từng lĩnh vực
# ═══════════════════════════════════════════════════════════════
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
        advice.append("🔍 <b>Hành động ngay:</b> Tìm kiếm ngay theo phương hướng và vị trí mô tả trong Hồ sơ 360° trước khi đồ vật bị xê dịch.")
    elif category == 'TÀI_CHÍNH':
        if pct >= 55:
            advice.append("💰 <b>Chiến lược tài chính:</b> Thời điểm thuận lợi để triển khai giao dịch/đầu tư, ưu tiên lĩnh vực hợp Hành Dụng Thần.")
        elif pct >= 45:
            advice.append("⚖️ <b>Chiến lược tài chính:</b> Chỉ nên đầu tư thăm dò tỷ trọng nhỏ, kiểm tra kỹ hợp đồng và dòng tiền.")
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
    V99.7: Sinh câu trả lời TRỰC TIẾP – ĐÚNG TRỌNG TÂM CÂU HỎI (Hỏi gì đáp nấy, không chung chung).
    """
    pct = weighted_pct or 50
    q = (question or '').strip()
    q_low = q.lower()
    person = _extract_person(q)
    direction = _extract_direction(chart_data, dung_than)
    omni_data = omni_data if isinstance(omni_data, dict) else {}
    factors_text = _connect_factors(all_factors or [])
    try:
        _dos_short = extract_deep_divination_dossier(
            question=q, dung_than=dung_than, weighted_pct=pct, category=category,
            chart_data=chart_data, luc_hao_data=luc_hao_data, mai_hoa_data=mai_hoa_data
        )
        _extra_badges = []
        if _dos_short.get('short_classical_badge'):
            _extra_badges.append(_dos_short['short_classical_badge'])
        if _dos_short.get('lh_luc_thu_prose'):
            _extra_badges.append(_dos_short['lh_luc_thu_prose'])
        if _extra_badges:
            factors_text = factors_text.rstrip('.') + '. Đặc biệt theo cổ thư, quẻ hiện ' + ' kết hợp cùng '.join(_extra_badges) + '.'
    except Exception:
        pass
    uk_clean = ung_ky_str if (ung_ky_str and ung_ky_str != '?' and 'xem mục' not in ung_ky_str.lower()) else omni_data.get('exact_timestamp', 'trong chu kỳ Can Chi gần nhất')

    # 1. TRỌNG TÂM: BỆNH TẬT / SỨC KHỎE / QUA KHỎI KHÔNG
    if category == 'SỨC_KHỎE_GIA_ĐÌNH' or any(w in q_low for w in ['ốm', 'bệnh', 'đau', 'khỏe', 'qua khỏi', 'qua được', 'sống', 'nguy kịch', 'viện', 'mổ']):
        subj_lbl = person.capitalize() if person != 'bạn' else 'Người bệnh'
        co_the = omni_data.get('co_the', '') or kc_detail
        co_the_str = f" Trọng điểm cơ thể cần lưu ý: <b>{co_the}</b>." if co_the else ""
        if pct >= 55:
            head = f"🏥 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>{subj_lbl} CÓ KHẢ NĂNG QUA KHỎI & HỒI PHỤC TỐT ({pct}% — CÁT)</b>."
            body = f"Hào Dụng Thần (<b>{dung_than}</b>) và sinh khí còn vững, gặp thầy gặp thuốc cứu giải.{co_the_str} {factors_text} Dự kiến chuyển biến tích cực rõ rệt vào khoảng <b>{uk_clean}</b>."
        elif pct >= 45:
            head = f"🏥 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>TÌNH TRẠNG CỦA {subj_lbl.upper()} ĐANG GIẰNG CO — CẦN TÍCH CỰC ĐIỀU TRỊ ({pct}% — BÌNH)</b>."
            body = f"Chính khí của Dụng Thần (<b>{dung_than}</b>) và tà khí đang giằng co mạnh.{co_the_str} {factors_text} Nếu được can thiệp y tế đúng phác đồ và vượt qua mốc <b>{uk_clean}</b> thì sẽ chuyển nguy thành an."
        else:
            head = f"🏥 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>{subj_lbl.upper()} ĐANG RẤT NGUY KỊCH / TIÊN LƯỢNG NẶNG ({pct}% — HUNG)</b>."
            body = f"Quẻ báo Dụng Thần (<b>{dung_than}</b>) suy yếu hoặc lâm Tuần Không/xung khắc mạnh.{co_the_str} {factors_text} Cần lập tức ưu tiên cấp cứu/chuyên khoa tuyến trên và theo dõi đặc biệt sát sao quanh mốc <b>{uk_clean}</b>."
        return _md_to_html_bold(f"{head}<br>{body}")

    # 2. TRỌNG TÂM: TÌM ĐỒ / MẤT ĐỒ / Ở ĐÂU
    if category == 'TÌM_ĐỒ' or any(w in q_low for w in ['tìm', 'mất', 'thất lạc', 'ở đâu', 'chỗ nào', 'để đâu', 'cất đâu']):
        where_sum = omni_data.get('where_summary', f'Hướng <b>{direction}</b>')
        height_d = omni_data.get('height_desc', '')
        places_d = omni_data.get('places', '')
        loc_detail = f" Vị trí cụ thể: <b>{places_d}</b> ({height_d})." if places_d else ""
        if pct >= 55:
            head = f"📍 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CÓ THỂ TÌM LẠI ĐƯỢC ({pct}% — CÁT) — ĐANG Ở {direction.upper()}</b>."
            body = f"Đồ vật chưa mất hẳn, hiện nằm tại: {where_sum}.{loc_detail} {factors_text} Hãy tìm ngay trong khoảng <b>{uk_clean}</b>."
        elif pct >= 45:
            head = f"📍 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CƠ HỘI TÌM LẠI 50/50 ({pct}% — BÌNH) — HƯỚNG {direction.upper()}</b>."
            body = f"Đồ vật đang bị che khuất hoặc để lẫn tại: {where_sum}.{loc_detail} {factors_text} Cần tìm kỹ các ngăn/góc khuất theo hướng này quanh mốc <b>{uk_clean}</b>."
        else:
            head = f"📍 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>KHÓ TÌM LẠI / ĐÃ BỊ DI CHUYỂN XA ({pct}% — HUNG) — MANH MỐI HƯỚNG {direction.upper()}</b>."
            body = f"Quẻ báo hào Tài/Dụng Thần suy hoặc bị khắc, khả năng tìm lại thấp. Phương vị manh mối cuối cùng: {where_sum}.{loc_detail} {factors_text}"
        return _md_to_html_bold(f"{head}<br>{body}")

    # 3. TRỌNG TÂM: KHI NÀO / BAO GIỜ / THÁNG MẤY / NGÀY NÀO
    if any(w in q_low for w in ['khi nào', 'bao giờ', 'lúc nào', 'tháng mấy', 'ngày nào', 'mấy giờ', 'năm nào']):
        status_w = "THUẬN LỢI ỨNG NGHIỆM" if pct >= 55 else ("ỨNG NGHIỆM NHƯNG CHẬM TRỄ" if pct >= 45 else "BỊ TRÌ HOÃN / KHÓ ỨNG NGHIỆM SỚM")
        head = f"⏳ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>THỜI ĐIỂM ỨNG KỲ LÀ {uk_clean.upper()} ({pct}% — {status_w})</b>."
        body = f"Dựa trên sự hội tụ của Dụng Thần (<b>{dung_than}</b>) và vòng Can Chi: {factors_text} Phương hướng thuận lợi hỗ trợ: <b>{direction}</b>."
        return _md_to_html_bold(f"{head}<br>{body}")

    # 4. TRỌNG TÂM: AI / NGƯỜI NÀO / TRAI HAY GÁI / BAO NHIÊU TUỔI
    if any(w in q_low for w in ['là ai', 'người nào', 'trai hay gái', 'nam hay nữ', 'bao nhiêu tuổi', 'mấy tuổi']):
        g_str = omni_data.get('gender', 'Nam/Nữ theo quẻ')
        a_str = omni_data.get('age_tier', '')
        by_str = ", ".join(omni_data.get('birth_years', [])[:3])
        head = f"👤 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>{g_str} — {a_str} (Khoảng: {by_str})</b>."
        body = f"Người này ứng vào Dụng Thần <b>{dung_than}</b> tại hướng <b>{direction}</b>. {factors_text}"
        return _md_to_html_bold(f"{head}<br>{body}")

    # 5. TRỌNG TÂM: CÁI GÌ / ĐỒ VẬT GÌ / BAO NHIÊU / MẤY
    if any(w in q_low for w in ['cái gì', 'đồ gì', 'vật gì', 'bao nhiêu', 'có mấy', 'số lượng']):
        obj_str = omni_data.get('objects', '')
        qty_str = omni_data.get('quantity', '')
        col_str = omni_data.get('colors', '')
        head = f"📦 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>{obj_str[:120]}</b>."
        body = f"Màu sắc đặc trưng: <b>{col_str}</b> | {qty_str}. {factors_text}"
        return _md_to_html_bold(f"{head}<br>{body}")

    # 6. TRỌNG TÂM: MUA BÁN ĐẤT ĐAI / NHÀ CỬA / ĐẦU TƯ / TÀI CHÍNH / CÓ LÃI KHÔNG
    if category in ('TÀI_CHÍNH', 'NHÀ_CỬA') or any(w in q_low for w in ['mua đất', 'bán đất', 'mua nhà', 'bán nhà', 'đầu tư', 'có lãi', 'lời', 'lỗ', 'kinh doanh', 'vốn', 'tiền']):
        if pct >= 55:
            head = f"💰 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>THUẬN LỢI — CÓ LÃI & KHẢ QUAN ({pct}% — CÁT)</b>."
            body = f"Dụng Thần (<b>{dung_than}</b>) đắc khí, dòng tiền và cơ hội sinh lời tốt. {factors_text} Hướng cát lợi: <b>{direction}</b> | Mốc thời gian vượng khí: <b>{uk_clean}</b>."
        elif pct >= 45:
            head = f"💰 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CƠ HỘI TRUNG BÌNH — LỢI NHUẬN MỎNG, CẦN THẬN TRỌNG ({pct}% — BÌNH)</b>."
            body = f"Dụng Thần (<b>{dung_than}</b>) ở thế giằng co, có thể thực hiện nhưng phải đàm phán kỹ giá cả và pháp lý, tránh dùng đòn bẩy quá sức. {factors_text} Mốc ứng kỳ: <b>{uk_clean}</b>."
        else:
            head = f"💰 <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CHƯA NÊN ĐẦU TƯ / KHÓ CÓ LÃI NGAY, DỄ ĐỌNG VỐN ({pct}% — HUNG)</b>."
            body = f"Dụng Thần (<b>{dung_than}</b>) đang suy yếu hoặc chịu xung khắc/Tuần Không, xuống tiền lúc này dễ bị kẹt thanh khoản hoặc hao hụt. {factors_text} Nên giữ tiền mặt và chờ qua mốc <b>{uk_clean}</b>."
        return _md_to_html_bold(f"{head}<br>{body}")

    # 7. TRỌNG TÂM: CÔNG VIỆC / CHUYỂN VIỆC / XIN VIỆC / THI CỬ / SỰ NGHIỆP
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

    # 8. TRỌNG TÂM: TÌNH CẢM / HÔN NHÂN / VỢ CHỒNG / NGƯỜI YÊU
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
                head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>TÌNH CẢM CỦA {_target_p.upper()} ĐANG NGUỘI LẠNH / RẠN NỨT LỚN ({pct}% — HUNG)</b>."
                body = f"Hào Dụng Thần (<b>{dung_than}</b>) và trục Thế – Ứng đang xung khắc/suy yếu mạnh, báo hiệu {_target_p.lower()} đang rất mệt mỏi, bất mãn hoặc xa cách về cảm xúc. {factors_text} Cần kiên nhẫn hóa giải, tránh tranh cãi gay gắt trước mốc <b>{uk_clean}</b>."
        elif any(w in q_low for w in ['quay lại', 'hàn gắn', 'làm lành']):
            if pct >= 55:
                head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CÓ KHẢ NĂNG QUAY LẠI & HÀN GẮN THÀNH CÔNG ({pct}% — CÁT)</b>."
            elif pct >= 45:
                head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CÒN DUYÊN NỢ DÙNG DẰNG — CẦN CHỦ ĐỘNG MỀM MỎNG MỚI HÀN GẮN ĐƯỢC ({pct}% — BÌNH)</b>."
            else:
                head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>RẤT KHÓ QUAY LẠI — DUYÊN KHÍ ĐANG BẾ TẮC ({pct}% — HUNG)</b>."
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

    # 9. CÁC CÂU HỎI KHÁC (ĐỐI KHÁNG / XUẤT HÀNH / TỔNG QUÁT)
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
    factors_text = _connect_factors(all_factors)
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
    V100.0 — SIÊU NÃO THẦN ĐOÁN CỔ THƯ HỢP NHẤT:
    Khai thác trực tiếp 19 bộ cổ thư & thư viện quy tắc nâng cao trong GitHub:
    1. luc_hao_ky_mon_rules (81 Cách Cục Lưu Bá Ôn, Bát Môn Bay Cung, Sao Cửa Tổ Hợp, Can Chi Tượng Ý, Lục Thú, Phục Thần, Hào Biến)
    2. km_luan_nang_cao (4 Cách Nhìn Kỳ Môn, Nội/Ngoại Bàn Xa Gần, Vận Hạn Tứ Trụ)
    3. qmdg_knowledge_complete (Tra cứu Cửu Cung, Cửu Tinh, Bát Môn, Bát Thần, Thiên Can)
    4. qmdg_decoder & qmdg_inference_rules (Chẩn bệnh Y Dịch, Truy vết Mất Đồ, Phác họa Tướng Mạo/Tính Cách)
    5. kinh_dich_64_que, thoan_tu_64, iching_integrated_data (64 Quẻ Bản/Biến, Lục Thân 6 Chủ Đề, Mai Hoa Thể Dụng, Thiết Bản 60 Hoa Giáp)
    6. van_vat_chi_tiet & van_vat_mo_rong (60 Trạng Thái Ngũ Hành × 12 Trường Sinh, Thám Tử Mô Tả)
    7. ai_tools & skill_library (Khổng Minh Lục Diệu Âm Lịch, Học Thuật Cổ Thư)
    """
    res = {
        "km_cach_cuc_prose": "",
        "km_mon_cung_prose": "",
        "km_sao_cua_than_prose": "",
        "km_xa_gan_prose": "",
        "km_topic_forensic": "",
        "lh_hexagram_prose": "",
        "lh_hao_dong_prose": "",
        "lh_luc_thu_prose": "",
        "mh_the_dung_prose": "",
        "tb_nap_am_prose": "",
        "km_luc_dieu_prose": "",
        "van_vat_forensic": "",
        "short_classical_badge": "",
        "prompt_dossier": "",
    }
    q_low = (question or "").lower()
    chart_data = chart_data if isinstance(chart_data, dict) else {}
    luc_hao_data = luc_hao_data if isinstance(luc_hao_data, dict) else {}
    mai_hoa_data = mai_hoa_data if isinstance(mai_hoa_data, dict) else {}

    # ── 1. KỲ MÔN ĐỘN GIÁP CỔ THƯ (LƯU BÁ ÔN 81 CÁCH CỤC · BÁT MÔN BAY CUNG · 4 CÁCH NHÌN) ──
    try:
        from luc_hao_ky_mon_rules import (
            THAP_CAN_KHAC_UNG, BAT_MON_BAY_CUNG, SAO_CUA_TO_HOP, SAO_CUA_TO_HOP_BS,
            CAN_CHI_TUONG_Y, LUC_THAN_Y_NGHIA, PHUC_THAN_RULES, HAO_BIEN_RULES, tra_ban_cung
        )
    except Exception:
        THAP_CAN_KHAC_UNG, BAT_MON_BAY_CUNG, SAO_CUA_TO_HOP, SAO_CUA_TO_HOP_BS = {}, {}, {}, {}
        CAN_CHI_TUONG_Y, LUC_THAN_Y_NGHIA, PHUC_THAN_RULES, HAO_BIEN_RULES = {}, {}, {}, []
        tra_ban_cung = lambda x: (None, None)

    try:
        from km_luan_nang_cao import luan_nhin_xa_gan
    except Exception:
        luan_nhin_xa_gan = None

    try:
        from qmdg_knowledge_complete import tra_cuu_cung, tra_cuu_sao, tra_cuu_mon, tra_cuu_than
    except Exception:
        tra_cuu_cung = tra_cuu_sao = tra_cuu_mon = tra_cuu_than = lambda x: {}

    can_ngay = chart_data.get("can_ngay", "")
    chi_ngay = chart_data.get("chi_ngay", "")
    can_gio = chart_data.get("can_gio", "")
    chi_gio = chart_data.get("chi_gio", "")
    ctb = chart_data.get("can_thien_ban", {}) or {}
    dia_ban = chart_data.get("dia_ban") or chart_data.get("dia_can") or {}
    thien_ban = chart_data.get("thien_ban", {}) or {}
    nhan_ban = chart_data.get("nhan_ban", {}) or {}
    than_ban = chart_data.get("than_ban", {}) or {}

    dt_can_map = {
        "Quan Quỷ": can_gio,
        "Thê Tài": can_gio,
        "Tử Tôn": can_gio,
        "Phụ Mẫu": chart_data.get("can_nam", "") or can_gio,
        "Huynh Đệ": chart_data.get("can_thang", "") or can_gio,
        "Bản Thân": can_ngay,
    }
    dt_can = dt_can_map.get(dung_than, can_gio) or can_gio

    def _find_cung_by_can(target_c):
        if not target_c:
            return None
        for k, v in ctb.items():
            if v == target_c and str(k).isdigit():
                return int(k)
        if target_c == "Giáp":
            for k, v in ctb.items():
                if v in ("Mậu", "Kỷ") and str(k).isdigit():
                    return int(k)
        return None

    bt_cung = _find_cung_by_can(can_ngay)
    dt_cung = _find_cung_by_can(dt_can)
    sv_cung = _find_cung_by_can(can_gio)
    target_cung = dt_cung or sv_cung or bt_cung
    if dung_than == "Bản Thân" and sv_cung and sv_cung != bt_cung:
        target_cung = sv_cung

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

        # 1a. 81 Cách Cục Lưu Bá Ôn (Thập Can Khắc Ứng)
        if c_thien and c_dia:
            cc_key = f"{c_thien}+{c_dia}"
            cc_info = THAP_CAN_KHAC_UNG.get(cc_key, {})
            if cc_info:
                ten_cc = cc_info.get("ten", cc_key)
                ch_cc = cc_info.get("cat_hung", "BÌNH")
                luan_cc = cc_info.get("luan", "").rstrip(".")
                res["km_cach_cuc_prose"] = (
                    f"Tại <b>Cung {target_cung} ({cung_dir})</b> — nơi tọa đóng của Dụng Thần, "
                    f"Thiên Bàn <b>{c_thien}</b> hội Địa Bàn <b>{c_dia}</b> lập thành cách cục cổ thư Lưu Bá Ôn "
                    f"<b>«{ten_cc}» ({cc_key} — {ch_cc})</b>, sách dạy rằng: <i>«{luan_cc}»</i>."
                )
                res["short_classical_badge"] = f"cách cục Lưu Bá Ôn <b>«{ten_cc}» ({cc_key})</b> tại {cung_dir}"

        # 1b. Bát Môn Bay Cung (Đắc Tướng / Hòa Nghĩa / Môn Chế / Môn Bức / Phục-Phản Ngâm / Nhập Mộ)
        if cua_dt and cua_dt != "?":
            cua_full = cua_dt if "Môn" in cua_dt else f"{cua_dt} Môn"
            bm_info = BAT_MON_BAY_CUNG.get(cua_full, {})
            if bm_info:
                state_lbl = "bình hòa với cung vị"
                if target_cung == bm_info.get("phuc_ngam"):
                    state_lbl = "rơi vào thế <b>Môn Phục Ngâm</b> (cửa đứng yên tại bản cung, chủ về sự việc dùng dằng, nội tâm trăn trở, cần kiên nhẫn chờ thời)"
                elif target_cung == bm_info.get("phan_ngam"):
                    state_lbl = "rơi vào thế <b>Môn Phản Ngâm</b> (cửa xung đối cung, chủ về biến chuyển nhanh hoặc thay đổi kế hoạch bất ngờ)"
                elif target_cung == bm_info.get("nhap_mo"):
                    state_lbl = "lâm <b>Môn Nhập Mộ</b> (khí lực của cửa tạm thời thu liễm, bị che khuất hoặc chờ ngày Xung Mộ mới khai mở)"
                elif target_cung in (bm_info.get("buc") or []):
                    state_lbl = "phạm <b>Môn Bức (Cửa khắc Cung)</b>, báo hiệu sự việc có lực ép hoặc gượng gạo nếu cưỡng cầu"
                elif target_cung in (bm_info.get("che") or []):
                    state_lbl = "ở thế <b>Môn Chế (Cung khắc Cửa)</b>, hoàn cảnh khách quan đang kiềm chế bước tiến của hành động"
                elif target_cung in (bm_info.get("nghia") or []):
                    state_lbl = "đạt thế <b>Hòa Nghĩa (Cửa sinh Cung — Đại Cát)</b>, hành động và hoàn cảnh nâng đỡ nhau thuận lợi"
                elif target_cung in (bm_info.get("tuong") or []):
                    state_lbl = "đắc cách <b>Đắc Tướng (Cung sinh Cửa — Cát)</b>, môi trường xung quanh tiếp thêm sinh khí cho mục tiêu"
                y_nghia_mon = bm_info.get("y_nghia", "").rstrip(".")
                res["km_mon_cung_prose"] = (
                    f"Xét Nhân Bàn hành động, <b>{cua_full}</b> ({y_nghia_mon.lower() if y_nghia_mon else 'chủ về nhân hòa'}) "
                    f"bay vào Cung {target_cung} {state_lbl}."
                )

        # 1c. Tổ Hợp Sao - Cửa - Thần & Can Chi Tượng Ý
        sao_cua_parts = []
        if sao_dt and cua_dt and sao_dt != "?" and cua_dt != "?":
            cua_full = cua_dt if "Môn" in cua_dt else f"{cua_dt} Môn"
            sc_info = SAO_CUA_TO_HOP.get((sao_dt, cua_full)) or SAO_CUA_TO_HOP_BS.get((sao_dt, cua_full)) or {}
            if sc_info and sc_info.get("luan"):
                sao_cua_parts.append(
                    f"Sự hội tụ giữa Cửu Tinh <b>{sao_dt}</b> và <b>{cua_full}</b> tạo thành tổ hợp: "
                    f"<i>{sc_info.get('luan', '').rstrip('.')}</i>"
                    + (f" ({sc_info.get('ung_dung', '').rstrip('.')})" if sc_info.get("ung_dung") else "")
                )
            else:
                s_kc = tra_cuu_sao(sao_dt) or {}
                m_kc = tra_cuu_mon(cua_dt) or {}
                s_tc = s_kc.get("Tinh_Chat", "")
                m_ld = m_kc.get("Luan_Doan", "")
                if s_tc or m_ld:
                    sao_cua_parts.append(
                        f"Trên Thiên Bàn có sao <b>{sao_dt}</b> ({s_tc[:90].rstrip('.') if s_tc else 'tinh tú chủ thời cơ'}) "
                        f"đi cùng <b>{cua_full}</b> ({m_ld[:90].rstrip('.') if m_ld else 'nhân hòa'})"
                    )
        if than_dt and than_dt != "?":
            t_kc = tra_cuu_than(than_dt) or {}
            t_tc = t_kc.get("Tinh_Chat", "") or t_kc.get("Luan_Doan", "")
            if t_tc:
                sao_cua_parts.append(f"được Bát Thần <b>{than_dt}</b> ({t_tc[:100].rstrip('.')}) dẫn khí")
        if c_thien and c_thien in CAN_CHI_TUONG_Y:
            ct_info = CAN_CHI_TUONG_Y[c_thien]
            if category == "TÌNH_CẢM" or any(w in q_low for w in ["yêu", "vợ", "chồng", "hôn nhân", "tình cảm", "người yêu"]):
                sao_cua_parts.append(
                    f"tượng Thiên Can <b>{c_thien}</b> phản ánh tính cách đối phương/mối quan hệ mang nét <i>{ct_info.get('tinh_cach', '').lower()}</i>, "
                    f"trong tình cảm hôn nhân thì <i>{ct_info.get('hon_nhan', '').lower()}</i>"
                )
            elif category == "SỨC_KHỎE_GIA_ĐÌNH" or any(w in q_low for w in ["bệnh", "ốm", "đau", "khỏe", "viện"]):
                sao_cua_parts.append(
                    f"tượng Thiên Can <b>{c_thien}</b> ứng với cơ thể vùng <b>{ct_info.get('co_the', '')}</b> (tạng <b>{ct_info.get('an_tang', '')}</b>), "
                    f"dễ phát sinh chứng <i>{ct_info.get('benh', '').lower()}</i>"
                )
        if sao_cua_parts:
            res["km_sao_cua_than_prose"] = "; ".join(sao_cua_parts) + "."

        # 1d. Nội Bàn / Ngoại Bàn (Xa gần, Nhanh chậm)
        if luan_nhin_xa_gan and "is_duong_don" in chart_data:
            try:
                xg_raw = luan_nhin_xa_gan(bool(chart_data.get("is_duong_don", True)), target_cung, False, False)
                if "NỘI BÀN" in str(xg_raw).upper():
                    res["km_xa_gan_prose"] = "Cung Dụng Thần nằm ở <b>Nội Bàn</b>, báo hiệu sự việc diễn ra ở phạm vi gần, trong nội bộ gia đình/cơ quan và tốc độ chuyển biến tương đối nhanh."
                elif "NGOẠI BÀN" in str(xg_raw).upper():
                    res["km_xa_gan_prose"] = "Cung Dụng Thần nằm ở <b>Ngoại Bàn</b>, báo hiệu sự việc liên quan tới yếu tố bên ngoài, khoảng cách xa hoặc cần thêm thời gian để hoàn tất."
            except Exception:
                pass

        # 1e. Chuyên gia giải mã cổ thư theo từng chủ đề (qmdg_decoder & qmdg_inference_rules)
        try:
            from qmdg_decoder import decode_illness, decode_lost_item, decode_appearance, decode_character
            _cua_full_dec = (cua_dt if "Môn" in cua_dt else f"{cua_dt} Môn") if cua_dt and cua_dt != "?" else ""
            if category == "SỨC_KHỎE_GIA_ĐÌNH" or any(w in q_low for w in ["bệnh", "ốm", "đau", "khỏe", "qua khỏi", "viện"]):
                ill_str = decode_illness(sao_dt, c_thien, target_cung)
                ill_clean = re.sub(r"\[[^\]]+\]:?\s*", "", str(ill_str or "")).replace("\n- ", "; ").replace("\n", " ").strip(" ;.")
                if ill_clean:
                    res["km_topic_forensic"] = f"Theo <b>Y Dịch Kỳ Môn</b>: {ill_clean}."
            elif category == "TÌM_ĐỒ" or any(w in q_low for w in ["tìm", "mất", "thất lạc", "ở đâu", "để đâu"]):
                lost_str = decode_lost_item(_cua_full_dec, target_cung)
                lost_clean = re.sub(r"\[[^\]]+\]:?\s*", "", str(lost_str or "")).replace("\n- ", "; ").replace("\n", " ").strip(" ;.")
                if lost_clean:
                    res["km_topic_forensic"] = f"Theo <b>Pháp Quyết Truy Vết Kỳ Môn</b>: {lost_clean}."
            elif category == "TÌNH_CẢM" or any(w in q_low for w in ["ai", "người yêu", "vợ", "chồng", "đối tác"]):
                app_str = re.sub(r"\[[^\]]+\]:?\s*", "", str(decode_appearance(sao_dt) or "")).strip().rstrip(".")
                char_str = re.sub(r"\[[^\]]+\]:?\s*", "", str(decode_character(_cua_full_dec) or "")).strip().rstrip(".")
                if app_str and char_str:
                    res["km_topic_forensic"] = (
                        f"Phác họa thần thái qua Cửu Tinh & Bát Môn: người này có nét <i>{app_str.lower()}</i>, "
                        f"tâm tính bên trong <i>{char_str.lower()}</i>."
                    )
                elif app_str or char_str:
                    res["km_topic_forensic"] = f"Phác họa thần thái qua Cửu Tinh & Bát Môn: <i>{(app_str or char_str).lower()}</i>."
        except Exception:
            pass

    # ── 2. LỤC HÀO KINH DỊCH CỔ THƯ (64 QUẺ BẢN/BIẾN · LỤC THÚ · HÀO ĐỘNG · PHỤC THẦN · LỤC THÂN 6 CHỦ ĐỀ) ──
    try:
        from kinh_dich_64_que import tra_kinh_dich, tra_nap_am, tra_the_dung, MAI_HOA_UNG_KY
    except Exception:
        tra_kinh_dich = tra_nap_am = lambda x: None
        tra_the_dung = lambda x, y: None
        MAI_HOA_UNG_KY = {}

    try:
        from iching_integrated_data import LUC_THAN_MEANINGS
    except Exception:
        LUC_THAN_MEANINGS = {}

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
            lk_ban = kd_ban.get("loi_khuyen", "")
            lh_parts.append(
                f"Trên hệ thống <b>Lục Hào Kinh Dịch</b>, quẻ chủ lập được là <b>{ban_name}</b>{cung_txt}"
                + (f", mang tượng <i>«{yn_ban.rstrip('.')}»</i>" if yn_ban else "")
                + (f" ({lk_ban.rstrip('.')})" if lk_ban else "")
            )
            if bien_name and bien_name != ban_name:
                kd_bien = tra_kinh_dich(bien_name) or {}
                yn_bien = kd_bien.get("y_nghia", "")
                ch_bien = kd_bien.get("cat_hung", "")
                lh_parts.append(
                    f"biến sang quẻ <b>{bien_name}</b>"
                    + (f" (tượng <i>«{yn_bien.rstrip('.')}»</i> — {ch_bien})" if yn_bien else "")
                    + ", phản ánh xu hướng chuyển hóa từ hiện tại sang kết cục"
                )
        if lh_parts:
            res["lh_hexagram_prose"] = ", ".join(lh_parts) + "."

        # Tìm Hào Thế, Hào Ứng, Hào Dụng Thần và Lục Thú
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

        # Ý nghĩa chuyên sâu của Lục Thân theo đúng chủ đề câu hỏi (iching_integrated_data)
        topic_lt_key = "career"
        if category == "TÌNH_CẢM" or any(w in q_low for w in ["yêu", "vợ", "chồng", "hôn nhân", "tình cảm", "chia tay", "quay lại"]):
            topic_lt_key = "love"
        elif category in ("TÀI_CHÍNH", "NHÀ_CỬA") or any(w in q_low for w in ["tiền", "đầu tư", "mua đất", "bán đất", "lãi", "kinh doanh", "vốn"]):
            topic_lt_key = "wealth"
        elif category == "SỨC_KHỎE_GIA_ĐÌNH" or any(w in q_low for w in ["bệnh", "ốm", "đau", "khỏe", "viện", "thuốc"]):
            topic_lt_key = "health"
        elif category == "TÌM_ĐỒ" or any(w in q_low for w in ["tìm", "mất", "thất lạc", "ở đâu"]):
            topic_lt_key = "lost_item"
        elif any(w in q_low for w in ["kiện", "tòa", "tranh chấp", "pháp lý"]):
            topic_lt_key = "legal"

        lt_topic_desc = (LUC_THAN_MEANINGS.get(dung_than, {}) or {}).get(topic_lt_key, "")

        # Phân tích Hào Dụng Thần + Lục Thú + Phục Thần + Hào Động
        hao_details = []
        if dt_hao:
            dt_cc = dt_hao.get("can_chi", "") or dt_hao.get("chi", "")
            dt_nh = dt_hao.get("ngu_hanh", "")
            dt_vs = dt_hao.get("vuong_suy", "")
            dt_lthu = dt_hao.get("luc_thu") or dt_hao.get("luc_than_kd") or dt_hao.get("luc_than_td") or ""
            hao_details.append(
                f"Hào Dụng Thần <b>{dung_than}</b> tọa tại <b>Hào {dt_idx} ({dt_cc} — hành {dt_nh})</b>"
                + (f", đạt trạng thái <b>{dt_vs}</b>" if dt_vs else "")
                + (f" — trong chủ đề này đại diện cho <i>{lt_topic_desc.lower().rstrip('.')}</i>" if lt_topic_desc else "")
            )
            if dt_lthu and dt_lthu in LUC_THAN_Y_NGHIA:
                lt_info = LUC_THAN_Y_NGHIA[dt_lthu]
                hao_details.append(
                    f"Hào Dụng Thần lâm Lục Thú <b>{dt_lthu}</b> ({lt_info.get('tinh_chat', '').lower()}), "
                    f"mang hàm ý: <i>{lt_info.get('y_nghia', '').rstrip('.')}</i>"
                )
                res["lh_luc_thu_prose"] = f"Lục Thú <b>{dt_lthu}</b> lâm Dụng Thần ({lt_info.get('y_nghia', '').rstrip('.')})"
        else:
            pt_rule = PHUC_THAN_RULES.get("PT01", {})
            hao_details.append(
                f"Hào Dụng Thần <b>{dung_than}</b> hiện không lộ diện trực tiếp trên 6 hào chính mà ẩn dưới dạng <b>Phục Thần</b> "
                f"({pt_rule.get('ket_luan', 'sự việc hoặc tâm tư thật sự vẫn đang tiềm ẩn bên trong, chờ ngày Xung Phi hoặc Xuất Không mới bộc lộ rõ')})"
            )

        if the_hao and ung_hao:
            t_cc = the_hao.get("chi", "") or the_hao.get("can_chi", "")
            u_cc = ung_hao.get("chi", "") or ung_hao.get("can_chi", "")
            t_nh = the_hao.get("ngu_hanh", "")
            u_nh = ung_hao.get("ngu_hanh", "")
            t_lthu = the_hao.get("luc_thu") or the_hao.get("luc_than_kd") or ""
            u_lthu = ung_hao.get("luc_thu") or ung_hao.get("luc_than_kd") or ""
            hao_details.append(
                f"Trục tương tác giữa <b>Hào Thế (Hào {the_idx} {t_cc}/{t_nh}{f' lâm {t_lthu}' if t_lthu else ''} — Bản thân)</b> "
                f"và <b>Hào Ứng (Hào {ung_idx} {u_cc}/{u_nh}{f' lâm {u_lthu}' if u_lthu else ''} — Đối phương/Môi trường)</b> "
                f"phản ánh trực tiếp sự gắn kết và thế chủ động của bạn trong tình huống này"
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
                hao_details.append("Điểm chuyển dịch thiên cơ nằm ở " + ", cùng với ".join(dong_descs))

        if hao_details:
            res["lh_hao_dong_prose"] = ". ".join(hao_details) + "."

    # ── 3. MAI HOA DỊCH SỐ CỔ THƯ (THỂ DỤNG SINH KHẮC & ỨNG KỲ MAI HOA) ──
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
                uk_mh = (MAI_HOA_UNG_KY.get(qh_td, {}) or {}).get("giai_thich", "").rstrip(".")
                res["mh_the_dung_prose"] = (
                    f"Theo <b>Mai Hoa Dịch Số</b>, quẻ Thể ({the_q_name + ' ' if the_q_name else ''}hành <b>{the_hanh}</b>) "
                    f"và quẻ Dụng ({dung_q_name + ' ' if dung_q_name else ''}hành <b>{dung_hanh}</b>) lập thế <b>{qh_td}</b>: "
                    f"<i>{ct_td}</i>"
                    + (f" ({uk_mh})." if uk_mh else ".")
                )

    # ── 4. THIẾT BẢN THẦN TOÁN (60 HOA GIÁP NẠP ÂM) & KHỔNG MINH LỤC DIỆU ──
    if can_ngay and chi_ngay and tra_nap_am:
        na_info = tra_nap_am(f"{can_ngay} {chi_ngay}") or {}
        if na_info and na_info.get("nap_am"):
            res["tb_nap_am_prose"] = (
                f"Trong <b>Thiết Bản Thần Toán (60 Hoa Giáp)</b>, trụ ngày <b>{can_ngay} {chi_ngay}</b> "
                f"ứng vào Nạp Âm <b>{na_info.get('nap_am')}</b> (hành {na_info.get('hanh', '')}), "
                f"mang khí chất: <i>«{na_info.get('giai_thich', '').rstrip('.')}»</i>."
            )

    try:
        import datetime as _dt
        from ai_tools import get_lunar_date_offline, get_khong_minh_luc_dieu
        _today = _dt.date.today()
        lm, ld = get_lunar_date_offline(_today)
        if lm and ld:
            ld_summary, _ = get_khong_minh_luc_dieu(int(lm), int(ld))
            chi_list = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
            chi_val = (chi_list.index(chi_gio) + 1) if chi_gio in chi_list else 1
            ld_names = {
                1: "Đại An (Tốt — mọi việc yên tâm, hành sự hanh thông)",
                2: "Lưu Niên (Chậm — việc dễ dây dưa, cần kiên nhẫn tháo gỡ)",
                3: "Tốc Hỷ (Tốt — tin vui đến nhanh, mưu sự đắc lợi)",
                4: "Xích Khẩu (Khẩu thiệt — đề phòng tranh cãi, thị phi)",
                5: "Tiểu Cát (Tốt — may mắn, có quý nhân nâng đỡ)",
                0: "Không Vong (Trống rỗng — tạm thời chưa nên nóng vội xuất kích)"
            }
            cur_ld = ld_names.get((int(lm) + int(ld) + chi_val - 2) % 6, "Đại An")
            res["km_luc_dieu_prose"] = (
                f"Kết hợp <b>Khổng Minh Lục Diệu</b> (ngày {ld}/{lm} Âm lịch, giờ {chi_gio or 'hiện tại'}), "
                f"thời vận ứng vào cung <b>{cur_ld}</b> ({ld_summary})."
            )
    except Exception:
        pass

    # ── 5. VẠN VẬT LOẠI TƯỢNG CHUYÊN SÂU (60 TRẠNG THÁI NGŨ HÀNH × 12 TRƯỜNG SINH) ──
    if hanh_dt and hanh_dt != "?" and ts_stage:
        try:
            from van_vat_chi_tiet import get_van_vat_chi_tiet
            vv_info = get_van_vat_chi_tiet(hanh_dt, ts_stage) or {}
            if vv_info:
                if category == "TÌNH_CẢM" or any(w in q_low for w in ["yêu", "vợ", "chồng", "hôn nhân", "tình cảm"]):
                    ng_desc = vv_info.get("con_nguoi", "")
                    if ng_desc:
                        res["van_vat_forensic"] = f"Theo <b>Vạn Vật Loại Tượng ({hanh_dt} ở {ts_stage})</b>, thần thái và tâm lý của đối tượng hiện tại như: <i>{ng_desc.rstrip('.')}</i>."
                elif category == "SỨC_KHỎE_GIA_ĐÌNH" or any(w in q_low for w in ["bệnh", "ốm", "đau", "khỏe"]):
                    b_desc = vv_info.get("benh_tat", "")
                    if b_desc:
                        res["van_vat_forensic"] = f"Theo <b>Vạn Vật Y Lý ({hanh_dt} ở {ts_stage})</b>, triệu chứng và thể trạng ứng với: <i>{b_desc.rstrip('.')}</i>."
                elif category in ("TÀI_CHÍNH", "NHÀ_CỬA") or any(w in q_low for w in ["nhà", "đất", "mua", "bán", "đầu tư"]):
                    nc_desc = vv_info.get("nha_cua", "")
                    if nc_desc:
                        res["van_vat_forensic"] = f"Theo <b>Vạn Vật Phong Thủy ({hanh_dt} ở {ts_stage})</b>, đặc điểm môi trường/tài sản ứng với: <i>{nc_desc.rstrip('.')}</i>."
        except Exception:
            pass

    # Tổng hợp hồ sơ cổ thư thành văn bản chuẩn cho cả AI Online và AI Offline
    dossier_lines = []
    for k_name, label_name in [
        ("km_cach_cuc_prose", "81 Cách Cục Lưu Bá Ôn"),
        ("km_mon_cung_prose", "Bát Môn Bay Cung"),
        ("km_sao_cua_than_prose", "Tổ Hợp Sao-Cửa-Thần & Tượng Ý"),
        ("km_xa_gan_prose", "Nội/Ngoại Bàn Xa Gần"),
        ("km_topic_forensic", "Giải Mã Chuyên Sâu Theo Chủ Đề"),
        ("lh_hexagram_prose", "Quẻ Chủ & Quẻ Biến Kinh Dịch"),
        ("lh_hao_dong_prose", "Chi Tiết Hào Dụng Thần, Thế/Ứng & Hào Động"),
        ("mh_the_dung_prose", "Mai Hoa Thể Dụng"),
        ("tb_nap_am_prose", "Thiết Bản Nạp Âm 60 Hoa Giáp"),
        ("km_luc_dieu_prose", "Khổng Minh Lục Diệu"),
        ("van_vat_forensic", "Vạn Vật Loại Tượng Chuyên Sâu"),
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
    V100.0 — SIÊU NÃO THẦN ĐOÁN CỔ THƯ HỢP NHẤT:
    Kết nối toàn bộ 10 Hệ Thống Quẻ, 19 Bộ Cổ Thư trong GitHub (81 Cách Cục Lưu Bá Ôn,
    Bát Môn Bay Cung, Tổ Hợp Sao-Cửa-Thần, Lục Hào 64 Quẻ Bản/Biến, Lục Thú, Phục Thần,
    Mai Hoa Thể Dụng, Thiết Bản 60 Hoa Giáp, Khổng Minh Lục Diệu, Vạn Vật 12 Trường Sinh)
    và 40 Chuyên Gia AI thành 4 đoạn văn xuôi tiếng Việt sâu sắc, mạch lạc, chi tiết như thần.
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

    def _v_word(v_str):
        vu = str(v_str or "").upper()
        if "ĐẠI CÁT" in vu:
            return "rất thuận lợi (Đại Cát)"
        if "CÁT" in vu:
            return "thuận lợi (Cát)"
        if "ĐẠI HUNG" in vu:
            return "nhiều bất lợi lớn (Đại Hung)"
        if "HUNG" in vu:
            return "đang có lực cản (Hung)"
        return "ở thế cân bằng, giằng co (Bình hòa)"

    # ── ĐOẠN 1: THẤU THỊ TÂM CƠ & GIẢI MÃ BÀN KỲ MÔN ĐỘN GIÁP (81 CÁCH CỤC LƯU BÁ ÔN · BÁT MÔN · SAO THẦN) ──
    p1_parts = []
    p1_parts.append(
        f"Xét trên nền tảng cốt lõi của Tam Thức (gồm Kỳ Môn Độn Giáp {_v_word(ky_mon_verdict)}, "
        f"Lục Hào Kinh Dịch {_v_word(luc_hao_verdict)} và Mai Hoa Dịch Số {_v_word(mai_hoa_verdict)}), "
        f"trọng tâm câu hỏi <i>«{question}»</i> ứng trực tiếp vào hào Dụng Thần <b>{dung_than}</b>"
        + (f" (thuộc hành <b>{hanh_dt}</b>)" if hanh_dt and hanh_dt != "?" else "")
        + "."
    )

    if ts_stage:
        con_nguoi_ts = ts_info.get("con_nguoi", "đang vận động theo chu kỳ")
        p1_parts.append(
            f"Trong vòng 12 Trường Sinh, Dụng Thần đang ở trạng thái <b>{ts_stage}</b> "
            f"(ví như <i>{con_nguoi_ts.lower()}</i>)"
            + (f" và đạt trạng thái khí <b>{nk_stage}</b> theo mùa," if nk_stage else ",")
            + " phản ánh chân thực nội lực hiện tại của sự việc."
        )

    if dossier.get("km_cach_cuc_prose"):
        p1_parts.append(dossier["km_cach_cuc_prose"])
    if dossier.get("km_mon_cung_prose"):
        p1_parts.append(dossier["km_mon_cung_prose"])
    if dossier.get("km_sao_cua_than_prose"):
        p1_parts.append(dossier["km_sao_cua_than_prose"])
    if dossier.get("km_xa_gan_prose"):
        p1_parts.append(dossier["km_xa_gan_prose"])
    if dossier.get("km_topic_forensic"):
        p1_parts.append(dossier["km_topic_forensic"])
    if dossier.get("van_vat_forensic"):
        p1_parts.append(dossier["van_vat_forensic"])

    # Bổ sung giải nghĩa tự nhiên các yếu tố đặc biệt trên bàn quẻ
    km_lh_mh_raw = f"{ky_mon_reason} | {luc_hao_reason} | {mai_hoa_reason}".upper()
    nuances = []
    if "PHỤC THẦN" in km_lh_mh_raw and not dossier.get("lh_hao_dong_prose"):
        nuances.append("hào Dụng Thần đang ở thế <b>Phục Thần (ẩn tàng)</b>, nghĩa là tâm tư thật sự hoặc kết quả cốt lõi vẫn đang được giấu kín ở bên trong chứ chưa bộc lộ hết ra ngoài mặt")
    if "KHÔNG VONG" in km_lh_mh_raw or "TUẦN KHÔNG" in km_lh_mh_raw:
        nuances.append("cung quẻ tạm thời gặp <b>Tuần Không</b>, tạo ra cảm giác chững lại, trống trải hoặc đối phương đang giữ một khoảng lặng nhất định cần chờ đến ngày Xuất Không để sáng tỏ")
    if "CUNG BT SINH DT" in km_lh_mh_raw or "CUNG DT TƯƠNG SINH BT" in km_lh_mh_raw or "TỶ HÒA" in km_lh_mh_raw:
        nuances.append("giữa bản thân bạn và đối phương/mục tiêu vẫn có dòng khí tương sinh hoặc Tỷ Hòa nâng đỡ nhau, chứng tỏ sợi dây liên kết gốc rễ vẫn còn bền chặt")
    if "NGUYÊN THẦN VƯỢNG" in km_lh_mh_raw or "DT VƯỢNG" in km_lh_mh_raw or "DT TƯỚNG" in km_lh_mh_raw:
        nuances.append("khí lực gốc của Dụng Thần và Nguyên Thần (nguồn trợ lực) vẫn vượng, khẳng định nền tảng bên trong vẫn tốt đẹp")
    if "TAM HÌNH" in km_lh_mh_raw:
        nuances.append("trong quẻ xuất hiện thế <b>Tam Hình</b>, báo hiệu có sự tự ái ngầm, gượng gạo hoặc xung đột tâm lý cần được cư xử khéo léo, mềm mỏng")
    if nuances:
        p1_parts.append("Đồng thời, quẻ chỉ rõ " + "; bên cạnh đó ".join(nuances) + ".")

    paragraph_1 = " ".join(p1_parts)

    # ── ĐOẠN 2: GIẢI MÃ THẦN CƠ LỤC HÀO KINH DỊCH & MAI HOA DỊCH SỐ (QUẺ BẢN/BIẾN · HÀO ĐỘNG · LỤC THÚ · THỂ DỤNG) ──
    p2_parts = []
    if dossier.get("lh_hexagram_prose"):
        p2_parts.append(dossier["lh_hexagram_prose"])
    if dossier.get("lh_hao_dong_prose"):
        p2_parts.append(dossier["lh_hao_dong_prose"])
    if dossier.get("mh_the_dung_prose"):
        p2_parts.append(dossier["mh_the_dung_prose"])
    if thoan_name and thoan_info.get("thoan"):
        p2_parts.append(
            f"Lời <b>Thoán Từ Kinh Dịch</b> của quẻ <b>{thoan_name}</b> cũng khẳng định: "
            f"<i>«{thoan_info.get('thoan', '').rstrip('.')}»</i> "
            f"({thoan_info.get('lk', thoan_info.get('dai_tuong', '')).rstrip('.')})."
        )
    if not p2_parts:
        p2_parts.append(
            f"Đối chiếu sang hệ thống Lục Hào Kinh Dịch ({_v_word(luc_hao_verdict)}) và Mai Hoa Dịch Số ({_v_word(mai_hoa_verdict)}), "
            f"tương quan giữa Hào Thế – Hào Ứng và cặp quái Thể – Dụng cho thấy sự việc đang vận động đúng theo quy luật sinh khắc của Dụng Thần <b>{dung_than}</b>."
        )
    paragraph_2 = " ".join(p2_parts)

    # ── ĐOẠN 3: ĐỐI CHIẾU ĐA HỆ THỐNG (ĐẠI LỤC NHÂM · THÁI ẤT · THIẾT BẢN 60 HOA GIÁP · TỬ VI · KHỔNG MINH LỤC DIỆU) ──
    p3_parts = []
    ln_up = str(luc_nham_reason or "").upper()
    ln_flow = ""
    if "SƠ TRUYỀN" in ln_up or "MẠT TRUYỀN" in ln_up:
        if "MẠT TRUYỀN SINH CAN" in ln_up or "TUONG LAI TOT" in ln_up or "KQ TỐT" in ln_up:
            ln_flow = "mặc dù giai đoạn khởi đầu (Sơ Truyền) có thể vướng chút băn khoăn hoặc chậm trễ, nhưng càng về giai đoạn kết cục (Mạt Truyền) thì khí số lại tương sinh tốt đẹp"
        else:
            ln_flow = "diễn biến từ khởi đầu (Sơ Truyền) qua Trung Truyền tới kết cục (Mạt Truyền) đòi hỏi sự kiên nhẫn điều tiết từng bước"
        if "DỊCH MÃ" in ln_up:
            ln_flow += " và có sao Dịch Mã thúc đẩy nên sự chuyển biến sẽ diễn ra khá nhanh"

    p3_parts.append(
        f"Khi mở rộng tầm nhìn sang các hệ thống Thái Ất – Lục Nhâm – Thiết Bản – Tử Vi, "
        f"<b>Đại Lục Nhâm</b> ({_v_word(luc_nham_verdict)}) và <b>Thái Ất Thần Số</b> ({_v_word(thai_at_verdict)}) "
        f"cho thấy {ln_flow if ln_flow else 'thế trận giữa Chủ và Khách đang đòi hỏi sự điềm tĩnh, lấy nhu thắng cương và chủ động nắm bắt thời cơ'}."
    )

    if dossier.get("tb_nap_am_prose"):
        p3_parts.append(dossier["tb_nap_am_prose"])

    tv_clean = str(tu_vi_reason or "").strip()
    if tv_clean:
        p3_parts.append(
            f"Bên cạnh đó, lá số <b>Tử Vi Đẩu Số</b> ứng thời ({tv_clean}) kết hợp cùng <b>Thiết Bản Thần Toán</b> ({_v_word(thiet_ban_verdict)}) "
            f"giúp soi chiếu rõ thêm nhân duyên và phúc khí hỗ trợ cho bạn."
        )
    if dossier.get("km_luc_dieu_prose"):
        p3_parts.append(dossier["km_luc_dieu_prose"])
    if xem_ngay_reason:
        p3_parts.append(
            f"Xét thêm về tiết khí và thời điểm hiện tại ({xem_ngay_reason}), việc chọn đúng khung giờ hoàng đạo và phương vị cát lợi sẽ giúp kích hoạt tối đa cát khí."
        )

    paragraph_3 = " ".join(p3_parts)

    # ── ĐOẠN 4: ĐÚC KẾT TỪ HỘI ĐỒNG 40 CHUYÊN GIA AI, ỨNG KỲ ĐỊNH LƯỢNG & PHÁP QUYẾT HÓA GIẢI ──
    p4_parts = []
    if exp_html_items:
        clean_exps = []
        for item in exp_html_items:
            txt = re.sub(r'<[^>]+>', '', str(item)).lstrip('• ').strip()
            if 'Hiện tại đang có xung đột, cần giải quyết gấp' in txt:
                continue
            _is_wealth_q = any(w in q_low for w in ['tiền', 'tài chính', 'đầu tư', 'lãi', 'lỗ', 'mua', 'bán', 'kinh doanh', 'vốn', 'lộc', 'giàu', 'nợ', 'tài sản', 'lương', 'thu nhập'])
            if ('SINH LỜI TỐT' in txt or 'Đầu tư có lãi' in txt or 'Tài chính vững vàng' in txt) and not _is_wealth_q:
                continue
            txt = re.sub(r'^[^\w]*(Chart Interpreter AI \(Đại sư Kỳ Môn\)|Chart Interpreter AI|Luc Hao Expert AI|Mai Hoa Expert AI|Relationship AI|Wealth Advisor AI|Career Advisor AI|Health Advisor AI|Direction Advisor AI|Feng Shui AI):\s*', '', txt)
            txt = re.sub(r'\(Hào Thế\s*\([^)]*\)\s*và Hào Ứng\s*\([^)]*\):?\s*', '(', txt)
            txt = re.sub(r'\(\s*[+-]?\d+\s*đ\s*\)', '', txt)
            txt = txt.replace('Cứngỏi', 'Cứng cỏi').replace('→', ' cho thấy ').replace('—', ', ').replace('[', '').replace(']', '')
            txt = re.sub(r'\(\s*\)', '', txt)
            txt = re.sub(r'\s+', ' ', txt).strip(' .;,-')
            if txt and len(clean_exps) < 4:
                clean_exps.append(txt)
        if clean_exps:
            p4_parts.append(
                "Tổng hợp hội chẩn từ <b>Hội Đồng 40 Chuyên Gia AI</b> khẳng định: "
                + "; đồng thời ".join(clean_exps) + "."
            )

    clean_advs = [re.sub(r'<[^>]+>', '', str(a)).strip() for a in advice_parts if str(a).strip()]
    if clean_advs:
        p4_parts.append("Từ toàn bộ 19 bộ cổ thư và 10 hệ thống quẻ nêu trên, <b>pháp quyết hành động thiết thực nhất dành cho bạn</b> là: " + " ".join(clean_advs))
    if ung_ky_str and ung_ky_str != "?" and "chưa rõ" not in ung_ky_str.lower():
        p4_parts.append(f"Mốc thời gian <b>Ứng Kỳ</b> quan trọng cần đặc biệt lưu tâm là: <b>{ung_ky_str}</b>.")

    paragraph_4 = " ".join(p4_parts)

    return (
        f'<div style="margin-top:14px;padding:18px 20px;background:rgba(15,23,42,0.58);border-radius:14px;border:1px solid rgba(110,231,183,0.4);line-height:1.78;font-size:0.98em;color:#f1f5f9;">'
        f'<div style="font-size:1.08em;font-weight:800;color:#6ee7b7;margin-bottom:10px;border-bottom:1px solid rgba(110,231,183,0.25);padding-bottom:6px;">'
        f'📖 BÀI LUẬN GIẢI THẦN ĐOÁN CỔ THƯ HỢP NHẤT V100.0 (10 HỆ THỐNG · 19 CỔ THƯ · 40 CHUYÊN GIA AI)</div>'
        f'<p style="margin:0 0 12px 0;text-align:justify;color:#e2e8f0;"><b>1. Thấu thị tâm cơ & Giải mã Kỳ Môn Độn Giáp (81 Cách Cục Lưu Bá Ôn · Bát Môn · Sao Thần):</b> {paragraph_1}</p>'
        f'<p style="margin:0 0 12px 0;text-align:justify;color:#e2e8f0;"><b>2. Giải mã thần cơ Lục Hào Kinh Dịch & Mai Hoa Dịch Số (Quẻ Bản/Biến · Lục Thú · Thể Dụng):</b> {paragraph_2}</p>'
        f'<p style="margin:0 0 12px 0;text-align:justify;color:#e2e8f0;"><b>3. Đối chiếu vận số đa chiều (Đại Lục Nhâm · Thái Ất · Thiết Bản 60 Hoa Giáp · Tử Vi · Lục Diệu):</b> {paragraph_3}</p>'
        + (f'<p style="margin:0;text-align:justify;color:#fef3c7;"><b>4. Đúc kết từ Hội Đồng 40 Chuyên Gia AI, Ứng Kỳ & Pháp quyết hành động:</b> {paragraph_4}</p>' if paragraph_4 else '')
        + f'</div>'
    )
