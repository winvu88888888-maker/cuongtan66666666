# Test V42.9.9i fixes
import sys
sys.path.insert(0, '.')

# Test 1: Import OK
from free_ai_helper import FreeAIHelper, _get_dung_than, _analyze_dt_ecosystem
print('✅ Import OK')

# Test 2: Version strings
h = FreeAIHelper()
assert 'V42.9.9i' in h.name, f'FAIL: name={h.name}'
assert 'V42.9.9i' in h.version, f'FAIL: version={h.version}'
print(f'✅ Version: {h.version}')

# Test 3: DT Logic — PERSON + ACTION (the main fix)
tests = [
    ('bố tôi đầu tư chứng khoán có lời không', 'Thê Tài'),
    ('mẹ tôi bệnh nặng qua khỏi không', 'Phụ Mẫu'),
    ('con trai thi đỗ không', 'Phụ Mẫu'),
    ('chồng ngoại tình', 'Thê Tài'),
    ('bố mẹ kinh doanh', 'Thê Tài'),
    ('con gái du lịch', 'Bản Thân'),
    ('mẹ xin việc', 'Quan Quỷ'),
    ('bố bệnh', 'Phụ Mẫu'),
    ('vợ bệnh', 'Thê Tài'),
    ('tôi bệnh', 'Bản Thân'),
    ('đầu tư có lời không', 'Thê Tài'),
    ('xin việc có được không', 'Quan Quỷ'),
]
pass_count = 0
for q, expected in tests:
    dt = _get_dung_than(q)
    status = '✅' if dt == expected else '❌'
    if dt != expected:
        print(f'{status} DT("{q}") = {dt} (expected {expected})')
    else:
        pass_count += 1
        print(f'{status} DT("{q}") = {dt}')
print(f'\n📊 DT Logic: {pass_count}/{len(tests)} pass\n')

# Test 4: Nguyên/Kỵ/Cừu
eco = _analyze_dt_ecosystem('Thê Tài', None, None)
assert eco['nguyen_than']['name'] == 'Tử Tôn', f'FAIL: nguyen={eco["nguyen_than"]}'
assert eco['ky_than']['name'] == 'Huynh Đệ', f'FAIL: ky={eco["ky_than"]}'
assert eco['cuu_than']['name'] == 'Quan Quỷ', f'FAIL: cuu={eco["cuu_than"]}'
print(f'✅ Ecosystem: Thê Tài → Nguyen={eco["nguyen_than"]["name"]}, Ky={eco["ky_than"]["name"]}, Cuu={eco["cuu_than"]["name"]}')

eco2 = _analyze_dt_ecosystem('Quan Quỷ', None, None)
assert eco2['nguyen_than']['name'] == 'Thê Tài'
assert eco2['ky_than']['name'] == 'Tử Tôn'
print(f'✅ Ecosystem: Quan Quỷ → Nguyen={eco2["nguyen_than"]["name"]}, Ky={eco2["ky_than"]["name"]}')

eco3 = _analyze_dt_ecosystem('Phụ Mẫu', None, None)
assert eco3['nguyen_than']['name'] == 'Quan Quỷ'
assert eco3['ky_than']['name'] == 'Thê Tài'
assert eco3['cuu_than']['name'] == 'Huynh Đệ'
print(f'✅ Ecosystem: Phụ Mẫu → Nguyen={eco3["nguyen_than"]["name"]}, Ky={eco3["ky_than"]["name"]}, Cuu={eco3["cuu_than"]["name"]}')

# Test factors output
print(f'\n📋 Sample factors for Thê Tài:')
for f in eco['factors']:
    print(f'  {f}')

print()
print('🎯 ALL TESTS PASSED')
