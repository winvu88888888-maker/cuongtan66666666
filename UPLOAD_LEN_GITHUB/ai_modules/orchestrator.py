"""
Main Orchestrator - Điều phối tất cả AI modules
Tự động hóa toàn bộ quy trình phát triển
"""

import os
import json
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

# Import all AI modules
from secretary_ai import SecretaryAI
from gemini_dev_helper import GeminiDevHelper
from code_writer_ai import CodeWriterAI
from code_fixer_ai import CodeFixerAI
from memory_system import MemorySystem
from code_analyzer_ai import CodeAnalyzerAI
from tester_ai import TestingAI
from packager_ai import PackagerAI


class AIOrchestrator:
    """Điều phối tất cả AI modules"""
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        """
        Khởi tạo AI Orchestrator
        
        Args:
            gemini_api_key: Gemini API key
        """
        print("🚀 Khởi tạo AI Development System...")
        
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        
        # Initialize all modules
        self.secretary = SecretaryAI(self.gemini_api_key)
        self.code_writer = CodeWriterAI(self.gemini_api_key)
        self.code_fixer = CodeFixerAI(self.gemini_api_key)
        self.memory = MemorySystem()
        self.analyzer = CodeAnalyzerAI(self.gemini_api_key)
        self.tester = TestingAI(self.gemini_api_key)
        self.packager = PackagerAI()
        
        if self.gemini_api_key:
            self.gemini = GeminiDevHelper(self.gemini_api_key)
        else:
            self.gemini = None
            print("⚠️ Gemini API key not provided, some features will be limited")
        
        print("✅ AI Development System ready!")
    
    def process_request(self, user_request: str, auto_execute: bool = True) -> Dict[str, Any]:
        """
        Xử lý yêu cầu từ người dùng - quy trình hoàn chỉnh
        
        Args:
            user_request: Yêu cầu từ người dùng
            auto_execute: Tự động thực thi hay chờ xác nhận
            
        Returns:
            Kết quả xử lý
        """
        print("\n" + "="*80)
        print("🎯 BẮT ĐẦU XỬ LÝ YÊU CẦU")
        print("="*80)
        
        start_time = time.time()
        
        # PHASE 1: Phân tích yêu cầu
        print("\n📋 PHASE 1: PHÂN TÍCH YÊU CẦU")
        print("-" * 80)
        analysis = self.secretary.analyze_request(user_request)
        print(f"✅ Phân tích hoàn tất")
        print(f"   - Độ phức tạp: {analysis['estimated_complexity']}")
        print(f"   - Yêu cầu: {len(analysis['parsed_requirements'])} items")
        
        # PHASE 2: Tư vấn QMDG
        print("\n🔮 PHASE 2: TƯ VẤN KỲ MÔN ĐỘN GIÁP")
        print("-" * 80)
        qmdg_result = self.secretary.consult_qmdg(
            topic="Phát triển phần mềm",
            question=f"Thời điểm này có tốt để thực hiện: {user_request[:100]}?"
        )
        print(f"✅ Tư vấn QMDG hoàn tất")
        print(f"   - Thuận lợi: {'Có' if qmdg_result.get('analysis', {}).get('favorable') else 'Cần cân nhắc'}")
        
        # PHASE 3: Lập kế hoạch
        print("\n📝 PHASE 3: LẬP KẾ HOẠCH")
        print("-" * 80)
        plan = self.secretary.create_project_plan(analysis, qmdg_result)
        self.secretary.print_plan_summary(plan)
        
        # Save plan to memory
        plan_id = self.memory.store_project_plan(plan['project_name'], plan)
        print(f"✅ Kế hoạch đã lưu vào memory (ID: {plan_id})")
        
        if not auto_execute:
            print("\n⏸️ Dừng để xem xét kế hoạch. Set auto_execute=True để tiếp tục.")
            return {
                "status": "planned",
                "plan": plan,
                "plan_id": plan_id
            }
        
        # PHASE 4: Thực thi kế hoạch
        print("\n⚙️ PHASE 4: THỰC THI KẾ HOẠCH")
        print("-" * 80)
        execution_result = self._execute_plan(plan)
        
        # PHASE 5: Kiểm tra và sửa lỗi
        print("\n🔍 PHASE 5: KIỂM TRA VÀ SỬA LỖI")
        print("-" * 80)
        analysis_result = self.analyzer.analyze_project(execution_result['project_dir'])
        fix_result = self._check_and_fix(execution_result)
        
        # PHASE 6: Kiểm thử thực tế
        print("\n🧪 PHASE 6: KIỂM THỬ THỰC TẾ")
        print("-" * 80)
        test_results = self.tester.run_tests(execution_result['project_dir'])
        
        # PHASE 7: Đóng gói & Báo cáo
        print("\n📦 PHASE 7: ĐÓNG GÓI & BÁO CÁO")
        print("-" * 80)
        zip_path = self.packager.package_project(execution_result['project_dir'], plan['project_name'])
        report_path = self.packager.generate_final_report(analysis_result, test_results, qmdg_result)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        final_result = {
            "status": "completed",
            "plan": plan,
            "plan_id": plan_id,
            "execution": execution_result,
            "fixes": fix_result,
            "analysis": analysis_result,
            "tests": test_results,
            "package": zip_path,
            "report": report_path,
            "total_time": total_time,
            "timestamp": datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()
        }
        
        # Log to memory
        self.memory.log_execution(
            workflow_name="full_development_cycle",
            input_data={"request": user_request},
            output_data=final_result,
            status="success",
            execution_time=int(total_time * 1000)
        )
        
        print("\n" + "="*80)
        print("✅ HOÀN TẤT!")
        print("="*80)
        print(f"⏱️ Tổng thời gian: {total_time:.2f}s")
        print(f"📁 Files tạo: {len(execution_result.get('created_files', []))}")
        print(f"🔧 Lỗi đã sửa: {fix_result.get('total_fixes', 0)}")
        
        return final_result
    
    def _execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Thực thi kế hoạch"""
        created_files = []
        errors = []
        
        project_name = plan['project_name']
        output_dir = Path(f"generated_projects/{project_name}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Tạo dự án tại: {output_dir}")
        
        # Tạo các files cơ bản
        basic_files = [
            {
                "name": "main",
                "description": "Main entry point",
                "language": "python",
                "requirements": ["Initialize application", "Handle command line args"]
            },
            {
                "name": "config",
                "description": "Configuration module",
                "language": "python",
                "requirements": ["Load config from file", "Environment variables support"]
            },
            {
                "name": "utils",
                "description": "Utility functions",
                "language": "python",
                "requirements": ["Common helper functions", "Error handling"]
            }
        ]
        
        for file_spec in basic_files:
            try:
                print(f"   ✍️ Tạo {file_spec['name']}.py...")
                result = self.code_writer.write_code_from_spec(file_spec)
                
                # Save to file
                file_path = output_dir / f"{file_spec['name']}.py"
                file_path.write_text(result['code'], encoding='utf-8')
                created_files.append(str(file_path))
                
                # Store in memory
                self.memory.store_code(
                    project_name=project_name,
                    file_path=str(file_path),
                    code_content=result['code'],
                    language=file_spec['language']
                )
                
                print(f"   ✅ {file_spec['name']}.py created")
                
            except Exception as e:
                error_msg = f"Error creating {file_spec['name']}.py: {str(e)}"
                errors.append(error_msg)
                print(f"   ❌ {error_msg}")
        
        # Tạo README
        readme_content = f"""# {project_name}

