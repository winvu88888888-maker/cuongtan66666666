import json
from free_ai_helper import FreeAIHelper
from free_qmdg import FreeQMDG

def mock_gemini(*args, **kwargs):
    return "MOCKED_GEMINI_OUTPUT"

def run_test():
    qmdg = FreeQMDG()
    chart = qmdg.lap_que_nhanh("2026-05-05 10:00")
    
    helper = FreeAIHelper()
    # Mock online AI to speed up test
    helper._try_online_ai = lambda *a, **k: "MOCKED GEMINI"
    
    question = "Tôi muốn hỏi đầu tư chứng khoán năm nay thế nào. Tôi mua đất ở hướng đông nam được không? Bệnh đau lưng của tôi khi nào khỏi?"
    
    print("=== TESTING V42.9.10 ===")
    print(f"Câu hỏi: {question}")
    
    # Capture offline output
    global_dict = {}
    import sys
    
    # We will just call answer_question directly
    ans, q_parsed = helper.answer_question(question, chart_data=chart)
    
    # Search for V42.9.10 elements in the answer
    print("\n--- RESULTS ---")
    if "XUNG ĐỘT" in ans:
        print("✅ Conflict UI Warning Found")
    else:
        print("❌ Conflict UI Warning NOT Found")
        
    if "TỔNG QUAN:" in ans:
        print("✅ Cross-Question Synthesis Found")
    else:
        print("❌ Cross-Question Synthesis NOT Found")
        
    if "Bản Thân" in ans or "Thê Tài" in ans or "Phụ Mẫu" in ans or "Tử Tôn" in ans:
        print("✅ Dụng Thần mapping logic worked")
        
    print("\nLength of offline output:", len(ans))
    
    with open('_test_out_v42_9_10.md', 'w', encoding='utf-8') as f:
        f.write(ans)
    print("Dumped full output to _test_out_v42_9_10.md")

if __name__ == "__main__":
    run_test()
