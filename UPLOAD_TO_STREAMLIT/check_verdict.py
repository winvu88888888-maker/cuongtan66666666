# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper
h = FreeAIHelper()
r = h.answer_question('u17 viet nam va u17 malaysia doi nao thang', chart_data=None, topic=None)

# Find competition verdict lines
lines = r.split('\n')
for i, line in enumerate(lines):
    s = line.strip()
    if any(k in s for k in ['THẮNG', 'THUA', 'PHÁN', 'KHẲNG']):
        print(f'[{i}] {s[:180]}')

print(f'\nPHÁN QUYẾT count: {r.count("PHÁN QUYẾT")}')
print(f'KHẲNG ĐỊNH count: {r.count("KHẲNG ĐỊNH")}')
print(f'THẮNG count: {r.count("THẮNG")}')
print(f'u17 viet nam count: {r.count("u17 viet nam")}')
print(f'u17 malaysia count: {r.count("u17 malaysia")}')
