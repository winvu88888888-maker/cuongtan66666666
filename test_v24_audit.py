import sys
from free_ai_helper import FreeAIHelper

chart_data = {
    'can_ngay': 'Giáp',
    'chi_ngay': 'Tý',
    'chi_nam': 'Hợi',
    'can_gio': 'Bính',
    'chi_gio': 'Dần',
    'can_thien_ban': {'3': 'Mậu', '4': 'Bính', '9': 'Đinh'},
    'thien_ban': {'3': 'Thiên Cầm', '4': 'Thiên Tâm', '9': 'Thiên Cột'},
    'nhan_ban': {'3': 'Tử Môn', '4': 'Khai Môn', '9': 'Kinh Môn'},
    'than_ban': {'3': 'Cửu Thiên', '4': 'Trực Phù', '9': 'Lục Hợp'}
}

luc_hao_data = {
    'ban': {'name': 'Thuần Càn', 'quai_id': 1},
    'hao': [
        {'name':'Hào 1', 'chi':'Tý', 'than':'Tử Tôn', 'luc_than':'Thanh Long'}, 
        {'name':'Hào 2', 'chi':'Dần', 'than':'Thê Tài', 'luc_than':'Chu Tước'}
    ],
    'dung_than': 'Thê Tài'
}

mai_hoa_data = {
    'upper': 1, 'lower': 2, 'dong_hao': 1, 'ten': 'Thiên Trạch Lý',
    'ten_ho': 'Gia Nhân', 'ten_qua_bien': 'Thiên Thủy Tụng'
}

helper = FreeAIHelper()
# Đổi fake API key để nó chỉ chạy Offline và raise Exception nếu Online
helper._api_key = "FAKE_KEY"

ans = helper.answer_question(
    question="Kinh doanh tháng tới có lợi nhuận không?",
    dung_than="Thê Tài",
    chart_data=chart_data,
    luc_hao_data=luc_hao_data,
    mai_hoa_data=mai_hoa_data,
    topic="TÀI_CHÍNH"
)

print("\n\n" + "="*50)
print("V26.2 OFFLINE OUTPUT KẾT QUẢ TỪ ANSWER_QUESTION")
print("="*50)
print(ans)
