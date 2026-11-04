# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from free_ai_helper import FreeAIHelper

fake_chart = {
    'can_ngay': 'Giáp', 'chi_ngay': 'Dần',
    'can_gio': 'Bính', 'chi_gio': 'Ngọ',
    'can_thang': 'Canh', 'chi_thang': 'Thìn',
    'can_nam': 'Mậu', 'chi_nam': 'Tuất',
    'can_thien_ban': {1:'Canh',2:'Tân',3:'Nhâm',4:'Quý',5:'Giáp',6:'Ất',7:'Bính',8:'Đinh',9:'Mậu'},
    'thien_ban': {1:'Bồng',2:'Nhậm',3:'Trụ',4:'Tâm',5:'Cầm',6:'Phụ',7:'Anh',8:'Nhuế',9:'Xung'},
    'nhan_ban': {1:'Hưu Môn',2:'Sinh Môn',3:'Thương Môn',4:'Đỗ Môn',5:'Cảnh Môn',6:'Tử Môn',7:'Kinh Môn',8:'Khai Môn',9:'Đinh Môn'},
    'than_ban': {1:'Trực Phù',2:'Đằng Xà',3:'Thái Âm',4:'Lục Hợp',5:'Câu Trận',6:'Chu Tước',7:'Cửu Địa',8:'Cửu Thiên',9:'Bạch Hổ'},
    'dia_can': {1:'Ất',2:'Bính',3:'Đinh',4:'Mậu',5:'Kỷ',6:'Canh',7:'Tân',8:'Nhâm',9:'Quý'},
    'hanh_dt': '',
}

h = FreeAIHelper()
res = h.answer_question('bao gio toi co nguoi yeu', chart_data=fake_chart)
with open('test_ung_ky_output.txt', 'w', encoding='utf-8') as f:
    f.write(res)
print("Done")
