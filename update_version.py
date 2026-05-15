import os
import glob

def replace_in_file(filepath, old_str, new_str):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

if __name__ == "__main__":
    root_dir = r"C:\Users\GHC\.gemini\antigravity\scratch\cuongtan66666666_fix"
    py_files = glob.glob(os.path.join(root_dir, "*.py"))
    
    for py_file in py_files:
        replace_in_file(py_file, "V42.9.40", "V42.9.40")
        
    print("Version update complete.")
