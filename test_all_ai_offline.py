# -*- coding: utf-8 -*-
"""
TEST TOÀN DIỆN AI OFFLINE — Tử Vi + Xem Ngày + Thắng Thua + Câu hỏi chung
"""
import sys, os
sys.path.insert(0, '.')

from free_ai_helper import FreeAIHelper, _is_competition_question, _extract_two_sides

helper = FreeAIHelper()

results = []

def test_question(label, question, must_contain=None, must_not_contain=None):
    """Test 1 câu hỏi AI Offline"""
    print(f"\n{'='*60}")
    print(f"📋 {label}")
    print(f"   Q: {question}")
    
    try:
        result = helper.answer_question(question, chart_data=None, topic=None)
        if not result:
            print(f"   ❌ FAIL — Result is empty!")
            results.append((label, 'FAIL', 'Empty result'))
            return
        
        rlen = len(result)
        ok = True
        issues = []
        
        # Check must_contain
        if must_contain:
            for kw in must_contain:
                if kw not in result:
                    ok = False
                    issues.append(f"Missing: '{kw}'")
        
        # Check must_not_contain
        if must_not_contain:
            for kw in must_not_contain:
                if kw in result:
                    ok = False
                    issues.append(f"Should NOT contain: '{kw}'")
        
        # General checks
        has_verdict = any(k in result for k in ['KHẲNG ĐỊNH', 'PHÁN QUYẾT', 'CÂU TRẢ LỜI'])
        has_analysis = any(k in result for k in ['LỤC HÀO', 'KỲ MÔN', 'MAI HOA'])
        
        status = '✅ PASS' if ok else '❌ FAIL'
        tag = f"{rlen} chars | verdict={'YES' if has_verdict else 'NO'} | analysis={'YES' if has_analysis else 'NO'}"
        
        if issues:
            tag += f" | Issues: {'; '.join(issues)}"
        
        print(f"   {status} — {tag}")
        
        # Show key parts
        if 'KHẲNG ĐỊNH' in result:
            idx = result.index('KHẲNG ĐỊNH')
            snippet = result[max(0,idx-20):idx+200].replace('\n', ' | ')
            print(f"   KẾT LUẬN: {snippet[:150]}")
        
        results.append((label, 'PASS' if ok else 'FAIL', tag))
        
    except Exception as e:
        import traceback
        print(f"   ❌ ERROR: {e}")
        traceback.print_exc()
        results.append((label, 'ERROR', str(e)[:100]))

# ═══════════════════════════════════════
# TEST 1: THẮNG THUA / COMPETITION
# ═══════════════════════════════════════
print("\n" + "🏆"*20)
print("PHẦN 1: THẮNG THUA / COMPETITION")
print("🏆"*20)

test_question(
    "1a. MU vs Liverpool ai thắng?",
    "MU vs Liverpool ai thắng?",
    must_contain=['MU', 'Liverpool', 'THẮNG'],
    must_not_contain=['Đặc điểm người được hỏi']
)

test_question(
    "1b. Chelsea vs Arsenal (standalone vs)",
    "Chelsea vs Arsenal",
    must_contain=['Chelsea', 'Arsenal'],
    must_not_contain=['Đặc điểm người được hỏi']
)

test_question(
    "1c. Câu không dấu",
    "MU vs Liverpool ai thang?",
    must_contain=['MU', 'Liverpool'],
)

# ═══════════════════════════════════════
# TEST 2: CÓ/KHÔNG — YES/NO
# ═══════════════════════════════════════
print("\n" + "❓"*20)
print("PHẦN 2: CÂU HỎI CÓ/KHÔNG")
print("❓"*20)

test_question(
    "2a. Có nên đầu tư?",
    "Tôi có nên đầu tư bất động sản không?",
    must_contain=['KHẲNG ĐỊNH'],
)

test_question(
    "2b. Có nên kết hôn?",
    "Có nên kết hôn năm nay không?",
    must_contain=['KHẲNG ĐỊNH'],
)

# ═══════════════════════════════════════
# TEST 3: SỨC KHỎE / SINH TỬ
# ═══════════════════════════════════════
print("\n" + "🏥"*20)
print("PHẦN 3: SỨC KHỎE / SINH TỬ")
print("🏥"*20)

test_question(
    "3a. Bố bệnh nặng",
    "Bố tôi bệnh nặng có qua khỏi không?",
    must_contain=['KHẲNG ĐỊNH'],
)

# ═══════════════════════════════════════
# TEST 4: TÀI CHÍNH
# ═══════════════════════════════════════
print("\n" + "💰"*20)
print("PHẦN 4: TÀI CHÍNH")
print("💰"*20)

test_question(
    "4a. Kinh doanh năm nay",
    "Kinh doanh năm nay có lãi không?",
    must_contain=['KHẲNG ĐỊNH'],
)

# ═══════════════════════════════════════
# TEST 5: TÌNH CẢM
# ═══════════════════════════════════════
print("\n" + "❤️"*20)
print("PHẦN 5: TÌNH CẢM")
print("❤️"*20)

test_question(
    "5a. Người yêu có thật lòng?",
    "Người yêu tôi có thật lòng không?",
    must_contain=['KHẲNG ĐỊNH'],
)

# ═══════════════════════════════════════
# TEST 6: THỜI GIAN / KHI NÀO
# ═══════════════════════════════════════
print("\n" + "⏰"*20)
print("PHẦN 6: THỜI GIAN")
print("⏰"*20)

test_question(
    "6a. Bao giờ có việc?",
    "Bao giờ tôi xin được việc mới?",
    must_contain=['KHẲNG ĐỊNH'],
)

# ═══════════════════════════════════════
# TEST 7: TÌM ĐỒ
# ═══════════════════════════════════════
print("\n" + "🔍"*20)
print("PHẦN 7: TÌM ĐỒ")
print("🔍"*20)

test_question(
    "7a. Mất điện thoại",
    "Tôi mất điện thoại ở đâu?",
    must_contain=['KHẲNG ĐỊNH'],
)

# ═══════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════
print("\n\n" + "="*60)
print("📊 KẾT QUẢ TỔNG HỢP")
print("="*60)

pass_count = sum(1 for _, s, _ in results if s == 'PASS')
fail_count = sum(1 for _, s, _ in results if s == 'FAIL')
error_count = sum(1 for _, s, _ in results if s == 'ERROR')

for label, status, detail in results:
    icon = '✅' if status == 'PASS' else '❌' if status == 'FAIL' else '💥'
    print(f"  {icon} {label}: {detail[:80]}")

print(f"\n  TỔNG: {pass_count} PASS / {fail_count} FAIL / {error_count} ERROR")
if fail_count == 0 and error_count == 0:
    print("  🎉 TẤT CẢ PASS!")
