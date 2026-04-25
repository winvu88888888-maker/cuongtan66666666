# -*- coding: utf-8 -*-
"""Test các trường hợp đơn lẻ + multi-intent"""
import sys
sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper
import re

helper = FreeAIHelper()

tests = [
    ("Multi-intent (3 vế)", "nhà tôi có mấy anh chị em , các anh chị em tôi đang làm nghề gì , bao nhiêu tuổi",
     ["🔮", "🎂", "👥"]),
    ("Đơn: nghề gì", "tôi nên làm nghề gì", ["🔮"]),
    ("Đơn: tuổi", "người đó bao nhiêu tuổi", ["🎂"]),
    ("Đơn: bao nhiêu", "nhà tôi có mấy anh em", ["👥"]),
    ("Đơn: có/không", "tôi có được thăng chức không", ["✅", "🟡", "🔴"]),
]

for label, q, expected_icons in tests:
    print(f"\n{'='*60}")
    print(f"TEST: {label}")
    print(f"  Q: {q}")
    result = helper.answer_question(q, chart_data=None, topic=None)
    if not result:
        print("  ❌ FAIL: No result")
        continue
    
    # Extract green box content
    green_match = re.search(
        r'font-size:2em[^>]*>(.*?)</div>',
        result, re.DOTALL
    )
    if green_match:
        raw = green_match.group(1)
        clean = re.sub(r'<[^>]+>', ' ', raw).strip()
        # Condense whitespace
        clean = re.sub(r'\s+', ' ', clean)
        print(f"  GREEN BOX: {clean[:200]}")
        
        # Check icons
        found_any = False
        for icon in expected_icons:
            if icon in clean:
                found_any = True
                break
        if found_any:
            print(f"  ✅ PASS: Found expected icon(s)")
        else:
            print(f"  ❌ FAIL: Expected one of {expected_icons}")
    else:
        print(f"  ⚠️ Could not extract green box")

    # Check for CÂU TRẢ LỜI in green box
    if green_match and "CÂU TRẢ LỜI:" in green_match.group(1):
        print(f"  ❌ WARNING: 'CÂU TRẢ LỜI:' in green box!")

print(f"\n{'='*60}")
print("ALL TESTS COMPLETE")
