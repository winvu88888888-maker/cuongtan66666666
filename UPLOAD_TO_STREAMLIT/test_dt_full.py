"""Full DT verification test V21.0"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from free_ai_helper import FreeAIHelper

h = FreeAIHelper()
mock = {'can_ngay':'Giáp','chi_ngay':'Tý','can_thang':'Bính','chi_thang':'Dần',
        'can_nam':'Ất','chi_nam':'Tị','can_gio':'Canh','chi_gio':'Ngọ',
        'can_thien_ban':{1:'Ất',2:'Kỷ'},'can_dia_ban':{},'thien_ban':{},'nhan_ban':{},'than_ban':{}}

tests = [
    ('Tôi có nên mua nhà bây giờ không?', 'Thê Tài'),
    ('Bố tôi bệnh nặng có qua khỏi không?', 'Phụ Mẫu'),
    ('Sức khỏe tôi năm nay thế nào?', 'Bản Thân'),
    ('Khi nào tôi được thăng chức?', 'Quan Quỷ'),
    ('Bao giờ tôi lấy vợ?', 'Thê Tài'),
    ('Con trai có đi du học được không?', 'Tử Tôn'),
    ('Người yêu có thật lòng không?', 'Thê Tài'),
    ('Tôi có mấy anh chị em?', 'Huynh Đệ'),
    ('Mẹ tôi ốm có nên phẫu thuật?', 'Phụ Mẫu'),
    ('Vận mệnh tôi năm nay thế nào?', 'Bản Thân'),
    ('Mất điện thoại ở đâu?', 'Thê Tài'),
    ('Có quý nhân giúp tôi không?', 'Bản Thân'),
    ('Đi xe hôm nay có an toàn không?', 'Bản Thân'),
    ('Thi đại học có đỗ không?', 'Quan Quỷ'),
]

correct = 0
for q, exp in tests:
    r = h.answer_question(question=q, chart_data=mock)
    dt_line = '?'
    for line in r.split('\n'):
        if '🎯' in line and 'Dụng Thần' in line:
            dt_line = line.strip()
            break
    ok = exp in dt_line
    if ok:
        correct += 1
    icon = '✅' if ok else '❌'
    print(f'{icon} Q={q[:40]:42s} Exp={exp:12s} Got={dt_line[20:50]}')

print(f'\n{"="*60}')
print(f'ĐỘ CHÍNH XÁC: {correct}/{len(tests)} = {correct*100//len(tests)}%')
