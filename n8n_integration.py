"""
n8n Integration Module
Tích hợp Python với n8n để tự động hóa workflows
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime


class N8nClient:
    """Client để tương tác với n8n API"""
    
    def __init__(self, base_url: str = "http://localhost:5678", api_key: str = None):
        """
        Khởi tạo n8n client
        
        Args:
            base_url: URL của n8n instance (mặc định: http://localhost:5678)
            api_key: API key để xác thực
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or self._load_api_key()
        self.headers = {
            "X-N8N-API-KEY": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _load_api_key(self) -> str:
        """Load API key từ file config"""
        try:
            with open('n8n_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('api_key', '')
        except FileNotFoundError:
            return ''
    
    def test_connection(self) -> bool:
        """Kiểm tra kết nối với n8n"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/workflows",
                headers=self.headers,
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Lỗi kết nối: {e}")
            return False
    
    # ==================== WORKFLOW MANAGEMENT ====================
    
    def get_workflows(self) -> List[Dict]:
        """Lấy danh sách tất cả workflows"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/workflows",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            print(f"❌ Lỗi lấy workflows: {e}")
            return []
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """Lấy thông tin chi tiết của một workflow"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Lỗi lấy workflow {workflow_id}: {e}")
            return None
    
    def create_workflow(self, workflow_data: Dict) -> Optional[Dict]:
        """Tạo workflow mới"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/workflows",
                headers=self.headers,
                json=workflow_data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Lỗi tạo workflow: {e}")
            return None
    
    def update_workflow(self, workflow_id: str, workflow_data: Dict) -> Optional[Dict]:
        """Cập nhật workflow"""
        try:
            response = requests.patch(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                headers=self.headers,
                json=workflow_data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Lỗi cập nhật workflow: {e}")
            return None
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """Xóa workflow"""
        try:
            response = requests.delete(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"❌ Lỗi xóa workflow: {e}")
            return False
    
    def activate_workflow(self, workflow_id: str) -> bool:
        """Kích hoạt workflow"""
        try:
            response = requests.patch(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                headers=self.headers,
                json={"active": True}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"❌ Lỗi kích hoạt workflow: {e}")
            return False
    
    def deactivate_workflow(self, workflow_id: str) -> bool:
        """Tắt workflow"""
        try:
            response = requests.patch(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                headers=self.headers,
                json={"active": False}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"❌ Lỗi tắt workflow: {e}")
            return False
    
    # ==================== EXECUTION MANAGEMENT ====================
    
    def execute_workflow(self, workflow_id: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """Thực thi workflow với dữ liệu đầu vào"""
        try:
            payload = {"workflowData": data} if data else {}
            response = requests.post(
                f"{self.base_url}/api/v1/workflows/{workflow_id}/execute",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Lỗi thực thi workflow: {e}")
            return None
    
    def get_executions(self, workflow_id: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """Lấy danh sách executions"""
        try:
            params = {"limit": limit}
            if workflow_id:
                params["workflowId"] = workflow_id
            
            response = requests.get(
                f"{self.base_url}/api/v1/executions",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            print(f"❌ Lỗi lấy executions: {e}")
            return []
    
    def get_execution(self, execution_id: str) -> Optional[Dict]:
        """Lấy thông tin chi tiết của một execution"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/executions/{execution_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Lỗi lấy execution: {e}")
            return None
    
    def delete_execution(self, execution_id: str) -> bool:
        """Xóa execution"""
        try:
            response = requests.delete(
                f"{self.base_url}/api/v1/executions/{execution_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"❌ Lỗi xóa execution: {e}")
            return False
    
    # ==================== UTILITY METHODS ====================
    
    def get_workflow_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê về workflows"""
        workflows = self.get_workflows()
        active_count = sum(1 for w in workflows if w.get('active', False))
        
        return {
            'total_workflows': len(workflows),
            'active_workflows': active_count,
            'inactive_workflows': len(workflows) - active_count,
            'workflows': workflows
        }
    
    def get_execution_statistics(self, workflow_id: Optional[str] = None) -> Dict[str, Any]:
        """Lấy thống kê về executions"""
        executions = self.get_executions(workflow_id=workflow_id, limit=100)
        
        success_count = sum(1 for e in executions if e.get('finished', False) and not e.get('stoppedAt'))
        error_count = sum(1 for e in executions if e.get('stoppedAt'))
        
        return {
            'total_executions': len(executions),
            'successful': success_count,
            'failed': error_count,
            'executions': executions
        }
    
    def print_status(self):
        """In ra trạng thái hiện tại của n8n"""
        print("\n" + "="*60)
        print("🚀 N8N STATUS DASHBOARD")
        print("="*60)
        
        if not self.test_connection():
            print("❌ Không thể kết nối với n8n!")
            return
        
        print("✅ Kết nối thành công!")
        print(f"📍 URL: {self.base_url}")
        
        # Workflow statistics
        stats = self.get_workflow_statistics()
        print(f"\n📊 WORKFLOWS:")
        print(f"   • Tổng số: {stats['total_workflows']}")
        print(f"   • Đang chạy: {stats['active_workflows']}")
        print(f"   • Tắt: {stats['inactive_workflows']}")
        
        if stats['workflows']:
            print(f"\n📋 Danh sách workflows:")
            for wf in stats['workflows']:
                status = "🟢" if wf.get('active') else "⚪"
                print(f"   {status} {wf.get('name', 'Unnamed')} (ID: {wf.get('id')})")
        
        # Execution statistics
        exec_stats = self.get_execution_statistics()
        print(f"\n⚡ EXECUTIONS (100 gần nhất):")
        print(f"   • Tổng số: {exec_stats['total_executions']}")
        print(f"   • Thành công: {exec_stats['successful']}")
        print(f"   • Lỗi: {exec_stats['failed']}")
        
        print("="*60 + "\n")


# ==================== WORKFLOW TEMPLATES ====================

class WorkflowTemplates:
    """Các workflow templates hữu ích"""
    
    @staticmethod
    def auto_backup_workflow(backup_path: str = "C:/Backups") -> Dict:
        """Workflow tự động backup files"""
        return {
            "name": "🗂️ Auto Backup Files",
            "nodes": [
                {
                    "parameters": {
                        "rule": {
                            "interval": [
                                {
                                    "field": "hours",
                                    "hoursInterval": 6
                                }
                            ]
                        }
                    },
                    "type": "n8n-nodes-base.scheduleTrigger",
                    "typeVersion": 1.3,
                    "position": [240, 300],
                    "name": "Every 6 Hours"
                },
                {
                    "parameters": {
                        "jsCode": f"const timestamp = new Date().toISOString();\nconst backup_path = '{backup_path}';\n\nreturn [{{\n  json: {{\n    backup_path: backup_path,\n    timestamp: timestamp,\n    message: 'Backup scheduled at ' + timestamp\n  }}\n}}];"
                    },
                    "type": "n8n-nodes-base.code",
                    "typeVersion": 2,
                    "position": [460, 300],
                    "name": "Prepare Backup Data"
                }
            ],
            "connections": {
                "Every 6 Hours": {
                    "main": [[{"node": "Prepare Backup Data", "type": "main", "index": 0}]]
                }
            },
            "settings": {
                "executionOrder": "v1"
            },
            "active": False
        }
    
    @staticmethod
    def github_auto_push_workflow() -> Dict:
        """Workflow tự động push lên GitHub"""
        return {
            "name": "🚀 Auto GitHub Push",
            "nodes": [
                {
                    "parameters": {
                        "rule": {
                            "interval": [
                                {
                                    "field": "minutes",
                                    "minutesInterval": 30
                                }
                            ]
                        }
                    },
                    "type": "n8n-nodes-base.scheduleTrigger",
                    "typeVersion": 1.3,
                    "position": [240, 300],
                    "name": "Every 30 Minutes"
                },
                {
                    "parameters": {
                        "jsCode": "const timestamp = new Date().toISOString();\n\nreturn [{\n  json: {\n    action: 'git_push',\n    timestamp: timestamp,\n    message: 'Auto commit at ' + timestamp\n  }\n}];"
                    },
                    "type": "n8n-nodes-base.code",
                    "typeVersion": 2,
                    "position": [460, 300],
                    "name": "Prepare Git Data"
                }
            ],
            "connections": {
                "Every 30 Minutes": {
                    "main": [[{"node": "Prepare Git Data", "type": "main", "index": 0}]]
                }
            },
            "settings": {
                "executionOrder": "v1"
            },
            "active": False
        }
    
    @staticmethod
    def notification_workflow() -> Dict:
        """Workflow gửi thông báo"""
        return {
            "name": "🔔 Send Notifications",
            "nodes": [
                {
                    "parameters": {
                        "rule": {
                            "interval": [
                                {
                                    "field": "hours",
                                    "hoursInterval": 1
                                }
                            ]
                        }
                    },
                    "type": "n8n-nodes-base.scheduleTrigger",
                    "typeVersion": 1.3,
                    "position": [240, 300],
                    "name": "Every Hour"
                },
                {
                    "parameters": {
                        "jsCode": "const timestamp = new Date().toISOString();\nconst hour = new Date().getHours();\n\nreturn [{\n  json: {\n    title: 'Hourly Notification',\n    message: 'System is running at hour ' + hour,\n    timestamp: timestamp\n  }\n}];"
                    },
                    "type": "n8n-nodes-base.code",
                    "typeVersion": 2,
                    "position": [460, 300],
                    "name": "Format Notification"
                }
            ],
            "connections": {
                "Every Hour": {
                    "main": [[{"node": "Format Notification", "type": "main", "index": 0}]]
                }
            },
            "settings": {
                "executionOrder": "v1"
            },
            "active": False
        }


# ==================== HELPER FUNCTIONS ====================

def setup_n8n_config(api_key: str, base_url: str = "http://localhost:5678"):
    """Lưu cấu hình n8n vào file"""
    config = {
        "api_key": api_key,
        "base_url": base_url,
        "created_at": datetime.now().isoformat()
    }
    
    with open('n8n_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ Đã lưu cấu hình n8n!")


def quick_test():
    """Test nhanh kết nối n8n"""
    client = N8nClient()
    client.print_status()


if __name__ == "__main__":
    # Test module
    print("🔧 Testing n8n Integration Module...")
    quick_test()
