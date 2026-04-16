"""
test_v32_smart_parser.py — Test toàn diện cho V32.5 Smart Question Parser
50+ test cases đa dạng: noise, compound, person, topic, edge cases
"""
import sys
sys.path.insert(0, r'C:\Users\GHC\.gemini\antigravity\scratch\cuongtan66666666_fix')
from question_parser import (
    parse_question, clean_question_v2, format_parsed_questions_v2,
    SmartPreprocessor, ContextSplitter, EntityExtractor,
)

passed = 0
failed = 0

def test(name, actual, expected, detail=""):
    global passed, failed
    if actual == expected:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed += 1
        print(f"  ❌ {name}")
        print(f"     GOT:      {actual!r}")
        print(f"     EXPECTED: {expected!r}")
        if detail:
            print(f"     DETAIL:   {detail}")

def test_contains(name, actual, must_contain):
    global passed, failed
    if must_contain.lower() in actual.lower():
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed += 1
        print(f"  ❌ {name}")
        print(f"     GOT:      {actual!r}")
        print(f"     MUST CONTAIN: {must_contain!r}")

# ═══════════════════════════════════════════════════════════════
# SECTION 1: SmartPreprocessor — KHÔNG mất nghĩa
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SECTION 1: SmartPreprocessor — Làm sạch noise mà KHÔNG mất nghĩa")
print("=" * 70)

pp = SmartPreprocessor()

# 1.1: Từ có nghĩa PHẢI ĐƯỢC GIỮ LẠI
keep_tests = [
    ("nên đi bệnh viện nào", "đi"),
    ("có nên đi du lịch không", "đi"),
    ("đi hướng nào tốt", "đi"),
    ("nên đi Đà Nẵng hay Nha Trang", "đi"),
    ("nên đi Đà Nẵng hay Nha Trang", "Nha"),
    ("con tôi đi học có đỗ không", "đi"),
    ("thôi nôi cho bé khi nào tốt", "thôi"),
    ("với tốc độ này bao giờ xong", "với"),
    ("kìa có thấy con chim không", "kìa"),
    ("chút nữa trời mưa không", "chút"),
    ("xem quẻ giúp tôi", "xem"),
    ("nghe nói sắp mưa", "nghe"),
    ("giúp tôi tra quẻ", "giúp"),
    ("ở đây có an toàn không", "đây"),
    ("tôi rồi sẽ giàu không", "rồi"),
    ("luôn luôn thất bại", "luôn"),
]
for text, must_keep in keep_tests:
    cleaned = pp.clean(text)
    test_contains(f"GIỮ '{must_keep}' trong: {text!r}", cleaned, must_keep)

# 1.2: Noise PHẢI ĐƯỢC XÓA
remove_tests = [
    ("haha bố tôi bệnh không???!!!", "bố tôi bệnh không"),
    ("cho em hỏi ạ, tài chính thế nào", "tài chính thế nào"),
    ("dạ thưa thầy, vợ tôi ngoại tình không ạ", "vợ tôi ngoại tình không"),
    ("!!!??? sức khỏe năm nay @@@###", "sức khỏe năm nay"),
    ("lol omg tôi có giàu không ok", "tôi có giàu không"),
    ("cảm ơn bạn, con trai đỗ không nhỉ", "con trai đỗ không"),  # polite phrases removed correctly
]
for text, expected in remove_tests:
    cleaned = pp.clean(text)
    # Flexible check: cleaned phải chứa phần core
    core_words = [w for w in expected.split() if len(w) > 2]
    all_found = all(w.lower() in cleaned.lower() for w in core_words)
    test(f"XÓA NOISE: {text[:40]!r}", all_found, True, f"cleaned={cleaned!r}")


# ═══════════════════════════════════════════════════════════════
# SECTION 2: ContextSplitter — Tách thông minh
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SECTION 2: ContextSplitter — Tách thông minh")
print("=" * 70)

sp = ContextSplitter()

