# -*- coding: utf-8 -*-
"""Test full pipeline với Vietnamese CÓ DẤU"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from free_ai_helper import FreeAIHelper, _get_dung_than

# Test 1: Standalone DT detection
tests = [
    ('Năm nay có nên đầu tư kinh doanh không', 'Thê Tài'),
    ('Tôi có nên mua nhà không', 'Thê Tài'),
    ('Mẹ tôi bệnh có khỏi không', 'Phụ Mẫu'),
    ('Bao giờ tôi có người yêu', 'Thê Tài'),
    ('Năm nay làm ăn có phát tài không', 'Thê Tài'),
    ('Con tôi thi đại học có đỗ không', 'Tử Tôn'),
    ('Chuyển việc có tốt hơn không', 'Quan Quỷ'),
]

print('=' * 60)
print('TEST 1: _get_dung_than (Vietnamese WITH diacritics)')
print('=' * 60)
for q, expected in tests:
    dt = _get_dung_than(q)
    ok = '✅' if dt == expected else '❌'
    print(f'  {ok} Q: {q}')
    print(f'     DT: {dt} (expected: {expected})')
    print()

# Test 2: Full pipeline with FreeAIHelper.answer_question
print('=' * 60)
print('TEST 2: Full answer_question pipeline')
print('=' * 60)

helper = FreeAIHelper()
fake_chart = {
    'can_ngay': 'Giáp', 'chi_ngay': 'Dần',
    'can_gio': 'Bính', 'chi_gio': 'Ngọ',
    'can_thang': 'Canh', 'chi_thang': 'Thìn',
    'can_nam': 'Mậu', 'chi_nam': 'Tuất',
    'can_thien_ban': {},
    'thien_ban': {}, 'nhan_ban': {}, 'than_ban': {},
    'hanh_dt': '',
}

for q, expected_dt in tests[:4]:
    print(f'\nQ: {q}')
    try:
        result = helper.answer_question(q, fake_chart)
        if isinstance(result, dict):
            dt = result.get('dung_than', '?')
            cat = result.get('detected_category', '?')
            pct = result.get('weighted_pct', '?')
            ok = '✅' if dt == expected_dt else '❌'
            print(f'  {ok} DT: {dt} | Category: {cat} | Pct: {pct}%')
        elif isinstance(result, tuple):
            print(f'  Result is tuple ({len(result)} elements)')
            # Look for DT in the text result
            for i, r in enumerate(result):
                if isinstance(r, str):
                    for line in r.split('\n'):
                        if 'DT:' in line or 'dung_than' in line:
                            print(f'    [{i}] {line.strip()[:150]}')
                elif isinstance(r, dict):
                    dt = r.get('dung_than', '?')
                    cat = r.get('detected_category', '?')
                    pct = r.get('weighted_pct', '?')
                    ok = '✅' if dt == expected_dt else '❌'
                    print(f'  {ok} DT: {dt} | Category: {cat} | Pct: {pct}%')
        else:
            print(f'  Result type: {type(result)}')
    except Exception as e:
        print(f'  ❌ ERROR: {type(e).__name__}: {e}')
        import traceback
        traceback.print_exc()
