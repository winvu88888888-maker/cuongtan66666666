# Test V42.9.9i — Full pipeline test via FreeAIHelper.answer_question()
import sys, os
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.path.insert(0, '.')

from free_ai_helper import FreeAIHelper, _analyze_dt_ecosystem

h = FreeAIHelper()

# Test cases: (question, expected_DT_in_output)
tests = [
    ('bo toi dau tu chung khoan co loi khong', 'Thê Tài'),
    ('me toi benh nang qua khoi khong', 'Phụ Mẫu'),
    ('con trai thi do khong', 'Phụ Mẫu'),  
    ('bo benh', 'Phụ Mẫu'),
    ('dau tu co loi khong', 'Thê Tài'),
]

print(f'Version: {h.version}')
print(f'Name: {h.name}')
print()

for q, expected_dt in tests:
    result = h.answer_question(q)
    # Check DT in logs
    dt_found = None
    for log in h.logs:
        if 'DT' in log.get('step', '') and log.get('status') in ('PERSON_STATE', 'ACTION_OVERRIDE', 'PERSON_ONLY'):
            detail = log.get('detail', '')
            # Extract DT from detail
            if 'DT=' in detail:
                dt_found = detail.split('DT=')[-1].strip()
            break
    
    # Check if expected DT appears in output
    has_dt = expected_dt in result
    status = 'PASS' if has_dt else 'CHECK'
    print(f'[{status}] "{q}" -> DT in output: {"YES" if has_dt else "NO"} (expected={expected_dt})')
    h.logs = []  # Reset

print()

# Verify ecosystem analysis appears in output
print('--- Checking ecosystem display ---')
result2 = h.answer_question('dau tu co phieu co loi khong')
if 'Nguyen Than' in result2 or 'Nguyen Th' in result2 or 'HE SINH THAI' in result2 or 'Nguyên Thần' in result2:
    print('PASS: Ecosystem analysis VISIBLE in output')
else:
    # Check for unicode version
    eco_markers = ['SINH THÁI', 'Nguyên Thần', 'Kỵ Thần', 'Cừu Thần', 'HỆ SINH']
    found = [m for m in eco_markers if m in result2]
    if found:
        print(f'PASS: Ecosystem analysis VISIBLE ({found})')
    else:
        print('FAIL: Ecosystem analysis NOT found in output')
        # Show first 2000 chars
        print(result2[:2000])

print()
print('ALL DONE')
