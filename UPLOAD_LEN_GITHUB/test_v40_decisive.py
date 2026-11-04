"""Test V40: Decisive Conclusion — VÌ SAO + ỨNG KỲ + GIẢI PHÁP"""
import sys
sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper

ai = FreeAIHelper()

# 5 câu hỏi kiểm tra
test_cases = [
    "Mua nhà năm nay tốt không?",
    "Bố tôi có qua khỏi không?",
    "Có nên đầu tư crypto?",
    "Công việc tháng này thế nào?",
    "Tìm điện thoại ở đâu?",
]

REQUIRED_MARKERS = {
    "VÌ SAO": ["VÌ SAO", "📋 VÌ SAO"],
    "ỨNG KỲ": ["ỨNG KỲ", "⏳ ỨNG KỲ", "tháng", "ÂL"],
    "GIẢI PHÁP": ["GIẢI PHÁP", "🔧 GIẢI PHÁP"],
    "KHẲNG ĐỊNH": ["KHẲNG ĐỊNH", "📢", "CÂU TRẢ LỜI"],
}

print("=" * 60)
print("TEST V40: DECISIVE CONCLUSION")
print("=" * 60)

passed = 0
failed = 0

for q in test_cases:
    print(f"\n{'─' * 60}")
    print(f"❓ {q}")
    
    result = ai.answer_question(q)
    
    if not result:
        print("  ❌ FAIL: Không có kết quả!")
        failed += 1
        continue
    
    all_ok = True
    for marker_name, keywords in REQUIRED_MARKERS.items():
        found = any(kw in result for kw in keywords)
        if found:
            print(f"  ✅ {marker_name}: FOUND")
        else:
            print(f"  ❌ {marker_name}: MISSING!")
            all_ok = False
    
    # Kiểm tra có bằng chứng cụ thể (factor text with +/- score)
    import re
    factor_refs = re.findall(r'[+-]\d+', result)
    if len(factor_refs) >= 3:
        print(f"  ✅ BẰNG CHỨNG CỤ THỂ: {len(factor_refs)} điểm số trích dẫn")
    else:
        print(f"  ⚠️ BẰNG CHỨNG CỤ THỂ: chỉ {len(factor_refs)} điểm số (cần >= 3)")
    
    # Trích xuất kết luận chính
    for line in result.split('\n'):
        if '📢' in line and ('CÂU TRẢ LỜI' in line or 'PHÁN QUYẾT' in line or 'KẾT LUẬN' in line):
            print(f"  → {line.strip()[:100]}")
            break
    
    if all_ok:
        passed += 1
    else:
        failed += 1

print(f"\n{'=' * 60}")
print(f"KẾT QUẢ: {passed}/{len(test_cases)} PASS, {failed}/{len(test_cases)} FAIL")
print("=" * 60)
