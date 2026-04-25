# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper
h = FreeAIHelper()

# Test COMPETITION
print('='*60)
print('TEST COMPETITION: u17 viet nam va u17 malaysia')
print('='*60)
r = h.answer_question('u17 viet nam va u17 malaysia doi nao thang', chart_data=None, topic=None)

# Count sections
for label in ['KẾT LUẬN AI OFFLINE','PROTOCOL 27','THÁM TỬ KIỂM CHỨNG','VẠN VẬT CỤ THỂ','KẾT LUẬN TỔNG HỢP','DETERMINISTIC']:
    cnt = r.count(label)
    status = '✅' if cnt <= 1 else '❌'
    print(f'  {status} {label}: {cnt}x')

# Show header + key lines only
print()
print('HEADER + KEY VERDICT LINES:')
for i, line in enumerate(r.split('\n')):
    stripped = line.strip()
    if any(k in stripped for k in ['THẮNG','THUA','HÒA','KẾT LUẬN AI','PHÁN QUYẾT','Phương pháp','KHẲNG ĐỊNH']):
        # Skip HTML-only lines
        if stripped.startswith('<div') and 'KẾT LUẬN' not in stripped:
            continue
        print(f'  [{i}] {stripped[:220]}')

# Count total lines in output
total_lines = len(r.split('\n'))
print(f'\nTotal output lines: {total_lines}')

# Check if VẠN VẬT is visible outside collapse
splits = r.split('<details>')
if len(splits) > 1:
    before_collapse = splits[0]
    if 'VẠN VẬT' in before_collapse:
        print('❌ VẠN VẬT visible OUTSIDE collapse!')
    else:
        print('✅ VẠN VẬT hidden inside collapse (or absent for competition)')
