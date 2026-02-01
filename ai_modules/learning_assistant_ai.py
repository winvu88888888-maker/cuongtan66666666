"""
LEARNING ASSISTANT AI - Trợ Lý Học QMDG
Hướng dẫn và dạy học Kỳ Môn Độn Giáp cho người mới
"""


# Bài học cơ bản
LESSONS = {
    "basic": {
        "1": {
            "title": "Giới thiệu Kỳ Môn Độn Giáp",
            "content": """
## Bài 1: Kỳ Môn Độn Giáp là gì?

**Kỳ Môn Độn Giáp** (奇門遁甲) là một trong 3 đại học thuật số của Trung Hoa cổ đại, cùng với Thái Ất và Lục Nhâm.

### Cấu trúc cơ bản:
- **Cửu Cung Bát Quái**: 9 cung (1-9), 8 quái
- **Bát Môn**: 8 cửa (Khai, Hưu, Sinh, Thương, Đỗ, Cảnh, Tử, Kinh)
- **Cửu Tinh**: 9 sao (Thiên Bồng, Thiên Nhuế, Thiên Xung, Thiên Phụ, Thiên Cầm, Thiên Tâm, Thiên Trụ, Thiên Nhậm, Thiên Anh)
- **Bát Thần**: 8 thần (Trực Phù, Đằng Xà, Thái Âm, Lục Hợp, Câu Trần, Chu Tước, Cửu Địa, Cửu Thiên)

### Ứng dụng:
- Xem thời điểm tốt/xấu
- Dự đoán sự việc
- Chọn hướng, phương vị
- Mưu sự, chiến lược
""",
            "quiz": [
                {"q": "QMDG có bao nhiêu Môn?", "a": "8", "options": ["6", "8", "9", "10"]},
                {"q": "QMDG có bao nhiêu Sao?", "a": "9", "options": ["7", "8", "9", "10"]}
            ]
        },
        "2": {
            "title": "Bát Môn (8 Cửa)",
            "content": """
## Bài 2: Bát Môn - 8 Cửa

### Môn Cát (Tốt):
1. **Khai Môn** (開門) - Cửa Mở: Tốt cho mọi việc, đặc biệt khởi sự
2. **Hưu Môn** (休門) - Cửa Nghỉ: Tốt cho nghỉ ngơi, yên ổn
3. **Sinh Môn** (生門) - Cửa Sinh: Tốt cho cầu tài, sinh sản

### Môn Hung (Xấu):
4. **Thương Môn** (傷門) - Cửa Thương: Xấu, tranh chấp, tổn thương
5. **Đỗ Môn** (杜門) - Cửa Đỗ: Bế tắc, ẩn náu
6. **Cảnh Môn** (景門) - Cửa Cảnh: Hư ảo, không thực

### Môn Đại Hung:
7. **Tử Môn** (死門) - Cửa Tử: Cực xấu, bế tắc
8. **Kinh Môn** (驚門) - Cửa Kinh: Kinh sợ, bất an
""",
            "quiz": [
                {"q": "Môn nào tốt nhất cho việc cầu tài?", "a": "Sinh Môn", "options": ["Khai Môn", "Sinh Môn", "Hưu Môn", "Cảnh Môn"]},
                {"q": "Môn nào xấu nhất?", "a": "Tử Môn", "options": ["Thương Môn", "Đỗ Môn", "Tử Môn", "Kinh Môn"]}
            ]
        },
        "3": {
            "title": "Cửu Tinh (9 Sao)",
            "content": """
## Bài 3: Cửu Tinh - 9 Sao

### Sao Cát (Tốt):
1. **Thiên Tâm** (天心): Sao Y dược, chữa bệnh, giúp đỡ
2. **Thiên Phụ** (天輔): Sao Văn xương, học hành, thi cử
3. **Thiên Nhậm** (天任): Sao Tài lộc, cầu tài, kinh doanh
4. **Thiên Cầm** (天禽): Sao Trung tâm, ổn định

### Sao Hung (Xấu):
5. **Thiên Bồng** (天蓬): Sao Trộm cướp, bí mật, ngầm
6. **Thiên Nhuế** (天芮): Sao Bệnh tật, ốm đau
7. **Thiên Trụ** (天柱): Sao Phá hoại, tranh cãi
8. **Thiên Anh** (天英): Sao Hỏa tai, nóng nảy

### Sao Bình:
9. **Thiên Xung** (天沖): Sao Xung đột, đi xa
""",
            "quiz": [
                {"q": "Sao nào tốt cho việc chữa bệnh?", "a": "Thiên Tâm", "options": ["Thiên Phụ", "Thiên Tâm", "Thiên Nhậm", "Thiên Cầm"]},
                {"q": "Sao nào liên quan đến bệnh tật?", "a": "Thiên Nhuế", "options": ["Thiên Bồng", "Thiên Nhuế", "Thiên Trụ", "Thiên Anh"]}
            ]
        }
    },
    "intermediate": {
        "1": {
            "title": "Dụng Thần - Xác định mục tiêu",
            "content": """
## Dụng Thần trong QMDG

**Dụng Thần** là yếu tố đại diện cho mục tiêu bạn đang hỏi.

### Dụng Thần phổ biến:
| Chủ đề | Dụng Thần | Vị trí |
|--------|-----------|--------|
| Tiền bạc, tài chính | Sinh Môn | Cung có Sinh Môn |
| Công việc, sự nghiệp | Khai Môn | Cung có Khai Môn |
| Sức khỏe, bệnh tật | Thiên Tâm | Cung có Thiên Tâm |
| Tình cảm, hôn nhân | Lục Hợp | Cung có Lục Hợp |
| Di chuyển, xuất hành | Mã Tinh | Cung có Mã Tinh |

### Nguyên tắc:
1. Xác định Dụng Thần theo chủ đề
2. Tìm cung chứa Dụng Thần
3. Phân tích quan hệ với cung Bản Thân (Can Ngày)
""",
            "quiz": []
        }
    },
    "advanced": {
        "1": {
            "title": "Luận giải tổng hợp",
            "content": """
## Phương pháp luận giải tổng hợp

### Bước 1: Xác định Dụng Thần
- Dựa trên chủ đề câu hỏi

### Bước 2: Phân tích cung Dụng Thần
- Sao, Môn, Thần tại cung
- Can Thiên Bàn, Can Địa Bàn
- Không Vong, Dịch Mã

### Bước 3: Phân tích quan hệ
- Dụng Thần sinh/khắc Bản Thân?
- Có Không Vong không?
- Có Dịch Mã không?

### Bước 4: Kết luận
- Tổng hợp điểm tốt/xấu
- Tính xác suất
- Xác định thời gian
""",
            "quiz": []
        }
    }
}


