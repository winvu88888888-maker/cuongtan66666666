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
def _connect_factors(factors_list):
    """
    Biến danh sách factors thành đoạn văn có logic, không bị nhầm Kỵ Thần Suy thành yếu tố xấu.
    """
    if not factors_list:
        return ""

    good = []
    bad = []
    neutral = []

    for f in factors_list:
        f_str = str(f).strip()
        if not f_str:
            continue
        cleaned = _clean_factor(f_str)
        if not cleaned or len(cleaned) < 3:
            continue

        # Ưu tiên 1: Xét hệ sinh thái DT (Nguyên Thần / Kỵ Thần)
        if 'HỆ SINH THÁI DT' in f_str or 'Kỵ Thần' in f_str or 'Nguyên Thần' in f_str:
            if any(k in f_str for k in ['Sức khắc yếu', 'Không đủ sức khắc', 'ít ảnh hưởng', 'SINH DT', 'Nguyên Thần']):
                if 'VƯỢNG' in f_str or 'SINH' in f_str or 'yếu' in f_str:
                    good.append(cleaned)
                    continue
            if 'Kỵ Thần' in f_str and ('VƯỢNG' in f_str or 'MẠNH' in f_str or 'ĐỘNG' in f_str):
                bad.append(cleaned)
                continue

        # Ưu tiên 2: Xét điểm số ở cuối chuỗi (+10, -8, v.v.)
        m_score = re.search(r'([+-]\d+)\s*$', f_str)
        if m_score:
            sc_val = int(m_score.group(1))
            if sc_val > 0:
                good.append(cleaned)
                continue
            elif sc_val < 0:
                bad.append(cleaned)
                continue

        # Ưu tiên 3: Ký hiệu rõ ràng
        if any(x in f_str for x in ['⊕', '✅', '🟢', 'CÁT', 'Đắc lệnh']):
            good.append(cleaned)
        elif any(x in f_str for x in ['⊖', '🔴', '❌', '⚠️', 'HUNG', 'Nguyệt Phá', 'Nhật Phá', 'Tuần Không', 'Nhập Mộ', 'Phục Thần']):
            bad.append(cleaned)
        elif any(x in f_str.lower() for x in ['sinh dt', 'dt vượng', 'dt tướng', 'trường sinh', 'đế vượng', 'lâm quan', 'nhật sinh', 'nguyệt sinh']):
            good.append(cleaned)
        elif any(x in f_str.lower() for x in ['khắc dt', 'dt suy', 'dt tử', 'dt tuyệt', 'dt bệnh']):
            bad.append(cleaned)
        else:
            neutral.append(cleaned)

    # Khử trùng lặp
    good = list(dict.fromkeys(good))
    bad = list(dict.fromkeys(bad))

    parts = []
    if good:
        parts.append("<b>Điểm sáng thuận lợi:</b> " + "; ".join(good[:3]))
    if bad:
        connector = " <b>Tuy nhiên cần lưu ý lực cản:</b> " if good else "<b>Lực cản chính trong quẻ:</b> "
        parts.append(f"{connector}" + "; ".join(bad[:3]))
    if not good and not bad and neutral:
        parts.append("<b>Yếu tố nổi bật:</b> " + "; ".join(neutral[:2]))

    return ". ".join(parts) + "." if parts else ""


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

    # 8. TRỌNG TÂM: TÌNH CẢM / HÔN NHÂN / GIA ĐẠO
    if category == 'TÌNH_CẢM' or any(w in q_low for w in ['yêu', 'cưới', 'hôn nhân', 'vợ chồng', 'chia tay', 'quay lại', 'tình cảm']):
        if pct >= 55:
            head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>TÌNH CẢM THUẬN HÒA & GẮN KẾT TỐT ({pct}% — CÁT)</b>."
        elif pct >= 45:
            head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>CÒN DÙNG DẰNG / CẦN THẤU HIỂU & NHƯỜNG NHỊN ({pct}% — BÌNH)</b>."
        else:
            head = f"❤️ <b>TRẢ LỜI TRỌNG TÂM ({q}):</b> <b>ĐANG CÓ XUNG KHẮC / TRỞ NGẠI LỚN ({pct}% — HUNG)</b>."
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
