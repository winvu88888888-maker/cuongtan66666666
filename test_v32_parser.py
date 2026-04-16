"""
V32 Parser Bug Reproduction — Phát hiện tất cả edge case
"""
import sys
sys.path.insert(0, r'C:\Users\GHC\.gemini\antigravity\scratch\cuongtan66666666_fix')
from interaction_diagrams import split_compound_question, clean_question, _detect_question_type

# ═══════════════════════════════════════════
# BUG 1: "đi" bị xóa khỏi clean_question vì nằm trong _NOISE_WORDS
# ═══════════════════════════════════════════
print("=" * 60)
print("BUG 1: Noise word 'đi' xóa nhầm")
bug1_tests = [
    ("nên đi bệnh viện nào?", "nên đi bệnh viện nào"),
    ("có nên đi du lịch không?", "có nên đi du lịch không"),
    ("đi hướng nào tốt?", "đi hướng nào tốt"),
    ("nên đi Đà Nẵng hay Nha Trang?", "nên đi Đà Nẵng hay Nha Trang"),
    ("con tôi đi học có đỗ không?", "con tôi đi học có đỗ không"),
]
for raw, expected in bug1_tests:
    cleaned = clean_question(raw)
    status = "✅" if expected.lower() in cleaned.lower() else "❌ BUG"
    print(f"  {status} | {raw!r} -> {cleaned!r} (expected: {expected!r})")

# ═══════════════════════════════════════════
# BUG 2: "ai " (có space) false positive trên "con trai", "ngoại"
# ═══════════════════════════════════════════
print("\n" + "=" * 60)
print("BUG 2: 'ai ' false positive")
bug2_tests = [
    ("con trai tôi thi đỗ không", "CÓ/KHÔNG"),  # Should NOT match "ai" but fails
    ("vợ tôi có ngoại tình không", None),          # "ngoại" should NOT match "ai"
    ("ai lấy tiền tôi", "AI"),                     # đúng, phải match "ai"
    ("người nào lấy tiền tôi", "AI"),              # đúng
]
for text, expected_type in bug2_tests:
    qtype, d_id, label = _detect_question_type(text)
    if expected_type:
        status = "✅" if qtype == expected_type else f"❌ BUG (got {qtype})"
    else:
        status = f"INFO: {qtype}"
    print(f"  {status} | {text!r} -> {qtype} ({d_id})")

# ═══════════════════════════════════════════
# BUG 3: Tách quá aggressive bằng "," — xẻ nhầm
# ═══════════════════════════════════════════
print("\n" + "=" * 60)
print("BUG 3: Comma splitting edge cases")
bug3_tests = [
    ("mất điện thoại ở đâu, có tìm được không?", 2),
    ("bệnh nặng, có nguy hiểm không?", 1),  # context-related → should be 1 question
    ("tài chính, sức khỏe, tình cảm năm nay?", 3),  # parallel topics → should be 3
    ("bố ơi, con thi có đỗ không?", 1),  # "bố ơi" is address, not a question
]
for text, expected_count in bug3_tests:
    pqs = split_compound_question(text)
    actual = len(pqs)
    status = "✅" if actual == expected_count else f"❌ BUG (got {actual})"
    print(f"  {status} | {text!r} -> {actual} câu (expected {expected_count})")
    for pq in pqs:
        print(f"      [{pq['index']}] {pq['text']!r} | {pq['qtype']} | {pq['diagram_id']}")

# ═══════════════════════════════════════════
# BUG 4: Noise "thôi" xóa nhầm trong "thôi nôi"
# ═══════════════════════════════════════════
print("\n" + "=" * 60)
print("BUG 4: Other dangerous noise words")
bug4_tests = [
    ("thôi nôi cho bé khi nào tốt", "thôi nôi"),
    ("với tốc độ này bao giờ xong", "với tốc"),
    ("kìa có thấy con chim không", "kìa"),
    ("chút nữa trời mưa không", "chút nữa"),
]
for text, must_contain in bug4_tests:
    cleaned = clean_question(text)
    status = "✅" if must_contain.lower() in cleaned.lower() else f"❌ BUG ({cleaned!r})"
    print(f"  {status} | {text!r} -> {cleaned!r}")

# ═══════════════════════════════════════════
# EDGE: Câu hỏi dài nhiều ý + noise
# ═══════════════════════════════════════════
print("\n" + "=" * 60)
print("EDGE: Câu hỏi dài + noise")
long_q = "haha cho em hỏi nha, bố em bị bệnh nặng hay không???... và khi nào khỏi ạ, nên đi bệnh viện nào tốt nhất, và chi phí bao nhiêu cảm ơn!"
pqs = split_compound_question(long_q)
print(f"  INPUT: {long_q}")
print(f"  CLEANED: {clean_question(long_q)}")
print(f"  TÁCH: {len(pqs)} câu")
for pq in pqs:
    p = pq.get('person') or '-'
    print(f"    [{pq['index']}] {pq['text']!r}")
    print(f"        Person={p} | DT={pq['dung_than']} | Type={pq['qtype']} | Diagram={pq['diagram_id']}")
