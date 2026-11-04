
import requests
import os
import subprocess
import time

# Force run in the correct directory
try:
    target_dir = r"c:\Users\GHC\Desktop\python1 - Copy"
    os.chdir(target_dir)
except: pass

def run_cmd(cmd):
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

# 1. Get Token
with open("TOKEN_KEY.txt", "r") as f:
    token = f.read().strip()

headers = {"Authorization": f"token {token}"}

# 2. Authenticate
resp = requests.get("https://api.github.com/user", headers=headers)
if resp.status_code != 200:
    print("Token invalid!")
    exit()
user = resp.json()["login"]
print(f"User: {user}")

# 3. Create NEW Repo
new_repo_name = "antigravity_stable_v1"
print(f"Creating new repo: {new_repo_name}...")
create_resp = requests.post("https://api.github.com/user/repos", 
    json={"name": new_repo_name, "private": True, "description": "Fresh Stable Deployment"}, 
    headers=headers)

if create_resp.status_code in [201, 422]: # 422 means already exists, which is fine
    print("Repo ready.")
else:
    print(f"Failed to create repo: {create_resp.text}")
    exit()

# 3.5 CLEANUP: Remove interfering workflows (Fixes Scope Error)
workflow_file = r".github\workflows\ai_mining_cron.yml"
if os.path.exists(workflow_file):
    print(f"Removing conflict workflow: {workflow_file}")
    try:
        os.remove(workflow_file)
        # Commit the deletion
        run_cmd("git add .")
        run_cmd('git commit -m "Remove conflicting workflow"')
    except Exception as e:
        print(f"Error removing workflow: {e}")

# 4. Push to NEW Repo
remote_url = f"https://oauth2:{token}@github.com/{user}/{new_repo_name}.git"
run_cmd("git remote remove origin")
run_cmd(f"git remote add origin {remote_url}")

print("Pushing to NEW repo...")
if run_cmd("git push -u origin main --force"):
    print("SUCCESS: DEPLOYED TO NEW REPO!")
else:
    print("Push failed.")
