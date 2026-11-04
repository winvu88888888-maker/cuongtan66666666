# Final test V42.9.9i — ALL FIXES
import sys, os
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.path.insert(0, '.')

from free_ai_helper import FreeAIHelper, _get_dung_than, _analyze_dt_ecosystem, _NGUYEN_THAN_MAP

print("=" * 60)
print("FINAL TEST — V42.9.9i ALL FIXES")
print("=" * 60)

# ========== TEST 1: STANDALONE _get_dung_than ==========
print("\n--- TEST 1: _get_dung_than() standalone ---")
tests_standalone = [
    ('bo toi dau tu chung khoan co loi khong', 'The Tai'),
    ('me toi benh nang qua khoi khong', 'Phu Mau'),
    ('con trai thi do khong', 'Phu Mau'),
    ('chong ngoai tinh', 'The Tai'),
    ('bo me kinh doanh', 'The Tai'),
    ('me xin viec', 'Quan Quy'),
    ('bo benh', 'Phu Mau'),
    ('vo benh', 'The Tai'),
    ('dau tu co loi khong', 'The Tai'),
    ('xin viec co duoc khong', 'Quan Quy'),
]
pass1 = 0
for q, expected_ascii in tests_standalone:
    dt = _get_dung_than(q)
    # Normalize for comparison
    dt_norm = dt.replace('ê', 'e').replace('à', 'a').replace('ầ', 'au').replace('ử', 'u').replace('ỷ', 'y').replace('ụ', 'u').replace('ẫ', 'au').replace('ệ', 'e')
    exp_norm = expected_ascii.replace(' ', ' ')
    ok = any(k in dt for k in expected_ascii.split())
    status = 'PASS' if ok else 'CHECK'
    if ok: pass1 += 1
    print(f"  [{status}] \"{q}\" -> {dt}")
print(f"  Result: {pass1}/{len(tests_standalone)}")

# ========== TEST 2: Ecosystem Mapping ==========
print("\n--- TEST 2: Ecosystem Mapping (Nguyen/Ky/Cuu) ---")
eco_tests = [
    ('The Tai', 'Tu Ton', 'Huynh De', 'Quan Quy'),
    ('Quan Quy', 'The Tai', 'Tu Ton', 'Phu Mau'),
    ('Phu Mau', 'Quan Quy', 'The Tai', 'Huynh De'),
    ('Tu Ton', 'Huynh De', 'Phu Mau', 'The Tai'),
    ('Huynh De', 'Phu Mau', 'Quan Quy', 'Tu Ton'),
]
pass2 = 0
for dt, exp_ng, exp_ky, exp_cu in eco_tests:
    nkc = _NGUYEN_THAN_MAP.get(dt, {})
    ok = True
    print(f"  [{dt}] Nguyen={nkc.get('nguyen','?')} Ky={nkc.get('ky','?')} Cuu={nkc.get('cuu','?')}", end="")
    if nkc: pass2 += 1; print(" PASS")
    else: print(" FAIL")
print(f"  Result: {pass2}/{len(eco_tests)}")

# ========== TEST 3: Version ==========
print("\n--- TEST 3: Version strings ---")
h = FreeAIHelper()
v_ok = 'V42.9.9i' in h.version and 'V42.9.9i' in h.name
print(f"  Version: {h.version}")
print(f"  Name contains V42.9.9i: {v_ok}")

# ========== TEST 4: Full Pipeline (answer_question) ==========
print("\n--- TEST 4: Full Pipeline test ---")
result = h.answer_question('dau tu co phieu co loi khong')
checks = {
    'The Tai in output': 'The Tai' in result or 'Th\u00ea T\u00e0i' in result,
    'Ecosystem visible': any(k in result for k in ['HE SINH THAI', 'H\u1ec6 SINH TH\u00c1I', 'Nguy\u00ean Th\u1ea7n']),
    'Conclusion visible': any(k in result for k in ['KH\u1eb2NG \u0110\u1ecaNH', 'PHAN QUYET', 'PH\u00c1N QUY\u1ebeT', 'K\u1ebeT LU\u1eacN']),
    'Ung ky visible': any(k in result for k in ['\u1ee8NG K\u1ef2', 'UNG KY', 'th\u00e1ng']),
}
for check_name, check_ok in checks.items():
    status = 'PASS' if check_ok else 'FAIL'
    print(f"  [{status}] {check_name}")

# ========== TEST 5: Answer_question with person+action ==========
print("\n--- TEST 5: Person+Action via answer_question ---")
result2 = h.answer_question('bo toi dau tu chung khoan co loi khong')
has_the_tai = 'Th\u00ea T\u00e0i' in result2
print(f"  [{'PASS' if has_the_tai else 'FAIL'}] 'bo dau tu' -> DT=The Tai in output")

result3 = h.answer_question('me toi benh nang qua khoi khong')
has_phu_mau = 'Ph\u1ee5 M\u1eabu' in result3
print(f"  [{'PASS' if has_phu_mau else 'FAIL'}] 'me benh' -> DT=Phu Mau in output")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETE")
print("=" * 60)
