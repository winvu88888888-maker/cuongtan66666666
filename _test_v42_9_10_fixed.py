# -*- coding: utf-8 -*-
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from free_ai_helper import FreeAIHelper

helper = FreeAIHelper()
# Mock chart data
chart_data = {
    'can_ngay': 'Giáp',
    'chi_ngay': 'Tý',
    'can_thang': 'Mậu',
    'chi_thang': 'Thìn',
    'can_nam': 'Bính',
    'chi_nam': 'Ngọ',
    'can_gio': 'Đinh',
    'chi_gio': 'Mão',
    'tiet_khi': 'Lập Xuân',
    'cuc': 'Dương Độn 1 Cục',
    'luc_hao_info': {},
    'ky_mon_info': {},
    'mai_hoa_info': {},
    'luc_nham_info': {},
    'thai_at_info': {}
}

question = "Tôi muốn hỏi đầu tư chứng khoán năm nay thế nào, mua đất ở hướng đông nam được không, và bệnh đau lưng khi nào khỏi?"
ans, q_parsed = helper.answer_question(question, chart_data=chart_data)

with open('_test_out_v42_9_10_fixed.txt', 'w', encoding='utf-8') as f:
    f.write(ans)

print("Test finished. Output length:", len(ans))
