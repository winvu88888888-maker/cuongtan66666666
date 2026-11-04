# -*- coding: utf-8 -*-
"""
AUDIT TOÀN DIỆN V42.8 — Kiểm tra mọi bug còn sót
"""
import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("🔍 AUDIT TOÀN DIỆN — Tìm bug dữ liệu/logic")
print("=" * 70)

errors = []
warnings = []

# ═══ TEST 1: solar2lunar accuracy ═══
print("\n📋 TEST 1: solar2lunar accuracy")
from xem_ngay_dep import solar2lunar

test_cases = [
    # (dd, mm, yyyy, expected_d, expected_m, expected_y, label)
    (15, 1, 1990, 19, 12, 1989, "15/01/1990 = 19/12/Kỷ Tỵ"),
    (27, 1, 1990, 1, 1, 1990, "27/01/1990 = Mùng 1 Tết Canh Ngọ"),
    (23, 4, 2026, 7, 3, 2026, "23/04/2026 = 7/3 Bính Ngọ"),
    (24, 4, 2026, 8, 3, 2026, "24/04/2026 = 8/3 Bính Ngọ"),
    (1, 2, 2025, 4, 1, 2025, "01/02/2025 = 4/1 Ất Tỵ"),
    (29, 1, 2025, 1, 1, 2025, "29/01/2025 = Mùng 1 Tết Ất Tỵ"),
    (10, 2, 2024, 1, 1, 2024, "10/02/2024 = Mùng 1 Tết Giáp Thìn"),
]

for dd, mm, yyyy, exp_d, exp_m, exp_y, label in test_cases:
    d, m, y, leap = solar2lunar(dd, mm, yyyy)
    status = "✅" if (d == exp_d and m == exp_m and y == exp_y) else "❌"
    if status == "❌":
        errors.append(f"solar2lunar({dd}/{mm}/{yyyy}) = {d}/{m}/{y}, expected {exp_d}/{exp_m}/{exp_y}")
    print(f"  {status} {label}: got {d}/{m}/{y} {'(nhuận)' if leap else ''}")

# ═══ TEST 2: Tu Vi lap_la_so return keys ═══
print("\n📋 TEST 2: Tu Vi lap_la_so return keys")
from tu_vi import lap_la_so

ls = lap_la_so(1989, 12, 19, 0, 'nam')  # Kỷ Tỵ
required_keys = ['nam_sinh', 'thang_am', 'ngay_am', 'gio', 'can_nam', 'chi_nam',
                 'nap_am', 'menh_cung', 'than_cung', 'cuc', 'cuc_ten',
                 'cung_map', 'tu_hoa', 'dai_han', 'luu_nien', 'gioi_tinh']

for key in required_keys:
    if key in ls:
        val = ls[key]
        vtype = type(val).__name__
        if key == 'menh_cung':
            if isinstance(val, dict) and 'chi' in val:
                print(f"  ✅ {key}: dict with chi='{val['chi']}'")
            else:
                errors.append(f"menh_cung is not dict with 'chi': {val}")
                print(f"  ❌ {key}: WRONG TYPE {vtype} = {val}")
        elif key == 'than_cung':
            if isinstance(val, dict) and 'chi' in val:
                print(f"  ✅ {key}: dict with chi='{val['chi']}'")
            else:
                errors.append(f"than_cung is not dict with 'chi': {val}")
                print(f"  ❌ {key}: WRONG TYPE {vtype} = {val}")
        elif key == 'cuc':
            print(f"  ℹ️ {key}: {vtype} = {val} (number, use cuc_ten for display)")
        elif key == 'cuc_ten':
            print(f"  ✅ {key}: '{val}'")
        elif key == 'cung_map':
            if isinstance(val, dict) and len(val) > 0:
                print(f"  ✅ {key}: dict with {len(val)} cung")
            else:
                errors.append(f"cung_map is empty or wrong type")
                print(f"  ❌ {key}: EMPTY or WRONG")
        elif key == 'dai_han':
            if isinstance(val, list) and len(val) > 0:
                dh = val[0]
                print(f"  ✅ {key}: list[{len(val)}], first={dh}")
                # Check dai_han structure
                dh_keys = ['tu', 'den', 'tuoi_range', 'cung', 'chi']
                for dk in dh_keys:
                    if dk not in dh:
                        errors.append(f"dai_han[0] missing key '{dk}'")
                        print(f"    ❌ Missing key '{dk}' in dai_han entry")
            else:
                errors.append(f"dai_han is empty or wrong type")
                print(f"  ❌ {key}: EMPTY or WRONG")
        elif key == 'luu_nien':
            if isinstance(val, dict):
                ln_keys = ['nam', 'tuoi', 'cung', 'chi']
                missing = [k for k in ln_keys if k not in val]
                if missing:
                    errors.append(f"luu_nien missing keys: {missing}")
                    print(f"  ❌ {key}: missing {missing}")
                else:
                    print(f"  ✅ {key}: {val}")
            else:
                errors.append(f"luu_nien is not dict: {val}")
                print(f"  ❌ {key}: not dict")
        else:
            print(f"  ✅ {key}: {vtype}")
    else:
        errors.append(f"Missing key '{key}' in lap_la_so return")
        print(f"  ❌ MISSING: {key}")

