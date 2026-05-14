# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from free_ai_helper import v32_parse_question
res = v32_parse_question('Tôi có bao nhiêu đứa con, và tôi đang làm công ty sản xuất gì')
for r in res:
    print(r)
