"""
AI Sửa Code (Code Fixer AI)
Tự động phát hiện và sửa lỗi trong code
"""

import ast
import re
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from gemini_dev_helper import GeminiDevHelper


class CodeFixerAI:
    """AI tự động sửa lỗi code"""
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        """
        Khởi tạo Code Fixer AI
        
        Args:
            gemini_api_key: API key cho Gemini AI
        """
        self.gemini_helper = GeminiDevHelper(gemini_api_key) if gemini_api_key else None
        self.fix_history = []
        
    def detect_errors(self, code: str, language: str = "python") -> List[Dict[str, Any]]:
        """
        Phát hiện lỗi trong code
        
        Args:
            code: Code cần kiểm tra
            language: Ngôn ngữ lập trình
            
        Returns:
            List các lỗi tìm thấy
        """
        print(f"🔍 Đang phát hiện lỗi...")
        errors = []
        
        if language == "python":
            # Syntax errors
            syntax_errors = self._check_python_syntax(code)
            errors.extend(syntax_errors)
            
            # Style errors
            style_errors = self._check_python_style(code)
            errors.extend(style_errors)
            
            # Logic errors (basic)
            logic_errors = self._check_python_logic(code)
            errors.extend(logic_errors)
        
        print(f"✅ Tìm thấy {len(errors)} lỗi!")
        return errors
    
    def auto_fix(self, code: str, errors: Optional[List[Dict[str, Any]]] = None, language: str = "python") -> Dict[str, Any]:
        """
        Tự động sửa lỗi
        
        Args:
            code: Code có lỗi
            errors: List lỗi (nếu đã detect)
            language: Ngôn ngữ lập trình
            
        Returns:
            Dict chứa code đã sửa và thông tin
        """
        print(f"🔧 Đang tự động sửa lỗi...")
        
        if errors is None:
            errors = self.detect_errors(code, language)
        
        if not errors:
            return {
                "fixed_code": code,
                "changes": [],
                "success": True,
                "message": "Không có lỗi cần sửa"
            }
        
        fixed_code = code
        changes = []
        
        # Try to fix each error
        for error in errors:
            if error['severity'] == 'critical':
                # Use AI for critical errors
                if self.gemini_helper:
                    fix_result = self.gemini_helper.fix_code(fixed_code, error['message'])
                    if fix_result.get('fixed_code'):
                        fixed_code = fix_result['fixed_code']
                        changes.append({
                            "error": error['message'],
                            "fix": fix_result.get('explanation', 'AI auto-fix'),
                            "type": "ai_fix"
                        })
                else:
                    # Basic fixes without AI
                    fixed_code, change = self._basic_fix(fixed_code, error)
                    if change:
                        changes.append(change)
            else:
                # Auto-fix for non-critical errors
                fixed_code, change = self._basic_fix(fixed_code, error)
                if change:
                    changes.append(change)
        
        result = {
            "fixed_code": fixed_code,
            "changes": changes,
            "success": len(changes) > 0,
            "original_errors": len(errors),
            "fixed_errors": len(changes)
        }
        
        self.fix_history.append(result)
        
        print(f"✅ Đã sửa {len(changes)}/{len(errors)} lỗi!")
        return result
    
    def refactor(self, code: str, goal: str = "improve readability") -> Dict[str, Any]:
        """
        Refactor code
        
        Args:
            code: Code cần refactor
            goal: Mục tiêu refactoring
            
        Returns:
            Dict chứa code đã refactor
        """
        print(f"♻️ Đang refactor code (goal: {goal})...")
        
        if self.gemini_helper:
            result = self.gemini_helper.refactor_code(code, goal)
        else:
            result = self._basic_refactor(code)
        
        print(f"✅ Refactoring hoàn tất!")
        return result
    
    def _check_python_syntax(self, code: str) -> List[Dict[str, Any]]:
        """Kiểm tra syntax Python"""
        errors = []
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append({
                "type": "syntax",
                "severity": "critical",
                "line": e.lineno,
                "message": str(e),
                "suggestion": "Fix syntax error"
            })
        
        return errors
    
    def _check_python_style(self, code: str) -> List[Dict[str, Any]]:
        """Kiểm tra style Python (PEP 8 cơ bản)"""
        errors = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Line too long
            if len(line) > 120:
                errors.append({
                    "type": "style",
                    "severity": "warning",
                    "line": i,
                    "message": f"Line too long ({len(line)} > 120)",
                    "suggestion": "Break line into multiple lines"
                })
            
            # Trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                errors.append({
                    "type": "style",
                    "severity": "info",
                    "line": i,
                    "message": "Trailing whitespace",
                    "suggestion": "Remove trailing whitespace"
                })
            
            # Multiple statements on one line
            if ';' in line and not line.strip().startswith('#'):
                errors.append({
                    "type": "style",
                    "severity": "warning",
                    "line": i,
                    "message": "Multiple statements on one line",
                    "suggestion": "Use separate lines"
                })
        
        return errors
    
    def _check_python_logic(self, code: str) -> List[Dict[str, Any]]:
        """Kiểm tra logic errors cơ bản"""
        errors = []
        
        # Check for common issues
        if "except:" in code or "except :" in code:
            errors.append({
                "type": "logic",
                "severity": "warning",
                "line": None,
                "message": "Bare except clause",
                "suggestion": "Specify exception type"
            })
        
        if re.search(r'==\s*True', code) or re.search(r'==\s*False', code):
            errors.append({
                "type": "logic",
                "severity": "info",
                "line": None,
                "message": "Comparison with True/False",
                "suggestion": "Use 'if variable:' instead"
            })
        
        # Check for potential division by zero
        if re.search(r'/\s*0\b', code):
            errors.append({
                "type": "logic",
                "severity": "warning",
                "line": None,
                "message": "Potential division by zero",
                "suggestion": "Add zero check"
            })
        
        return errors
    
    def _basic_fix(self, code: str, error: Dict[str, Any]) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Basic fixes không cần AI"""
        fixed_code = code
        change = None
        
        if error['type'] == 'style':
            if 'Trailing whitespace' in error['message']:
                # Remove trailing whitespace
                lines = fixed_code.split('\n')
                fixed_lines = [line.rstrip() for line in lines]
                fixed_code = '\n'.join(fixed_lines)
                change = {
                    "error": error['message'],
                    "fix": "Removed trailing whitespace",
                    "type": "auto_fix"
                }
            
            elif 'Line too long' in error['message']:
                # This is complex, skip for now
                pass
        
        elif error['type'] == 'logic':
            if 'Bare except clause' in error['message']:
                # Replace 'except:' with 'except Exception:'
                fixed_code = re.sub(r'\bexcept\s*:', 'except Exception:', fixed_code)
                change = {
                    "error": error['message'],
                    "fix": "Changed to 'except Exception:'",
                    "type": "auto_fix"
                }
            
            elif 'Comparison with True/False' in error['message']:
                # Replace '== True' with direct check
                fixed_code = re.sub(r'==\s*True\b', '', fixed_code)
                fixed_code = re.sub(r'==\s*False\b', ' is False', fixed_code)
                change = {
                    "error": error['message'],
                    "fix": "Simplified boolean comparison",
                    "type": "auto_fix"
                }
        
        return fixed_code, change
    
    def _basic_refactor(self, code: str) -> Dict[str, Any]:
        """Basic refactoring không cần AI"""
        refactored = code
        changes = []
        
        # Remove trailing whitespace
        lines = refactored.split('\n')
        refactored = '\n'.join(line.rstrip() for line in lines)
        changes.append("Removed trailing whitespace")
        
        # Normalize indentation
        # (This is complex, skip for now)
        
        return {
            "refactored_code": refactored,
            "changes_made": changes,
            "improvements": ["Code formatting improved"]
        }
    
    def fix_file(self, file_path: str) -> Dict[str, Any]:
        """
        Sửa lỗi trong file
        
        Args:
            file_path: Đường dẫn file
            
        Returns:
            Kết quả fix
        """
        print(f"📄 Đang sửa file: {file_path}...")
        
        path = Path(file_path)
        if not path.exists():
            return {"error": "File not found"}
        
        code = path.read_text(encoding='utf-8')
        language = path.suffix[1:]  # Remove dot
        
        result = self.auto_fix(code, language=language)
        
        if result['success']:
            # Backup original
            backup_path = path.with_suffix(path.suffix + '.bak')
            backup_path.write_text(code, encoding='utf-8')
            
            # Save fixed code
            path.write_text(result['fixed_code'], encoding='utf-8')
            
            print(f"✅ File đã được sửa! Backup: {backup_path}")
        
        return result


def demo_code_fixer():
    """Demo Code Fixer AI"""
    print("🚀 DEMO: CODE FIXER AI\n")
    
    fixer = CodeFixerAI()
    
    # Sample buggy code
    buggy_code = """
def calculate(a, b):
    result = a / 0    
    if result == True:
        print("Success")  ;  print("Done")
    except:
        pass
    return result   
"""
    
    print("Original code:")
    print(buggy_code)
    print()
    
    # Detect errors
    errors = fixer.detect_errors(buggy_code)
    print(f"Found {len(errors)} errors:")
    for err in errors:
        print(f"  - [{err['severity']}] {err['message']}")
    print()
    
    # Auto fix
    result = fixer.auto_fix(buggy_code, errors)
    print(f"Fixed code:")
    print(result['fixed_code'])
    print()
    
    print(f"Changes made:")
    for change in result['changes']:
        print(f"  - {change['fix']}")


if __name__ == "__main__":
    demo_code_fixer()
