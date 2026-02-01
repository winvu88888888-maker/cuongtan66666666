
import os
import json
import sys
from gemini_helper import GeminiQMDGHelperV172

# Load API Key
def get_api_key():
    try:
        if os.path.exists("custom_data.json"):
            with open("custom_data.json", "r") as f:
                data = json.load(f)
                return data.get("GEMINI_API_KEY")
    except: pass
    return None

api_key = get_api_key()
if not api_key:
    print("❌ Không tìm thấy API Key trong custom_data.json")
    sys.exit(1)

print(f"✅ Đã tìm thấy API Key. Đang khởi tạo Đại Pháp Sư AI...")
helper = GeminiQMDGHelperV172(api_key)

# Test Persona: A risky gambling question
question = "Mai tôi muốn đánh lô con gì để trúng lớn? (Gợi ý dựa trên giờ Tỵ ngày mai)"
print(f"❓ Câu hỏi: {question}")
print("⏳ Đang gọi AI (Kiểm tra nhân cách mới)...")

response = helper.answer_question(question)

print("-" * 50)
print("🤖 PHÁN QUYẾT CỦA ĐẠI PHÁP SƯ:")
print(response)
print("-" * 50)

if "CÓ" in response.upper() or "KHÔNG" in response.upper() or any(char.isdigit() for char in response):
    print("✅ THÀNH CÔNG: AI trả lời quyết đoán có số liệu/kết luận.")
else:
    print("⚠️ THẤT BẠI: AI vẫn trả lời chung chung.")
