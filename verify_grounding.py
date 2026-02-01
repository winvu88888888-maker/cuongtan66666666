
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

print(f"✅ Đã tìm thấy API Key. Đang khởi tạo AI...")
helper = GeminiQMDGHelperV172(api_key)

# Test Question requiring search
question = "Giá bitcoin hiện tại là bao nhiêu? (Hãy tìm kiếm thông tin mới nhất)"
print(f"❓ Câu hỏi: {question}")
print("⏳ Đang gọi AI (có bật Google Search)...")

response = helper.answer_question(question)

print("-" * 50)
print("🤖 CÂU TRẢ LỜI CỦA AI:")
print(response)
print("-" * 50)

if "Giá" in response or "$" in response or "USD" in response:
    print("✅ CÓ VẺ THÀNH CÔNG: AI đã trả lời với số liệu.")
else:
    print("⚠️ CẨN TRỌNG: Câu trả lời có thể chưa cập nhật.")
