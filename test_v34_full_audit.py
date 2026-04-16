# -*- coding: utf-8 -*-
"""V34.0 FULL AUDIT: Test TẤT CẢ sơ đồ (MASTER + SD0-SD16) với 20+ câu hỏi.
Liệt kê slot nào còn '?' hoặc thiếu dữ liệu → để biết cần fix gì.
"""
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(__file__))

from free_ai_helper import FreeAIHelper
from interaction_diagrams import (
    DIAGRAM_MASTER, DIAGRAMS as INTERACTION_DIAGRAMS,
    match_question_to_diagram, split_compound_question, clean_question,
)

h = FreeAIHelper()

# ═══════════════════════════════════════════════════════════════
# MOCK DATA — giả lập dữ liệu thực tế đầy đủ
# ═══════════════════════════════════════════════════════════════

chart = {
    'can_ngay': 'Giáp', 'chi_ngay': 'Tý', 'can_gio': 'Bính', 'chi_gio': 'Ngọ',
    'can_thang': 'Đinh', 'chi_thang': 'Mão', 'can_nam': 'Ất', 'chi_nam': 'Tỵ',
    'tiet_khi': 'Xuân Phân',
    'can_thien_ban': {1: 'Bính', 2: 'Đinh', 3: 'Mậu', 4: 'Kỷ', 6: 'Tân', 7: 'Nhâm', 8: 'Quý', 9: 'Ất'},
    'thien_ban': {1: 'Thiên Anh', 2: 'Thiên Nhuế', 3: 'Thiên Xung', 4: 'Thiên Phụ', 6: 'Thiên Tâm', 7: 'Thiên Trụ', 8: 'Thiên Nhậm', 9: 'Thiên Bồng'},
    'nhan_ban': {1: 'Kinh Môn', 2: 'Tử Môn', 3: 'Khai Môn', 4: 'Hưu Môn', 6: 'Sinh Môn', 7: 'Thương Môn', 8: 'Đỗ Môn', 9: 'Cảnh Môn'},
    'than_ban': {1: 'Trực Phù', 2: 'Đằng Xà', 3: 'Thái Âm', 4: 'Lục Hợp', 6: 'Bạch Hổ', 7: 'Huyền Vũ', 8: 'Cửu Địa', 9: 'Cửu Thiên'},
    'dia_ban': {1: 'Tý', 2: 'Sửu', 3: 'Dần', 4: 'Mão', 6: 'Tị', 7: 'Ngọ', 8: 'Mùi', 9: 'Thân'},
    'truc_phu': 'Thiên Xung', 'truc_su': 'Khai Môn',
    'cuc': 3, 'is_duong_don': True,
    'khong': {'giờ': [3, 4]},
    'ma': {'gio': '5', 'ngay': '3'},
    'nap_am': 'Hải Trung Kim', 'nap_am_hanh': 'Kim',
    'dac_biet': [],
    'cung_ban_than': 3, 'cung_su_viec': 1,
    'cungs': {c: {} for c in range(1, 10)},
    'tam_ky': [],
}

mai_hoa = {
    'upper_symbol': 'Càn', 'upper_element': 'Kim', 'ten_thuong': 'Càn', 'hanh_thuong': 'Kim',
    'lower_symbol': 'Ly', 'lower_element': 'Hỏa', 'ten_ha': 'Ly', 'hanh_ha': 'Hỏa',
    'ten_ho': 'Chấn', 'the_quai': 'Ly', 'dung_quai': 'Càn', 'ho_quai': 'Chấn',
    'ten_qua_bien': 'Thiên Sơn Độn', 'bien_quai': 'Độn',
    'dong_hao': 3,
    'interpretation': 'Trời lửa → mâu thuẫn ban đầu nhưng sáng tỏ',
    'ho_quai_str': 'Chấn',
}