{plan.get('description', 'Generated project')}

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Project Structure

{chr(10).join(f"- `{Path(f).name}`" for f in created_files)}

## Generated by

AI Development System - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        readme_path = output_dir / "README.md"
        readme_path.write_text(readme_content, encoding='utf-8')
        created_files.append(str(readme_path))
        
        # Tạo requirements.txt
        requirements_content = """# Project dependencies
# Add your dependencies here
"""
        req_path = output_dir / "requirements.txt"
        req_path.write_text(requirements_content, encoding='utf-8')
        created_files.append(str(req_path))
        
        return {
            "created_files": created_files,
            "errors": errors,
            "project_dir": str(output_dir)
        }
    
    def _check_and_fix(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Kiểm tra và sửa lỗi"""
        all_fixes = []
        total_errors = 0
        total_fixes = 0
        
        for file_path in execution_result.get('created_files', []):
            if not file_path.endswith('.py'):
                continue
            
            try:
                print(f"   🔍 Kiểm tra {Path(file_path).name}...")
                
                code = Path(file_path).read_text(encoding='utf-8')
                errors = self.code_fixer.detect_errors(code)
                
                if errors:
                    total_errors += len(errors)
                    print(f"   ⚠️ Tìm thấy {len(errors)} lỗi")
                    
                    # Auto fix
                    fix_result = self.code_fixer.auto_fix(code, errors)
                    
                    if fix_result['success']:
                        # Save fixed code
                        Path(file_path).write_text(fix_result['fixed_code'], encoding='utf-8')
                        total_fixes += fix_result['fixed_errors']
                        all_fixes.append({
                            "file": file_path,
                            "fixes": fix_result['changes']
                        })
                        print(f"   ✅ Đã sửa {fix_result['fixed_errors']} lỗi")
                else:
                    print(f"   ✅ Không có lỗi")
                    
            except Exception as e:
                print(f"   ❌ Lỗi khi kiểm tra: {str(e)}")
        
        return {
            "total_errors": total_errors,
            "total_fixes": total_fixes,
            "fixes": all_fixes
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê hệ thống"""
        return self.memory.get_statistics()
    
    def close(self):
        """Đóng tất cả connections"""
        self.memory.close()


def main():
    """Main function - Demo tự động"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🤖 AI DEVELOPMENT SYSTEM - AUTOMATIC MODE 🤖         ║
║                                                              ║
║  Hệ thống AI tự động phát triển phần mềm                    ║
║  Tích hợp: n8n + Gemini AI + Kỳ Môn Độn Giáp               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Khởi tạo orchestrator
    orchestrator = AIOrchestrator()
    
    # Yêu cầu mẫu
    user_request = """
    Tạo một ứng dụng Python đơn giản để quản lý tasks.
    Cần có các chức năng: thêm task, xóa task, đánh dấu hoàn thành, hiển thị danh sách.
    """
    
    print(f"\n📝 YÊU CẦU: {user_request.strip()}\n")
    
    # Xử lý tự động
    result = orchestrator.process_request(user_request, auto_execute=True)
    
    # Hiển thị kết quả
    print("\n📊 KẾT QUẢ CUỐI CÙNG:")
    print(f"   - Status: {result['status']}")
    print(f"   - Project: {result['plan']['project_name']}")
    print(f"   - Files: {len(result['execution']['created_files'])}")
    print(f"   - Time: {result['total_time']:.2f}s")
    
    # Thống kê
    print("\n📈 THỐNG KÊ HỆ THỐNG:")
    stats = orchestrator.get_statistics()
    print(json.dumps(stats, indent=2))
    
    orchestrator.close()


if __name__ == "__main__":
    main()