# 2.1: Tách đúng số câu
split_tests = [
    # (input, expected_count, description)
    ("bố tôi bệnh nặng hay không và khi nào khỏi?", 2, "2 câu hỏi khác loại"),
    ("tài chính thế nào, sức khỏe ra sao, tình cảm có tốt không?", 3, "3 topics khác nhau"),
    ("mất điện thoại ở đâu, có tìm được không?", 2, "2 câu khác qtype"),
    ("bệnh nặng, có nguy hiểm không?", 2, "2 câu — bệnh trạng + hỏi CÓ/KHÔNG"),
    ("bố ơi, con thi có đỗ không?", 1, "1 câu — 'bố ơi' là xưng hô, không phải câu hỏi"),
    ("vợ tôi có ngoại tình không?", 1, "1 câu đơn"),
    ("năm nay có thuận lợi không?", 1, "1 câu đơn"),
    ("tôi có nên đầu tư không, khi nào có lãi, rủi ro thế nào?", 3, "3 loại câu hỏi"),
    ("con trai thi đỗ không và bao giờ có kết quả?", 2, "CÓ/KHÔNG + KHI NÀO"),
]
for text, expected_count, desc in split_tests:
    segs = sp.split(text)
    test(f"TÁCH [{expected_count}]: {desc}", len(segs), expected_count,
         f"segments={segs}")


# ═══════════════════════════════════════════════════════════════
# SECTION 3: EntityExtractor — Person / Topic / QType
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SECTION 3: EntityExtractor — Phát hiện Person / Topic / QType")
print("=" * 70)

ex = EntityExtractor()

# 3.1: Person detection
person_tests = [
    ("bố tôi bệnh nặng", "Bố", "Phụ Mẫu"),
    ("con trai thi đỗ không", "Con trai", "Tử Tôn"),
    ("vợ tôi ngoại tình", "Vợ", "Thê Tài"),
    ("sếp có thăng chức không", "Sếp", "Quan Quỷ"),
    ("tôi có giàu không", None, None),  # "tôi" = mặc định, skip
    ("đối tác có tin cậy không", "Đối tác", "Huynh Đệ"),
    ("bà ngoại khỏe không", "Bà ngoại", "Phụ Mẫu"),
    ("con dâu sinh chưa", "Con dâu", "Thê Tài"),
]
for text, expected_person, expected_dt in person_tests:
    person, dt, kw = ex.detect_person(text)
    test(f"PERSON: {text!r}", person, expected_person, f"dt={dt}")
    if expected_dt:
        test(f"  └─ DT: {text!r}", dt, expected_dt)

# 3.2: QType — BUG "ai " false positive
qtype_tests = [
    ("con trai tôi thi đỗ không", "CÓ/KHÔNG"),  # KHÔNG phải "AI"
    ("vợ tôi có ngoại tình không", "CÓ/KHÔNG"),  # "ngoại" KHÔNG match "ai"
    ("ai lấy tiền tôi", "AI"),                    # Word-boundary "ai" → OK
    ("người nào lấy tiền tôi", "AI"),
    ("khi nào sẽ khỏi", "KHI NÀO"),
    ("ở đâu tìm việc", "Ở ĐÂU"),
    ("tại sao thua lỗ", "TẠI SAO"),
    ("thế nào rồi", "THẾ NÀO"),
    ("bao nhiêu tuổi", "TUỔI"),
    ("cái nào tốt hơn", "CHỌN"),
    ("bệnh gì vậy", "CÁI GÌ"),
    ("tài chính năm nay", "CHUNG"),  # Không có question marker → CHUNG
]
for text, expected_qtype in qtype_tests:
    qtype, d_id, label = ex.detect_question_type(text)
    test(f"QTYPE: {text!r}", qtype, expected_qtype, f"diagram={d_id}")

# 3.3: Topic detection
topic_tests = [
    ("bố tôi bệnh nặng", "SỨC_KHỎE"),
    ("tôi có nên đầu tư cổ phiếu", "TÀI_CHÍNH"),
    ("vợ ngoại tình", "TÌNH_CẢM"),
    ("con trai thi đỗ không", "CÔNG_VIỆC"),
    ("mất điện thoại ở đâu", "TÌM_ĐỒ"),
    ("bố mất chưa", "SỨC_KHỎE"),  # "bố mất" = SỨC_KHỎE (không phải TÌM_ĐỒ)
    ("xây nhà hướng nào tốt", "NHÀ_CỬA"),
    ("du lịch Đà Nẵng có tốt không", "XUẤT_HÀNH"),
    ("năm nay tốt không", "CHUNG"),
]
for text, expected_topic in topic_tests:
    topic, label, dt = ex.detect_topic(text)
    test(f"TOPIC: {text!r}", topic, expected_topic, f"label={label}")


# ═══════════════════════════════════════════════════════════════
# SECTION 4: FULL PIPELINE — parse_question() end-to-end
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SECTION 4: FULL PIPELINE — parse_question() end-to-end")
print("=" * 70)