luc_hao = {
    'dong_hao': [2, 5],
    'chi_thang': 'Mão', 'can_ngay': 'Giáp', 'chi_ngay': 'Tý',
    'haos': [
        {'hao': 1, 'luc_than': 'Phụ Mẫu', 'chi': 'Tuất', 'hanh': 'Thổ', 'ngu_hanh': 'Thổ', 'the_ung': '', 'dong': False},
        {'hao': 2, 'luc_than': 'Thê Tài', 'chi': 'Thân', 'hanh': 'Kim', 'ngu_hanh': 'Kim', 'the_ung': 'Thế', 'dong': True},
        {'hao': 3, 'luc_than': 'Quan Quỷ', 'chi': 'Ngọ', 'hanh': 'Hỏa', 'ngu_hanh': 'Hỏa', 'the_ung': '', 'dong': False},
        {'hao': 4, 'luc_than': 'Tử Tôn', 'chi': 'Dần', 'hanh': 'Mộc', 'ngu_hanh': 'Mộc', 'the_ung': '', 'dong': False},
        {'hao': 5, 'luc_than': 'Huynh Đệ', 'chi': 'Hợi', 'hanh': 'Thủy', 'ngu_hanh': 'Thủy', 'the_ung': 'Ứng', 'dong': True},
        {'hao': 6, 'luc_than': 'Phụ Mẫu', 'chi': 'Sửu', 'hanh': 'Thổ', 'ngu_hanh': 'Thổ', 'the_ung': '', 'dong': False},
    ],
    'cuu_than': 'Mộc',
    'bien': {'name': 'Trạch Thiên Quải', 'details': [
        {'hao': 2, 'luc_than': 'Thê Tài', 'can_chi': 'Giáp Thân', 'ngu_hanh': 'Kim'},
        {'hao': 5, 'luc_than': 'Huynh Đệ', 'can_chi': 'Tân Hợi', 'ngu_hanh': 'Thủy'},
    ]},
}

# V23 LH factors (simulate scoring output)
v23_lh_factors = [
    'Nguyệt(Mão/Mộc) sinh DT +8',
    'Nhật(Giáp/Mộc) sinh DT +6',
    'NT(Mộc) Nguyên Thần vượng +6',
    'KT(Thủy) Kỵ Thần suy +3',
    'CừuT(Kim) Cừu Thần khắc KT +4',
    'Thế(Thân/Kim) khắc Ứng(Hợi/Thủy) +5',
    'Tuần Không: DT Tuần Không -15',
    'Nguyệt Phá: hào 3 Nguyệt Phá -12',
    'THAM SINH VONG KHẮC +10',
    'Hào ThêTài(Tuất) hợp DT -3',
    'Tam Hợp Hỏa sinh DT +6',
    'TIẾN THẦN (Tý→Sửu) +8',
    'Phục Thần Hỏa ẩn dưới hào 3',
    'PHẢN NGÂM hào Thế -5',
    'Hóa Hồi Đầu: hào 2 Biến Kim khắc Hỏa DT -4',
]

v24_km_factors = [
    'Cung DT: Cung1 (Thủy) + Sao Thiên Anh + Cửa Kinh Môn + Thần Trực Phù',
    'BT(Cung3) sinh SV(Cung1) → BT hỗ trợ SV +5',
    'Trực Phù: Thiên Xung | Trực Sử: Khai Môn',
    'KM Không Vong: Cung3, Cung4',
    'Mã Tinh: Cung5',
    'Tam Kỳ: Ất kỳ tại Cung9',
]

v24_mh_factors = [
    'Thể(Ly/Hỏa) bị Dụng(Càn/Kim) KHẮC → bất lợi -6',
    'Hỗ(Chấn/Mộc) SINH Thể(Ly/Hỏa) → hỗ trợ +4',
    'Hỗ(Chấn/Mộc) bị Dụng(Càn/Kim) KHẮC → Dụng áp đảo -3',
]

unified_v22 = {
    'unified_pct': 65, 'tier_cap': 'TRUNG BÌNH', 'lh_pct': 60,
    'ts_stage': 'Đế Vượng', 'ngu_khi': 'Tướng',
    'hanh_vat': {'hinh': 'Nhọn, tam giác', 'chat_lieu': 'Điện, lửa, nhựa', 'mau': 'Đỏ, hồng', 'huong': 'Nam', 'co_the': 'Tim, huyết mạch'},
    'van_vat_cu_the': {'do_vat': 'Bếp điện mới', 'nha_cua': 'Nhà ấm áp', 'nguoi': 'Người nổi bật', 'benh': 'Tim mạch tốt'},
    'tier_data': {'kich_thuoc': 'Lớn', 'tinh_trang': 'Mới', 'so_luong': 'Nhiều', 'chat_luong': 'Cao', 'con_nguoi': 'Khỏe mạnh'},
}

