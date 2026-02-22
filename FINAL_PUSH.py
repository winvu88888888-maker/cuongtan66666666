import subprocess
import os

import shutil
import stat

def on_rm_error(func, path, exc_info):
    # Error handler for read-only files (like .git files)
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

def run_git():
    # Get the directory where THIS script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"[*] Starting FINAL PUSH (NUCLEAR RESET MODE) from: {script_dir}")
    
    # READ TOKEN SAFELY
    token_path = os.path.join(script_dir, "TOKEN_KEY.txt")
    if not os.path.exists(token_path):
        print("[!] Error: TOKEN_KEY.txt not found!")
        return
        
    with open(token_path, "r") as f:
        token = f.read().strip()
        
    # --- AUTO-SYNC FIX: Copy core files to sub-folders to ensure consistency ---
    core_files = ["app.py", "gemini_helper.py", "qmdg_decoder.py", "orchestrator.py", "qmdg_orchestrator.py", "requirements.txt"]
    target_dirs = ["UPLOAD_TO_STREAMLIT", "UPLOAD_LEN_GITHUB"]
    
    print(f"[*] Auto-Syncing core files to sub-directories...")
    for target in target_dirs:
        target_path = os.path.join(script_dir, target)
        if os.path.exists(target_path):
            for file in core_files:
                src = os.path.join(script_dir, file)
                dst = os.path.join(target_path, file)
                if os.path.exists(src):
                    try:
                        shutil.copy2(src, dst)
                        print(f"    Synced {file} -> {target}/")
                    except Exception as e:
                        print(f"    Failed to sync {file}: {e}")
    # ---------------------------------------------------------------------------
        
    remote_url = f"https://oauth2:{token}@github.com/winvu88888888-maker/cuongtan66666666.git"

    # 1. NUCLEAR OPTION: Delete .git folder to wipe bad history
    git_dir = os.path.join(script_dir, ".git")
    if os.path.exists(git_dir):
        print(f"[*] Wiping old history (Deleting .git)...")
        try:
            shutil.rmtree(git_dir, onerror=on_rm_error)
        except Exception as e:
            print(f"[!] Warning: Could not fully delete .git: {e}")
            # Try continue anyway, init might fix it or fail

    # 2. RUN COMMANDS
    commands = [
        ["git", "init"],
        ["git", "config", "user.email", "winvu88888888@gmail.com"], # No --global to be safe
        ["git", "config", "user.name", "winvu88888888"],
        ["git", "branch", "-M", "main"],
        ["git", "remote", "add", "origin", remote_url],
        ["git", "add", "."],  # Changed from -A to . for current dir
        ["git", "add", "UPLOAD_TO_STREAMLIT/*"], # Explicitly add subfolders
        ["git", "add", "UPLOAD_LEN_GITHUB/*"],
        ["git", "commit", "-m", "🚀 FORCE UPDATE: Detailed Decoder & Fixes"],
        ["git", "push", "-u", "origin", "main", "--force"]
    ]
    
    for cmd in commands:
        try:
            print(f"Executing: {' '.join(cmd)}")
            result = subprocess.run(cmd, cwd=script_dir, capture_output=True, text=True, check=False)
            if result.returncode == 0:
                print(f"[OK] {result.stdout.strip()}")
            else:
                print(f"[!] Error: {result.stderr.strip()}")
                if "fatal: remote origin already exists" in result.stderr:
                     # Fallback if delete failed but init worked
                     subprocess.run(["git", "remote", "set-url", "origin", remote_url], cwd=script_dir)
        except Exception as e:
            print(f"[!!] Fatal Error: {e}")

if __name__ == "__main__":
    run_git()
