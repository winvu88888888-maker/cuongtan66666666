"""Test V21.0 Offline Conclusion Output"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from free_ai_helper import FreeAIHelper

h = FreeAIHelper()  # Không API key → chỉ offline
mock = {'can_ngay':'Giáp','chi_ngay':'Tý','can_thang':'Bính','chi_thang':'Dần',
        'can_nam':'Ất','chi_nam':'Tị','can_gio':'Canh','chi_gio':'Ngọ',
        'can_thien_ban':{1:'Ất',2:'Kỷ',3:'Đinh',4:'Bính',5:'Mậu',6:'Canh',7:'Tân',8:'Nhâm',9:'Quý'},
        'can_dia_ban':{1:'Nhâm',2:'Kỷ',3:'Canh',4:'Tân',5:'Mậu',6:'Ất',7:'Bính',8:'Đinh',9:'Giáp'},
        'thien_ban':{1:'Thiên Bồng',2:'Thiên Nhuế',3:'Thiên Xung',4:'Thiên Phụ',5:'Thiên Cầm',6:'Thiên Tâm',7:'Thiên Trụ',8:'Thiên Nhậm',9:'Thiên Anh'},
        'nhan_ban':{1:'Hưu Môn',2:'Tử Môn',3:'Thương Môn',4:'Đỗ Môn',5:'',6:'Khai Môn',7:'Kinh Môn',8:'Sinh Môn',9:'Cảnh Môn'},
        'than_ban':{1:'Trực Phù',2:'Đằng Xà',3:'Thái Âm',4:'Lục Hợp',5:'',6:'Bạch Hổ',7:'Huyền Vũ',8:'Cửu Địa',9:'Cửu Thiên'}}

tests = [
    "Tôi có nên mua nhà bây giờ không?",
    "Bố tôi bệnh nặng có qua khỏi không?",
    "Khi nào tôi được thăng chức?",
    "Người yêu có thật lòng không?",
    "Tôi có mấy anh chị em?",
    "Vận mệnh tôi năm nay thế nào?",
]

for q in tests:
    print(f"\n{'='*70}")
    print(f"Q: {q}")
    print('='*70)
    r = h.answer_question(question=q, chart_data=mock)
    # Show only the SHORT conclusion (before <details>)
    if '<details>' in r:
        short = r.split('<details>')[0]
    else:
        short = r[:2000]
    # Truncate each line
    for line in short.split('\n'):
        if line.strip():
            print(line[:120])
    print(f"\n[Total output: {len(r)} chars]")