verdicts = {'km': 'CÁT', 'lh': 'HUNG', 'mh': 'CÁT', 'ln': 'CÁT', 'ta': 'BÌNH'}


# ═══════════════════════════════════════════════════════════════
# 20 CÂU HỎI ĐA DẠNG — Cover tất cả SĐ
# ═══════════════════════════════════════════════════════════════

QUESTIONS = [
    # (câu hỏi, expected_diagram_id, DT, hành_DT, mô tả)
    ("bố tôi bệnh nặng hay không", "SD1", "Quan Quỷ", "Hỏa", "SD1: Có/không + Sức khỏe"),
    ("tôi có nên đầu tư crypto không", "SD1", "Thê Tài", "Kim", "SD1: Có/không + Tài chính"),
    ("người yêu tôi bao nhiêu tuổi", "SD2", "Thê Tài", "Kim", "SD2: Tuổi"),
    ("nên kinh doanh gì", "SD3", "Thê Tài", "Kim", "SD3: Cái gì"),
    ("mất điện thoại ở đâu", "SD4", "Thê Tài", "Kim", "SD4: Ở đâu"),
    ("khi nào thăng chức", "SD5", "Quan Quỷ", "Hỏa", "SD5: Khi nào"),
    ("năm nay tài lộc thế nào", "SD6", "Thê Tài", "Kim", "SD6: Tài lộc"),
    ("tôi có lấy vợ được không", "SD7", "Thê Tài", "Kim", "SD7: Tình duyên"),
    ("bà ngoại ung thư có qua khỏi không", "SD8", "Quan Quỷ", "Hỏa", "SD8: Sức khỏe"),
    ("xin việc mới có được không", "SD9", "Quan Quỷ", "Hỏa", "SD9: Công việc"),
    ("kiện tụng đối phương thắng hay thua", "SD10", "Quan Quỷ", "Hỏa", "SD10: Kiện tụng"),
    ("mất xe máy tìm lại được không", "SD11", "Thê Tài", "Kim", "SD11: Mất đồ"),
    ("đi du lịch tuần này nên không", "SD12", "Thê Tài", "Kim", "SD12: Xuất hành"),
    ("ai lấy trộm tiền của tôi", "SD13", "Thê Tài", "Kim", "SD13: Ai"),
    ("tại sao công việc bế tắc", "SD14", "Quan Quỷ", "Hỏa", "SD14: Tại sao"),
    ("tình hình sức khỏe tôi thế nào", "SD15", "Quan Quỷ", "Hỏa", "SD15: Thế nào"),
    ("nên chọn việc A hay việc B", "SD16", "Quan Quỷ", "Hỏa", "SD16: Chọn lựa"),
    ("năm nay tốt không", "SD0", "Quan Quỷ", "Hỏa", "SD0: Tổng quát"),
    ("con dâu bao giờ sinh", "SD5", "Tử Tôn", "Mộc", "SD5: Khi nào + con"),
    ("đối tác có tin cậy không", "SD1", "Quan Quỷ", "Hỏa", "SD1: Có/không + đối tác"),
]


# ═══════════════════════════════════════════════════════════════
# HELPER: Extract tất cả {slot} từ template
# ═══════════════════════════════════════════════════════════════

def extract_template_slots(template_str):
    """Trích xuất tất cả {slot_name} từ template."""
    # Match {word} nhưng không match {total_score:+d}
    slots = re.findall(r'\{([a-z_]+?)(?::[^}]*)?\}', template_str)
    return list(dict.fromkeys(slots))  # Dedupe giữ thứ tự


