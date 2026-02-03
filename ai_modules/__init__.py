# AI Modules Package
# Version 2.0 - With Protection and Version Tracking

"""
AI Factory Modules - 17 Core AI Modules
- Tự động backup và bảo vệ khỏi bị xóa
- Version tracking tích hợp
"""

__version__ = "2.0.0"
__author__ = "GHC"

# Module registry for protection
PROTECTED_MODULES = [
    "autonomous_miner",
    "code_analyzer_ai", 
    "code_fixer_ai",
    "code_writer_ai",
    "factory_manager",
    "gemini_dev_helper",
    "hub_searcher",
    "maintenance_manager",
    "memory_system",
    "mining_strategist",
    "orchestrator",
    "packager_ai",
    "secretary_ai",
    "shard_manager",
    "tester_ai",
    "web_searcher",
    "backup_manager"
]

def list_all_modules():
    """Liệt kê tất cả modules và trạng thái"""
    from pathlib import Path
    import importlib
    
    modules_dir = Path(__file__).parent
    result = {
        "total": len(PROTECTED_MODULES),
        "loaded": [],
        "missing": [],
        "version": __version__
    }
    
    for module_name in PROTECTED_MODULES:
        try:
            # Check if file exists
            module_file = modules_dir / f"{module_name}.py"
            if module_file.exists():
                result["loaded"].append(module_name)
            else:
                result["missing"].append(module_name)
        except Exception as e:
            result["missing"].append(f"{module_name} (error: {e})")
    
    return result

def check_integrity():
    """Kiểm tra tính toàn vẹn của tất cả modules"""
    status = list_all_modules()
    if status["missing"]:
        # Thử restore từ backup
        try:
            from . import backup_manager
            restore_result = backup_manager.restore_missing_modules()
            return {
                "status": "restored",
                "details": restore_result
            }
        except Exception as e:
            return {
                "status": "error",
                "missing": status["missing"],
                "error": str(e)
            }
    return {"status": "ok", "total": status["total"]}

def run_backup():
    """Chạy backup tất cả modules"""
    try:
        from . import backup_manager
        return backup_manager.backup_all_modules(force=True)
    except Exception as e:
        return {"error": str(e)}

# ============ Lazy Imports ============
# Chỉ import khi cần để tránh circular imports

def get_orchestrator():
    from .orchestrator import AIOrchestrator
    return AIOrchestrator

def get_memory_system():
    from .memory_system import MemorySystem
    return MemorySystem

def get_hub_searcher():
    from .hub_searcher import HubSearcher
    return HubSearcher

def get_shard_manager():
    from .shard_manager import search_index, get_full_entry, add_entry
    return {"search_index": search_index, "get_full_entry": get_full_entry, "add_entry": add_entry}

def get_web_searcher():
    from .web_searcher import get_web_searcher
    return get_web_searcher()

def get_backup_manager():
    from . import backup_manager
    return backup_manager
