"""Test 9 câu hỏi — V32.4 Full Pipeline"""
import sys, os
sys.path.insert(0, r'C:\Users\GHC\.gemini\antigravity\scratch\cuongtan66666666_fix')

from free_ai_helper import FreeAIHelper

helper = FreeAIHelper()

questions = [
    "tôi bao nhiêu tuổi",
    "bố tôi còn sống hay đã mất, và đang ở đâu",
    "công ty tôi sản xuất gì, có phát triển hay thụt lùi",
    "khi nào tôi có tiền và khi nào tôi mua được nhà mặt đất",
    "nhà tôi có mấy đứa con",
    "hôm nay tôi về quê tốt không",
    "vợ tôi bao nhiêu tuổi",
    "người yêu cháu gái của chị gái tôi có giàu không, có tốt không, là người thế nào, có yêu thật lòng cháu gái tôi không",
]

for i, q in enumerate(questions, 1):
    print(f"\n{'='*80}")
    print(f"CÂU {i}: {q}")
    print(f"{'='*80}")
    try:
        result = helper.answer_question(q)
        if result:
            # Chỉ in phần KẾT LUẬN chính (không in chi tiết 5 PP)
            lines = result.split('\n')
            important = []
            in_details = False
            for line in lines:
                if '<details>' in line:
                    in_details = True
                    important.append("  [... Chi tiết 5 PP ẩn ...]")
                    continue
                if '</details>' in line:
                    in_details = False
                    continue
                if not in_details:
                    important.append(line)
            
            output = '\n'.join(important)
            # Giới hạn output
            if len(output) > 1500:
                output = output[:1500] + "\n... [CẮT BỚT]"
            print(output)
        else:
            print("⚠️ KẾT QUẢ TRỐNG!")
    except Exception as e:
        print(f"❌ LỖI: {e}")

print(f"\n{'='*80}")
print("HOÀN TẤT TEST 8 CÂU HỎI")
