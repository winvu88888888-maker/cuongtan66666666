import shutil
import os
import subprocess

source_dir = r"c:\Users\GHC\Desktop\python1 - Copy\UPLOAD_TO_STREAMLIT"
dest_dir = r"c:\Users\GHC\Desktop\python1 - Copy\UPLOAD_LEN_GITHUB"

files = [
    "gemini_helper.py",
    "qmdg_knowledge_complete.py",
    "qmdg_advanced_rules.py",
    "qmdg_inference_rules.py",
    "qmdg_response_template.py",
    "auto_knowledge_updater.py",
    "qmdg_data.py"
]

print(f"Syncing from {source_dir} to {dest_dir}...")

for f in files:
    src = os.path.join(source_dir, f)
    dst = os.path.join(dest_dir, f)
    try:
        shutil.copy2(src, dst)
        print(f"✅ Copied {f}")
    except Exception as e:
        print(f"❌ Failed to copy {f}: {e}")

print("Deploying to GitHub...")
try:
    os.chdir(dest_dir)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "feat: Auto-sync comprehensive QMDG knowledge system"], check=False)
    subprocess.run(["git", "push", "origin", "main", "--force"], check=True)
    print("✅ Deployed successfully!")
except Exception as e:
    print(f"❌ Deployment failed: {e}")
