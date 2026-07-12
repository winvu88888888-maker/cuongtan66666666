# -*- coding: utf-8 -*-
import ast
import os

class CodeAnalyzerAI:
    def __init__(self, gemini_helper=None):
        self.gemini = gemini_helper

    def analyze_project(self, project_path):
        """Phân tích toàn bộ project"""
        results = {
            "structure": self._analyze_structure(project_path),
            "metrics": {"total_lines": 0, "functions": 0, "classes": 0},
            "security_issues": [],
            "quality_score": 0
        }
        
        for root, _, files in os.walk(project_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    file_analysis = self._analyze_file(file_path)
                    results["metrics"]["total_lines"] += file_analysis["lines"]
                    results["metrics"]["functions"] += file_analysis["functions"]
                    results["metrics"]["classes"] += file_analysis["classes"]
        
        return results

    def _analyze_structure(self, path):
        structure = []
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 4 * level
            structure.append(f"{indent}{os.path.basename(root)}/")
            for f in files:
                structure.append(f"{indent}    {f}")
        return "\n".join(structure)

    def _analyze_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
            functions = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
            classes = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
            return {
                "lines": len(content.splitlines()),
                "functions": functions,
                "classes": classes
            }
        except:
            return {"lines": 0, "functions": 0, "classes": 0}

    def get_ai_review(self, code):
        """Sử dụng Gemini để review sâu"""
        if not self.gemini:
            return "Gemini helper not configured."
        
        prompt = f"""
        Hãy phân tích đoạn code sau về:
        1. Lỗ hổng bảo mật.
        2. Hiệu năng (Performance).
        3. Khả năng bảo trì (Maintainability).
        Code:
        {code}
        """
        return self.gemini.generate_content(prompt)