import threading
import time
import os
import sys

# Ensure paths are correct
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from autonomous_miner import run_daemon, load_config
except ImportError:
    from ai_modules.autonomous_miner import run_daemon, load_config

class GlobalFactoryManager:
    """Manages the 24/7 Mining Daemon across all Streamlit sessions."""
    _instance = None
    _lock = threading.Lock()
    _thread = None

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def ensure_running(self):
        """Checks config and starts thread if needed."""
        try:
            config = load_config()
            if config.get("autonomous_247"):
                with self._lock:
                    if self._thread is None or not self._thread.is_alive():
                        print("⚙️ [GlobalFactoryManager] Khởi động tiến trình chạy ngầm 24/7...")
                        self._thread = threading.Thread(target=run_daemon, daemon=True)
                        self._thread.start()
                        return "Started"
                    return "Running"
            return "Disabled"
        except Exception as e:
            print(f"❌ [GlobalFactoryManager] Error: {e}")
            return "Error"

    def stop(self):
        """The daemon checks config in its loop, so we just set config to false and it stops itself."""
        pass

def init_global_factory():
    """Helper for Streamlit to call once."""
    manager = GlobalFactoryManager.get_instance()
    return manager.ensure_running()
