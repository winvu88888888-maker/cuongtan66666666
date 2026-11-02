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
) -> str:
    """
    V99.9.7: Nối toàn bộ dữ liệu rời rạc của 10 Hệ Thống Quẻ, Sơ Đồ Lực Lượng, 40 Chuyên Gia AI,
    Kinh Dịch Thoán Từ và Cảnh Báo thành 3 đoạn văn xuôi tiếng Việt mạch lạc, tự nhiên, dễ hiểu, dễ đọc.
    """
    q_low = (question or "").lower()
    thoan_info = thoan_info if isinstance(thoan_info, dict) else {}
    ts_info = ts_info if isinstance(ts_info, dict) else {}
    nk_info = nk_info if isinstance(nk_info, dict) else {}
    exp_html_items = exp_html_items or []
    warn_parts = warn_parts or []
    advice_parts = advice_parts or []

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

    # ── ĐOẠN 1: TAM THỨC HỢP GIẢI (KỲ MÔN · LỤC HÀO · MAI HOA) & LỰC LƯỢNG DỤNG THẦN ──
    p1_parts = []
    p1_parts.append(
        f"Xét trên nền tảng cốt lõi của Tam Thức (gồm Kỳ Môn Độn Giáp {_v_word(ky_mon_verdict)}, "
        f"Lục Hào Kinh Dịch {_v_word(luc_hao_verdict)} và Mai Hoa Dịch Số {_v_word(mai_hoa_verdict)}), "
        f"chủ thể trọng tâm của câu hỏi ứng vào hào Dụng Thần <b>{dung_than}</b>"
        + (f" (thuộc hành <b>{hanh_dt}</b>)" if hanh_dt and hanh_dt != "?" else "")
        + "."
    )

    if ts_stage:
        con_nguoi_ts = ts_info.get("con_nguoi", "đang vận động theo chu kỳ")
        p1_parts.append(
            f"Trong vòng 12 Trường Sinh, Dụng Thần đang ở trạng thái <b>{ts_stage}</b> "
            f"(ví như <i>{con_nguoi_ts.lower()}</i>)"
            + (f" và đạt trạng thái khí <b>{nk_stage}</b> theo mùa," if nk_stage else ",")
            + " phản ánh rõ thực trạng nội lực hiện tại của sự việc."
        )

    # Giải nghĩa tự nhiên từ Kỳ Môn, Lục Hào, Mai Hoa
    km_lh_mh_raw = f"{ky_mon_reason} | {luc_hao_reason} | {mai_hoa_reason}".upper()
    nuances = []
    if "PHỤC THẦN" in km_lh_mh_raw:
        nuances.append("hào Dụng Thần đang ở thế <b>Phục Thần (ẩn tàng)</b>, nghĩa là tâm tư thật sự hoặc kết quả cốt lõi vẫn đang được giấu kín ở bên trong chứ chưa bộc lộ ra ngoài mặt")
    if "KHÔNG VONG" in km_lh_mh_raw or "TUẦN KHÔNG" in km_lh_mh_raw:
        nuances.append("cung quẻ tạm thời gặp <b>Tuần Không</b>, tạo ra cảm giác chững lại, trống trải hoặc đối phương đang giữ một khoảng lặng nhất định")
    if "CUNG BT SINH DT" in km_lh_mh_raw or "CUNG DT TƯƠNG SINH BT" in km_lh_mh_raw or "TỶ HÒA" in km_lh_mh_raw:
        nuances.append("giữa bản thân bạn và đối phương/mục tiêu vẫn có dòng khí tương sinh hoặc Tỷ Hòa nâng đỡ nhau, chứng tỏ sợi dây liên kết gốc rễ vẫn còn bền chặt")
    if "NGUYÊN THẦN VƯỢNG" in km_lh_mh_raw or "DT VƯỢNG" in km_lh_mh_raw or "DT TƯỚNG" in km_lh_mh_raw:
        nuances.append("khí lực gốc của Dụng Thần và Nguyên Thần (nguồn trợ lực) vẫn vượng, khẳng định nền tảng bên trong vẫn tốt đẹp")
    if "TAM HÌNH" in km_lh_mh_raw:
        nuances.append("trong quẻ xuất hiện thế <b>Tam Hình</b>, báo hiệu có sự tự ái ngầm, gượng gạo hoặc xung đột tâm lý cần được cư xử khéo léo")

    if nuances:
        p1_parts.append("Đi sâu vào chi tiết, quẻ chỉ rõ " + "; đồng thời ".join(nuances) + ".")

    paragraph_1 = " ".join(p1_parts)

    # ── ĐOẠN 2: ĐỐI CHIẾU ĐA HỆ THỐNG (ĐẠI LỤC NHÂM · THÁI ẤT · THIẾT BẢN · TỬ VI · XEM NGÀY) ──
    p2_parts = []
    ln_up = str(luc_nham_reason or "").upper()
    ln_flow = ""
    if "SƠ TRUYỀN" in ln_up or "MẠT TRUYỀN" in ln_up:
        if "MẠT TRUYỀN SINH CAN" in ln_up or "TUONG LAI TOT" in ln_up or "KQ TỐT" in ln_up:
            ln_flow = "mặc dù giai đoạn khởi đầu (Sơ Truyền) có thể vướng chút băn khoăn hoặc chậm trễ, nhưng càng về giai đoạn kết cục (Mạt Truyền) thì khí số lại tương sinh tốt đẹp"
        else:
            ln_flow = "diễn biến từ khởi đầu (Sơ Truyền) tới kết cục (Mạt Truyền) đòi hỏi sự kiên nhẫn điều tiết từng bước"
        if "DỊCH MÃ" in ln_up:
            ln_flow += " và có sao Dịch Mã thúc đẩy nên sự chuyển biến sẽ diễn ra khá nhanh"

    p2_parts.append(
        f"Khi đối chiếu mở rộng sang các hệ thống vận số lớn, Đại Lục Nhâm ({_v_word(luc_nham_verdict)}) và "
        f"Thái Ất Thần Số ({_v_word(thai_at_verdict)}) cho thấy {ln_flow if ln_flow else 'thế trận giữa Chủ và Khách đang đòi hỏi sự điềm tĩnh và chủ động nắm bắt thời cơ'}."
    )

    # Tử Vi & Thiết Bản
    tv_clean = str(tu_vi_reason or "").strip()
    if tv_clean:
        p2_parts.append(
            f"Bên cạnh đó, kết quả Thiết Bản Thần Toán ({_v_word(thiet_ban_verdict)}) kết hợp cùng lá số Tử Vi ứng thời "
            f"({tv_clean}) giúp làm rõ thêm bức tranh toàn cảnh về mặt nhân duyên và thời vận."
        )
    if xem_ngay_reason:
        p2_parts.append(
            f"Về mặt tiết khí và thời điểm hiện tại ({xem_ngay_reason}), bạn nên lưu ý chọn khung giờ hoàng đạo thuận lợi để mọi việc hanh thông hơn."
        )

    paragraph_2 = " ".join(p2_parts)

    # ── ĐOẠN 3: ĐÚC KẾT TỪ HỘI ĐỒNG 40 CHUYÊN GIA AI, KINH DỊCH THOÁN TỪ & LỜI KHUYÊN ──
    p3_parts = []
    if exp_html_items:
        # Chuyển các nhận định của Chuyên gia AI thành câu văn nối liền mạch, loại bỏ ký hiệu kỹ thuật thô
        clean_exps = []
        for item in exp_html_items:
            txt = re.sub(r'<[^>]+>', '', str(item)).lstrip('• ').strip()
            if 'Hiện tại đang có xung đột, cần giải quyết gấp' in txt:
                continue
            # Bỏ tiền tố tên tiếng Anh lặp lại để đọc mượt như văn nói
            txt = re.sub(r'^[^\w]*(Chart Interpreter AI \(Đại sư Kỳ Môn\)|Chart Interpreter AI|Luc Hao Expert AI|Mai Hoa Expert AI|Relationship AI|Wealth Advisor AI|Career Advisor AI|Health Advisor AI|Direction Advisor AI|Feng Shui AI):\s*', '', txt)
            txt = re.sub(r'\(Hào Thế \([^)]*\) và Hào Ứng \([^)]*\)\)', '', txt)
            txt = txt.replace('→', ' cho thấy ').replace('—', ', ').replace('[', '').replace(']', '')
            txt = re.sub(r'\s+', ' ', txt).strip(' .;,-')
            if txt and len(clean_exps) < 3:
                clean_exps.append(txt)
        if clean_exps:
            p3_parts.append(
                "Tổng hợp nhận định chuyên sâu từ <b>Hội Đồng Chuyên Gia AI</b> cho thấy: "
                + "; đồng thời ".join(clean_exps) + "."
            )

    if thoan_name and thoan_info.get("thoan"):
        p3_parts.append(
            f"Đặc biệt, lời <b>Thoán Từ Kinh Dịch</b> của quẻ <b>{thoan_name}</b> nhắn nhủ rằng: "
            f"<i>«{thoan_info.get('thoan', '')}»</i> ({thoan_info.get('lk', thoan_info.get('dai_tuong', ''))})."
        )

    clean_advs = [re.sub(r'<[^>]+>', '', str(a)).strip() for a in advice_parts if str(a).strip()]
    if clean_advs:
        p3_parts.append("Từ tất cả các phân tích trên, lời khuyên thiết thực nhất dành cho bạn là: " + " ".join(clean_advs))

    paragraph_3 = " ".join(p3_parts)

    return (
        f'<div style="margin-top:14px;padding:18px 20px;background:rgba(15,23,42,0.55);border-radius:14px;border:1px solid rgba(110,231,183,0.35);line-height:1.75;font-size:0.98em;color:#f1f5f9;">'
        f'<div style="font-size:1.08em;font-weight:800;color:#6ee7b7;margin-bottom:10px;border-bottom:1px solid rgba(110,231,183,0.25);padding-bottom:6px;">'
        f'📖 BÀI LUẬN GIẢI TỔNG HỢP CHI TIẾT (KẾT NỐI 10 HỆ THỐNG & 40 CHUYÊN GIA AI)</div>'
        f'<p style="margin:0 0 12px 0;text-align:justify;color:#e2e8f0;"><b>1. Giải mã cốt lõi từ Tam Thức (Kỳ Môn · Lục Hào · Mai Hoa):</b> {paragraph_1}</p>'
        f'<p style="margin:0 0 12px 0;text-align:justify;color:#e2e8f0;"><b>2. Đối chiếu chiều sâu vận số (Đại Lục Nhâm · Thái Ất · Thiết Bản · Tử Vi):</b> {paragraph_2}</p>'
        + (f'<p style="margin:0;text-align:justify;color:#fef3c7;"><b>3. Đúc kết từ Hội Đồng Chuyên Gia, Kinh Dịch & Cẩm nang hành động:</b> {paragraph_3}</p>' if paragraph_3 else '')
        + f'</div>'
    )
