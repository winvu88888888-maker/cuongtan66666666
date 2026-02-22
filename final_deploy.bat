@echo off
echo --- CAP NHAT LAN CUOI CUNG (FINAL DEPLOY) ---
echo 1. Dang dong goi code moi nhat (Git Add + Commit)...
git add .
git commit -m "Final Update: Prophet Mode & Authentic Background Calc"

echo 2. Dang day len web (Force Push)...
git push origin main --force

echo --- HOAN TAT 100% ---
pause
