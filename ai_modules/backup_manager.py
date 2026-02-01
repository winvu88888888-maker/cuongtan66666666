"""
AI Modules Backup Manager
Tự động backup và bảo vệ tất cả AI modules khỏi bị xóa
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path

# Cấu hình
AI_MODULES_PATH = Path(__file__).parent
BACKUP_BASE_PATH = Path("E:/Antigravity_Storage/ai_modules_backup")
DATA_HUB_PATH = AI_MODULES_PATH.parent / "data_hub"
LOG_FILE = BACKUP_BASE_PATH / "backup_log.json"

# Danh sách 22 AI modules cần bảo vệ (đã cập nhật)
PROTECTED_MODULES = [
    "autonomous_miner.py",
    "code_analyzer_ai.py",
    "code_fixer_ai.py",
    "code_writer_ai.py",
    "factory_manager.py",
    "gemini_dev_helper.py",
    "hub_searcher.py",
    "maintenance_manager.py",
    "memory_system.py",
    "mining_strategist.py",
    "orchestrator.py",
    "packager_ai.py",
    "secretary_ai.py",
    "shard_manager.py",
    "tester_ai.py",
    "web_searcher.py",
    "__init__.py",
    "backup_manager.py",
    # 5 NEW Super Intelligent AI Modules
    "chart_interpreter_ai.py",
    "scheduler_ai.py",
    "mai_hoa_expert_ai.py",
    "luc_hao_expert_ai.py",
    "topic_advisor_ai.py"
]

def ensure_backup_dir():
    """Tạo thư mục backup nếu chưa có"""
    BACKUP_BASE_PATH.mkdir(parents=True, exist_ok=True)
    return BACKUP_BASE_PATH

def get_module_hash(filepath):
    """Lấy hash của file để kiểm tra thay đổi"""
    import hashlib
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def backup_all_modules(force=False):
    """
    Backup tất cả AI modules
    Args:
        force: True để backup ngay cả khi không có thay đổi
    Returns:
        dict: Kết quả backup
    """
    ensure_backup_dir()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = BACKUP_BASE_PATH / f"backup_{timestamp}"
    
    results = {
        "timestamp": timestamp,
        "backed_up": [],
        "skipped": [],
        "errors": [],
        "total_modules": len(PROTECTED_MODULES)
    }
    
    # Đọc log cũ để so sánh hash
    old_hashes = {}
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
                old_hashes = log_data.get("hashes", {})
        except:
            pass
    
    new_hashes = {}
    files_to_backup = []
    
    for module in PROTECTED_MODULES:
        src_path = AI_MODULES_PATH / module
        if src_path.exists():
            current_hash = get_module_hash(src_path)
            new_hashes[module] = current_hash
            
            # Kiểm tra có thay đổi không
            if force or old_hashes.get(module) != current_hash:
                files_to_backup.append((src_path, module))
            else:
                results["skipped"].append(module)
        else:
            results["errors"].append(f"Missing: {module}")
    
    # Chỉ tạo folder và backup nếu có file cần backup
    if files_to_backup:
        backup_folder.mkdir(parents=True, exist_ok=True)
        for src_path, module in files_to_backup:
            try:
                dst_path = backup_folder / module
                shutil.copy2(src_path, dst_path)
                results["backed_up"].append(module)
            except Exception as e:
                results["errors"].append(f"{module}: {str(e)}")
    
    # Cập nhật log
    log_data = {
        "last_backup": timestamp,
        "hashes": new_hashes,
        "backup_folder": str(backup_folder) if files_to_backup else None,
        "total_backups": len(list(BACKUP_BASE_PATH.glob("backup_*")))
    }
    
    try:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
    except:
        pass
    
    return results

def restore_missing_modules():
    """
    Kiểm tra và khôi phục các modules bị thiếu từ backup gần nhất
    Returns:
        dict: Kết quả khôi phục
    """
    results = {
        "restored": [],
        "not_needed": [],
        "failed": [],
        "no_backup": []
    }
    
    # Tìm backup gần nhất
    backups = sorted(BACKUP_BASE_PATH.glob("backup_*"), reverse=True)
    if not backups:
        results["error"] = "Không có backup nào"
        return results
    
    latest_backup = backups[0]
    
    for module in PROTECTED_MODULES:
        src_path = AI_MODULES_PATH / module
        backup_path = latest_backup / module
        
        if src_path.exists():
            results["not_needed"].append(module)
        elif backup_path.exists():
            try:
                shutil.copy2(backup_path, src_path)
                results["restored"].append(module)
            except Exception as e:
                results["failed"].append(f"{module}: {str(e)}")
        else:
            results["no_backup"].append(module)
    
    return results

def list_all_modules():
    """
    Liệt kê tất cả AI modules và trạng thái
    Returns:
        dict: Thông tin các modules
    """
    modules_status = {}
    
    for module in PROTECTED_MODULES:
        path = AI_MODULES_PATH / module
        if path.exists():
            stat = path.stat()
            modules_status[module] = {
                "exists": True,
                "size_kb": round(stat.st_size / 1024, 2),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
        else:
            modules_status[module] = {
                "exists": False,
                "size_kb": 0,
                "modified": None
            }
    
    return {
        "total": len(PROTECTED_MODULES),
        "existing": sum(1 for m in modules_status.values() if m["exists"]),
        "missing": [k for k, v in modules_status.items() if not v["exists"]],
        "modules": modules_status
    }

def cleanup_old_backups(keep_count=10):
    """
    Xóa các backup cũ, chỉ giữ lại số lượng nhất định
    Args:
        keep_count: Số backup giữ lại (default: 10)
    """
    backups = sorted(BACKUP_BASE_PATH.glob("backup_*"), reverse=True)
    
    if len(backups) > keep_count:
        for old_backup in backups[keep_count:]:
            try:
                shutil.rmtree(old_backup)
            except:
                pass
    
    return len(backups) - keep_count if len(backups) > keep_count else 0

def get_backup_status():
    """Lấy trạng thái backup hiện tại"""
    if not LOG_FILE.exists():
        return {"status": "never_backed_up"}
    
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
            return {
                "status": "ok",
                "last_backup": log_data.get("last_backup"),
                "total_backups": log_data.get("total_backups", 0),
                "backup_location": str(BACKUP_BASE_PATH)
            }
    except:
        return {"status": "error_reading_log"}


# Auto-run khi import lần đầu - kiểm tra và restore nếu cần
def _auto_check():
    """Tự động kiểm tra khi module được import"""
    try:
        status = list_all_modules()
        if status["missing"]:
            # Có modules bị thiếu -> thử restore
            restore_missing_modules()
    except:
        pass

# Uncomment để bật auto-check
# _auto_check()


if __name__ == "__main__":
    # Test backup
    print("=== AI MODULES BACKUP MANAGER ===")
    print("\n1. Checking modules status...")
    status = list_all_modules()
    print(f"   Total: {status['total']}, Existing: {status['existing']}")
    if status['missing']:
        print(f"   Missing: {status['missing']}")
    
    print("\n2. Running backup...")
    result = backup_all_modules(force=True)
    print(f"   Backed up: {len(result['backed_up'])}")
    print(f"   Skipped: {len(result['skipped'])}")
    if result['errors']:
        print(f"   Errors: {result['errors']}")
    
    print("\n3. Backup status:")
    backup_status = get_backup_status()
    print(f"   Location: {backup_status.get('backup_location')}")
    print(f"   Total backups: {backup_status.get('total_backups')}")
    
    print("\n=== DONE ===")
