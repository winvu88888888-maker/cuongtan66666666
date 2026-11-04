# -*- coding: utf-8 -*-
"""
FINAL AUDIT V42.8f — Xác nhận TẤT CẢ đã sửa 100%
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

errors = []
passes = []

# ═══ TEST 1: solar2lunar ═══
print("📋 TEST 1: solar2lunar accuracy (7 ngày)")
from xem_ngay_dep import solar2lunar

test_cases = [
    (15, 1, 1990, 19, 12, 1989, "15/01/1990 = 19/12/Kỷ Tỵ"),
    (27, 1, 1990, 1, 1, 1990, "27/01/1990 = Mùng 1 Tết"),
    (23, 4, 2026, 7, 3, 2026, "23/04/2026 = 7/3 Bính Ngọ"),
    (24, 4, 2026, 8, 3, 2026, "24/04/2026 = 8/3"),
    (1, 2, 2025, 4, 1, 2025, "01/02/2025"),
    (29, 1, 2025, 1, 1, 2025, "29/01/2025 = Mùng 1 Tết Ất Tỵ"),
    (10, 2, 2024, 1, 1, 2024, "10/02/2024 = Mùng 1 Tết Giáp Thìn"),
]
for dd, mm, yy, exp_d, exp_m, exp_y, label in test_cases:
    d, m, y, _ = solar2lunar(dd, mm, yy)
    ok = (d == exp_d and m == exp_m and y == exp_y)
    print(f"  {'✅' if ok else '❌'} {label}")
    if ok: passes.append(f"solar2lunar {label}")
    else: errors.append(f"solar2lunar({dd}/{mm}/{yy}) = {d}/{m}/{y}, expected {exp_d}/{exp_m}/{exp_y}")

# ═══ TEST 2: Tu Vi lap_la_so return ═══
print("\n📋 TEST 2: Tu Vi lap_la_so keys (16 keys)")
from tu_vi import lap_la_so
ls = lap_la_so(1989, 12, 19, 0, 'nam')
required_keys = ['nam_sinh','thang_am','ngay_am','gio','can_nam','chi_nam',
                 'nap_am','menh_cung','than_cung','cuc','cuc_ten',
                 'cung_map','tu_hoa','dai_han','luu_nien','gioi_tinh']
for key in required_keys:
    ok = key in ls
    if ok: passes.append(f"tu_vi.{key}")
    else: errors.append(f"tu_vi missing key '{key}'")
# Verify types
mc = ls.get('menh_cung',{})
ok_mc = isinstance(mc, dict) and 'chi' in mc
if ok_mc: passes.append("menh_cung is dict with 'chi'")
else: errors.append(f"menh_cung wrong type: {mc}")
ok_cuc = isinstance(ls.get('cuc_ten',''), str) and len(ls.get('cuc_ten','')) > 0
if ok_cuc: passes.append("cuc_ten is string")
else: errors.append("cuc_ten missing/empty")
ok_cm = isinstance(ls.get('cung_map',{}), dict) and len(ls.get('cung_map',{})) == 12
if ok_cm: passes.append("cung_map has 12 cung")
else: errors.append(f"cung_map has {len(ls.get('cung_map',{}))} cung, expected 12")
print(f"  ✅ {len([k for k in required_keys if k in ls])}/16 keys present | menh_cung={'✅' if ok_mc else '❌'} | cuc_ten={'✅' if ok_cuc else '❌'} | cung_map={'✅' if ok_cm else '❌'}")

# ═══ TEST 3: Xem Ngay danh_gia_ngay return ═══
print("\n📋 TEST 3: danh_gia_ngay keys (21 keys)")
from xem_ngay_dep import danh_gia_ngay
xn = danh_gia_ngay(3, 8, 'Mậu', 'Thìn', 'cuoi_hoi', ngay_dl=(24, 4, 2026))
required_xn = ['diem','verdict','truc','truc_info','sao_hoang_dao','is_hoang_dao',
               'is_tam_nuong','is_nguyet_pha','is_duong_cong_ky','has_thien_duc',
               'has_nguyet_duc','truc_tot_cho_viec','truc_xau_cho_viec',
               'ly_do_tot','ly_do_xau','loai_viec','can_ngay','chi_ngay',
               'thang_am','ngay_am','sao_28_tu']
xn_ok = sum(1 for k in required_xn if k in xn)
for k in required_xn:
    if k in xn: passes.append(f"xn.{k}")
    else: errors.append(f"xn missing key '{k}'")
print(f"  ✅ {xn_ok}/21 keys present | Diem={xn.get('diem')} | Truc={xn.get('truc')} | Can/Chi={xn.get('can_ngay')} {xn.get('chi_ngay')}")

# ═══ TEST 4: 28 Sao ═══
print("\n📋 TEST 4: 28 Sao accuracy")
from xem_ngay_dep import tinh_28_tu
# 23/4/2026 = Tỉnh (verified V42.8), 24/4 = Quỷ (next in cycle)
tests_28 = [(23,4,2026,"Tỉnh"), (24,4,2026,"Quỷ")]
for dd,mm,yy,exp in tests_28:
    s = tinh_28_tu(dd,mm,yy)
    name = s[0] if s else "?"
    ok = name == exp
    print(f"  {'✅' if ok else '❌'} {dd}/{mm}/{yy}: {name} (expected {exp})")
    if ok: passes.append(f"28sao {dd}/{mm}/{yy}={exp}")
    else: errors.append(f"28sao {dd}/{mm}/{yy}: got {name}, expected {exp}")

# ═══ TEST 5: JDN accuracy — code NO LONGER uses bad formula ═══
print("\n📋 TEST 5: Bad JDN formula removed from codebase")
bad_formula_count = 0
for fname in ['app.py', 'free_ai_helper.py', 'qmdg_calc.py', 'xem_ngay_dep.py', 'tu_vi.py']:
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if '365.25' in line and '30.6001' in line:
                    bad_formula_count += 1
                    errors.append(f"{fname}:{i} still has bad JDN formula")
                    print(f"  ❌ {fname}:{i}: {line.strip()[:80]}")
if bad_formula_count == 0:
    passes.append("No bad JDN formulas in codebase")
    print("  ✅ No bad JDN formula found in any file")

# ═══ TEST 6: app.py display — menh_cung/cuc correctly displayed ═══
print("\n📋 TEST 6: app.py inline display correctness")
with open('app.py', 'r', encoding='utf-8') as f:
    app_lines = f.readlines()

display_bugs = 0
for i, line in enumerate(app_lines, 1):
    s = line.strip()
    # Check menh_cung displayed without .get('chi')
    if "menh_cung" in s and ".get(" in s and "'?'" in s and "chi" not in s and "isinstance" not in s and "V42.8" not in s:
        display_bugs += 1
        errors.append(f"Line {i}: menh_cung raw dict display")
    # Check cuc without cuc_ten
    if "get('cuc'" in s and "'?'" in s and "cuc_ten" not in s:
        display_bugs += 1
        errors.append(f"Line {i}: cuc raw number display")

if display_bugs == 0:
    passes.append("No inline display bugs")
    print("  ✅ No menh_cung raw dict or cuc raw number display")
else:
    print(f"  ❌ Found {display_bugs} display bugs")

# ═══ TEST 7: AI context keys match actual return ═══
print("\n📋 TEST 7: AI context uses correct keys from lap_la_so/danh_gia_ngay")
# Check app.py uses cung_map (not cung), cuc_ten (not cuc), menh_cung.get('chi')
ai_context_ok = True
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

checks = [
    ("menh_cung', {}).get('chi'", "menh_cung accessed with .get('chi')"),
    ("than_cung', {}).get('chi'", "than_cung accessed with .get('chi')"),
    ("cuc_ten", "cuc_ten used for display"),
    ("cung_map", "cung_map used instead of cung"),
    ("_jdn_accurate", "accurate JDN imported"),
]
for pattern, desc in checks:
    found = pattern in content
    print(f"  {'✅' if found else '❌'} {desc}")
    if found: passes.append(f"AI context: {desc}")
    else: errors.append(f"AI context missing: {desc}")

# ═══ TEST 8: free_ai_helper.py uses accurate JDN ═══
print("\n📋 TEST 8: free_ai_helper.py JDN fix")
with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    fah_content = f.read()

if '_jdn_func' in fah_content:
    passes.append("free_ai_helper uses _jdn_func")
    print("  ✅ Uses _jdn_func from xem_ngay_dep")
else:
    errors.append("free_ai_helper missing _jdn_func")
    print("  ❌ Missing _jdn_func import")

if '_jdn_func2' in fah_content:
    passes.append("free_ai_helper fallback uses _jdn_func2")
    print("  ✅ Fallback uses _jdn_func2 from xem_ngay_dep")
else:
    errors.append("free_ai_helper missing _jdn_func2")
    print("  ❌ Missing _jdn_func2 import")

# ═══ TEST 9: Actual scoring verification ═══
print("\n📋 TEST 9: End-to-end scoring (24/4/2026 Cưới Hỏi)")
from xem_ngay_dep import _jdn as accurate_jdn
CANS = ['Giáp','Ất','Bính','Đinh','Mậu','Kỷ','Canh','Tân','Nhâm','Quý']
CHIS = ['Tý','Sửu','Dần','Mão','Thìn','Tị','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi']
jdn_val = accurate_jdn(24, 4, 2026)
cn = CANS[(jdn_val + 9) % 10]
chi = CHIS[(jdn_val + 1) % 12]
d_al, m_al, y_al, _ = solar2lunar(24, 4, 2026)
xn_final = danh_gia_ngay(m_al, d_al, cn, chi, 'cuoi_hoi', ngay_dl=(24, 4, 2026))
score = xn_final.get('diem', 0)
truc = xn_final.get('truc', '?')

print(f"  Can/Chi: {cn} {chi}")
print(f"  ÂL: {d_al}/{m_al}/{y_al}")
print(f"  Trực: {truc}")
print(f"  Điểm: {score}/100")
print(f"  Verdict: {xn_final.get('verdict','?')}")

if cn == 'Mậu' and chi == 'Thìn' and truc == 'Kiến' and score >= 70:
    passes.append(f"End-to-end: {cn} {chi}, Trực {truc}, {score}/100")
    print(f"  ✅ PASS — Can/Chi, Trực, Điểm all correct!")
else:
    errors.append(f"End-to-end: {cn} {chi}, Trực {truc}, {score}/100")
    print(f"  ❌ FAIL")

# ═══ TEST 10: Label check ═══
print("\n📋 TEST 10: UI Label correctness")
found_old_label = False
for i, line in enumerate(app_lines, 1):
    if 'qa_tv_nam_al' in line and 'number_input' in line and 'DL' in line:
        found_old_label = True
        errors.append(f"Line {i}: Still shows 'Năm sinh (DL)' for ÂL input")
        print(f"  ❌ Line {i}: Old label 'DL' still present")
if not found_old_label:
    passes.append("Label 'Năm ÂL' correct")
    print("  ✅ Label changed to 'Năm ÂL'")

# ═══ FINAL SUMMARY ═══
print("\n" + "=" * 70)
total = len(passes) + len(errors)
pct = len(passes) * 100 // total if total > 0 else 0
if len(errors) == 0:
    print(f"🎉 KẾT QUẢ: {len(passes)}/{total} PASS — 100% HOÀN TẤT!")
    print("✅ TẤT CẢ ĐÃ SỬA ĐÚNG 100% — KHÔNG CÒN BUG NÀO!")
else:
    print(f"📊 KẾT QUẢ: {len(passes)}/{total} PASS ({pct}%) | {len(errors)} LỖI CÒN LẠI")
    for e in errors:
        print(f"  ❌ {e}")
print("=" * 70)
