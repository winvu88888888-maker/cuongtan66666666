@echo off
cd /d "%~dp0"

echo [1] Dang kiem tra va luu lai toan bo thay doi (Code + Data Hub)...
git add -A
git commit -m "🚀 Deploy: High-quality QMDG research focus and Deep AI Sanitation system"

echo [2] Dang gop du lieu tu Cloud...
git pull origin main --no-edit

echo [3] Dang day ban sua loi len Web...
git push origin main

echo ====================================
echo XONG! AI Factory da duoc nang cap!
echo Choi 1 phut roi F5 trang web.
echo ====================
pause