# ═══ TEST 3: Xem Ngay danh_gia_ngay return keys ═══
print("\n📋 TEST 3: Xem Ngay danh_gia_ngay return keys")
from xem_ngay_dep import danh_gia_ngay

xn = danh_gia_ngay(3, 8, 'Giáp', 'Thìn', 'cuoi_hoi', ngay_dl=(24, 4, 2026))
required_xn_keys = ['diem', 'verdict', 'truc', 'truc_info', 'sao_hoang_dao',
                     'is_hoang_dao', 'is_tam_nuong', 'is_nguyet_pha', 'is_duong_cong_ky',
                     'has_thien_duc', 'has_nguyet_duc', 'truc_tot_cho_viec', 'truc_xau_cho_viec',
                     'ly_do_tot', 'ly_do_xau', 'loai_viec', 'can_ngay', 'chi_ngay',
                     'thang_am', 'ngay_am', 'sao_28_tu']

for key in required_xn_keys:
    if key in xn:
        val = xn[key]
        vtype = type(val).__name__
        if key == 'truc_info':
            if isinstance(val, dict):
                ti_keys = ['nen', 'ky', 'mo_ta', 'cat_hung']
                missing = [k for k in ti_keys if k not in val]
                if missing:
                    warnings.append(f"truc_info missing keys: {missing}")
                    print(f"  ⚠️ {key}: missing {missing}")
                else:
                    print(f"  ✅ {key}: dict with {len(val)} keys")
            else:
                errors.append(f"truc_info is not dict")
                print(f"  ❌ {key}: not dict")
        elif key == 'sao_28_tu':
            if isinstance(val, (list, tuple)) and len(val) >= 4:
                print(f"  ✅ {key}: {val[0]} ({val[1]}) len={len(val)}")
            elif val is None:
                warnings.append(f"sao_28_tu is None")
                print(f"  ⚠️ {key}: None")
            else:
                print(f"  ℹ️ {key}: {val}")
        else:
            print(f"  ✅ {key}: {vtype} = {repr(val)[:80]}")
    else:
        errors.append(f"Missing key '{key}' in danh_gia_ngay return")
        print(f"  ❌ MISSING: {key}")

# ═══ TEST 4: 28 Sao accuracy ═══
print("\n📋 TEST 4: 28 Sao accuracy check")
from xem_ngay_dep import tinh_28_tu

test_28 = [
    (24, 4, 2026, "Tỉnh"),  # verified
]
for dd, mm, yy, expected in test_28:
    result = tinh_28_tu(dd, mm, yy)
    name = result[0] if result else "?"
    status = "✅" if name == expected else "❌"
    if status == "❌":
        errors.append(f"28 sao {dd}/{mm}/{yy}: got '{name}', expected '{expected}'")
    print(f"  {status} {dd}/{mm}/{yy}: got '{name}', expected '{expected}'")

# ═══ TEST 5: JDN Can/Chi calculation ═══
print("\n📋 TEST 5: JDN Can Chi ngày accuracy")
# Check if the inline JDN formula in app.py is correct
# app.py line 3303: _jdn = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day - 1524
# This is the Julian Day Number formula (simplified)
# Can ngay: (jdn + 9) % 10
# Chi ngay: (jdn + 1) % 12

CANS = ['Giáp','Ất','Bính','Đinh','Mậu','Kỷ','Canh','Tân','Nhâm','Quý']
CHIS = ['Tý','Sửu','Dần','Mão','Thìn','Tị','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi']

def jdn_simple(dd, mm, yy):
    """Same formula as app.py line 3303"""
    return int(365.25 * (yy + 4716)) + int(30.6001 * (mm + 1)) + dd - 1524

def jdn_accurate(dd, mm, yy):
    """Accurate JDN from xem_ngay_dep"""
    from xem_ngay_dep import _jdn
    return _jdn(dd, mm, yy)

# Test known dates
test_jdn = [
    (24, 4, 2026, 'Giáp', 'Thìn'),  # 24/4/2026
    (23, 4, 2026, 'Quý', 'Mão'),    # 23/4/2026  
]

