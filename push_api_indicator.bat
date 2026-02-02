@echo off
echo ====================================================
echo   DEPLOY TÍNH NĂNG LED INDICATOR CHO API STATUS
echo ====================================================
echo.

cd /d "%~dp0"

echo [1] Adding changes...
git add app.py FEATURE_LED_INDICATOR.md

echo.
echo [2] Committing...
git commit -m "✨ ADD: LED indicator real-time cho API status + Auto-check mỗi 30s"

echo.
echo [3] Pulling latest...
git pull --rebase origin main

echo.
echo [4] Pushing to GitHub...
git push origin main

echo.
echo ====================================================
echo              DONE!
echo ====================================================
echo.
echo ✨ TÍNH NĂNG MỚI:
echo    - Đèn LED 🟢🔴🟡 hiển thị trạng thái API
echo    - Auto-check mỗi 30 giây
echo    - Hiển thị model name và quota warning
echo.
echo Web: https://cuongtan888888.streamlit.app/
echo Chờ 1-2 phút để deploy, sau đó Ctrl+F5!
echo.
pause
