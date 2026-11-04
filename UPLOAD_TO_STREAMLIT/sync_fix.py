import shutil
import os
import time

print("Starting Universal Sync Fix...")

# Source file (presumed in current directory)
src = "app.py"

# Destinations
dests = [
    os.path.join("UPLOAD_LEN_GITHUB", "app.py"),
    os.path.join("UPLOAD_TO_STREAMLIT", "app.py")
]

if not os.path.exists(src):
    print(f"CRITICAL ERROR: Source file {src} not found!")
    exit(1)

for dest in dests:
    try:
        # Ensure dir exists
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        
        # Copy
        shutil.copy2(src, dest)
        print(f"✅ Successfully copied {src} to {dest}")
    except Exception as e:
        print(f"❌ Error copying to {dest}: {e}")

print("Universal Sync Fix Complete.")
