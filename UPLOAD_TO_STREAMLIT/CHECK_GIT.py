import subprocess
import os

def check_git():
    try:
        result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True, check=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_git()
