# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Test the actual DT override logic
q_ascii = 'toi co nen dau tu kinh doanh nam nay khong'
q_vn = 'tôi có nên đầu tư kinh doanh năm nay không'

kws_ascii = ['anh chi em', 'anh em', 'may anh', 'may chi', 'bao nhieu anh']
kws_vn = ['anh chị em', 'anh em', 'mấy anh', 'mấy chị', 'bao nhiêu anh']

print("=== ASCII question ===")
for kw in kws_ascii:
    if kw in q_ascii:
        print(f"  ⚠️ MATCH: '{kw}' in '{q_ascii}'")

print("\n=== Vietnamese question ===")
for kw in kws_vn:
    if kw in q_vn:
        print(f"  ⚠️ MATCH: '{kw}' in '{q_vn}'")

# Now check WHAT HAPPENED on the live app
# The app receives question from user's textarea
# "toi co nen dau tu kinh doanh nam nay khong"
# → q_lower = "toi co nen dau tu kinh doanh nam nay khong"
# Check: 'anh' in q_lower
print("\n=== Check substring 'anh' ===")
print(f"  'anh' in ASCII q: {'anh' in q_ascii}")  # kinh do'anh' 
print(f"  'anh' in VN q: {'anh' in q_vn}")  # doanh contains anh

# CRITICAL: Check what keywords in the code are ACTUALLY matching
# The code at line 12493 says:
# if any(kw in q_lower for kw in ['anh chị em', 'anh em', 'mấy anh', 'mấy chị', 'bao nhiêu anh']):
# But wait - 'mấy anh' won't match ASCII 'may anh'
# And 'anh em' won't match ASCII either
# BUT the screenshot shows DT = Huynh Đệ... so something else is matching

# Let's check the CATEGORY detection
print("\n=== Category detection ===")
from free_ai_helper import FreeAIHelper
h = FreeAIHelper()
# Check what category "toi co nen dau tu kinh doanh nam nay khong" falls into
# The answer is in CATEGORIES dict
import re
code = open('free_ai_helper.py', 'r', encoding='utf-8').read()
cat_start = code.find("CATEGORIES = {")
cat_end = code.find("\n}", cat_start) + 2
if cat_start > 0:
    # Find 'CHUNG' category dung_than
    idx = code.find("'CHUNG'", cat_start)
    if idx > 0:
        chunk = code[idx:idx+300]
        print(f"  CHUNG category chunk: {chunk[:200]}")
