# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper
h = FreeAIHelper()

# Call _generate_direct_answer via helper
da = h._generate_direct_answer(
    question='u17 viet nam va u17 malaysia doi nao thang',
    dung_than='Bản Thân',
    final_verdict='BÌNH',
    pct=49,
    cat_count=5,
    hung_count=4,
    evidence=['test'],
    impacts=['test'],
    ky_mon_reason='test',
    luc_hao_reason='test',
    mai_hoa_reason='test',
    chart_data=None,
    lh_factors=['V28 KM BT khắc Cung SV → chủ THẮNG +5'],
    km_factors=['KM Cửa Hưu Môn Cát +4'],
    mh_factors=['MH Thể sinh Dụng -3'],
)

print(f"direct_answer length: {len(da)}")
print(f"Lines: {len(da.split(chr(10)))}")

# Find key sections
for keyword in ['PHÁN QUYẾT', 'KHẲNG ĐỊNH', 'THẮNG', 'THUA', 'THÁM TỬ', 'VÌ SAO']:
    count = da.count(keyword)
    if count > 0:
        print(f"  ✅ {keyword}: {count}x")
    else:
        print(f"  ❌ {keyword}: 0x")

# Show first 30 lines
lines = da.split('\n')
print("\nFirst 30 lines:")
for i, line in enumerate(lines[:30]):
    if line.strip():
        print(f"  [{i}] {line.strip()[:150]}")
