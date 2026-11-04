# -*- coding: utf-8 -*-
"""Test tích hợp Grammar Analyzer vào pipeline chính."""
import sys
sys.path.insert(0, '.')
from question_parser import parse_question, format_parsed_questions_v2

# ═══ Test 1: Câu phức tạp — 3 câu hỏi, 1 người ═══
print("=" * 80)
print("TEST 1: 3 câu hỏi cùng 1 đối tượng")
print("=" * 80)
q1 = "người yêu của cháu gái chị tôi nó có tốt không giàu không nó có yêu thật lòng không"
results = parse_question(q1)
print(f"\nINPUT: {q1}")
print(f"TÁCH: {len(results)} câu\n")
for r in results:
    print(f"  [{r['index']}] '{r['text']}'")
    print(f"      Khảo sát: {r.get('inquiry_focus', '?')}")
    print(f"      DT: {r['dung_than']} | Mục đích: Hỏi {r.get('ask_purpose', '?')}")
    print(f"      Lý do: {r.get('dung_than_reason', '-')}")
    print(f"      Topic: {r['topic_label']} | QType: {r['qtype_label']}")
    print()
print(format_parsed_questions_v2(results))

# ═══ Test 2: 5 câu hỏi khác đối tượng ═══
print("\n" + "=" * 80)
print("TEST 2: 5 câu hỏi — 5 DT khác nhau")
print("=" * 80)
q2 = "bố tôi bệnh nặng không, vợ tôi có ngoại tình không, con trai thi đỗ không, tôi có giàu không, em tôi xin việc được không"
results2 = parse_question(q2)
print(f"\nINPUT: {q2[:60]}...")
print(f"TÁCH: {len(results2)} câu\n")
for r in results2:
    print(f"  [{r['index']}] '{r['text']}'")
    print(f"      Khảo sát: {r.get('inquiry_focus', '?')} | DT: {r['dung_than']} | Hỏi {r.get('ask_purpose', '?')}")
    print()
print(format_parsed_questions_v2(results2))

# ═══ Test 3: Câu phức — VẬT + NGƯỜI ═══
print("\n" + "=" * 80)
print("TEST 3: Hỏi về VẬT + NGƯỜI + BẢN THÂN")
print("=" * 80)
q3 = "xe của chị tôi bị mất ở đâu, bệnh của bố tôi nặng không, tôi có nên đầu tư cổ phiếu không"
results3 = parse_question(q3)
print(f"\nINPUT: {q3[:60]}...")
print(f"TÁCH: {len(results3)} câu\n")
for r in results3:
    g = r.get('grammar', {})
    s = g.get('subject', {}) if g else {}
    print(f"  [{r['index']}] '{r['text']}'")
    print(f"      Subject: {s.get('label', '?')} ({s.get('type', '?')})")
    if s.get('owner'):
        print(f"      └─ Thuộc: {s['owner']} ({s.get('owner_dt', '?')})")
    print(f"      DT: {r['dung_than']} | Hỏi {r.get('ask_purpose', '?')}")
    print()
print(format_parsed_questions_v2(results3))

# ═══ Test 4: Kiểm tra DT khác nhau cho mỗi câu ═══
print("\n" + "=" * 80)
print("TEST 4: Validate — mỗi câu có DT chính xác")
print("=" * 80)

checks = [
    # (input, expected_count, expected_dts)
    (
        "bố tôi bệnh nặng không, vợ tôi có ngoại tình không, con trai thi đỗ không",
        3,
        ['Phụ Mẫu', 'Thê Tài', 'Tử Tôn'],
    ),
    (
        "tôi có giàu không, sếp tôi thăng chức không, em tôi xin việc được không",
        3,
        ['Thê Tài', 'Quan Quỷ', 'Huynh Đệ'],
    ),
    (
        "xe của chị tôi mất ở đâu, bệnh của bố tôi nặng không",
        2,
        ['Thê Tài', 'Quan Quỷ'],
    ),
]

all_pass = True
for q_input, exp_count, exp_dts in checks:
    results = parse_question(q_input)
    count_ok = len(results) == exp_count
    dts_ok = [r['dung_than'] for r in results] == exp_dts
    
    if count_ok and dts_ok:
        print(f"  ✅ {q_input[:50]}...")
        print(f"     DT: {[r['dung_than'] for r in results]}")
    else:
        all_pass = False
        print(f"  ❌ {q_input[:50]}...")
        print(f"     GOT:      count={len(results)}, DT={[r['dung_than'] for r in results]}")
        print(f"     EXPECTED: count={exp_count}, DT={exp_dts}")
    print()

print("=" * 80)
if all_pass:
    print("🎉 ALL INTEGRATION TESTS PASSED!")
print("=" * 80)
