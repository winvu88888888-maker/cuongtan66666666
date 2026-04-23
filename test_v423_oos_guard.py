"""
V42.3 OUT-OF-SCOPE GUARD — Test Suite
Kiểm tra logic từ chối câu hỏi thể thao/cá cược/ngoài phạm vi
"""
import sys
sys.path.insert(0, '.')

from free_ai_helper import FreeAIHelper

helper = FreeAIHelper()

# ═══════════════════════════════════════════
# TEST 1: CÂU HỎI PHẢI BỊ TỪ CHỐI (expect "NGOÀI PHẠM VI")
# ═══════════════════════════════════════════
REJECT_QUESTIONS = [
    # --- Thể thao trực tiếp ---
    "Đội bóng A và đội bóng B đội nào thắng và tỷ số bao nhiêu?",
    "Manchester United vs Liverpool ai thắng?",
    "Trận chung kết World Cup đội nào vô địch?",
    "Kết quả trận đấu tối nay?",
    "Dự đoán tỷ số trận Real Madrid gặp Barca?",
    "Soi kèo trận đêm nay",
    "Kèo nhà cái cho trận Chelsea đấu Arsenal",
    "Champions League mùa này đội nào vô địch?",
    "Ngoại hạng Anh ai xuống hạng?",
    "Bóng đá hôm nay đội nào thắng?",
    "Trận bán kết kết quả bao nhiêu?",
    "Messi ghi bàn không?",
    # --- Không dấu ---
    "doi nao thang tran dem nay?",
    "ty so bao nhieu?",
    "soi keo tran chung ket",
    "ca do bong da co nen khong?",
    # --- Cá cược ---
    "Cá độ bóng đá có nên không?",
    "Đặt kèo trận tối nay",
    "Tài xỉu bóng đá hôm nay",
    # --- Giá cổ phiếu cụ thể ---
    "Giá bitcoin ngày mai bao nhiêu?",
    "Coin nào tăng mạnh nhất?",
    "Cổ phiếu nào tăng ngày mai?",
    # --- V-League ---
    "V-League đội nào vô địch năm nay?",
    # --- Combo: sport + predict ---
    "Giải đấu tennis ai thắng?",
    "Trận đấu boxing kết quả thế nào?",
]

# ═══════════════════════════════════════════
# TEST 2: CÂU HỎI PHẢI ĐƯỢC XỬ LÝ BÌNH THƯỜNG (expect KHÔNG bị từ chối)
# ═══════════════════════════════════════════
ALLOW_QUESTIONS = [
    # --- Huyền học hợp lệ ---
    "Tôi có nên đầu tư kinh doanh lúc này không?",
    "Sức khỏe bố tôi có qua khỏi không?",
    "Tình cảm của tôi với người yêu thế nào?",
    "Tôi mất điện thoại, tìm ở đâu?",
    "Tài chính năm nay thế nào?",
    "Tôi có nên đi du lịch tuần này không?",
    "Con trai tôi thi đậu không?",
    "Vợ chồng tôi có nên ly hôn?",
    "Năm nay vận mệnh tôi thế nào?",
    # --- Câu hỏi tài chính TỔNG QUÁT (KHÔNG cụ thể giá) → hợp lệ ---
    "Tôi có nên đầu tư crypto không?",
    "Mua vàng lúc này có lợi không?",
    "Kinh doanh buôn bán có thuận lợi không?",
    # --- Từ "thắng" nhưng KHÔNG phải thể thao ---
    "Tôi có thắng kiện không?",
    "Kiện tụng có thắng được không?",
    # --- Từ "đội" nhưng KHÔNG phải thể thao ---
    "Đội ngũ công ty tôi có ổn không?",
]

print("=" * 70)
print("🧪 V42.3 OUT-OF-SCOPE GUARD — TEST SUITE")
print("=" * 70)

# ── RUN REJECT TESTS ──
print(f"\n{'='*70}")
print(f"📛 TEST NHÓM 1: CÂU HỎI PHẢI BỊ TỪ CHỐI ({len(REJECT_QUESTIONS)} câu)")
print(f"{'='*70}")

reject_pass = 0
reject_fail = 0
for i, q in enumerate(REJECT_QUESTIONS, 1):
    result = helper.answer_question(q)
    is_rejected = "NGOÀI PHẠM VI" in result or "KHÔNG THỂ TRẢ LỜI" in result
    status = "✅ REJECTED" if is_rejected else "❌ NOT REJECTED"
    if is_rejected:
        reject_pass += 1
    else:
        reject_fail += 1
    print(f"  {i:2d}. {status} | {q[:60]}")
    if not is_rejected:
        print(f"      → GOT: {result[:100]}...")

# ── RUN ALLOW TESTS ──
print(f"\n{'='*70}")
print(f"✅ TEST NHÓM 2: CÂU HỎI PHẢI ĐƯỢC XỬ LÝ ({len(ALLOW_QUESTIONS)} câu)")
print(f"{'='*70}")

allow_pass = 0
allow_fail = 0
for i, q in enumerate(ALLOW_QUESTIONS, 1):
    result = helper.answer_question(q)
    is_rejected = "NGOÀI PHẠM VI" in result or "KHÔNG THỂ TRẢ LỜI" in result
    status = "✅ ALLOWED" if not is_rejected else "❌ FALSE REJECT"
    if not is_rejected:
        allow_pass += 1
    else:
        allow_fail += 1
    print(f"  {i:2d}. {status} | {q[:60]}")
    if is_rejected:
        print(f"      → FALSE POSITIVE! Bị từ chối nhầm!")

# ── SUMMARY ──
print(f"\n{'='*70}")
print(f"📊 KẾT QUẢ TỔNG HỢP")
print(f"{'='*70}")
total = len(REJECT_QUESTIONS) + len(ALLOW_QUESTIONS)
total_pass = reject_pass + allow_pass
print(f"  Từ chối đúng:      {reject_pass}/{len(REJECT_QUESTIONS)}")
print(f"  Cho phép đúng:     {allow_pass}/{len(ALLOW_QUESTIONS)}")
print(f"  TỔNG:              {total_pass}/{total} ({total_pass/total*100:.1f}%)")
print(f"  False Negative:    {reject_fail} (không từ chối khi nên)")  
print(f"  False Positive:    {allow_fail} (từ chối nhầm)")
print(f"\n{'='*70}")
if total_pass == total:
    print("🎉 PERFECT SCORE — V42.3 OOS Guard HOẠT ĐỘNG HOÀN HẢO!")
else:
    print(f"⚠️ CẦN FIX: {total - total_pass} test cases FAILED")
print(f"{'='*70}")
