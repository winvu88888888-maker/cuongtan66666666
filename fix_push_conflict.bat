@echo off
cd /d "%~dp0"
echo ====================================================
echo   DONG BO DU LIEU TU CLOUD (FIX CONFLICT)
echo ====================================================

echo [1] Lay du lieu moi nhat tu Cloud...
git pull --rebase origin main

echo.
echo [2] Dang day code "AI Thong Minh" len...
git push origin main

echo.
echo ====================================================
echo             XONG! REFRESH WEB SAU 1 PHUT
echo ====================================================
pause
