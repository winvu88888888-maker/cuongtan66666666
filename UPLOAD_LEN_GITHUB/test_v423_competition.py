"""
V42.3 COMPETITION (THẮNG THUA) ANALYSIS — Test Suite
Kiểm tra phân tích Thế vs Ứng / Chủ vs Khách / Thể vs Dụng
"""
import sys
sys.path.insert(0, '.')

from free_ai_helper import FreeAIHelper, _is_competition_question

helper = FreeAIHelper()

# ═══════════════════════════════════════════
# TEST 1: DETECTION — is_competition_question
# ═══════════════════════════════════════════
COMP_QUESTIONS = [
    "Đội bóng A và đội bóng B đội nào thắng và tỷ số bao nhiêu?",
    "Manchester United vs Liverpool ai thắng?",
    "Trận chung kết World Cup đội nào vô địch?",
    "Bóng đá hôm nay đội nào thắng?",
    "Trận bán kết kết quả bao nhiêu?",
    "Giải đấu tennis ai thắng?",
    "Trận đấu boxing kết quả thế nào?",
    "Đội A đấu đội B thắng thua thế nào?",
]

NOT_COMP_QUESTIONS = [
    "Tôi có thắng kiện không?",  # Kiện tụng, không phải competition
    "Tài chính năm nay thế nào?",
    "Sức khỏe bố tôi có qua khỏi không?",
    "Mua vàng lúc này có lợi không?",
]

print("=" * 70)
print("🧪 V42.3 THẮNG THUA ANALYSIS — TEST SUITE")
print("=" * 70)

print(f"\n{'='*70}")
print(f"🔍 TEST 1: DETECTION (_is_competition_question)")
print(f"{'='*70}")

det_pass = 0
for q in COMP_QUESTIONS:
    r = _is_competition_question(q)
    s = "✅" if r else "❌"
    if r: det_pass += 1
    print(f"  {s} [{'COMP' if r else 'MISS'}] {q[:60]}")

for q in NOT_COMP_QUESTIONS:
    r = _is_competition_question(q)
    s = "✅" if not r else "❌"
    if not r: det_pass += 1
    print(f"  {s} [{'OK  ' if not r else 'FP  '}] {q[:60]}")

print(f"\n  Detection: {det_pass}/{len(COMP_QUESTIONS) + len(NOT_COMP_QUESTIONS)} correct")

# ═══════════════════════════════════════════
# TEST 2: FULL PIPELINE — answer_question
# ═══════════════════════════════════════════
print(f"\n{'='*70}")
print(f"⚔️ TEST 2: FULL PIPELINE — answer_question")
print(f"{'='*70}")

TEST_QUESTIONS = [
    "Đội bóng A và đội bóng B đội nào thắng và tỷ số bao nhiêu?",
    "Manchester vs Liverpool ai thắng trận đêm nay?",
    "Trận chung kết ai vô địch?",
]

for q in TEST_QUESTIONS:
    print(f"\n{'─'*60}")
    print(f"❓ CÂU HỎI: {q}")
    print(f"{'─'*60}")
    result = helper.answer_question(q)
    
    # Check key elements
    has_verdict = "PHÁN QUYẾT" in result
    has_the_ung = "Thế" in result or "THẾ" in result
    has_method = "LH:" in result or "KM:" in result or "MH:" in result or "Lục Hào" in result
    has_conclusion = "KHẲNG ĐỊNH" in result
    not_rejected = "NGOÀI PHẠM VI" not in result
    
    print(f"  ✅ Có phán quyết: {has_verdict}")
    print(f"  ✅ Có Thế/Ứng:    {has_the_ung}")
    print(f"  ✅ Có PP căn cứ:   {has_method}")
    print(f"  ✅ Có kết luận:    {has_conclusion}")
    print(f"  ✅ Không bị chặn:  {not_rejected}")
    
    # Show key sections
    lines = result.split('\n')
    for l in lines:
        if any(kw in l for kw in ['PHÁN QUYẾT', 'KHẲNG ĐỊNH', 'Thế=', 'Ứng=', 'LH:', 'KM:', 'MH:', 'CĂN CỨ', 'PHƯƠNG PHÁP', 'LỜI KHUYÊN', '⚔️']):
            print(f"    📋 {l.strip()[:100]}")

print(f"\n{'='*70}")
print(f"🎉 TEST COMPLETE")
print(f"{'='*70}")