def check_filled_template(filled, template_slots):
    """Check xem template đã fill hết chưa — tìm slot còn '{xxx}' trong output."""
    unfilled = re.findall(r'\{([a-z_]+?)(?::[^}]*)?\}', filled)
    return unfilled


# ═══════════════════════════════════════════════════════════════
# AUDIT 1: SĐ_MASTER — Test với 20 câu hỏi
# ═══════════════════════════════════════════════════════════════

print("=" * 80)
print("  V34.0 FULL AUDIT: TẤT CẢ SƠ ĐỒ × 20 CÂU HỎI")
print("=" * 80)

master_template_slots = extract_template_slots(DIAGRAM_MASTER['template'])
print(f"\n📐 SĐ_MASTER template có {len(master_template_slots)} slots: {', '.join(master_template_slots[:10])}...")

# Thống kê tổng
all_master_results = []
all_question_results = []

for q_text, expected_sd, dt, hanh, desc in QUESTIONS:
    print(f"\n{'─'*70}")
    print(f"  📝 {desc}")
    print(f"  Câu hỏi: \"{q_text}\"")
    print(f"  DT={dt}, Hành={hanh}, Expected SD={expected_sd}")
    
    # === Test SĐ_MASTER ===
    try:
        filled_master, info_master = h._fill_master_diagram(
            q_text, '🏥 Test', dt, hanh,
            unified_v22, v23_lh_factors, chart, luc_hao,
            mai_hoa_data=mai_hoa, v24_km_factors=v24_km_factors
        )
        
        slots_master = info_master.get('slots', {})
        
        # Check each slot
        missing_master = []
        questionmark_master = []
        na_master = []
        ok_master = []
        
        for slot_name in master_template_slots:
            val = str(slots_master.get(slot_name, '<<MISSING>>'))
            if val == '<<MISSING>>':
                missing_master.append(slot_name)
            elif val in ('?', ''):
                questionmark_master.append(slot_name)
            elif val in ('N/A', 'Không phát hiện'):
                na_master.append(slot_name)
            else:
                ok_master.append(slot_name)
        
        total_m = len(master_template_slots)
        ok_count_m = len(ok_master)
        pct_m = ok_count_m / total_m * 100 if total_m else 0
        
        # Also check for unfilled {slot} in rendered output
        unfilled_render = check_filled_template(filled_master, master_template_slots)
        
        # Print summary
        status = '✅' if pct_m >= 90 else '🟡' if pct_m >= 70 else '❌'
        print(f"\n  SĐ_MASTER: {status} {ok_count_m}/{total_m} ({pct_m:.0f}%)")
        if questionmark_master:
            print(f"    ❓ Dấu '?': {', '.join(questionmark_master)}")
        if missing_master:
            print(f"    🚫 MISSING: {', '.join(missing_master)}")
        if na_master:
            print(f"    ⚪ N/A: {', '.join(na_master)}")
        if unfilled_render:
            print(f"    🔴 UNFILLED in render: {', '.join(unfilled_render)}")
        
        all_master_results.append({
            'q': q_text, 'desc': desc, 'ok': ok_count_m, 'total': total_m,
            'missing': missing_master, 'qmark': questionmark_master, 'na': na_master,
            'unfilled': unfilled_render,
        })
    except Exception as e:
        print(f"\n  SĐ_MASTER: 💥 ERROR: {e}")
        import traceback; traceback.print_exc()
        all_master_results.append({
            'q': q_text, 'desc': desc, 'ok': 0, 'total': len(master_template_slots),
            'missing': master_template_slots, 'qmark': [], 'na': [], 'unfilled': [],
            'error': str(e),
        })
    
    # === Test SĐ thể loại ===
    try:
        # Match diagram
        matched_id, matched_diag = match_question_to_diagram(q_text)
        if matched_id == 'SD0' and expected_sd != 'SD0':
            # Use expected
            matched_id = expected_sd
            matched_diag = INTERACTION_DIAGRAMS.get(expected_sd, {})
        
        if matched_diag and 'template' in matched_diag:
            sd_template_slots = extract_template_slots(matched_diag['template'])
            
            filled_sd, info_sd = h._fill_question_diagram(
                matched_id, q_text, dt, hanh,
                unified_v22, v23_lh_factors, v24_km_factors,
                v24_mh_factors, chart, luc_hao, mai_hoa,
                verdicts_dict=verdicts
            )
            
            # Check unfilled slots in rendered template
            unfilled_sd = check_filled_template(filled_sd, sd_template_slots)
            
            # Check slot values from info
            sd_slots_data = {}
            # Parse filled template to find remaining '?'
            qmark_in_render = []
            for line in filled_sd.split('\n'):
                # Find patterns like ": ?" or "= ?" or ": N/A"
                if re.search(r':\s*\?\s*[│|]', line) or re.search(r'=\s*\?\s', line):
                    # Extract the label
                    m = re.search(r'[│║]\s*[⊕⊖⭐🚪🐉📍✨🔢📅🏛📊🎖🔑📜⚡☰🔥🔄☯△↗👻⭕💥📐🔧🎨🧭📏🆕🔢💎🧑🏥🔮🏠]\s*([^:]+):\s*\?', line)
                    if m:
                        qmark_in_render.append(m.group(1).strip())
                    else:
                        qmark_in_render.append(line.strip()[:40])
            
            total_sd = len(sd_template_slots)
            unfilled_count = len(unfilled_sd)
            ok_sd = total_sd - unfilled_count
            pct_sd = ok_sd / total_sd * 100 if total_sd else 0
            
            status_sd = '✅' if not unfilled_sd else '❌'
            print(f"\n  {matched_id} ({matched_diag.get('name', '')[:30]}):")
            print(f"    {status_sd} {ok_sd}/{total_sd} slots filled ({pct_sd:.0f}%)")
            if unfilled_sd:
                print(f"    🔴 UNFILLED: {', '.join(unfilled_sd)}")
            if qmark_in_render:
                print(f"    ❓ '?' in output: {', '.join(qmark_in_render[:5])}")
            
            all_question_results.append({
                'q': q_text, 'desc': desc, 'sd': matched_id,
                'ok': ok_sd, 'total': total_sd,
                'unfilled': unfilled_sd, 'qmark_render': qmark_in_render,
            })
        else:
            print(f"\n  {matched_id}: ⚪ No template found")
            all_question_results.append({
                'q': q_text, 'desc': desc, 'sd': matched_id,
                'ok': 0, 'total': 0, 'unfilled': [], 'qmark_render': [],
            })
    except Exception as e:
        print(f"\n  {expected_sd}: 💥 ERROR: {e}")
        import traceback; traceback.print_exc()
        all_question_results.append({
            'q': q_text, 'desc': desc, 'sd': expected_sd,
            'ok': 0, 'total': 0, 'unfilled': [], 'qmark_render': [],
            'error': str(e),
        })


