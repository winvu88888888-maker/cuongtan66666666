import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')

from free_ai_helper import FreeAIHelper
helper = FreeAIHelper()

print("[TEST 1] HÓA HỒI ĐẦU SINH")
# Hào 2 Mộc động biến thành Thủy -> Thủy sinh Mộc -> Hóa Hồi Đầu Sinh
luc_hao_1 = {
    "ban": {
        "name": "Càn Vi Thiên",
        "palace": "Càn",
        "haos": [
            {"hao": 1, "luc_than": "Phụ Mẫu", "can_chi": "Giáp Tý", "ngu_hanh": "Thủy", "chi": "Tý"},
            {"hao": 2, "luc_than": "Quan Quỷ", "can_chi": "Giáp Dần", "ngu_hanh": "Mộc", "chi": "Dần"},
            {"hao": 3, "luc_than": "Tử Tôn", "can_chi": "Giáp Thìn", "ngu_hanh": "Thổ", "chi": "Thìn"},
            {"hao": 4, "luc_than": "Thê Tài", "can_chi": "Nhâm Ngọ", "ngu_hanh": "Hỏa", "chi": "Ngọ"},
            {"hao": 5, "luc_than": "Huynh Đệ", "can_chi": "Nhâm Thân", "ngu_hanh": "Kim", "chi": "Thân"},
            {"hao": 6, "luc_than": "Phụ Mẫu", "can_chi": "Nhâm Tuất", "ngu_hanh": "Thổ", "chi": "Tuất"}
        ]
    },
    "dong_hao": [2],
    "bien": {
        "haos": [
            {"hao": 1, "luc_than": "Phụ Mẫu", "can_chi": "Giáp Tý", "ngu_hanh": "Thủy", "chi": "Tý"},
            {"hao": 2, "luc_than": "Quan Quỷ", "can_chi": "Giáp Tý", "ngu_hanh": "Thủy", "chi": "Tý"}, # Hào biến
            {"hao": 3, "luc_than": "Tử Tôn", "can_chi": "Giáp Thìn", "ngu_hanh": "Thổ", "chi": "Thìn"},
            {"hao": 4, "luc_than": "Thê Tài", "can_chi": "Nhâm Ngọ", "ngu_hanh": "Hỏa", "chi": "Ngọ"},
            {"hao": 5, "luc_than": "Huynh Đệ", "can_chi": "Nhâm Thân", "ngu_hanh": "Kim", "chi": "Thân"},
            {"hao": 6, "luc_than": "Phụ Mẫu", "can_chi": "Nhâm Tuất", "ngu_hanh": "Thổ", "chi": "Tuất"}
        ]
    },
    "can_ngay": "Giáp", "chi_ngay": "Ngọ", "chi_thang": "Thìn"
}

res1 = helper._analyze_luc_hao_full(luc_hao_1, "Quan Quỷ", False)
print("Hồi Đầu Sinh detected:", "Hồi Đầu Sinh" in str(res1) or "HỒI ĐẦU SINH" in str(res1) or "HB01" in str(res1))
if "Hồi Đầu Sinh" not in str(res1) and "HB01" not in str(res1):
    print("OUTPUT1:")
    print(res1)

print("\n[TEST 2] ÁM ĐỘNG")
# Hào 1 Tý (Thủy) TĨNH. Ngày Ngọ (Hỏa) xung Tý -> Ám Động
luc_hao_2 = {
    "ban": {
        "name": "Càn Vi Thiên",
        "palace": "Càn",
        "haos": [
            {"hao": 1, "luc_than": "Thê Tài", "can_chi": "Giáp Tý", "ngu_hanh": "Thủy", "chi": "Tý"}, # Tý bị Ngọ xung
            {"hao": 2, "luc_than": "Quan Quỷ", "can_chi": "Giáp Dần", "ngu_hanh": "Mộc", "chi": "Dần"},
            {"hao": 3, "luc_than": "Tử Tôn", "can_chi": "Giáp Thìn", "ngu_hanh": "Thổ", "chi": "Thìn"},
            {"hao": 4, "luc_than": "Thê Tài", "can_chi": "Nhâm Ngọ", "ngu_hanh": "Hỏa", "chi": "Ngọ"},
            {"hao": 5, "luc_than": "Huynh Đệ", "can_chi": "Nhâm Thân", "ngu_hanh": "Kim", "chi": "Thân"},
            {"hao": 6, "luc_than": "Phụ Mẫu", "can_chi": "Nhâm Tuất", "ngu_hanh": "Thổ", "chi": "Tuất"}
        ]
    },
    "dong_hao": [],
    "bien": {"haos": []},
    "can_ngay": "Giáp", "chi_ngay": "Ngọ", "chi_thang": "Thìn"
}

res2 = helper._analyze_luc_hao_full(luc_hao_2, "Thê Tài", False)
print("Ám Động detected:", "ÁM ĐỘNG" in str(res2) or "Ám Động" in str(res2) or "NN08" in str(res2))
if "ÁM ĐỘNG" not in str(res2) and "Ám Động" not in str(res2) and "NN08" not in str(res2):
    print("OUTPUT2:")
    print(res2)
