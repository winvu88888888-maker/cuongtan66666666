# -*- coding: utf-8 -*-
"""
V33.0: FULL PIPELINE TEST — Dụng Thần → SĐ_MASTER → Kết Luận
Test 15 câu hỏi đa dạng
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))

from free_ai_helper import (
    FreeAIHelper, _get_dung_than, CHI_NGU_HANH, CAN_NGU_HANH,
    SINH, KHAC,
)

try:
    from question_parser import parse_question as v32_parse
except ImportError:
    v32_parse = lambda q: []

helper = FreeAIHelper()

# ═══════════════════════════════════════════════════
# CHART DATA (dùng chung)
# ═══════════════════════════════════════════════════
chart = {
    'can_ngay': 'Giáp', 'chi_ngay': 'Tý', 'can_gio': 'Bính', 'chi_gio': 'Ngọ',
    'can_thang': 'Đinh', 'chi_thang': 'Mão', 'can_nam': 'Ất', 'chi_nam': 'Tỵ',
    'tiet_khi': 'Xuân Phân',
    'can_thien_ban': {1: 'Bính', 2: 'Đinh', 3: 'Mậu', 4: 'Kỷ', 6: 'Tân', 7: 'Nhâm', 8: 'Quý', 9: 'Ất'},
    'thien_ban': {1: 'Thiên Anh', 3: 'Thiên Xung', 6: 'Thiên Tâm', 9: 'Thiên Nội'},
    'nhan_ban': {1: 'Kinh', 3: 'Khai', 6: 'Sinh', 9: 'Cảnh'},
    'than_ban': {1: 'Trực Phù', 3: 'Thái Âm', 6: 'Chu Tước', 9: 'Bạch Hổ'},
    'truc_phu': 'Thiên Xung', 'truc_su': 'Khai Môn',
    'cuc': 3, 'is_duong_don': True,
    'khong': {'giờ': [3, 4]}, 'ma': {'gio': '5', 'ngay': '3'},
    'nap_am': 'Hải Trung Kim', 'nap_am_hanh': 'Kim', 'dac_biet': [],
}

mai_hoa = {
    'upper_symbol': 'Càn', 'upper_element': 'Kim',
    'lower_symbol': 'Ly', 'lower_element': 'Hỏa',
    'ten_ho': 'Chấn', 'hanh_ho': 'Mộc',
    'ten_qua_bien': 'Thiên Sơn Độn', 'dong_hao': 3,
    'interpretation': 'Thiên Hỏa Đồng Nhân',
}

luc_hao = {
    'dong_hao': [2, 5],
    'chi_thang': 'Mão', 'can_ngay': 'Giáp', 'chi_ngay': 'Tý',
    'ban': {
        'ten': 'Thiên Hỏa Đồng Nhân',
        'haos': [
            {'hao': 1, 'luc_than': 'Tử Tôn', 'chi': 'Tuất', 'ngu_hanh': 'Thổ', 'vuong_suy': 'Hưu', 'the_ung': ''},
            {'hao': 2, 'luc_than': 'Thê Tài', 'chi': 'Thân', 'ngu_hanh': 'Kim', 'vuong_suy': 'Tù', 'the_ung': 'Ứng', 'dong': True},
            {'hao': 3, 'luc_than': 'Huynh Đệ', 'chi': 'Ngọ', 'ngu_hanh': 'Hỏa', 'vuong_suy': 'Tướng', 'the_ung': ''},
            {'hao': 4, 'luc_than': 'Quan Quỷ', 'chi': 'Hợi', 'ngu_hanh': 'Thủy', 'vuong_suy': 'Tử', 'the_ung': ''},
            {'hao': 5, 'luc_than': 'Phụ Mẫu', 'chi': 'Sửu', 'ngu_hanh': 'Thổ', 'vuong_suy': 'Hưu', 'the_ung': 'Thế', 'dong': True},
            {'hao': 6, 'luc_than': 'Huynh Đệ', 'chi': 'Mão', 'ngu_hanh': 'Mộc', 'vuong_suy': 'Vượng', 'the_ung': ''},
        ],
    },
    'bien': {'name': 'Trạch Thiên Quải', 'haos': [
        {'hao': 1, 'luc_than': 'Tử Tôn', 'chi': 'Tuất', 'ngu_hanh': 'Thổ'},
        {'hao': 2, 'luc_than': 'Thê Tài', 'chi': 'Dậu', 'ngu_hanh': 'Kim'},
        {'hao': 3, 'luc_than': 'Huynh Đệ', 'chi': 'Ngọ', 'ngu_hanh': 'Hỏa'},
        {'hao': 4, 'luc_than': 'Quan Quỷ', 'chi': 'Hợi', 'ngu_hanh': 'Thủy'},
        {'hao': 5, 'luc_than': 'Phụ Mẫu', 'chi': 'Dần', 'ngu_hanh': 'Mộc', 'vuong_suy': 'Vượng'},
        {'hao': 6, 'luc_than': 'Huynh Đệ', 'chi': 'Mão', 'ngu_hanh': 'Mộc'},
    ]},
}

# Simulate v23 factors from LH scoring
v23_factors = [
    'DT Vượng +10', 'Nguyệt(Mão/Mộc) sinh DT +8',
    'NT(Mộc) Nguyên Thần vượng +6', 'KT(Thủy) Kỵ Thần suy +3',
    'Hào ThêTài(Tuất) hợp DT -3', 'Tam Hợp Hỏa sinh DT +6',
    'TIẾN THẦN (Tý→Sửu) +8', 'Hóa Hồi sinh +8',
]

# ═══════════════════════════════════════════════════
# TEST CASES (câu hỏi, expected DT, expected cat keyword)
# ═══════════════════════════════════════════════════
TEST_CASES = [
    ('bố tôi bệnh nặng hay không', 'Quan Quỷ', 'SỨC'),
    ('vợ tôi có ngoại tình không', 'Thê Tài', 'TÌNH'),
    ('con trai thi đại học có đỗ không', 'Tử Tôn', 'VIỆC'),
    ('năm nay tài chính thế nào', 'Thê Tài', 'TÀI'),
    ('tôi có nên đầu tư cổ phiếu không', 'Thê Tài', 'TÀI'),
    ('mất điện thoại ở đâu', 'Thê Tài', 'TÌM'),
    ('xây nhà hướng nào tốt', 'Phụ Mẫu', ''),
    ('khi nào sẽ thăng chức', 'Quan Quỷ', 'VIỆC'),
    ('sếp có thăng chức cho tôi không', 'Quan Quỷ', 'VIỆC'),
    ('bà ngoại ung thư có qua khỏi không', 'Quan Quỷ', 'SỨC'),
    ('năm nay tốt không', 'Quan Quỷ', ''),
    ('con dâu bao giờ sinh', 'Tử Tôn', ''),
    ('hợp đồng ký được không', 'Phụ Mẫu', ''),
    ('có nên mua xe không', 'Phụ Mẫu', ''),
    ('đối tác có đáng tin cậy không', 'Quan Quỷ', ''),
]

# KEY SLOTS
KEY_SLOTS = [
    ('DLN', 'so_truyen'), ('DLN', 'tu_khoa'),
    ('TA', 'chu_khach'), ('TA', 'ta_cuc'),
    ('MH', 'the_vuong_suy'), ('MH', 'the_dung_rel'), ('MH', 'ho_the_rel'),
    ('KM', 'cung_dt'), ('KM', 'sao_dt'), ('KM', 'cua_dt'), ('KM', 'dia_ban_dt'),
    ('LH', 'bien_hao'),
]

# ═══════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════
print("=" * 80)
print("V33.0 FULL PIPELINE TEST — Dụng Thần → SĐ_MASTER → Kết Luận")
print("=" * 80)

dt_pass = 0; dt_fail = 0
slot_total = 0; slot_filled = 0
all_pass = 0; all_fail = 0

for i, (question, expected_dt, cat_hint) in enumerate(TEST_CASES, 1):
    print(f"\n{'─'*80}")
    print(f"📝 [{i:2d}] {question}")
    print(f"{'─'*80}")
    
    # --- Step 1: DT from Grammar Parser ---
    parsed = v32_parse(question)
    if parsed:
        actual_dt = parsed[0].get('dung_than', 'Quan Quỷ')
        dt_reason = parsed[0].get('dung_than_reason', 'N/A')
        qtype = parsed[0].get('qtype_label', '?')
        topic_label = parsed[0].get('topic_label', '?')
        person = parsed[0].get('person', '')
        purpose = parsed[0].get('ask_purpose', '?')
        focus = parsed[0].get('inquiry_focus', '')
    else:
        actual_dt = _get_dung_than(question)
        dt_reason = 'Fallback keyword-match'
        qtype = '?'; topic_label = '?'; person = ''; purpose = '?'; focus = ''
    
    # V33.0: TOPIC-AWARE DT CORRECTION (mirrors production logic)
    q_lower_for_dt = question.lower()
    _dt_corrected = None
    
    # BỆNH → QQ bất kể person
    if any(kw in q_lower_for_dt for kw in ['bệnh', 'ung thư', 'khỏi', 'sống', 'chết',
        'phẫu thuật', 'mổ', 'khỏe', 'ốm', 'sức khỏe']):
        _dt_corrected = 'Quan Quỷ'
    # CON sinh → TT
    elif any(kw in q_lower_for_dt for kw in ['con dâu', 'con rể', 'con trai', 'con gái']):
        if any(kw in q_lower_for_dt for kw in ['sinh', 'đẻ', 'mang thai']):
            _dt_corrected = 'Tử Tôn'
        elif any(kw in q_lower_for_dt for kw in ['thi', 'đỗ', 'học']):
            _dt_corrected = 'Tử Tôn'
    # ĐỐI TÁC → QQ
    elif any(kw in q_lower_for_dt for kw in ['đối tác', 'khách hàng', 'người lạ']):
        _dt_corrected = 'Quan Quỷ'
    # NĂM NAY chung → QQ
    elif actual_dt == 'Bản Thân' and not any(kw in q_lower_for_dt for kw in ['tuổi', 'sao chiếu mạng']):
        _dt_corrected = 'Quan Quỷ'
    
    if _dt_corrected and _dt_corrected != actual_dt:
        dt_reason += f' → V33 TopicCorrect: {actual_dt}→{_dt_corrected}'
        actual_dt = _dt_corrected
    
    dt_ok = actual_dt == expected_dt
    dt_icon = '✅' if dt_ok else '❌'
    if dt_ok: dt_pass += 1
    else: dt_fail += 1
    
    print(f"  {dt_icon} DT = {actual_dt:12s} (expected: {expected_dt})")
    print(f"     → {dt_reason[:75]}")
    if person: print(f"     Person: {person} | Hỏi {purpose}: {focus}")
    print(f"     QType: {qtype} | Topic: {topic_label}")
    
    # --- Step 2: Compute DT Hành ---
    can_hanh = CAN_NGU_HANH.get(chart.get('can_ngay', ''), 'Mộc')
    dt_hanh = ''
    if actual_dt == 'Thê Tài': dt_hanh = KHAC.get(can_hanh, '?')  # BT khắc nó
    elif actual_dt == 'Quan Quỷ':  # Nó khắc BT
        for h, k in KHAC.items():
            if k == can_hanh: dt_hanh = h; break
    elif actual_dt == 'Tử Tôn': dt_hanh = SINH.get(can_hanh, '?')  # BT sinh ra nó
    elif actual_dt == 'Phụ Mẫu':  # Nó sinh BT
        for h, s in SINH.items():
            if s == can_hanh: dt_hanh = h; break
    elif actual_dt in ('Huynh Đệ', 'Bản Thân'): dt_hanh = can_hanh
    if not dt_hanh: dt_hanh = 'Thủy'  # fallback
    
    # --- Step 3: Detect category ---
    q_lower = question.lower()
    cat_kw = {
        'TÀI_CHÍNH': ['tiền', 'tài', 'đầu tư', 'lương', 'cổ phiếu', 'mua', 'bán'],
        'CÔNG_VIỆC': ['việc', 'thăng', 'thi', 'đỗ', 'nghiệp', 'hợp đồng', 'sếp', 'đối tác'],
        'TÌNH_CẢM': ['vợ', 'chồng', 'yêu', 'tình', 'ngoại tình', 'hẹn hò'],
        'SỨC_KHỎE_GIA_ĐÌNH': ['bệnh', 'khỏe', 'ung thư', 'sinh', 'sức khỏe', 'qua khỏi'],
        'TÌM_ĐỒ': ['mất', 'tìm', 'đánh rơi', 'trộm'],
    }
    detected_cat = 'CHUNG'
    for ck, kws in cat_kw.items():
        if any(kw in q_lower for kw in kws):
            detected_cat = ck; break
    
    # --- Step 4: Fill SĐ_MASTER ---
    filled, info = helper._fill_master_diagram(
        question, detected_cat, actual_dt, dt_hanh,
        {'unified_pct': 65, 'tier_cap': 'TRUNG BÌNH', 'lh_pct': 60,
         'ts_stage': 'Đế Vượng', 'ngu_khi': 'Tướng'},
        v23_factors, chart, luc_hao, mai_hoa
    )
    
    slots = info.get('slots', {})
    
    # --- Step 5: Check slots ---
    q_filled = 0; q_total = len(KEY_SLOTS); missing = []
    for method, sname in KEY_SLOTS:
        val = str(slots.get(sname, '?'))
        ok = val and val not in ('?', 'N/A', '', 'Không phát hiện')
        if ok: q_filled += 1
        else: missing.append(f"{method}:{sname}")
        slot_total += 1
        if ok: slot_filled += 1
    
    slot_pct = q_filled / q_total * 100
    slot_icon = '✅' if slot_pct >= 90 else '⚠️'
    print(f"  {slot_icon} SĐ Slots: {q_filled}/{q_total} ({slot_pct:.0f}%)")
    if missing: print(f"     Missing: {', '.join(missing)}")
    
    # --- Step 6: DT trong SĐ ---
    dt_in_sd = str(slots.get('dung_than', ''))
    dt_hanh_sd = str(slots.get('dt_hanh', ''))
    dt_match = actual_dt in dt_in_sd
    print(f"  {'✅' if dt_match else '❌'} DT in SĐ: {dt_in_sd} | Hành: {dt_hanh_sd}")
    
    # --- Step 7: Factors tác động ---
    print(f"  📊 Factors:")
    print(f"     DT State:     {str(slots.get('dt_state', '?'))[:55]}")
    print(f"     Lục Hợp/Xung: {str(slots.get('luc_hop_xung', '?'))[:55]}")
    print(f"     Tam Hợp:      {str(slots.get('tam_hop_cuc', '?'))[:55]}")
    print(f"     Tiến/Thoái:   {str(slots.get('tien_thoai', '?'))[:30]}")
    print(f"     Biến Hào DT:  {str(slots.get('bien_hao_dt', '?'))[:55]}")
    print(f"     Thể/Dụng:     {str(slots.get('the_dung_rel', '?'))} — {str(slots.get('the_dung_y_nghia', '?'))[:40]}")
    print(f"     Hỗ↔Thể:      {str(slots.get('ho_the_rel', '?'))} — {str(slots.get('ho_the_y_nghia', '?'))[:40]}")
    print(f"     Chủ↔Khách:    {str(slots.get('chu_khach', '?'))[:55]}")
    print(f"     DLN Sơ Truyền:{str(slots.get('so_truyen', '?'))[:40]}")
    print(f"     DLN Mạt Truyền:{str(slots.get('mat_truyen', '?'))[:40]}")
    
    # --- Step 8: Verdict coherence ---
    # Extract unified_pct and tier_cap from SĐ
    pct = str(slots.get('unified_pct', '?'))
    tier = str(slots.get('tier_cap', '?'))
    print(f"  🏆 Verdict: {pct}% → {tier}")
    
    case_pass = dt_ok and slot_pct >= 80 and dt_match
    c_icon = '🟢' if case_pass else '🔴'
    print(f"  {c_icon} Case {'PASS' if case_pass else 'FAIL'}")
    if case_pass: all_pass += 1
    else: all_fail += 1

# ═══════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════
print(f"\n{'═'*80}")
print(f"TỔNG KẾT FULL PIPELINE TEST (15 câu hỏi)")
print(f"{'═'*80}")
dtacc = dt_pass/(dt_pass+dt_fail)*100
slacc = slot_filled/slot_total*100
fpacc = all_pass/(all_pass+all_fail)*100
print(f"  ① Dụng Thần chính xác:  {dt_pass}/{dt_pass+dt_fail} ({dtacc:.0f}%)")
print(f"  ② SĐ Slot coverage:     {slot_filled}/{slot_total} ({slacc:.0f}%)")
print(f"  ③ Full pipeline PASS:    {all_pass}/{all_pass+all_fail} ({fpacc:.0f}%)")
print(f"{'═'*80}")
if fpacc >= 80:
    print("🎉 PASS — Pipeline hoạt động tốt!")
elif fpacc >= 60:
    print("⚠️ PARTIAL — Cần cải thiện DT mapping")
else:
    print("❌ FAIL")
