# -*- coding: utf-8 -*-
import subprocess
import os
import requests
from pathlib import Path

class TestingAI:
    def __init__(self, gemini_helper):
        self.gemini = gemini_helper

    def generate_tests(self, code, file_name):
        """Tạo test cases tự động"""
        prompt = f"""
        Dựa trên đoạn code sau, hãy viết một file test sử dụng thư viện pytest.
        Chỉ trả về code Python, không giải thích.
        File cần test: {file_name}
        Code:
        {code}
        """
        test_code = self.gemini.generate_content(prompt)
        # Làm sạch code từ markdown nếu có
        test_code = test_code.replace("```python", "").replace("```", "").strip()
        return test_code

    def run_tests(self, project_path):
        """Chạy pytest và trả về kết quả"""
        try:
            result = subprocess.run(
                ["pytest", project_path, "--json-report"], 
                capture_output=True, 
                text=True
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def save_test_file(self, project_path, file_name, content):
        test_file_path = os.path.join(project_path, f"test_{file_name}")
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return test_file_path

    def fetch_real_world_examples(self, topic):
        """Sử dụng Gemini để tìm kiếm/mô phỏng ví dụ thực tế từ internet"""
        prompt = f"Hãy cung cấp 3 ví dụ thực tế về đầu vào (input) và đầu ra (output) cho chủ đề: {topic}. Trả về duy nhất JSON list [{{'input': '...', 'output': '...'}}]."
        try:
            response = self.gemini.generate_content(prompt)
            clean_json = response.replace("```json", "").replace("```", "").strip()
            return clean_json
        except:
            return "[]"

    def download_external_examples(self, query, download_path):
        """Tải ví dụ code thực tế từ GitHub để làm mẫu kiểm thử"""
        print(f"🌐 Đang tìm kiếm ví dụ thực tế cho: {query}...")
        search_url = f"https://api.github.com/search/repositories?q={query}+language:python"
        try:
            response = requests.get(search_url)
            if response.status_code == 200:
                items = response.json().get('items', [])
                if items:
                    repo_url = items[0].get('html_url')
                    print(f"✅ Tìm thấy repo mẫu: {repo_url}")
                    # Logic clone repo hoặc tải file cụ thể có thể thêm ở đây
                    return repo_url
            return None
        except Exception as e:
            print(f"❌ Lỗi khi tải ví dụ: {e}")
            return None