class LearningAssistantAI:
    """
    Trợ lý học QMDG
    - Cung cấp bài học theo trình độ
    - Quiz kiểm tra kiến thức
    - Giải đáp thắc mắc
    """
    
    def __init__(self):
        self.lessons = LESSONS
        self.progress = {}
    
    def get_lesson(self, level, lesson_num):
        """Lấy nội dung bài học"""
        level_lessons = self.lessons.get(level, {})
        lesson = level_lessons.get(str(lesson_num))
        
        if lesson:
            return {
                "title": lesson["title"],
                "content": lesson["content"],
                "has_quiz": len(lesson.get("quiz", [])) > 0
            }
        return {"error": "Không tìm thấy bài học"}
    
    def get_quiz(self, level, lesson_num):
        """Lấy câu hỏi quiz"""
        level_lessons = self.lessons.get(level, {})
        lesson = level_lessons.get(str(lesson_num))
        
        if lesson and lesson.get("quiz"):
            return lesson["quiz"]
        return []
    
    def check_answer(self, level, lesson_num, question_index, answer):
        """Kiểm tra câu trả lời"""
        quiz = self.get_quiz(level, lesson_num)
        if question_index < len(quiz):
            correct = quiz[question_index]["a"]
            is_correct = answer.strip() == correct.strip()
            return {
                "correct": is_correct,
                "your_answer": answer,
                "correct_answer": correct,
                "message": "✅ Chính xác!" if is_correct else f"❌ Sai. Đáp án đúng: {correct}"
            }
        return {"error": "Không tìm thấy câu hỏi"}
    
    def get_curriculum(self):
        """Lấy chương trình học"""
        output = []
        output.append("## 📚 CHƯƠNG TRÌNH HỌC QMDG")
        output.append("")
        
        for level, lessons in self.lessons.items():
            level_name = {"basic": "Cơ bản", "intermediate": "Trung cấp", "advanced": "Nâng cao"}.get(level, level)
            output.append(f"### {level_name.upper()}")
            for num, lesson in lessons.items():
                output.append(f"- Bài {num}: {lesson['title']}")
            output.append("")
        
        return "\n".join(output)
    
    def explain_term(self, term):
        """Giải thích thuật ngữ"""
        terms = {
            "khai môn": "Cửa Mở - Tốt nhất trong Bát Môn, thích hợp cho mọi việc khởi sự",
            "sinh môn": "Cửa Sinh - Tốt cho cầu tài, sinh sản, phát triển",
            "hưu môn": "Cửa Nghỉ - Tốt cho nghỉ ngơi, yên ổn, hội họp",
            "tử môn": "Cửa Tử - Xấu nhất, không làm việc gì",
            "thiên tâm": "Sao Y dược - Tốt cho việc chữa bệnh, giúp đỡ người",
            "thiên phụ": "Sao Văn xương - Tốt cho học hành, thi cử",
            "dụng thần": "Yếu tố đại diện cho mục tiêu đang hỏi",
            "bản thân": "Đại diện cho người hỏi, thường là Can Ngày",
            "không vong": "Trạng thái trống rỗng, việc chưa thành hoặc không thực",
            "dịch mã": "Sao di chuyển, việc có biến động, di dời"
        }
        
        term_lower = term.lower()
        if term_lower in terms:
            return {"term": term, "explanation": terms[term_lower]}
        
        # Tìm gần đúng
        for t, exp in terms.items():
            if term_lower in t or t in term_lower:
                return {"term": t, "explanation": exp}
        
        return {"term": term, "explanation": "Không tìm thấy. Thử các thuật ngữ: " + ", ".join(list(terms.keys())[:5])}
    
    def get_study_plan(self, days=30):
        """Tạo kế hoạch học"""
        output = []
        output.append(f"## 📅 KẾ HOẠCH HỌC QMDG - {days} NGÀY")
        output.append("")
        
        # Basic: 10 days
        output.append("### Tuần 1-2: CƠ BẢN")
        output.append("- Ngày 1-3: Bài 1 - Giới thiệu QMDG")
        output.append("- Ngày 4-6: Bài 2 - Bát Môn")
        output.append("- Ngày 7-10: Bài 3 - Cửu Tinh")
        output.append("")
        
        # Intermediate: 10 days
        output.append("### Tuần 3-4: TRUNG CẤP")
        output.append("- Ngày 11-15: Dụng Thần")
        output.append("- Ngày 16-20: Bát Thần")
        output.append("")
        
        # Advanced: 10 days
        output.append("### Tuần 5-6: NÂNG CAO")
        output.append("- Ngày 21-25: Luận giải tổng hợp")
        output.append("- Ngày 26-30: Thực hành case study")
        
        return "\n".join(output)


# Singleton
_assistant = None

def get_learning_assistant():
    global _assistant
    if _assistant is None:
        _assistant = LearningAssistantAI()
    return _assistant


if __name__ == "__main__":
    assistant = get_learning_assistant()
    
    print(assistant.get_curriculum())
    print("\n" + "="*50 + "\n")
    
    lesson = assistant.get_lesson("basic", 1)
    print(lesson.get("content", ""))
