"""
AI Thư Ký Thông Minh (Smart Secretary AI)
Phân tích yêu cầu, tư vấn Kỳ Môn Độn Giáp, và lập kế hoạch phát triển
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from zoneinfo import ZoneInfo
try:
    from super_detailed_analysis import phan_tich_sieu_chi_tiet_chu_de
    from qmdg_calc import calculate_qmdg_params
except ImportError:
    pass

class SecretaryAI:
    """AI Thư Ký thông minh để quản lý dự án"""
    
    def __init__(self, gemini_api_key: Optional[str] = None, qmdg_api_url: str = "http://localhost:5000"):
        """
        Khởi tạo AI Secretary
        
        Args:
            gemini_api_key: API key cho Gemini AI
            qmdg_api_url: URL của QMDG API
        """
        self.gemini_api_key = gemini_api_key
        self.qmdg_api_url = qmdg_api_url
        self.project_history = []
        
    def analyze_request(self, user_request: str) -> Dict[str, Any]:
        """
        Phân tích yêu cầu của người dùng
        
        Args:
            user_request: Yêu cầu từ người dùng
            
        Returns:
            Dict chứa phân tích chi tiết
        """
        print(f"🤖 AI Thư Ký: Đang phân tích yêu cầu...")
        
        analysis = {
            "original_request": user_request,
            "timestamp": datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat(),
            "parsed_requirements": self._parse_requirements(user_request),
            "estimated_complexity": self._estimate_complexity(user_request),
            "suggested_approach": self._suggest_approach(user_request),
            "required_resources": self._identify_resources(user_request)
        }
        
        print(f"✅ Phân tích hoàn tất!")
        return analysis
    
    def consult_qmdg(self, topic: str, question: str, dt_obj: datetime = None) -> Dict[str, Any]:
        """
        Tư vấn Kỳ Môn Độn Giáp thực tế để tìm đường đi đúng
        """
        print(f"🔮 Đang tư vấn Kỳ Môn Độn Giáp...")
        if dt_obj is None:
            dt_obj = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))

        try:
            # Giả định các thông số cung được tính toán từ qmdg_calc
            params = calculate_qmdg_params(dt_obj)
            # Lấy thông tin cung Chủ (Cung mệnh/người hỏi) và Khách (Dụng thần công việc)
            # Ở đây giả định lấy cung 1 và cung 9 để phân tích mẫu
            chu = {"so": 1, "ten": "Khảm", "hanh": "Thủy", "sao": "Thiên Tâm", "cua": "Khai", "than": "Trực Phù", "can_thien": "Mậu", "can_dia": "Ất"}
            khach = {"so": 9, "ten": "Ly", "hanh": "Hỏa", "sao": "Thiên Anh", "cua": "Cảnh", "than": "Cửu Thiên", "can_thien": "Bính", "can_dia": "Canh"}
            
            analysis_result = phan_tich_sieu_chi_tiet_chu_de(topic, chu, khach, dt_obj)
            
            qmdg_result = {
                "datetime": dt_obj.isoformat(),
                "topic": topic,
                "analysis": analysis_result,
                "favorable": analysis_result['tong_hop']['diem'] > 50,
                "path_advice": analysis_result['tong_hop']['loi_khuyen']
            }
            
            print(f"✅ Tư vấn QMDG hoàn tất!")
            return qmdg_result
            
        except Exception as e:
            print(f"⚠️ Lỗi khi tư vấn QMDG: {e}")
            return {
                "error": str(e),
                "fallback_recommendation": "Tiếp tục với kế hoạch ban đầu"
            }
    
    def create_project_plan(self, analysis: Dict[str, Any], qmdg_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tạo kế hoạch dự án chi tiết
        
        Args:
            analysis: Kết quả phân tích yêu cầu
            qmdg_result: Kết quả tư vấn QMDG
            
        Returns:
            Kế hoạch dự án chi tiết
        """
        print(f"📋 Đang lập kế hoạch dự án...")
        
        plan = {
            "project_name": self._generate_project_name(analysis),
            "created_at": datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat(),
            "complexity": analysis["estimated_complexity"],
            "qmdg_favorable": qmdg_result.get("analysis", {}).get("favorable", True),
            
            "phases": [
                {
                    "name": "Phase 1: Chuẩn bị",
                    "duration": "1-2 ngày",
                    "tasks": [
                        "Setup môi trường phát triển",
                        "Cài đặt dependencies",
                        "Tạo cấu trúc dự án"
                    ]
                },
                {
                    "name": "Phase 2: Phát triển Core",
                    "duration": "3-5 ngày",
                    "tasks": [
                        "Implement core features",
                        "Tạo API endpoints",
                        "Database setup"
                    ]
                },
                {
                    "name": "Phase 3: Testing",
                    "duration": "2-3 ngày",
                    "tasks": [
                        "Unit testing",
                        "Integration testing",
                        "Bug fixing"
                    ]
                },
                {
                    "name": "Phase 4: Deployment",
                    "duration": "1 ngày",
                    "tasks": [
                        "Build production",
                        "Deploy to server",
                        "Monitoring setup"
                    ]
                }
            ],
            
            "resources_needed": analysis["required_resources"],
            "risks": self._identify_risks(analysis),
            "success_criteria": self._define_success_criteria(analysis),
            "qmdg_recommendations": qmdg_result.get("analysis", {}).get("recommendations", [])
        }
        
        # Lưu vào lịch sử
        self.project_history.append(plan)
        
        print(f"✅ Kế hoạch dự án đã sẵn sàng!")
        return plan
    
    def _parse_requirements(self, request: str) -> List[str]:
        """Phân tích và trích xuất yêu cầu"""
        # Đơn giản hóa: tách theo dấu câu
        requirements = []
        
        keywords = {
            "ai": "Tích hợp AI/Machine Learning",
            "web": "Phát triển web application",
            "api": "Tạo REST API",
            "database": "Thiết lập cơ sở dữ liệu",
            "test": "Automated testing",
            "deploy": "Deployment automation",
            "n8n": "n8n workflow automation",
            "gemini": "Gemini AI integration",
            "qmdg": "Kỳ Môn Độn Giáp integration"
        }
        
        request_lower = request.lower()
        for keyword, requirement in keywords.items():
            if keyword in request_lower:
                requirements.append(requirement)
        
        if not requirements:
            requirements.append("Phát triển tính năng tùy chỉnh")
        
        return requirements
    
    def _estimate_complexity(self, request: str) -> str:
        """Ước tính độ phức tạp"""
        request_lower = request.lower()
        
        high_complexity_keywords = ["ai", "machine learning", "automation", "workflow", "integration"]
        medium_complexity_keywords = ["api", "database", "web", "testing"]
        
        high_count = sum(1 for kw in high_complexity_keywords if kw in request_lower)
        medium_count = sum(1 for kw in medium_complexity_keywords if kw in request_lower)
        
        if high_count >= 2:
            return "High"
        elif high_count >= 1 or medium_count >= 3:
            return "Medium"
        else:
            return "Low"
    
    def _suggest_approach(self, request: str) -> List[str]:
        """Đề xuất cách tiếp cận"""
        approaches = [
            "Bắt đầu với prototype nhỏ",
            "Phát triển theo từng module độc lập",
            "Sử dụng agile methodology",
            "Continuous integration/deployment"
        ]
        
        if "ai" in request.lower():
            approaches.append("Tích hợp AI từ giai đoạn đầu")
        
        if "n8n" in request.lower():
            approaches.append("Thiết kế workflows trước khi code")
        
        return approaches
    
    def _identify_resources(self, request: str) -> Dict[str, List[str]]:
        """Xác định nguồn lực cần thiết"""
        resources = {
            "technologies": [],
            "apis": [],
            "tools": [],
            "infrastructure": []
        }
        
        request_lower = request.lower()
        
        if "n8n" in request_lower:
            resources["tools"].append("n8n")
            resources["infrastructure"].append("n8n server")
        
        if "gemini" in request_lower or "ai" in request_lower:
            resources["apis"].append("Gemini API")
            resources["technologies"].append("Python")
        
        if "web" in request_lower:
            resources["technologies"].extend(["Streamlit", "HTML/CSS/JavaScript"])
            resources["infrastructure"].append("Web server")
        
        if "database" in request_lower:
            resources["technologies"].append("PostgreSQL/MongoDB")
            resources["infrastructure"].append("Database server")
        
        return resources
    
    def _generate_project_name(self, analysis: Dict[str, Any]) -> str:
        """Tạo tên dự án"""
        timestamp = datetime.now().strftime("%Y%m%d")
        complexity = analysis["estimated_complexity"]
        return f"Project_{complexity}_{timestamp}"
    
    def _identify_risks(self, analysis: Dict[str, Any]) -> List[str]:
        """Xác định rủi ro"""
        risks = []
        
        if analysis["estimated_complexity"] == "High":
            risks.append("Dự án phức tạp, có thể mất nhiều thời gian hơn dự kiến")
        
        if "Gemini AI integration" in analysis["parsed_requirements"]:
            risks.append("Phụ thuộc vào API bên thứ 3 (rate limits, downtime)")
        
        if "Deployment automation" in analysis["parsed_requirements"]:
            risks.append("Cần cấu hình server và CI/CD cẩn thận")
        
        return risks
    
    def _define_success_criteria(self, analysis: Dict[str, Any]) -> List[str]:
        """Định nghĩa tiêu chí thành công"""
        criteria = [
            "Tất cả tính năng hoạt động đúng",
            "Không có lỗi critical",
            "Performance đạt yêu cầu",
            "Documentation đầy đủ"
        ]
        
        if "Automated testing" in analysis["parsed_requirements"]:
            criteria.append("Test coverage >= 80%")
        
        if "Deployment automation" in analysis["parsed_requirements"]:
            criteria.append("CI/CD pipeline hoạt động ổn định")
        
        return criteria
    
    def save_plan(self, plan: Dict[str, Any], filename: str = "project_plan.json"):
        """Lưu kế hoạch ra file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(plan, f, indent=2, ensure_ascii=False)
            print(f"✅ Đã lưu kế hoạch vào {filename}")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi lưu kế hoạch: {e}")
            return False
    
    def print_plan_summary(self, plan: Dict[str, Any]):
        """In tóm tắt kế hoạch"""
        print("\n" + "="*60)
        print(f"📋 KẾ HOẠCH DỰ ÁN: {plan['project_name']}")
        print("="*60)
        
        print(f"\n⏰ Thời gian tạo: {plan['created_at']}")
        print(f"📊 Độ phức tạp: {plan['complexity']}")
        print(f"🔮 QMDG thuận lợi: {'✅ Có' if plan['qmdg_favorable'] else '⚠️ Cần cân nhắc'}")
        
        print(f"\n📝 CÁC GIAI ĐOẠN:")
        for phase in plan['phases']:
            print(f"\n  {phase['name']} ({phase['duration']})")
            for task in phase['tasks']:
                print(f"    • {task}")
        
        print(f"\n⚠️ RỦI RO:")
        for risk in plan['risks']:
            print(f"  • {risk}")
        
        print(f"\n✅ TIÊU CHÍ THÀNH CÔNG:")
        for criterion in plan['success_criteria']:
            print(f"  • {criterion}")
        
        if plan.get('qmdg_recommendations'):
            print(f"\n🔮 GỢI Ý TỪ QMDG:")
            for rec in plan['qmdg_recommendations']:
                print(f"  • {rec}")
        
        print("\n" + "="*60 + "\n")


def demo_secretary():
    """Demo AI Secretary"""
    print("🚀 DEMO: AI THƯ KÝ THÔNG MINH\n")
    
    # Khởi tạo
    secretary = SecretaryAI()
    
    # Yêu cầu mẫu
    user_request = """
    Tôi muốn tạo một hệ thống AI phát triển phần mềm tự động với n8n.
    Hệ thống cần có AI để viết code, sửa code, phân tích code, testing,
    và tích hợp với Gemini AI và Kỳ Môn Độn Giáp.
    """
    
    # Bước 1: Phân tích yêu cầu
    analysis = secretary.analyze_request(user_request)
    
    # Bước 2: Tư vấn QMDG
    qmdg_result = secretary.consult_qmdg(
        topic="Phát triển phần mềm",
        question="Thời điểm này có tốt để bắt đầu dự án AI automation không?"
    )
    
    # Bước 3: Tạo kế hoạch
    plan = secretary.create_project_plan(analysis, qmdg_result)
    
    # Bước 4: Hiển thị kế hoạch
    secretary.print_plan_summary(plan)
    
    # Bước 5: Lưu kế hoạch
    secretary.save_plan(plan, "ai_dev_system_plan.json")


if __name__ == "__main__":
    demo_secretary()
