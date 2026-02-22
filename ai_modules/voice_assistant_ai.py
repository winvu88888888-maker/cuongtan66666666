"""
VOICE ASSISTANT AI - Trợ Lý Giọng Nói (Text-based simulation)
Xử lý câu hỏi tự nhiên và trả lời
"""

INTENTS = {
    "xin_chao": ["xin chào", "hello", "hi", "chào"],
    "hoi_gio": ["mấy giờ", "giờ tốt", "giờ nào"],
    "hoi_ngay": ["ngày nào", "ngày tốt", "chọn ngày"],
    "hoi_huong": ["hướng nào", "phương nào", "đi hướng"],
    "hoi_tinh_cam": ["người yêu", "tình cảm", "hôn nhân"],
    "hoi_cong_viec": ["công việc", "xin việc", "thăng tiến"],
    "hoi_tien": ["tiền", "tài", "đầu tư", "lương"]
}


class VoiceAssistantAI:
    def __init__(self, gemini_helper=None):
        self.gemini = gemini_helper
    
    def detect_intent(self, text):
        text_lower = text.lower()
        for intent, keywords in INTENTS.items():
            if any(kw in text_lower for kw in keywords):
                return intent
        return "unknown"
    
    def process_query(self, query):
        intent = self.detect_intent(query)
        
        responses = {
            "xin_chao": "Xin chào! Tôi có thể giúp gì cho bạn?",
            "hoi_gio": "Bạn muốn hỏi giờ tốt? Hãy cho tôi biết bạn muốn làm việc gì.",
            "hoi_ngay": "Bạn muốn chọn ngày tốt? Cho tôi biết sự kiện gì nhé!",
            "hoi_huong": "Bạn hỏi về phương hướng? Cho tôi biết Can ngày hoặc mục đích.",
            "hoi_tinh_cam": "Bạn hỏi về tình cảm? Tôi sẽ phân tích cho bạn.",
            "hoi_cong_viec": "Về công việc, bạn đang quan tâm điều gì?",
            "hoi_tien": "Về tài chính, bạn muốn biết gì?",
            "unknown": "Tôi chưa hiểu rõ. Bạn có thể hỏi về: giờ tốt, ngày tốt, hướng, tình cảm, công việc, tiền bạc."
        }
        
        return {
            "query": query,
            "intent": intent,
            "response": responses.get(intent, responses["unknown"]),
            "suggestions": self._get_suggestions(intent)
        }
    
    def _get_suggestions(self, intent):
        suggestions = {
            "hoi_gio": ["Xem giờ Hoàng Đạo hôm nay", "Giờ tốt để ký hợp đồng"],
            "hoi_ngay": ["Ngày tốt kết hôn", "Ngày tốt khai trương"],
            "hoi_huong": ["Hướng xuất hành", "Hướng nhà tốt"],
            "hoi_tinh_cam": ["Xem tương hợp", "Triển vọng tình cảm"],
            "hoi_cong_viec": ["Xin việc", "Thăng tiến"],
            "hoi_tien": ["Cầu tài", "Đầu tư"]
        }
        return suggestions.get(intent, ["Xem QMDG", "Xem Mai Hoa", "Xem Lục Hào"])
    
    def get_response(self, query):
        result = self.process_query(query)
        output = [f"**Bạn:** {result['query']}"]
        output.append(f"**AI:** {result['response']}")
        output.append("\n**Gợi ý:**")
        for s in result['suggestions']:
            output.append(f"- {s}")
        return "\n".join(output)


_ai = None
def get_voice_assistant(gemini_helper=None):
    global _ai
    if _ai is None: _ai = VoiceAssistantAI(gemini_helper)
    return _ai