# ═══════════════════════════════════════════════════════════════
# TỔNG KẾT
# ═══════════════════════════════════════════════════════════════

print("\n\n" + "=" * 80)
print("  📊 TỔNG KẾT AUDIT")
print("=" * 80)

# --- SĐ_MASTER ---
print("\n  ┌─── SĐ_MASTER ─────────────────────────────────────┐")
total_ok = sum(r['ok'] for r in all_master_results)
total_all = sum(r['total'] for r in all_master_results)
pct_total = total_ok / total_all * 100 if total_all else 0
print(f"  │ Tổng: {total_ok}/{total_all} ({pct_total:.1f}%)                        │")

# Count unique missing/qmark slots across all questions
all_qmark = set()
all_missing = set()
all_na = set()
all_unfilled_master = set()
for r in all_master_results:
    all_qmark.update(r['qmark'])
    all_missing.update(r['missing'])
    all_na.update(r['na'])
    all_unfilled_master.update(r['unfilled'])

if all_qmark:
    print(f"  │ Slots có dấu '?' ({len(all_qmark)}):                        │")
    for s in sorted(all_qmark):
        print(f"  │   ❓ {s:40s}        │")
if all_missing:
    print(f"  │ Slots MISSING ({len(all_missing)}):                          │")
    for s in sorted(all_missing):
        print(f"  │   🚫 {s:40s}        │")
