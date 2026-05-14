# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from free_ai_helper import _get_all_dung_than
res = _get_all_dung_than('Tôi có bao nhiêu đứa con, và tôi đang làm công ty sản xuất gì')
print("_get_all_dung_than:", res)
