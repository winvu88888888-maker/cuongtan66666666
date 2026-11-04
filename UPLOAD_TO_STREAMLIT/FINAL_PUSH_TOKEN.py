
import os
import time
import subprocess
import sys

# Force run in the correct directory
try:
    target_dir = r"c:\Users\GHC\Desktop\python1 - Copy"
    print(f"Switching to: {target_dir}")
    os.chdir(target_dir)
except Exception as e:
    print(f"Failed to switch directory: {e}")

def run_cmd(cmd):
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def push_with_token():
    print("--- AUTOMATED GITHUB DEPLOYMENT (TOKEN BYPASS) ---")
    
    # 1. Read Token
    token_path = "TOKEN_KEY.txt"
    if not os.path.exists(token_path):
        print(f"ERROR: File {token_path} not found!")
        return
        
    with open(token_path, "r") as f:
        token = f.read().strip()
        
    if not token or len(token) < 10:
        print("ERROR: Token file is empty or invalid!")
        return

    # 2. Configure Remote with Token
    # Detected correct user from token: winvu88888888-maker
    repo_owner = "winvu88888888-maker"
    repo_name = "cuongtan66666666"
    repo_url = f"github.com/{repo_owner}/{repo_name}.git"
    
    # Check if we need to switch account
    # We will force set the remote url with the token
    auth_url = f"https://oauth2:{token}@{repo_url}"
    
    print(f"Configuring Git Remote for {repo_owner}...")
    run_cmd(f"git remote set-url origin {auth_url}")

    # DEBUG: Check local state
    print("--- DEBUG INFO ---")
    run_cmd("git branch")
    run_cmd("git status")
    print("------------------")

    # 3. Push
    print("Pushing to GitHub...")
    # Try pushing HEAD to main to be safe
    if run_cmd("git push origin HEAD:main --force"):
        print("\nSUCCESS: DEPLOYMENT COMPLETE! 🚀")
        print("Please Reboot your App on Streamlit now.")
    else:
        print("\nPush failed. Token might be invalid or has no 'repo' scope.")

if __name__ == "__main__":
    push_with_token()
    print("\nClosing in 10 seconds...")
    time.sleep(10)