if all_na:
    print(f"  │ Slots = N/A ({len(all_na)}):                              │")
    for s in sorted(all_na):
        print(f"  │   ⚪ {s:40s}        │")
if all_unfilled_master:
    print(f"  │ UNFILLED in render ({len(all_unfilled_master)}):               │")
    for s in sorted(all_unfilled_master):
        print(f"  │   🔴 {s:40s}        │")
print(f"  └──────────────────────────────────────────────────┘")

# --- SĐ thể loại ---
print("\n  ┌─── SĐ THỂ LOẠI (SD0-SD16) ────────────────────────┐")
sd_issues = {}
for r in all_question_results:
    sd = r['sd']
    if r.get('unfilled') or r.get('qmark_render'):
        if sd not in sd_issues:
            sd_issues[sd] = {'unfilled': set(), 'qmark': []}
        sd_issues[sd]['unfilled'].update(r.get('unfilled', []))
        sd_issues[sd]['qmark'].extend(r.get('qmark_render', []))

if sd_issues:
    for sd_id in sorted(sd_issues.keys()):
        issues = sd_issues[sd_id]
        uf = issues['unfilled']
        qm = issues['qmark'][:5]
        print(f"  │ {sd_id}:                                            │")
        if uf:
            print(f"  │   🔴 Unfilled: {', '.join(sorted(uf)[:5])}         │")
        if qm:
            print(f"  │   ❓ '?' values: {len(qm)} slots                    │")
else:
    print(f"  │ ✅ Tất cả SĐ thể loại đều fill đủ!               │")

print(f"  └──────────────────────────────────────────────────┘")

# Per-SD summary table
print("\n  ┌─────┬──────┬──────┬────────────────────────────────┐")
print("  │  SĐ │  OK  │ Total│ Status                         │")
print("  ├─────┼──────┼──────┼────────────────────────────────┤")
sd_summary = {}
for r in all_question_results:
    sd = r['sd']
    if sd not in sd_summary:
        sd_summary[sd] = {'ok': 0, 'total': 0, 'unfilled': set(), 'count': 0}
    sd_summary[sd]['ok'] += r['ok']
    sd_summary[sd]['total'] += r['total']
    sd_summary[sd]['unfilled'].update(r.get('unfilled', []))
    sd_summary[sd]['count'] += 1

for sd_id in sorted(sd_summary.keys()):
    s = sd_summary[sd_id]
    ok = s['ok']
    total = s['total']
    pct = ok / total * 100 if total else 0
    uf = s['unfilled']
    icon = '✅' if not uf else '❌'
    uf_str = ', '.join(sorted(uf)[:3]) if uf else 'ALL OK'
    print(f"  │ {sd_id:3s} │ {ok:4d} │ {total:4d} │ {icon} {uf_str:28s}│")

print("  └─────┴──────┴──────┴────────────────────────────────┘")

# Final verdict
total_issues = len(all_qmark) + len(all_missing) + len(all_unfilled_master) + sum(len(v['unfilled']) for v in sd_issues.values())
print(f"\n  🎯 TỔNG SỐ VẤN ĐỀ: {total_issues}")
if total_issues == 0:
    print("  🎉 HOÀN HẢO! Tất cả sơ đồ đều đã fill đầy đủ!")
else:
    print(f"  ⚠️ Cần fix {total_issues} vấn đề để đạt 100%")

# Save results to JSON for processing
results_file = os.path.join(os.path.dirname(__file__), 'audit_v34_results.json')
try:
    # Convert sets to lists for JSON
    export = {
        'master': {
            'total_ok': total_ok, 'total_all': total_all,
            'qmark_slots': sorted(all_qmark),
            'missing_slots': sorted(all_missing),
            'na_slots': sorted(all_na),
            'unfilled_slots': sorted(all_unfilled_master),
        },
        'question_diagrams': {
            sd_id: {
                'unfilled': sorted(v['unfilled']),
                'qmark_count': len(v['qmark']),
            } for sd_id, v in sd_issues.items()
        },
    }
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(export, f, ensure_ascii=False, indent=2)
    print(f"\n  📄 Chi tiết → {results_file}")
except:
    pass
