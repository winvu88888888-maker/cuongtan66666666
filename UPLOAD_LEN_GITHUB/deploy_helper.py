"""
Auto-deploy helper: Set GitHub Secret + Trigger workflow
Reads credentials from TOKEN_KEY.txt and custom_data.json (NO hardcoded secrets)
"""
import urllib.request
import json
import base64
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = "winvu88888888-maker/cuongtan66666666"

def _read_token():
    token_path = os.path.join(SCRIPT_DIR, "TOKEN_KEY.txt")
    with open(token_path, "r") as f:
        return f.read().strip()

def _read_gemini_key():
    # Try factory_config first, then custom_data
    for fname in ["data_hub/factory_config.json", "custom_data.json"]:
        fpath = os.path.join(SCRIPT_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                key = data.get("api_key") or data.get("GEMINI_API_KEY")
                if key:
                    return key
    return None

def api_call(url, token, method="GET", data=None):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    if data:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        try:
            return resp.status, json.loads(resp.read())
        except:
            return resp.status, {}
    except urllib.error.HTTPError as e:
        return e.code, {"error": str(e)}
    except Exception as e:
        return 0, {"error": str(e)}

def set_github_secret():
    token = _read_token()
    gemini_key = _read_gemini_key()
    
    if not gemini_key:
        print("  ❌ Không tìm thấy GEMINI API KEY")
        return False
    
    print("🔑 [1/2] Setting GEMINI_API_KEY in GitHub Secrets...")
    
    status, key_data = api_call(f"https://api.github.com/repos/{REPO}/actions/secrets/public-key", token)
    if status != 200:
        print(f"  ❌ Failed to get public key: {key_data}")
        return False
    
    key_id = key_data["key_id"]
    public_key_b64 = key_data["key"]
    print(f"  ✅ Got public key: {key_id[:10]}...")
    
    try:
        from nacl import public as nacl_public
        public_key_bytes = base64.b64decode(public_key_b64)
        sealed_box = nacl_public.SealedBox(nacl_public.PublicKey(public_key_bytes))
        encrypted = sealed_box.encrypt(gemini_key.encode("utf-8"))
        encrypted_b64 = base64.b64encode(encrypted).decode("utf-8")
        print("  ✅ Encrypted secret")
    except ImportError:
        print("  ❌ pynacl not installed. Run: pip install pynacl")
        return False
    
    status, _ = api_call(
        f"https://api.github.com/repos/{REPO}/actions/secrets/GEMINI_API_KEY",
        token, method="PUT",
        data={"encrypted_value": encrypted_b64, "key_id": key_id}
    )
    
    if status in (201, 204):
        print(f"  ✅ GEMINI_API_KEY set successfully! (Status: {status})")
        return True
    else:
        print(f"  ❌ Failed: Status {status}")
        return False

def trigger_workflow():
    token = _read_token()
    print("🚀 [2/2] Triggering first mining cycle...")
    status, resp = api_call(
        f"https://api.github.com/repos/{REPO}/actions/workflows/ai_mining.yml/dispatches",
        token, method="POST", data={"ref": "main"}
    )
    if status == 204:
        print("  ✅ Mining workflow triggered!")
    else:
        print(f"  ⚠️ Status: {status} - {resp}")
        print(f"  👉 https://github.com/{REPO}/actions")

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "all"
    if action in ("secret", "all"):
        set_github_secret()
    if action in ("trigger", "all"):
        trigger_workflow()
    print("\n✨ Done!")
