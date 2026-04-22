import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')

print("======================================================================")
print("TEST V42.2 - KIEM TRA ÁM ĐỘNG & HÓA HỒI ĐẦU")
print("======================================================================")

from free_ai_helper import FreeAIHelper

helper = FreeAIHelper()

print("\n[TEST 1] HÓA HỒI ĐẦU SINH")
chart_data_1 = {
    "thong_tin_nguoi_hoi": {"cau_hoi": "Hỏi sếp việc này"},
    "chi_ngay": "Tý", "can_ngay": "Giáp", "chi_thang": "Thìn",
    "luc_hao": {
        "que_name": "Càn Vi Thiên", "que_so": 1,
        "luc_than": ["Phụ Mẫu", "Quan Quỷ", "Tử Tôn", "Thê Tài", "Huynh Đệ", "Phụ Mẫu"],
        "chi_hao": ["Dần", "Ngọ", "Tuất", "Tý", "Thìn", "Thân"],
        "can_hao": ["Giáp"] * 6,
        "the_hao": 1, "ung_hao": 4,
        # Hào 2 (Quan Quỷ Ngọ Hỏa) động hóa Dần Mộc (Mộc sinh Hỏa -> Hóa Hồi Đầu Sinh)
        "dong_hao": [2],
        "bien_hao": [{"hao": 2, "chi": "Dần", "luc_than": "Phụ Mẫu"}],
        "tuan_khong": ["Tuất", "Hợi"]
    }
}

result_1 = helper.answer_question("Hỏi sếp việc này", chart_data=chart_data_1)
if "Hồi Đầu Sinh" in result_1 or "HỒI ĐẦU SINH" in result_1:
    print("  ✅ PASS: Phát hiện Hóa Hồi Đầu Sinh")
else:
    print("  ❌ FAIL: Không phát hiện Hóa Hồi Đầu Sinh")
    open("test_output1.txt", "w", encoding="utf-8").write(result_1)
    print("      (Output written to test_output1.txt)")

print("\n[TEST 2] ÁM ĐỘNG (Nhật Xung Hào Tĩnh)")
chart_data_2 = {
    "thong_tin_nguoi_hoi": {"cau_hoi": "Hỏi tiền bạc tài sản"},
    "chi_ngay": "Ngọ", "can_ngay": "Giáp", "chi_thang": "Thìn", # Ngày Ngọ xung Tý
    "luc_hao": {
        "que_name": "Càn Vi Thiên", "que_so": 1,
        "luc_than": ["Phụ Mẫu", "Thê Tài", "Tử Tôn", "Thê Tài", "Huynh Đệ", "Phụ Mẫu"],
        "chi_hao": ["Dần", "Tý", "Tuất", "Ngọ", "Thìn", "Thân"], # Hào 2 Tý (tĩnh) bị ngày Ngọ xung -> Ám Động
        "can_hao": ["Giáp"] * 6,
        "the_hao": 1, "ung_hao": 4,
        "dong_hao": [],
        "bien_hao": [],
        "tuan_khong": ["Tuất", "Hợi"]
    }
}

result_2 = helper.answer_question("Hỏi tiền bạc tài sản", chart_data=chart_data_2)
if "ÁM ĐỘNG" in result_2 or "Ám Động" in result_2:
    print("  ✅ PASS: Phát hiện Ám Động")
else:
    print("  ❌ FAIL: Không phát hiện Ám Động")
    open("test_output2.txt", "w", encoding="utf-8").write(result_2)
    print("      (Output written to test_output2.txt)")

print("\n======================================================================")
print("HOAN THANH TEST V42.2")
print("======================================================================")
