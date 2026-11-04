"""Test V40 FULL: Kiểm tra toàn diện — lỗi runtime + output quality"""
import sys, traceback
sys.path.insert(0, '.')

print("=" * 70)
print("TEST V40 FULL — KIEM TRA TOAN DIEN")
print("=" * 70)

# ========================================
# PHASE 1: IMPORT + INIT
# ========================================
print("\n[PHASE 1] Import & Init...")
try:
    from free_ai_helper import FreeAIHelper
    ai = FreeAIHelper()
    print("  OK: FreeAIHelper init thanh cong")
except Exception as e:
    print(f"  FAIL: {e}")
    traceback.print_exc()
    sys.exit(1)

# ========================================
# PHASE 2: 10 CAU HOI DA DANG
# ========================================
test_cases = [
    ("Co/Khong", "Mua nha nam nay tot khong?"),
    ("Nen/Ko nen", "Co nen dau tu crypto?"),
    ("Sinh tu", "Bo toi co qua khoi khong?"),
    ("Tong quat", "Cong viec thang nay the nao?"),
    ("Tim do", "Tim dien thoai o dau?"),
    ("Tinh cam", "Nguoi yeu co yeu toi that long khong?"),
    ("Tai chinh", "Toi co giau duoc khong?"),
    ("Suc khoe", "Suc khoe cua me toi the nao?"),
    ("Nha cua", "Co nen ban nha khong?"),
    ("Xuat hanh", "Di cong tac co thuan loi khong?"),
]

print(f"\n[PHASE 2] Chay {len(test_cases)} cau hoi...")
errors = []
results = []

for i, (cat, question) in enumerate(test_cases, 1):
    print(f"\n  [{i}/{len(test_cases)}] {cat}: {question[:50]}...")
    try:
        result = ai.answer_question(question)
        if result and len(result) > 100:
            results.append((cat, question, result))
            print(f"    OK: {len(result)} chars")
        else:
            errors.append((cat, question, f"Output qua ngan: {len(result) if result else 0} chars"))
            print(f"    WARN: Output ngan ({len(result) if result else 0} chars)")
    except Exception as e:
        errors.append((cat, question, str(e)))
        print(f"    FAIL: {str(e)[:100]}")
        traceback.print_exc()

# ========================================
# PHASE 3: KIEM TRA OUTPUT QUALITY
# ========================================
print(f"\n[PHASE 3] Kiem tra chat luong output...")

REQUIRED_SECTIONS = {
    "VI SAO": ["VÌ SAO", "📋 VÌ SAO"],
    "UNG KY": ["ỨNG KỲ", "⏳ ỨNG KỲ"],
    "GIAI PHAP": ["GIẢI PHÁP", "🔧 GIẢI PHÁP"],
    "KHANG DINH": ["📢", "CÂU TRẢ LỜI", "PHÁN QUYẾT", "KẾT LUẬN"],
    "PHAN TICH": ["BƯỚC", "Kỳ Môn", "Lục Hào", "Mai Hoa"],
}

quality_pass = 0
quality_fail = 0

for cat, question, result in results:
    missing = []
    for section_name, keywords in REQUIRED_SECTIONS.items():
        if not any(kw in result for kw in keywords):
            missing.append(section_name)
    
    if missing:
        quality_fail += 1
        print(f"  WARN [{cat}]: Thieu {', '.join(missing)}")
    else:
        quality_pass += 1

# ========================================
# PHASE 4: KIEM TRA SPECIFIC BUGS
# ========================================
print(f"\n[PHASE 4] Kiem tra bug cu the...")

bug_count = 0

for cat, question, result in results:
    # Bug 1: "NGHIENG THUAN" van con (ngon ngu mo ho)
    if "NGHIÊNG THUẬN" in result or "nghiêng thuận" in result:
        print(f"  BUG: [{cat}] Van con 'NGHIENG THUAN' mo ho!")
        bug_count += 1
    
    # Bug 2: "khong the xac dinh" (AI ne tranh)
    if "không thể xác định" in result.lower():
        print(f"  BUG: [{cat}] Van con 'khong the xac dinh'!")
        bug_count += 1
    
    # Bug 3: Ket luan khong co % (thieu data)
    import re
    pct_matches = re.findall(r'\d+%', result)
    if len(pct_matches) < 2:
        print(f"  WARN: [{cat}] Chi co {len(pct_matches)} % trong output (can >= 2)")
    
    # Bug 4: Phan Quyet khong co trong 2000 chars dau
    first_2000 = result[:2000]
    has_verdict = any(kw in first_2000 for kw in ["📢", "PHÁN QUYẾT", "CÂU TRẢ LỜI", "KẾT LUẬN"])
    if not has_verdict:
        print(f"  WARN: [{cat}] Phan quyet khong nam trong 2000 chars dau!")

# ========================================
# PHASE 5: EXTRACT KET LUAN DE DOC
# ========================================
print(f"\n[PHASE 5] Trich xuat ket luan chinh...")

for cat, question, result in results:
    # Tim dong ket luan
    for line in result.split('\n'):
        if '📢' in line and len(line.strip()) > 10:
            clean = line.strip().replace('>', '').replace('*', '').strip()
            print(f"  [{cat:12s}] {clean[:90]}")
            break

# ========================================
# TONG KET
# ========================================
print(f"\n{'=' * 70}")
print(f"TONG KET:")
print(f"  Runtime errors: {len(errors)}/{len(test_cases)}")
print(f"  Quality PASS:   {quality_pass}/{len(results)}")
print(f"  Quality FAIL:   {quality_fail}/{len(results)}")
print(f"  Known bugs:     {bug_count}")
print(f"{'=' * 70}")

if errors:
    print("\nCHI TIET LOI:")
    for cat, q, err in errors:
        print(f"  [{cat}] {q[:40]}: {err[:80]}")

if len(errors) == 0 and quality_fail == 0 and bug_count == 0:
    print("\n>>> ALL PASS! San sang deploy. <<<")
elif len(errors) == 0:
    print(f"\n>>> PASS CO DIEU KIEN: {quality_fail} quality issues, {bug_count} bugs <<<")
else:
    print(f"\n>>> FAIL: {len(errors)} runtime errors <<<")
