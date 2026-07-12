"""
offline_brain.py — V42.9.42: Não Suy Luận AI Offline
Biến dữ liệu thô (verdicts, factors, %) thành câu trả lời ngôn ngữ tự nhiên.

5 engine:
1. Narrative Builder — Viết câu trả lời theo DẠNG câu hỏi
2. Factor Connector — Kết nối factors thành logic (NHƯNG, DO ĐÓ, TUY NHIÊN)
3. Actionable Advice — Sinh lời khuyên hành động
4. Category Templates — Template riêng cho mỗi nhóm (tài chính, sức khỏe, tình cảm...)
5. Context Injector — Inject ngữ cảnh (tên người, vật phẩm...) vào câu trả lời
"""


# ═══════════════════════════════════════════════════════════════
# VERDICT LABELS
# ═══════════════════════════════════════════════════════════════
def _verdict_label(pct):
    if pct >= 75: return 'RẤT THUẬN LỢI'
    if pct >= 60: return 'THUẬN LỢI'
    if pct >= 50: return 'NGHIÊNG THUẬN'
    if pct >= 40: return 'CẦN CÂN NHẮC'
    if pct >= 25: return 'BẤT LỢI'
    return 'RẤT BẤT LỢI'

def _verdict_emoji(pct):
    if pct >= 60: return '✅'
    if pct >= 45: return '🟡'
    return '🔴'

def _verdict_tone(pct):
    """Trả về giọng điệu phù hợp"""
    if pct >= 70: return 'tích cực, tự tin'
    if pct >= 55: return 'khá lạc quan, nhưng thận trọng'
    if pct >= 45: return 'trung tính, cần xem xét kỹ'
    if pct >= 30: return 'lo ngại, cần chuẩn bị phương án dự phòng'
    return 'nghiêm trọng, nên hoãn hoặc đổi kế hoạch'


