@echo off
cd /d "%~dp0"

echo [1] Dang kiem tra va luu lai toan bo thay doi...
git add -A
git commit -m "🚀 Fix: Persistence, Topic Filtering and JSON Integrity"

echo [2] Dang gop du lieu tu Cloud...
git pull origin main --no-edit

echo [3] Dang day ban sua loi len Web...
git push origin main

echo ====================================
echo XONG! Choi 1 phut roi F5 trang web.
echo ====================
pause
