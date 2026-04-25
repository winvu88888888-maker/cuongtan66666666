# -*- coding: utf-8 -*-
"""Test competition detection + full answer flow"""
import sys, os
sys.path.insert(0, '.')

from free_ai_helper import _is_competition_question, _extract_two_sides, clean_question

# Test 1: Detection
print("=" * 70)
print("TEST 1: Competition question detection")
print("=" * 70)
tests = [
    'MU vs Liverpool ai thang?',
    'MU vs Liverpool ai thắng?',
    'đội MU hay Liverpool thắng thua',
    'MU đấu với Liverpool ai thắng',
    'Trận MU gặp Liverpool thắng thua thế nào',
    'mu vs liverpool',
    'MU hay Liverpool thắng',
    'MU thắng hay Liverpool thắng',
    'Chelsea vs Arsenal ai thắng',
]

for q in tests:
    cleaned = clean_question(q)
    is_comp = _is_competition_question(q)
    sides = _extract_two_sides(q) if is_comp else None
    tag = "✅ YES" if is_comp else "❌ NO "
    print(f"  {tag} | Q: {q}")
    if sides:
        print(f"         sides: A='{sides[0]}', B='{sides[1]}'")

# Test 2: Full answer flow
print()
print("=" * 70)
print("TEST 2: Full answer_question flow with competition")
print("=" * 70)

from free_ai_helper import FreeAIHelper

helper = FreeAIHelper()
q = "MU vs Liverpool ai thắng?"
try:
    result = helper.answer_question(q, chart_data=None, topic=None)
    # Check if result contains competition indicators
    if result:
        has_side_a = 'MU' in result
        has_side_b = 'Liverpool' in result
        has_verdict = 'PHÁN QUYẾT' in result or 'KHẲNG ĐỊNH' in result
        has_the_ung = 'Thế' in result and 'Ứng' in result
        has_thang = 'THẮNG' in result

        print(f"  Result length: {len(result)} chars")
        print(f"  Contains 'MU': {has_side_a}")
        print(f"  Contains 'Liverpool': {has_side_b}")
        print(f"  Contains 'PHÁN QUYẾT/KHẲNG ĐỊNH': {has_verdict}")
        print(f"  Contains 'Thế/Ứng': {has_the_ung}")
        print(f"  Contains 'THẮNG': {has_thang}")
        
        # Show first 500 chars
        print()
        print("  === FIRST 500 CHARS ===")
        print(result[:500])
        print()
        
        # Show last 800 chars (conclusion)
        print("  === LAST 800 CHARS (CONCLUSION) ===")
        print(result[-800:])
    else:
        print("  ❌ Result is empty!")
except Exception as e:
    import traceback
    print(f"  ❌ ERROR: {e}")
    traceback.print_exc()
