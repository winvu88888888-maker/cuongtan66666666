"""
AI Viết Code (Code Writer AI)
Tự động tạo code từ yêu cầu, sử dụng templates và Gemini AI
"""

import os
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
from gemini_dev_helper import GeminiDevHelper


class CodeWriterAI:
    """AI tự động viết code"""
    
    def __init__(self, gemini_api_key: Optional[str] = None, templates_dir: str = "code_templates"):
        """
        Khởi tạo Code Writer AI
        
        Args:
            gemini_api_key: API key cho Gemini AI
            templates_dir: Thư mục chứa code templates
        """
        self.gemini_helper = GeminiDevHelper(gemini_api_key) if gemini_api_key else None
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(exist_ok=True)
        self.generated_files = []
        
    def write_code_from_spec(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Viết code từ specification
        
        Args:
            spec: Specification chứa:
                - name: Tên file/module
                - description: Mô tả chức năng
                - language: Ngôn ngữ lập trình
                - requirements: Yêu cầu chi tiết
                - template: Template sử dụng (optional)
                
        Returns:
            Dict chứa code và metadata
        """
        print(f"✍️ Đang viết code cho: {spec.get('name', 'unnamed')}...")
        
        # Check if template exists
        if spec.get('template'):
            code = self._use_template(spec['template'], spec)
        elif self.gemini_helper:
            code = self._generate_with_ai(spec)
        else:
            code = self._generate_basic(spec)
        
        result = {
            "name": spec.get('name', 'generated_code'),
            "language": spec.get('language', 'python'),
            "code": code,
            "description": spec.get('description', ''),
            "validation": self._validate_code(code, spec.get('language', 'python'))
        }
        
        print(f"✅ Code đã được tạo!")
        return result
    
    def write_module(self, module_spec: Dict[str, Any], output_dir: str = ".") -> List[str]:
        """
        Viết toàn bộ module với nhiều files
        
        Args:
            module_spec: Specification cho module
            output_dir: Thư mục output
            
        Returns:
            List các files đã tạo
        """
        print(f"📦 Đang tạo module: {module_spec.get('name', 'unnamed_module')}...")
        
        output_path = Path(output_dir) / module_spec.get('name', 'module')
        output_path.mkdir(parents=True, exist_ok=True)
        
        created_files = []
        
        # Create __init__.py
        init_file = output_path / "__init__.py"
        init_content = self._generate_init_file(module_spec)
        init_file.write_text(init_content, encoding='utf-8')
        created_files.append(str(init_file))
        
        # Create each component file
        for component in module_spec.get('components', []):
            file_spec = {
                "name": component['name'],
                "description": component.get('description', ''),
                "language": module_spec.get('language', 'python'),
                "requirements": component.get('requirements', [])
            }
            
            result = self.write_code_from_spec(file_spec)
            
            # Save to file
            file_path = output_path / f"{component['name']}.py"
            file_path.write_text(result['code'], encoding='utf-8')
            created_files.append(str(file_path))
        
        # Create README
        readme_file = output_path / "README.md"
        readme_content = self._generate_readme(module_spec)
        readme_file.write_text(readme_content, encoding='utf-8')
        created_files.append(str(readme_file))
        
        self.generated_files.extend(created_files)
        
        print(f"✅ Module đã được tạo với {len(created_files)} files!")
        return created_files
    
    def _use_template(self, template_name: str, spec: Dict[str, Any]) -> str:
        """Sử dụng template có sẵn"""
        template_file = self.templates_dir / f"{template_name}.template"
        
        if not template_file.exists():
            print(f"⚠️ Template {template_name} không tồn tại, dùng AI generation")
            return self._generate_with_ai(spec)
        
        template = template_file.read_text(encoding='utf-8')
        
        # Replace placeholders
        code = template.format(
            name=spec.get('name', 'Module'),
            description=spec.get('description', ''),
            **spec.get('variables', {})
        )
        
        return code
    
    def _generate_with_ai(self, spec: Dict[str, Any]) -> str:
        """Generate code sử dụng Gemini AI"""
        if not self.gemini_helper:
            return self._generate_basic(spec)
        
        prompt = f"""
Tạo {spec.get('language', 'Python')} code cho:

Tên: {spec.get('name', 'unnamed')}
Mô tả: {spec.get('description', '')}

Yêu cầu:
{chr(10).join('- ' + req for req in spec.get('requirements', []))}

Code phải:
- Clean và readable
- Có docstrings đầy đủ
- Handle errors properly
- Follow best practices
"""
        
        code = self.gemini_helper.generate_code(prompt, spec.get('language', 'python'))
        return code
    
    def _generate_basic(self, spec: Dict[str, Any]) -> str:
        """Generate code cơ bản không dùng AI"""
        language = spec.get('language', 'python')
        
        if language == 'python':
            return f'''"""
{spec.get('description', 'Generated module')}
"""

class {spec.get('name', 'GeneratedClass')}:
    """Main class for {spec.get('name', 'module')}"""
    
    def __init__(self):
        """Initialize {spec.get('name', 'module')}"""
        pass
    
    def run(self):
        """Main execution method"""
        # TODO: Implement functionality
        pass


if __name__ == "__main__":
    obj = {spec.get('name', 'GeneratedClass')}()
    obj.run()
'''
        else:
            return f"// Generated code for {spec.get('name', 'module')}\n// TODO: Implement"
    
    def _validate_code(self, code: str, language: str) -> Dict[str, Any]:
        """Validate code"""
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        if language == 'python':
            # Basic Python validation
            try:
                compile(code, '<string>', 'exec')
            except SyntaxError as e:
                validation['valid'] = False
                validation['errors'].append(f"Syntax error: {str(e)}")
            
            # Check for basic quality
            if 'def ' not in code and 'class ' not in code:
                validation['warnings'].append("No functions or classes defined")
            
            if '"""' not in code and "'''" not in code:
                validation['warnings'].append("Missing docstrings")
        
        return validation
    
    def _generate_init_file(self, module_spec: Dict[str, Any]) -> str:
        """Generate __init__.py"""
        components = module_spec.get('components', [])
        imports = [f"from .{comp['name']} import *" for comp in components]
        
        return f'''"""
{module_spec.get('description', 'Generated module')}
"""

{chr(10).join(imports)}

__version__ = "{module_spec.get('version', '1.0.0')}"
__all__ = {[comp['name'] for comp in components]}
'''
    
    def _generate_readme(self, module_spec: Dict[str, Any]) -> str:
        """Generate README.md"""
        return f'''# {module_spec.get('name', 'Module')}

{module_spec.get('description', 'Generated module')}

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from {module_spec.get('name', 'module')} import *

# TODO: Add usage examples
```

## Components

{chr(10).join(f"- **{comp['name']}**: {comp.get('description', '')}" for comp in module_spec.get('components', []))}

## License

MIT
'''
    
    def create_template(self, name: str, content: str):
        """Tạo template mới"""
        template_file = self.templates_dir / f"{name}.template"
        template_file.write_text(content, encoding='utf-8')
        print(f"✅ Template {name} đã được tạo!")
    
    def list_templates(self) -> List[str]:
        """List tất cả templates"""
        return [f.stem for f in self.templates_dir.glob("*.template")]
    
    def save_code_to_file(self, code_result: Dict[str, Any], output_path: str) -> str:
        """Lưu code ra file"""
        file_path = Path(output_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_path.write_text(code_result['code'], encoding='utf-8')
        self.generated_files.append(str(file_path))
        
        print(f"✅ Đã lưu code vào {file_path}")
        return str(file_path)


def demo_code_writer():
    """Demo Code Writer AI"""
    print("🚀 DEMO: CODE WRITER AI\n")
    
    # Khởi tạo (không cần Gemini API cho demo)
    writer = CodeWriterAI()
    
    # Demo 1: Viết single file
    print("1️⃣ Viết single file...")
    spec = {
        "name": "calculator",
        "description": "Simple calculator module",
        "language": "python",
        "requirements": [
            "Support basic operations: +, -, *, /",
            "Handle division by zero",
            "Return float results"
        ]
    }
    
    result = writer.write_code_from_spec(spec)
    print(f"Code:\n{result['code']}\n")
    print(f"Validation: {result['validation']}\n")
    
    # Demo 2: Viết module
    print("2️⃣ Viết module...")
    module_spec = {
        "name": "math_utils",
        "description": "Mathematical utilities module",
        "version": "1.0.0",
        "language": "python",
        "components": [
            {
                "name": "basic_ops",
                "description": "Basic mathematical operations",
                "requirements": ["Add, subtract, multiply, divide"]
            },
            {
                "name": "advanced_ops",
                "description": "Advanced mathematical operations",
                "requirements": ["Power, square root, logarithm"]
            }
        ]
    }
    
    files = writer.write_module(module_spec, output_dir="generated_modules")
    print(f"Created files:")
    for f in files:
        print(f"  - {f}")


if __name__ == "__main__":
    demo_code_writer()
