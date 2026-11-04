# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, '.')
from free_ai_helper import _extract_two_sides, _is_competition_question

tests = [
    'u17 viet nam va u17 malaysia doi nao thang',
    'đội u17 việt nam và u17 malasia đội nào thắng',
    'MU vs Liverpool ai thang',
    'Viet Nam gap Thai Lan thang hay thua',
]
for q in tests:
    is_comp = _is_competition_question(q)
    a, b = _extract_two_sides(q)
    print(f'Q: {q}')
    print(f'  is_comp={is_comp}, A="{a}", B="{b}"')
    print()
