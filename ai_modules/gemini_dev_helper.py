"""
Gemini AI Development Helper
Hỗ trợ phát triển code với Gemini AI
"""

import google.generativeai as genai
from typing import Optional, Dict, List, Any
import json


class GeminiDevHelper:
    """Helper class để sử dụng Gemini AI cho phát triển phần mềm"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """
        Khởi tạo Gemini Dev Helper
        
        Args:
            api_key: Gemini API key
            model_name: Tên model Gemini
        """
        genai.configure(api_key=api_key)
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        ]
        self.model = genai.GenerativeModel(model_name, safety_settings=safety_settings)
        self.chat_history = []
        
    def generate_code(self, prompt: str, language: str = "python") -> str:
        """
        Tạo code từ mô tả bằng ngôn ngữ tự nhiên
        
        Args:
            prompt: Mô tả chức năng cần tạo
            language: Ngôn ngữ lập trình
            
        Returns:
            Code được generate
        """
        full_prompt = f"""
Bạn là một lập trình viên chuyên nghiệp. Hãy viết code {language} cho yêu cầu sau:

{prompt}

Yêu cầu:
- Code phải clean, readable, và follow best practices
- Thêm docstrings và comments đầy đủ
- Xử lý errors và edge cases
- Chỉ trả về code, không giải thích thêm

Code:
"""
        
        try:
            response = self.model.generate_content(full_prompt)
            code = response.text
            
            # Clean up code (remove markdown code blocks if present)
            if "```" in code:
                code = code.split("```")[1]
                if code.startswith(language):
                    code = code[len(language):].strip()
            
            return code.strip()
            
        except Exception as e:
            return f"# Error generating code: {str(e)}"
    
    def fix_code(self, code: str, error_message: str) -> Dict[str, Any]:
        """
        Sửa lỗi trong code
        
        Args:
            code: Code có lỗi
            error_message: Thông báo lỗi
            
        Returns:
            Dict chứa code đã sửa và giải thích
        """
        prompt = f"""
Bạn là một debugging expert. Code sau đây có lỗi:

```python
{code}
```

Lỗi:
{error_message}

Hãy:
1. Tìm nguyên nhân lỗi
2. Sửa code
3. Giải thích ngắn gọn

