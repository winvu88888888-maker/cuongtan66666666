import sys
sys.path.append('.')
from free_ai_helper import FreeAIHelper

ai = FreeAIHelper()
# Fake offline execution
ai.v8_mode = 'offline'

q = "ngày mai tôi phỏng vấn có đỗ công ty nào không trong 2 công ty. công ty 26tr đỗ không. công ty 22tr đỗ không"
res = ai.answer_question(q, None, "Tài Chính", None, None, None)
with open("test_out.html", "w", encoding="utf-8") as f:
    f.write(res)
print("SUCCESS!")
