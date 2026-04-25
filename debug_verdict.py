# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper
h = FreeAIHelper()
r = h.answer_question('u17 viet nam va u17 malaysia doi nao thang', chart_data=None, topic=None)

# Check logs for direct_answer
for log in h.logs:
    step = log.get('step', '')
    if 'direct' in step.lower() or 'answer' in step.lower() or 'thám' in step.lower():
        print(f"LOG: {log}")

# Check if PHÁN in the raw output
import re
phan_lines = [line for line in r.split('\n') if 'PH' in line and 'N QUY' in line]
print(f"\nPHÁN QUYẾT lines: {len(phan_lines)}")
for l in phan_lines:
    print(f"  {l.strip()[:150]}")

# Check with unicode
phan = '\u0050\u0048\u00c1\u004e'  # PHÁN
quyet = '\u0051\u0055\u0059\u1ebe\u0054'  # QUYẾT
print(f"\nSearching '{phan} {quyet}': {r.count(phan + ' ' + quyet)}")
