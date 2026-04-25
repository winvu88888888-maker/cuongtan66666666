# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper, _generate_direct_answer

# Call _generate_direct_answer directly
da = _generate_direct_answer(
    question='u17 viet nam va u17 malaysia doi nao thang',
    dung_than='Bản Thân',
    chart_data=None,
    luc_hao_data=None,
    mai_hoa_data=None,
    chain_evidence=[],
    verdicts_map={},
    hanh_dt='Thổ',
    final_pct=49,
    lh_factors=[],
    km_factors=[],
    mh_factors=[]
)

print(f"direct_answer length: {len(da) if da else 0}")
if da:
    lines = da.split('\n')
    print(f"Lines: {len(lines)}")
    # Find PHÁN QUYẾT
    for i, line in enumerate(lines):
        if 'PHÁN' in line or 'THẮNG' in line or 'KHẲNG' in line:
            print(f"[{i}] {line.strip()[:150]}")
else:
    print("direct_answer is EMPTY!")
