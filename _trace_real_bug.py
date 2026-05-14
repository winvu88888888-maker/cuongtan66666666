# -*- coding: utf-8 -*-
"""Trace REAL bug: DT = Bản Thân cho câu hỏi có dấu 'đầu tư kinh doanh'"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

# Test the actual engine
from free_ai_helper import FreeAIHelper, _get_dung_than, _get_all_dung_than

# Test 1: _get_dung_than standalone
tests = [
    "Năm nay có nên đầu tư kinh doanh không",
    "Tôi có nên mua nhà không",
    "Mẹ tôi bệnh có khỏi không",
    "Bao giờ tôi có người yêu",
    "Năm nay làm ăn có phát tài không",
]

print("=" * 80)
print("🔍 TEST 1: _get_dung_than (STANDALONE)")
print("=" * 80)
for q in tests:
    dt = _get_dung_than(q)
    print(f"  Q: {q}")
    print(f"  → DT: {dt}")
    print()

# Test 2: Full pipeline with FreeAIHelper.answer_question
# We need to see what answer_question actually produces
print("=" * 80)
print("🔍 TEST 2: FULL PIPELINE via answer_question")
print("=" * 80)

helper = FreeAIHelper()

# Fake chart data
fake_chart = {
    'can_ngay': 'Giáp', 'chi_ngay': 'Dần',
    'can_gio': 'Bính', 'chi_gio': 'Ngọ',
    'can_thang': 'Canh', 'chi_thang': 'Thìn',
    'can_nam': 'Mậu', 'chi_nam': 'Tuất',
    'can_thien_ban': {},
    'thien_ban': {}, 'nhan_ban': {}, 'than_ban': {},
    'hanh_dt': '',
}

q = "Năm nay có nên đầu tư kinh doanh không"
print(f"\n📋 Q: {q}")

# Call answer_question and trace output
result = helper.answer_question(q, fake_chart)

# The result contains _off_answer, _off_summary_extra, etc.
# Check result dict keys
if isinstance(result, dict):
    print(f"\nResult keys: {list(result.keys())[:20]}")
    print(f"  dung_than: {result.get('dung_than', '?')}")
    print(f"  detected_category: {result.get('detected_category', '?')}")
    print(f"  weighted_pct: {result.get('weighted_pct', '?')}")
    print(f"  _off_answer: {str(result.get('_off_answer', '?'))[:200]}")
    print(f"  ky_mon_verdict: {result.get('ky_mon_verdict', '?')}")
    print(f"  luc_hao_verdict: {result.get('luc_hao_verdict', '?')}")
    print(f"  mai_hoa_verdict: {result.get('mai_hoa_verdict', '?')}")
elif isinstance(result, tuple):
    print(f"Result is tuple with {len(result)} elements")
    # Try to find the text
    for i, r in enumerate(result):
        if isinstance(r, str) and len(r) > 10:
            # Look for DT: mentions
            if 'DT:' in r or 'Dụng Thần' in r:
                # Find the DT line
                for line in r.split('\n'):
                    if 'DT:' in line or 'Dụng Thần' in line or 'dung_than' in line:
                        print(f"  [{i}] {line.strip()[:150]}")
            if 'Bản Thân' in r:
                # Find context
                idx = r.find('Bản Thân')
                start = max(0, idx-50)
                end = min(len(r), idx+50)
                print(f"  [{i}] ...{r[start:end]}...")
    # Usually it's (analysis_text, html_card, dict_data)
    if len(result) >= 3 and isinstance(result[2], dict):
        d = result[2]
        print(f"\n  Dict result:")
        print(f"    dung_than: {d.get('dung_than', '?')}")
        print(f"    detected_category: {d.get('detected_category', '?')}")
        print(f"    weighted_pct: {d.get('weighted_pct', '?')}")
else:
    print(f"Result type: {type(result)}")
    print(f"Result: {str(result)[:500]}")
