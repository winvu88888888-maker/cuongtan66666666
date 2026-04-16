"""Test 9 câu hỏi — mô phỏng AI Offline V32.2"""
import sys, os
sys.path.insert(0, r'C:\Users\GHC\.gemini\antigravity\scratch\cuongtan66666666_fix')

from free_ai_helper import FreeAIHelper

helper = FreeAIHelper()

questions = [
    "tôi bao nhiêu tuổi",
    "bố tôi còn sống hay đã mất và đang ở đâu",
    "công ty tôi sản xuất gì có phát triển hay thụt lùi",
    "khi nào tôi có tiền và khi nào tôi mua được nhà mặt đất",
    "nhà tôi có mấy đứa con",
    "hôm nay tôi về quê tốt không",
    "vợ tôi bao nhiêu tuổi",
    "người yêu cháu gái của chị gái tôi có giàu không có tốt không là người thế nào có yêu thật lòng cháu gái tôi không",
]

for i, q in enumerate(questions, 1):
    print(f"\n{'='*80}")
    print(f"CÂU {i}: {q}")
    print(f"{'='*80}")
    try:
        result = helper.answer_question(q)
        # Print first 1000 chars of result
        if result:
            print(result[:1500])
            if len(result) > 1500:
                print(f"\n... [{len(result)} chars total]")
        else:
            print("(no result)")
    except Exception as e:
        print(f"ERROR: {e}")
    print()
