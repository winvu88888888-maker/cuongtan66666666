import os
import json
import uuid
from datetime import datetime

class FeedbackRAG:
    """
    V25.0 Feedback RAG 
    Quản lý bộ nhớ kinh nghiệm thực tế của người dùng.
    """
    def __init__(self, db_path="data_hub/user_experience_db.json"):
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        if not os.path.exists("data_hub"):
            os.makedirs("data_hub", exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def save_feedback(self, question, dung_than, result_status, feedback_text, user_analysis="", chart_summary=""):
        """
        Lưu phản hồi kinh nghiệm vào cơ sở dữ liệu học tập.
        result_status: 'DUNG' hoặc 'SAI'
        user_analysis: (Ghi chú chuyên sâu) Người xem tự phân tích tại sao hôm đó AI lại luận sai, sai ở bước nào.
        """
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []

        new_entry = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": question,
            "dung_than": dung_than,
            "result_status": result_status,
            "feedback_text": feedback_text,
            "user_analysis": user_analysis,
            "chart_summary": chart_summary
        }
        
        data.append(new_entry)
        
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        return True

    def search_experience(self, question, dung_than, top_k=3):
        """
        Tìm kiếm các án lệ kinh nghiệm tương tự.
        RAG cơ bản: So khớp từ khóa và Dụng Thần.
        """
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return []

        if not data:
            return []

        q_lower = question.lower()
        scored_data = []

        for entry in data:
            score = 0
            # 1. Trùng Dụng Thần: Cực kỳ quan trọng
            if entry.get("dung_than") == dung_than:
                score += 50
                
            # 2. Xử lý trùng lặp từ khóa (Jaccard similarity cơ bản)
            db_q = entry.get("question", "").lower()
            q_words = set(q_lower.split())
            db_words = set(db_q.split())
            common_words = q_words.intersection(db_words)
            if db_words:
                score += (len(common_words) / len(db_words)) * 50

            if score > 0:
                scored_data.append((score, entry))

        # Sort desc
        scored_data.sort(key=lambda x: x[0], reverse=True)
        
        # Chỉ lấy top_k có điểm > 20
        results = [item[1] for item in scored_data if item[0] > 20][:top_k]
        return results

    def build_rag_prompt(self, experiences):
        """
        Build chuỗi prompt RAG dựa trên các Án Lệ.
        """
        if not experiences:
            return ""
        
        prompt = "\n[🔴 BỘ NHỚ KINH NGHIỆM THỰC TẾ (RAG) - CỐT LÕI CẦN LƯU Ý🔴]\n"
        prompt += "Dưới đây là một số trường hợp GIỐNG HỆT hoặc TƯƠNG TỰ trong quá khứ do chính thầy phong thủy ghi nhận lại kết quả thực tế ngoài đời. BẮT BUỘC PHẢI THAM KHẢO VÀ RÚT KINH NGHIỆM ĐỂ SUY LUẬN TRÁNH SAI LẦM:\n"
        
        for idx, ex in enumerate(experiences):
            prompt += f"\n👉 ÁN LỆ #{idx+1}:\n"
            prompt += f"   - Câu hỏi quá khứ: '{ex['question']}' (Dụng thần: {ex['dung_than']})\n"
            prompt += f"   - Đánh giá của thầy phong thủy về AI cũ: {ex['result_status']}\n"
            prompt += f"   - 💡 BÀI HỌC THỰC TẾ RÚT RA: {ex['feedback_text']}\n"
            if ex.get('user_analysis') and ex['user_analysis'].strip():
                prompt += f"   - 🔎 LỜI GIẢI MÃ LỖI SAI DO THẦY PHONG THỦY GHI CHÚ: {ex['user_analysis']}\n"
            if ex.get('chart_summary'):
                prompt += f"   - Tóm tắt quẻ: {ex['chart_summary']}\n"
                
        prompt += "\n(=== Hết Bộ Nhớ Kinh Nghiệm ===) -> Yêu cầu phân tích quẻ hiện tại và khéo léo kết hợp nếu có dấu hiệu tương tự bị lặp lại!\n"
        return prompt