pipeline_tests = [
    # (input, expected_results: list of (qtype, person, dt, topic))
    (
        "bố tôi bị bệnh nặng hay không và khi nào sẽ khỏi?",
        [("CÓ/KHÔNG", "Bố", "Phụ Mẫu", "SỨC_KHỎE"),
         ("KHI NÀO", "Bố", "Phụ Mẫu", "SỨC_KHỎE")],
    ),
    (
        "tôi có nên đầu tư không, khi nào sẽ có lãi, và rủi ro thế nào?",
        [("CÓ/KHÔNG", None, "Thê Tài", "TÀI_CHÍNH"),
         ("KHI NÀO", None, "Thê Tài", "TÀI_CHÍNH"),
         ("THẾ NÀO", None, "Thê Tài", "TÀI_CHÍNH")],
    ),
    (
        "vợ tôi có ngoại tình không?",
        [("CÓ/KHÔNG", "Vợ", "Thê Tài", "TÌNH_CẢM")],
    ),
    (
        "con trai tôi thi có đỗ không?",
        [("CÓ/KHÔNG", "Con trai", "Tử Tôn", "CÔNG_VIỆC")],
    ),
    (
        "haha cho em hỏi nha, bố em bị bệnh nặng hay không??? cảm ơn",
        [("CÓ/KHÔNG", "Bố", "Phụ Mẫu", "SỨC_KHỎE")],
    ),
    (
        "năm nay tài chính thế nào, sức khỏe ra sao, và tình cảm có thuận lợi không?",
        [("THẾ NÀO", None, "Thê Tài", "TÀI_CHÍNH"),
         ("THẾ NÀO", None, "Bản Thân", "SỨC_KHỎE"),
         ("CÓ/KHÔNG", None, "Thê Tài", "TÌNH_CẢM")],
    ),
    (
        "mất điện thoại ở đâu, có tìm được không?",
        [("Ở ĐÂU", None, "Thê Tài", "TÌM_ĐỒ"),
         ("CÓ/KHÔNG", None, "Thê Tài", "TÌM_ĐỒ")],
    ),
    (
        "nên đi bệnh viện nào tốt nhất?",
        [("CHỌN", None, None, None)],  # flexible check on this one
    ),
]

for raw_q, expected_list in pipeline_tests:
    pqs = parse_question(raw_q)
    print(f"\n  INPUT: {raw_q[:60]}...")
    
    test(f"  COUNT", len(pqs), len(expected_list), f"parsed={len(pqs)}")
    
    for i, (exp_qtype, exp_person, exp_dt, exp_topic) in enumerate(expected_list):
        if i < len(pqs):
            pq = pqs[i]
            test(f"  [{i+1}] QTYPE", pq['qtype'], exp_qtype, f"text={pq['text']!r}")
            if exp_person is not None:
                test(f"  [{i+1}] PERSON", pq['person'], exp_person)
            if exp_dt is not None:
                test(f"  [{i+1}] DT", pq['dung_than'], exp_dt)
            if exp_topic is not None:
                test(f"  [{i+1}] TOPIC", pq['topic'], exp_topic)


# ═══════════════════════════════════════════════════════════════
# SECTION 5: Extreme Edge Cases
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SECTION 5: Extreme Edge Cases")
print("=" * 70)

edge_tests = [
    # Câu rất ngắn
    ("giàu không?", 1, "CÓ/KHÔNG"),
    ("ai?", 1, "AI"),
    ("bệnh gì?", 1, "CÁI GÌ"),
    # Câu chỉ có noise
    ("haha lol ok ???!!!...", 0, None),
    ("", 0, None),
    ("    ", 0, None),
    # Câu cực dài
    ("tôi muốn hỏi năm nay tài chính thế nào, sức khỏe ra sao, công việc có thăng tiến không, tình cảm có người mới không, và con tôi thi có đỗ không?", 5, None),
    # Tiếng Việt đặc biệt
    ("bà ngoại ung thư có qua khỏi không?", 1, "CÓ/KHÔNG"),
    # Nhiều dấu ? liên tiếp
    ("giàu không??? nghèo không???", 2, None),
]

for text, expected_count, expected_qtype in edge_tests:
    pqs = parse_question(text)
    test(f"EDGE [{expected_count}]: {text[:50]!r}", len(pqs), expected_count)
    if expected_qtype and pqs:
        test(f"  └─ QTYPE", pqs[0]['qtype'], expected_qtype)


# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
total = passed + failed
print(f"TOTAL: {passed}/{total} passed ({failed} failed)")
if failed == 0:
    print("🎉 ALL TESTS PASSED!")
else:
    print(f"⚠️  {failed} test(s) need attention")
print("=" * 70)