# ═══════════════════════════════════════════════════════════════
# 1. FACTOR CONNECTOR — Kết nối factors thành đoạn văn logic
# ═══════════════════════════════════════════════════════════════
def _connect_factors(factors_list):
    """
    Biến danh sách factors thành đoạn văn có logic.
    Input: ['⊕ Nguyệt Lệnh sinh DT', '⊖ Kỵ Thần động', '🔄 Phản Ngâm']
    Output: "Nguyệt Lệnh sinh trợ Dụng Thần (thuận lợi), tuy nhiên Kỵ Thần đang động
             gây bất lợi, đồng thời cục Phản Ngâm cho thấy sự việc biến động nhanh."
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
        # Phân loại
        if any(x in f_str for x in ['⊕', '✅', '🟢', 'sinh', 'vượng', 'CÁT', 'Cát', 'hợp', 'trợ']):
            good.append(_clean_factor(f_str))
        elif any(x in f_str for x in ['⊖', '🔴', '❌', 'khắc', 'hung', 'HUNG', 'phá', 'xung', 'suy', 'tử']):
            bad.append(_clean_factor(f_str))
        else:
            neutral.append(_clean_factor(f_str))
    
    parts = []
    if good:
        parts.append("Thuận lợi: " + ", ".join(good[:3]))
    if bad:
        connector = " Tuy nhiên, " if good else ""
        parts.append(f"{connector}bất lợi: " + ", ".join(bad[:3]))
    if neutral and len(neutral) <= 2:
        parts.append("Lưu ý thêm: " + ", ".join(neutral[:2]))
    
    return ". ".join(parts) + "." if parts else ""

def _clean_factor(f):
    """Bỏ emoji và ký hiệu, chỉ giữ nội dung"""
    for ch in ['⊕', '⊖', '✅', '🔴', '🟢', '🟡', '⚡', '💥', '⭕', '🔄', '☯', '△', '↗', '👻', '🔥']:
        f = f.replace(ch, '')
    return f.strip().strip('-').strip()


# ═══════════════════════════════════════════════════════════════
# 2. CATEGORY-SPECIFIC TEMPLATES
# ═══════════════════════════════════════════════════════════════
CATEGORY_TEMPLATES = {
    'TÀI_CHÍNH': {
        'high': "Tài lộc năm nay **rất vượng**. Dụng Thần được sinh trợ mạnh, cho thấy cơ hội kiếm tiền thuận lợi. {factors} Thời điểm tốt nhất là {ung_ky}. Nên mạnh dạn đầu tư hoặc mở rộng.",
        'mid': "Tài lộc **khá ổn** nhưng không nên quá mạo hiểm. {factors} Nên đầu tư vừa phải, tránh đặt cược lớn. Thời điểm cần lưu ý: {ung_ky}.",
        'low': "Tài lộc **không thuận lợi** giai đoạn này. {factors} Nên giữ tiền, tránh đầu tư mới. Chờ đến {ung_ky} mới nên hành động.",
    },
    'SỨC_KHỎE_GIA_ĐÌNH': {
        'high': "Sức khỏe {person} **ổn định**, không có gì đáng lo ngại. {factors} Tiếp tục duy trì lối sống hiện tại.",
        'mid': "Sức khỏe {person} **cần chú ý**. {factors} Nên đi khám định kỳ và chú ý nghỉ ngơi.",
        'low': "Sức khỏe {person} **đáng lo ngại**. {factors} Cần đi khám bác sĩ ngay. Tránh gắng sức, chú ý đặc biệt vào {ung_ky}.",
    },
    'TÌNH_CẢM': {
        'high': "Tình cảm **rất thuận lợi**. {factors} Đây là thời điểm tốt để tiến xa hơn trong mối quan hệ.",
        'mid': "Tình cảm **tạm ổn** nhưng cần nỗ lực hai bên. {factors} Nên chủ động quan tâm, tránh hiểu lầm.",
        'low': "Tình cảm **gặp trở ngại**. {factors} Cần kiên nhẫn, tránh tranh cãi. Thời điểm cải thiện: {ung_ky}.",
    },
    'CÔNG_VIỆC': {
        'high': "Công việc **rất thuận lợi**. {factors} Đây là lúc thể hiện năng lực, cơ hội thăng tiến cao.",
        'mid': "Công việc **ổn định** nhưng chưa có đột phá. {factors} Nên kiên trì, kết quả sẽ đến vào {ung_ky}.",
        'low': "Công việc **gặp khó khăn**. {factors} Nên thận trọng với quyết định lớn, tránh xung đột với cấp trên.",
    },
    'TÌM_ĐỒ': {
        'high': "Khả năng tìm lại **rất cao**. {factors} Đồ vật nằm ở {direction}, nên tìm trong {ung_ky}.",
        'mid': "Khả năng tìm lại **50-50**. {factors} Thử tìm theo hướng {direction}.",
        'low': "Khả năng tìm lại **thấp**. {factors} Đồ vật có thể đã bị di chuyển hoặc mất hẳn.",
    },
    'THẮNG_THUA': {
        'high': "Bên chủ **có lợi thế lớn**. {factors} Khả năng thắng cao.",
        'mid': "Hai bên **ngang sức**. {factors} Kết quả phụ thuộc vào diễn biến thực tế.",
        'low': "Bên chủ **bất lợi**. {factors} Khả năng thua khá cao.",
    },
    'CHUNG': {
        'high': "Tình hình **rất thuận lợi**. {factors} Có thể yên tâm tiến hành.",
        'mid': "Tình hình **tạm ổn**, cần cân nhắc thêm. {factors}",
        'low': "Tình hình **bất lợi**. {factors} Nên hoãn hoặc tìm phương án khác.",
    },
}

def _get_tier(pct):
    if pct >= 55: return 'high'
    if pct >= 40: return 'mid'
    return 'low'


# ═══════════════════════════════════════════════════════════════
# 3. QUESTION-TYPE SPECIFIC OPENERS
# ═══════════════════════════════════════════════════════════════
def _get_qtype_opener(question, pct):
    """Sinh câu mở đầu phù hợp với DẠNG câu hỏi"""
    q = question.lower()
    emoji = _verdict_emoji(pct)
    label = _verdict_label(pct)
    
    # CÓ/KHÔNG
    if any(kw in q for kw in ['có nên', 'có được', 'được không', 'nên không', 'có không', 'liệu có']):
        if pct >= 60:
            return f"{emoji} **CÓ — {label}** ({pct}%). "
        elif pct >= 45:
            return f"{emoji} **CÓ THỂ ĐƯỢC — nhưng cần thận trọng** ({pct}%). "
        else:
            return f"{emoji} **KHÔNG NÊN — {label}** ({pct}%). "
    
    # THẾ NÀO / RA SAO
    if any(kw in q for kw in ['thế nào', 'ra sao', 'như thế nào', 'tình hình']):
        return f"{emoji} **{label}** ({pct}%). "
    
    # KHI NÀO / BAO GIỜ
    if any(kw in q for kw in ['khi nào', 'bao giờ', 'lúc nào', 'thời điểm']):
        return f"⏳ Về thời điểm ({pct}% thuận lợi): "
    
    # Ở ĐÂU
    if any(kw in q for kw in ['ở đâu', 'chỗ nào', 'hướng nào', 'tìm đâu']):
        return f"📍 Về vị trí/hướng ({pct}% tìm thấy): "
    
    # CÁI GÌ
    if any(kw in q for kw in ['cái gì', 'làm gì', 'bán gì', 'kinh doanh gì', 'đầu tư gì']):
        return f"🎯 Gợi ý ({pct}%): "
    
    # TẠI SAO
    if any(kw in q for kw in ['tại sao', 'vì sao', 'nguyên nhân', 'lý do']):
        return f"🔍 Phân tích nguyên nhân ({pct}%): "
    
    # Default
    return f"{emoji} **{label}** ({pct}%). "


# ═══════════════════════════════════════════════════════════════
# 4. CONTEXT INJECTOR — Inject ngữ cảnh từ câu hỏi
# ═══════════════════════════════════════════════════════════════
PERSON_KEYWORDS = {
    'bố': 'bố', 'mẹ': 'mẹ', 'cha': 'cha', 'ba': 'ba', 'má': 'má',
    'vợ': 'vợ', 'chồng': 'chồng', 'con': 'con', 'cháu': 'cháu',
    'anh': 'anh', 'chị': 'chị', 'em': 'em', 'sếp': 'sếp', 'bạn': 'bạn',
    'người yêu': 'người yêu', 'con trai': 'con trai', 'con gái': 'con gái',
}

DIRECTION_MAP = {
    1: 'Bắc', 2: 'Tây Nam', 3: 'Đông', 4: 'Đông Nam',
    5: 'Trung Tâm', 6: 'Tây Bắc', 7: 'Tây', 8: 'Đông Bắc', 9: 'Nam',
}

def _extract_person(question):
    q = question.lower()
    for kw, label in sorted(PERSON_KEYWORDS.items(), key=lambda x: len(x[0]), reverse=True):
        if kw in q:
            return label
    return 'bạn'

def _extract_direction(chart_data):
    if not chart_data:
        return '?'
    cung = chart_data.get('cung_dung_than') or chart_data.get('cung_dt')
    if cung:
        try:
            return DIRECTION_MAP.get(int(cung), '?')
        except (ValueError, TypeError):
            pass
    return '?'


# ═══════════════════════════════════════════════════════════════
# 5. ACTIONABLE ADVICE — Sinh lời khuyên hành động
# ═══════════════════════════════════════════════════════════════
def _generate_advice(pct, category, ung_ky_str, factors_text):
    """Sinh 1-3 câu lời khuyên cụ thể"""
    advice = []
    
    if pct >= 65:
        advice.append("💡 **Nên hành động:** Đây là thời điểm thuận lợi, không nên do dự.")
    elif pct >= 50:
        advice.append("💡 **Có thể tiến hành** nhưng nên chuẩn bị kỹ, có phương án dự phòng.")
    elif pct >= 35:
        advice.append("⚠️ **Cần thận trọng:** Tình hình chưa rõ ràng, nên chờ thêm hoặc hỏi ý kiến người thân.")
    else:
        advice.append("🛑 **Nên hoãn lại:** Thời điểm này không thuận lợi. Chờ đến thời điểm tốt hơn.")
    
    if ung_ky_str and ung_ky_str != '?' and 'N/A' not in ung_ky_str:
        advice.append(f"⏰ **Thời điểm then chốt:** {ung_ky_str}")
    
    # Category-specific
    if category == 'TÀI_CHÍNH':
        if pct >= 55:
            advice.append("💰 Có thể đầu tư vừa phải, ưu tiên lĩnh vực phù hợp với Hành Dụng Thần.")
        else:
            advice.append("💰 Giữ tiền, tránh đầu tư mới, tránh cho vay.")
    elif category == 'SỨC_KHỎE_GIA_ĐÌNH':
        if pct < 50:
            advice.append("🏥 Nên đi khám bác sĩ, không tự ý dùng thuốc.")
    elif category == 'TÌNH_CẢM':
        if pct >= 55:
            advice.append("❤️ Chủ động bày tỏ, thời điểm tốt để gắn kết.")
        else:
            advice.append("❤️ Kiên nhẫn, tránh ép buộc, cho nhau không gian.")
    
    return "\n".join(advice)


# ═══════════════════════════════════════════════════════════════
# MASTER FUNCTION — Sinh câu trả lời thông minh hoàn chỉnh
# ═══════════════════════════════════════════════════════════════
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
    """
    MASTER FUNCTION: Biến dữ liệu offline thành câu trả lời tự nhiên.
    
    Returns: str — Câu trả lời hoàn chỉnh dạng HTML
    """
    if not verdicts_dict:
        verdicts_dict = {}
    if not all_factors:
        all_factors = []
    
    pct = weighted_pct or 50
    person = _extract_person(question)
    direction = _extract_direction(chart_data)
    tier = _get_tier(pct)
    
    # Lấy template theo category
    cat_key = category if category in CATEGORY_TEMPLATES else 'CHUNG'
    template = CATEGORY_TEMPLATES[cat_key].get(tier, CATEGORY_TEMPLATES['CHUNG'][tier])
    
    # Kết nối factors
    factors_text = _connect_factors(all_factors)
    
    # Fill template
    filled = template.format(
        factors=factors_text,
        person=person,
        direction=direction,
        ung_ky=ung_ky_str or 'xem chi tiết ứng kỳ bên dưới',
    )
    
    # Opener theo dạng câu hỏi
    opener = _get_qtype_opener(question, pct)
    
    # Lời khuyên
    advice = _generate_advice(pct, cat_key, ung_ky_str, factors_text)
    
    # Consensus từ 5 phương pháp
    consensus = _build_consensus(verdicts_dict)
    
    # === BUILD HTML ===
    # Màu nền theo verdict
    if pct >= 55:
        bg = 'linear-gradient(135deg, #064e3b, #065f46)'
        border_color = '#10b981'
        accent = '#6ee7b7'
    elif pct >= 40:
        bg = 'linear-gradient(135deg, #713f12, #854d0e)'
        border_color = '#f59e0b'
        accent = '#fcd34d'
    else:
        bg = 'linear-gradient(135deg, #7f1d1d, #991b1b)'
        border_color = '#ef4444'
        accent = '#fca5a5'
    
    html = f'''<div style="background:{bg};padding:20px;border-radius:14px;margin:12px 0;border:2px solid {border_color};box-shadow:0 4px 20px rgba(0,0,0,0.3);">
<div style="font-size:1.3em;font-weight:900;color:#ffffff;margin-bottom:12px;line-height:1.4;">
{opener}{filled}
</div>
<div style="border-top:1px solid rgba(255,255,255,0.2);padding-top:12px;margin-top:8px;">
<div style="font-size:1.05em;color:{accent};font-weight:700;margin-bottom:8px;">📊 Đồng Thuận 5 Phương Pháp:</div>
<div style="font-size:1em;color:#e2e8f0;">{consensus}</div>
</div>
<div style="border-top:1px solid rgba(255,255,255,0.2);padding-top:12px;margin-top:12px;">
<div style="font-size:1.05em;color:{accent};font-weight:700;margin-bottom:8px;">🎯 Lời Khuyên:</div>
<div style="font-size:1em;color:#f1f5f9;line-height:1.6;">{advice.replace(chr(10), "<br>")}</div>
</div>
</div>'''
    
    return html


def _build_consensus(verdicts_dict):
    """Xây dựng chuỗi consensus từ 5 PP"""
    if not verdicts_dict:
        return "Chưa có dữ liệu consensus."
    
    PP_NAMES = {'km': 'Kỳ Môn', 'lh': 'Lục Hào', 'mh': 'Mai Hoa', 'ln': 'Đại Lục Nhâm', 'ta': 'Thái Ất'}
    PP_ICONS = {'km': '🏛', 'lh': '📊', 'mh': '☰', 'ln': '🔮', 'ta': '⚖️'}
    
    parts = []
    cat_count = 0
    hung_count = 0
    
    for pp_key, pp_name in PP_NAMES.items():
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
    
    total = cat_count + hung_count
    if total > 0:
        ratio = f" → <b>{cat_count} CÁT / {hung_count} HUNG</b>"
    else:
        ratio = " → Chưa rõ ràng"
    
    return " | ".join(parts) + ratio
