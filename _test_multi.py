# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from free_ai_helper import FreeAIHelper

helper = FreeAIHelper()
# Use a mock chart_data that resembles real input
chart_data = {
    'can_ngay': 'Giáp',
    'chi_ngay': 'Tý',
    'can_thang': 'Mậu',
    'chi_thang': 'Thìn',
    'can_nam': 'Bính',
    'chi_nam': 'Ngọ',
    'can_gio': 'Đinh',
    'chi_gio': 'Mão',
    'luc_hao_info': {},
    'ky_mon_info': {},
    'mai_hoa_info': {},
    'luc_nham_info': {},
    'thai_at_info': {}
}

question = "tôi về quê xe màu gì, lái xe là nam hay nữ, số tiền phải trả là bao nhiêu"
result = helper.answer_question(question, chart_data=chart_data)
print("====== RESULT ======")
print(result)