Trả về JSON format:
{{
    "fixed_code": "...",
    "explanation": "...",
    "root_cause": "..."
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text
            
            # Try to parse JSON
            if "```json" in result_text:
                json_str = result_text.split("```json")[1].split("```")[0].strip()
                result = json.loads(json_str)
            elif "```" in result_text:
                json_str = result_text.split("```")[1].strip()
                result = json.loads(json_str)
            else:
                result = json.loads(result_text)
            
            return result
            
        except Exception as e:
            return {
                "fixed_code": code,
                "explanation": f"Không thể tự động sửa: {str(e)}",
                "root_cause": "Unknown"
            }
    
    def explain_code(self, code: str) -> str:
        """
        Giải thích code
        
        Args:
            code: Code cần giải thích
            
        Returns:
            Giải thích chi tiết
        """
        prompt = f"""
Hãy giải thích code sau một cách chi tiết, dễ hiểu:

```python
{code}
```

Giải thích:
- Mục đích của code
- Cách hoạt động từng phần
- Input/Output
- Các edge cases được xử lý
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Không thể giải thích code: {str(e)}"
    
    def review_code(self, code: str) -> Dict[str, Any]:
        """
        Review code và đưa ra feedback
        
        Args:
            code: Code cần review
            
        Returns:
            Dict chứa feedback chi tiết
        """
        prompt = f"""
Bạn là một senior code reviewer. Hãy review code sau:

```python
{code}
```

Đánh giá theo các tiêu chí:
1. Code quality (1-10)
2. Readability (1-10)
3. Performance (1-10)
4. Security (1-10)
5. Best practices compliance

Trả về JSON format:
{{
    "overall_score": 0,
    "code_quality": 0,
    "readability": 0,
    "performance": 0,
    "security": 0,
    "strengths": ["..."],
    "weaknesses": ["..."],
    "suggestions": ["..."]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text
            
            # Parse JSON
            if "```json" in result_text:
                json_str = result_text.split("```json")[1].split("```")[0].strip()
                result = json.loads(json_str)
            elif "```" in result_text:
                json_str = result_text.split("```")[1].strip()
                result = json.loads(json_str)
            else:
                result = json.loads(result_text)
            
            return result
            
        except Exception as e:
            return {
                "overall_score": 0,
                "error": str(e)
            }
    
    def generate_tests(self, code: str, framework: str = "pytest") -> str:
        """
        Tạo test cases cho code
        
        Args:
            code: Code cần test
            framework: Test framework (pytest, unittest, etc.)
            
        Returns:
            Test code
        """
        prompt = f"""
Hãy viết test cases cho code sau sử dụng {framework}:

```python
{code}
```

Yêu cầu:
- Test coverage cao
- Test cả happy path và edge cases
- Test error handling
- Clear test names
- Chỉ trả về test code

Test code:
"""
        
        try:
            response = self.model.generate_content(prompt)
            test_code = response.text
            
            # Clean up
            if "```" in test_code:
                test_code = test_code.split("```")[1]
                if test_code.startswith("python"):
                    test_code = test_code[6:].strip()
            
            return test_code.strip()
            
        except Exception as e:
            return f"# Error generating tests: {str(e)}"
    
    def generate_documentation(self, code: str, doc_type: str = "docstring") -> str:
        """
        Tạo documentation cho code
        
        Args:
            code: Code cần document
            doc_type: Loại documentation (docstring, markdown, etc.)
            
        Returns:
            Documentation
        """
        prompt = f"""
Hãy tạo {doc_type} documentation cho code sau:

```python
{code}
```

Yêu cầu:
- Đầy đủ và chi tiết
- Dễ hiểu
- Include examples nếu có thể
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"# Error generating documentation: {str(e)}"
    
    def refactor_code(self, code: str, goal: str = "improve readability") -> Dict[str, Any]:
        """
        Refactor code
        
        Args:
            code: Code cần refactor
            goal: Mục tiêu refactoring
            
        Returns:
            Dict chứa code đã refactor và giải thích
        """
        prompt = f"""
Hãy refactor code sau với mục tiêu: {goal}

```python
{code}
```

Trả về JSON format:
{{
    "refactored_code": "...",
    "changes_made": ["..."],
    "improvements": ["..."]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text
            
            # Parse JSON
            if "```json" in result_text:
                json_str = result_text.split("```json")[1].split("```")[0].strip()
                result = json.loads(json_str)
            elif "```" in result_text:
                json_str = result_text.split("```")[1].strip()
                result = json.loads(json_str)
            else:
                result = json.loads(result_text)
            
            return result
            
        except Exception as e:
            return {
                "refactored_code": code,
                "error": str(e)
            }
    
    def optimize_performance(self, code: str) -> Dict[str, Any]:
        """
        Tối ưu performance của code
        
        Args:
            code: Code cần tối ưu
            
        Returns:
            Dict chứa code đã tối ưu và metrics
        """
        prompt = f"""
Hãy tối ưu performance cho code sau:

```python
{code}
```

Trả về JSON format:
{{
    "optimized_code": "...",
    "optimizations": ["..."],
    "estimated_improvement": "..."
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text
            
            # Parse JSON
            if "```json" in result_text:
                json_str = result_text.split("```json")[1].split("```")[0].strip()
                result = json.loads(json_str)
            elif "```" in result_text:
                json_str = result_text.split("```")[1].strip()
                result = json.loads(json_str)
            else:
                result = json.loads(result_text)
            
            return result
            
        except Exception as e:
            return {
                "optimized_code": code,
                "error": str(e)
            }
    
    def chat(self, message: str) -> str:
        """
        Chat với AI về code
        
        Args:
            message: Tin nhắn
            
        Returns:
            Phản hồi từ AI
        """
        try:
            # Maintain chat history
            if not hasattr(self, 'chat_session'):
                self.chat_session = self.model.start_chat(history=[])
            
            response = self.chat_session.send_message(message)
            return response.text
            
        except Exception as e:
            return f"Error: {str(e)}"


def demo_gemini_dev_helper():
    """Demo Gemini Dev Helper"""
    import os
    
    # Get API key from environment or config
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ Cần set GEMINI_API_KEY environment variable")
        return
    
    print("🤖 DEMO: GEMINI DEV HELPER\n")
    
    helper = GeminiDevHelper(api_key)
    
    # Demo 1: Generate code
    print("1️⃣ Generating code...")
    code = helper.generate_code(
        "Tạo function để tính số Fibonacci thứ n",
        language="python"
    )
    print(f"Generated code:\n{code}\n")
    
    # Demo 2: Review code
    print("2️⃣ Reviewing code...")
    review = helper.review_code(code)
    print(f"Review: {json.dumps(review, indent=2, ensure_ascii=False)}\n")
    
    # Demo 3: Generate tests
    print("3️⃣ Generating tests...")
    tests = helper.generate_tests(code)
    print(f"Test code:\n{tests}\n")


if __name__ == "__main__":
    demo_gemini_dev_helper()
