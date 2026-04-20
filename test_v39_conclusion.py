# -*- coding: utf-8 -*-
"""Test V39.0: Verify KẾT LUẬN KHẲNG ĐỊNH + VÌ SAO + GIẢI PHÁP"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

from free_ai_helper import FreeAIHelper

ai = FreeAIHelper()

test_cases = [
    "Mua nha nam nay tot khong?",
    "Co nen dau tu crypto?",
    "Cong viec the nao?",
]

REQUIRED_SECTIONS = ['PHÁN QUYẾT', 'VÌ SAO', 'KHẲNG ĐỊNH', 'GIẢI PHÁP', 'LỜI KHUYÊN']

for q in test_cases:
    print(f"\n{'='*60}")
    print(f"Q: {q}")
    print(f"{'='*60}")
    result = ai.answer_question(q)
    
    # Check required sections
    missing = []
    for section in REQUIRED_SECTIONS:
        if section not in result:
            missing.append(section)
    
    if missing:
        print(f"  ❌ MISSING: {', '.join(missing)}")
    else:
        print(f"  ✅ ALL SECTIONS PRESENT")
    
    # Extract conclusion lines
    for line in result.split('\n'):
        if any(kw in line for kw in REQUIRED_SECTIONS):
            print(f"  >> {line.strip()[:120]}")

print(f"\n{'='*60}")
print("TEST COMPLETE")
