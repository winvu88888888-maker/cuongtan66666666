import sys
import os
import traceback

def validate():
    print("[*] STARTING DEEP VALIDATION OF APP.PY")
    root = os.getcwd()
    sys.path.insert(0, root)
    
    # Mock streamlit to avoid UI errors during import check
    class MockStreamlit:
        def __init__(self):
            self.session_state = {}
        def error(self, *args, **kwargs): print(f"  [ST ERROR] {args}")
        def info(self, *args, **kwargs): print(f"  [ST INFO] {args}")
        def success(self, *args, **kwargs): print(f"  [ST SUCCESS] {args}")
        def warning(self, *args, **kwargs): print(f"  [ST WARNING] {args}")
        def markdown(self, *args, **kwargs): pass
        def sidebar(self, *args, **kwargs): return self
        def set_page_config(self, *args, **kwargs): pass
        def write(self, *args, **kwargs): print(f"  [ST WRITE] {args}")
        def code(self, *args, **kwargs): print(f"  [ST CODE] {args}")
        def stop(self, *args, **kwargs): pass
        def secrets(self): return {}

    sys.modules['streamlit'] = MockStreamlit()
    
    try:
        print("[1/3] Checking core modules...")
        import qmdg_calc
        import qmdg_data
        print("  - qmdg_calc: OK")
        print("  - qmdg_data: OK")
        
        print("[2/3] Checking analysis modules...")
        import phan_tich_da_tang
        import super_detailed_analysis
        print("  - phan_tich_da_tang: OK")
        print("  - super_detailed_analysis: OK")
        
        print("[3/3] Attempting to import app.py...")
        # We use runpy or manual import
        import importlib.util
        spec = importlib.util.spec_from_file_location("app", "app.py")
        app_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_mod)
        print("  - app.py: IMPORT SUCCESSFUL")
        
        print("\n[✔] ALL MODULES ARE SYNTACTICALLY CORRECT AND IMPORTABLE!")
    except Exception:
        print("\n[✖] VALIDATION FAILED!")
        print("-" * 50)
        traceback.print_exc()
        print("-" * 50)

if __name__ == "__main__":
    validate()