for dd, mm, yy, exp_can, exp_chi in test_jdn:
    j_simple = jdn_simple(dd, mm, yy)
    j_accurate = jdn_accurate(dd, mm, yy)
    
    can_s = CANS[(j_simple + 9) % 10]
    chi_s = CHIS[(j_simple + 1) % 12]
    
    can_a = CANS[(j_accurate + 9) % 10]
    chi_a = CHIS[(j_accurate + 1) % 12]
    
    match_simple = (can_s == exp_can and chi_s == exp_chi)
    match_accurate = (can_a == exp_can and chi_a == exp_chi)
    
    print(f"  {dd}/{mm}/{yy}:")
    print(f"    Simple JDN={j_simple}: {can_s} {chi_s} {'✅' if match_simple else '❌'}")
    print(f"    Accurate JDN={j_accurate}: {can_a} {chi_a} {'✅' if match_accurate else '❌'}")
    
    if j_simple != j_accurate:
        warnings.append(f"JDN mismatch {dd}/{mm}/{yy}: simple={j_simple} vs accurate={j_accurate} (diff={j_simple-j_accurate})")
    if not match_simple:
        errors.append(f"Simple JDN Can/Chi wrong for {dd}/{mm}/{yy}: got {can_s} {chi_s}, expected {exp_can} {exp_chi}")

# ═══ TEST 6: app.py inline display bugs ═══
print("\n📋 TEST 6: app.py inline display patterns")

with open('app.py', 'r', encoding='utf-8') as f:
    app_lines = f.readlines()

# Check menh_cung display WITHOUT .get('chi')
bug_count = 0
for i, line in enumerate(app_lines, 1):
    s = line.strip()
    # Pattern: .get('menh_cung','?') — this shows dict instead of string
    if "menh_cung" in s and "get(" in s and "'?'" in s and "chi" not in s and "isinstance" not in s and "V42.8" not in s:
        bug_count += 1
        errors.append(f"Line {i}: menh_cung displayed as raw dict: {s[:100]}")
        print(f"  ❌ Line {i}: menh_cung raw dict: {s[:100]}")

    # Pattern: .get('cuc','?') without cuc_ten
    if "get('cuc'" in s and "'?'" in s and "cuc_ten" not in s:
        bug_count += 1
        errors.append(f"Line {i}: cuc displayed as number: {s[:100]}")
        print(f"  ❌ Line {i}: cuc raw number: {s[:100]}")

if bug_count == 0:
    print("  ✅ No inline display bugs found")

# ═══ TEST 7: Check Xem Ngay main section ═══
print("\n📋 TEST 7: Xem Ngay main section data flow")
# Check if main Xem Ngay section (tab xem_ngay_dep) also has correct keys
for i, line in enumerate(app_lines, 1):
    s = line.strip()
    if 'current_view' in s and 'xem_ngay' in s:
        print(f"  ℹ️ Xem Ngay section at line {i}")

# ═══ TEST 8: Check app.py branch for Âm Lịch input — year used ═══
print("\n📋 TEST 8: Âm Lịch branch year usage")
# Line 3240: qa_tv_nam = st.number_input("Năm sinh (DL):", ...)
# Line 3251: _la_so = lap_la_so(qa_tv_nam, ...)
# Problem: label says "DL" but lap_la_so expects ÂL year
# If user enters 1990 (DL), and born in Jan → lunar year is 1989

for i, line in enumerate(app_lines, 1):
    s = line.strip()
    if 'qa_tv_nam_al' in s and 'number_input' in s:
        print(f"  ⚠️ Line {i}: {s[:100]}")
        warnings.append(f"Line {i}: Label says 'Năm sinh (DL)' but used directly in lap_la_so. User might enter solar year but lunar year is needed for accurate calculation.")

# Check if qa_tv_nam is solar year being passed directly
for i, line in enumerate(app_lines, 1):
    s = line.strip()
    if 'lap_la_so(qa_tv_nam,' in s:
        print(f"  ⚠️ Line {i}: {s[:80]}")
        warnings.append(f"Line {i}: qa_tv_nam (potentially solar year) passed directly to lap_la_so")

# ═══ SUMMARY ═══
print("\n" + "=" * 70)
print(f"📊 KẾT QUẢ AUDIT: {len(errors)} LỖI | {len(warnings)} CẢNH BÁO")
print("=" * 70)

if errors:
    print("\n🔴 LỖI:")
    for i, e in enumerate(errors, 1):
        print(f"  {i}. {e}")

if warnings:
    print("\n🟡 CẢNH BÁO:")
    for i, w in enumerate(warnings, 1):
        print(f"  {i}. {w}")

if not errors and not warnings:
    print("\n✅ Không tìm thấy lỗi hay cảnh báo nào!")
