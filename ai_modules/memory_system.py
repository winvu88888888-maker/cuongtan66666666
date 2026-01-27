"""
Memory System - AI Bộ Nhớ
Lưu trữ code, dữ liệu, và knowledge base
"""

import json
import sqlite3
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
from zoneinfo import ZoneInfo


class MemorySystem:
    """Hệ thống bộ nhớ cho AI"""
    
    def __init__(self, db_path: str = "ai_memory.db"):
        """
        Khởi tạo Memory System
        
        Args:
            db_path: Đường dẫn database
        """
        self.db_path = db_path
        self.conn = None
        self._init_database()
        
    def _init_database(self):
        """Khởi tạo database"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # Code repository table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS code_repository (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT,
                file_path TEXT,
                code_content TEXT,
                language TEXT,
                version TEXT,
                hash TEXT UNIQUE,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                metadata TEXT
            )
        """)
        
        # Knowledge base table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                content TEXT,
                source TEXT,
                category TEXT,
                tags TEXT,
                created_at TIMESTAMP
            )
        """)
        
        # Execution history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS execution_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workflow_name TEXT,
                input_data TEXT,
                output_data TEXT,
                status TEXT,
                execution_time INTEGER,
                created_at TIMESTAMP
            )
        """)
        
        # Project plans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT,
                plan_data TEXT,
                status TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)
        
        self.conn.commit()
        print(f"✅ Database initialized: {self.db_path}")
    
    def store_code(self, project_name: str, file_path: str, code_content: str, 
                   language: str = "python", metadata: Optional[Dict] = None) -> int:
        """
        Lưu code vào repository
        
        Args:
            project_name: Tên dự án
            file_path: Đường dẫn file
            code_content: Nội dung code
            language: Ngôn ngữ lập trình
            metadata: Metadata bổ sung
            
        Returns:
            ID của record
        """
        cursor = self.conn.cursor()
        
        # Calculate hash
        code_hash = hashlib.sha256(code_content.encode()).hexdigest()
        
        # Check if exists
        cursor.execute("SELECT id FROM code_repository WHERE hash = ?", (code_hash,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"⚠️ Code đã tồn tại (ID: {existing['id']})")
            return existing['id']
        
        # Insert new
        now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()
        metadata_json = json.dumps(metadata or {})
        
        cursor.execute("""
            INSERT INTO code_repository 
            (project_name, file_path, code_content, language, version, hash, created_at, updated_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (project_name, file_path, code_content, language, "1.0.0", code_hash, now, now, metadata_json))
        
        self.conn.commit()
        record_id = cursor.lastrowid
        
        print(f"✅ Đã lưu code (ID: {record_id})")
        return record_id
    
    def get_code(self, code_id: Optional[int] = None, project_name: Optional[str] = None, 
                 file_path: Optional[str] = None) -> Optional[Dict]:
        """
        Lấy code từ repository
        
        Args:
            code_id: ID của code
            project_name: Tên dự án
            file_path: Đường dẫn file
            
        Returns:
            Dict chứa thông tin code
        """
        cursor = self.conn.cursor()
        
        if code_id:
            cursor.execute("SELECT * FROM code_repository WHERE id = ?", (code_id,))
        elif project_name and file_path:
            cursor.execute("SELECT * FROM code_repository WHERE project_name = ? AND file_path = ?", 
                         (project_name, file_path))
        else:
            return None
        
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def search_code(self, query: str, language: Optional[str] = None) -> List[Dict]:
        """
        Tìm kiếm code
        
        Args:
            query: Từ khóa tìm kiếm
            language: Lọc theo ngôn ngữ
            
        Returns:
            List kết quả
        """
        cursor = self.conn.cursor()
        
        sql = "SELECT * FROM code_repository WHERE code_content LIKE ?"
        params = [f"%{query}%"]
        
        if language:
            sql += " AND language = ?"
            params.append(language)
        
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def store_knowledge(self, topic: str, content: str, source: str = "manual", 
                       category: str = "general", tags: Optional[List[str]] = None) -> int:
        """
        Lưu knowledge vào knowledge base
        
        Args:
            topic: Chủ đề
            content: Nội dung
            source: Nguồn
            category: Danh mục
            tags: Tags
            
        Returns:
            ID của record
        """
        cursor = self.conn.cursor()
        
        now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()
        tags_json = json.dumps(tags or [])
        
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, category, tags, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (topic, content, source, category, tags_json, now))
        
        self.conn.commit()
        record_id = cursor.lastrowid
        
        print(f"✅ Đã lưu knowledge (ID: {record_id})")
        return record_id
    
    def search_knowledge(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """
        Tìm kiếm knowledge
        
        Args:
            query: Từ khóa
            category: Danh mục
            
        Returns:
            List kết quả
        """
        cursor = self.conn.cursor()
        
        sql = "SELECT * FROM knowledge_base WHERE (topic LIKE ? OR content LIKE ?)"
        params = [f"%{query}%", f"%{query}%"]
        
        if category:
            sql += " AND category = ?"
            params.append(category)
        
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def log_execution(self, workflow_name: str, input_data: Dict, output_data: Dict, 
                     status: str, execution_time: int) -> int:
        """
        Log execution history
        
        Args:
            workflow_name: Tên workflow
            input_data: Dữ liệu đầu vào
            output_data: Dữ liệu đầu ra
            status: Trạng thái
            execution_time: Thời gian thực thi (ms)
            
        Returns:
            ID của record
        """
        cursor = self.conn.cursor()
        
        now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()
        input_json = json.dumps(input_data)
        output_json = json.dumps(output_data)
        
        cursor.execute("""
            INSERT INTO execution_history 
            (workflow_name, input_data, output_data, status, execution_time, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (workflow_name, input_json, output_json, status, execution_time, now))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_execution_history(self, workflow_name: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """
        Lấy execution history
        
        Args:
            workflow_name: Lọc theo workflow
            limit: Số lượng records
            
        Returns:
            List history
        """
        cursor = self.conn.cursor()
        
        if workflow_name:
            cursor.execute("""
                SELECT * FROM execution_history 
                WHERE workflow_name = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (workflow_name, limit))
        else:
            cursor.execute("""
                SELECT * FROM execution_history 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def store_project_plan(self, project_name: str, plan_data: Dict) -> int:
        """
        Lưu project plan
        
        Args:
            project_name: Tên dự án
            plan_data: Dữ liệu kế hoạch
            
        Returns:
            ID của record
        """
        cursor = self.conn.cursor()
        
        now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()
        plan_json = json.dumps(plan_data, ensure_ascii=False)
        
        cursor.execute("""
            INSERT INTO project_plans (project_name, plan_data, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (project_name, plan_json, "active", now, now))
        
        self.conn.commit()
        record_id = cursor.lastrowid
        
        print(f"✅ Đã lưu project plan (ID: {record_id})")
        return record_id
    
    def get_project_plan(self, project_name: str) -> Optional[Dict]:
        """Lấy project plan"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM project_plans WHERE project_name = ? ORDER BY created_at DESC LIMIT 1", 
                      (project_name,))
        row = cursor.fetchone()
        if row:
            result = dict(row)
            result['plan_data'] = json.loads(result['plan_data'])
            return result
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Code repository stats
        cursor.execute("SELECT COUNT(*) as count FROM code_repository")
        stats['total_code_files'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT language, COUNT(*) as count FROM code_repository GROUP BY language")
        stats['code_by_language'] = {row['language']: row['count'] for row in cursor.fetchall()}
        
        # Knowledge base stats
        cursor.execute("SELECT COUNT(*) as count FROM knowledge_base")
        stats['total_knowledge'] = cursor.fetchone()['count']
        
        # Execution history stats
        cursor.execute("SELECT COUNT(*) as count FROM execution_history")
        stats['total_executions'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT status, COUNT(*) as count FROM execution_history GROUP BY status")
        stats['executions_by_status'] = {row['status']: row['count'] for row in cursor.fetchall()}
        
        return stats
    
    def close(self):
        """Đóng database connection"""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed")


def demo_memory_system():
    """Demo Memory System"""
    print("🚀 DEMO: MEMORY SYSTEM\n")
    
    memory = MemorySystem("demo_memory.db")
    
    # Store code
    print("1️⃣ Storing code...")
    code_id = memory.store_code(
        project_name="demo_project",
        file_path="main.py",
        code_content="def hello():\n    print('Hello World')",
        language="python",
        metadata={"author": "AI", "purpose": "demo"}
    )
    
    # Retrieve code
    print("\n2️⃣ Retrieving code...")
    code = memory.get_code(code_id=code_id)
    print(f"Retrieved: {code['file_path']}")
    
    # Store knowledge
    print("\n3️⃣ Storing knowledge...")
    memory.store_knowledge(
        topic="Python Best Practices",
        content="Always use meaningful variable names",
        category="coding",
        tags=["python", "best-practices"]
    )
    
    # Search knowledge
    print("\n4️⃣ Searching knowledge...")
    results = memory.search_knowledge("Python")
    print(f"Found {len(results)} knowledge items")
    
    # Log execution
    print("\n5️⃣ Logging execution...")
    memory.log_execution(
        workflow_name="code_generation",
        input_data={"prompt": "Create hello world"},
        output_data={"code": "print('Hello')"},
        status="success",
        execution_time=1500
    )
    
    # Get statistics
    print("\n6️⃣ Statistics:")
    stats = memory.get_statistics()
    print(json.dumps(stats, indent=2))
    
    memory.close()


if __name__ == "__main__":
    demo_memory_system()
