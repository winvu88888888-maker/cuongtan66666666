
import requests
import os

import requests
import os

# Fix path to locate TOKEN_KEY.txt in the same dir as this script
script_dir = r"c:\Users\GHC\Desktop\python1 - Copy"
token_path = os.path.join(script_dir, "TOKEN_KEY.txt")

if not os.path.exists(token_path):
    print(f"TOKEN_KEY.txt not found at {token_path}")
    exit()

with open(token_path, "r") as f:
    token = f.read().strip()

print(f"Checking Token: {token[:4]}...{token[-4:]}")

headers = {"Authorization": f"token {token}"}
resp = requests.get("https://api.github.com/user", headers=headers)

if resp.status_code == 200:
    data = resp.json()
    login = data.get("login")
    print(f"LOGIN_SUCCESS: {login}")
    
    # Also check if repo exists
    repo_name = "cuongtan66666666"
    repo_resp = requests.get(f"https://api.github.com/repos/{login}/{repo_name}", headers=headers)
    if repo_resp.status_code == 200:
        print(f"REPO_EXISTS: {repo_name}")
    else:
        print(f"REPO_MISSING: {repo_name}")
        # Try to create it? checking permissions
        create_resp = requests.post("https://api.github.com/user/repos", 
            json={"name": repo_name, "private": True, "description": "Auto-created by Antigravity"}, 
            headers=headers)
        if create_resp.status_code == 201:
             print(f"REPO_CREATED: {repo_name}")
        else:
             print(f"REPO_CREATE_FAIL: {create_resp.status_code} - {create_resp.text}")

else:
    print(f"ERROR: {resp.status_code} - {resp.text}")
