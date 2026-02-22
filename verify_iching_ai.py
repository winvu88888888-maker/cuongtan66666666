
import sys
import os
import json
import datetime

# Add current dir to path
sys.path.append(os.getcwd())

# Mock AI Helper
class MockGeminiHelper:
    def _call_ai(self, prompt):
        print("\n[AI CALL DETECTED]")
        print(f"Prompt Length: {len(prompt)}")
        if "Thiên Bồng" in prompt:
            print("✅ Prompt contains detailed Star info.")
        else:
            print("❌ Prompt MISSING detailed Star info.")
        return "AI Response: Data verified."

try:
    from qmdg_orchestrator import AIOrchestrator
    print("✅ Imported AIOrchestrator")
except ImportError as e:
    print(f"❌ Import Failed: {e}")
    sys.exit(1)

# Initialize
mock_gemini = MockGeminiHelper()
orchestrator = AIOrchestrator(mock_gemini)

# Mock QMDG Data
mock_qmdg = {
    "can_ngay": "Giáp Tý", "can_gio": "Bính Dần",
    "can_nam": "Ất Tỵ", "chi_nam": "", "can_thang": "Mậu", "chi_thang": "Dần",
    "chi_ngay": "", "chi_gio": "",
    "tiet_khi": "Lập Xuân", "cuc": "Dương Độn 8 Cục",
    "truc_phu": "Thiên Bồng", "truc_su": "Hưu Môn",
    # Full 9 Palaces (simplified for test)
    "thien_ban": {"1":"Thiên Bồng", "3":"Thiên Xung", "9":"Thiên Anh"},
    "nhan_ban": {"1":"Hưu Môn", "3":"Thương Môn", "9":"Cảnh Môn"},
    "bat_than": {"1":"Trực Phù", "3":"Cửu Thiên", "9":"Đằng Xà"},
    "can_thien_ban": {"1":"Giáp", "3":"Ất", "9":"Bính"},
    "can_dia_ban": {"1":"Mậu", "3":"Kỷ", "9":"Canh"},
    "khong": {"ngay": "Tuất Hợi", "gio": "Tý Sửu"}
}

print("\n--- Testing _format_live_context ---")
context = orchestrator._format_live_context(mock_qmdg, None, None, "Tài Lộc")
print(context)

if "Thiên Bồng" in context and "Hưu Môn" in context:
    print("\n✅ Context Generation SUCCESS")
else:
    print("\n❌ Context Generation FAILED")

print("\n--- Testing run_pipeline ---")
orchestrator.run_pipeline("Tài lộc tháng này?", "Tài Lộc", mock_qmdg)
