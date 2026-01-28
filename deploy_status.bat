@echo off
echo ====================================================
echo   DEPLOY STATUS INDICATORS
echo ====================================================
echo.

cd /d "%~dp0"

echo [1] Adding changes...
git add web/ai_factory_tabs.py

echo.
echo [2] Committing...
git commit -m "✨ Add real-time status indicators with green/red lights"

echo.
echo [3] Pushing...
git push origin main

echo.
echo ====================================================
echo              DONE!
echo ====================================================
echo.
echo Vao web sau 1-2 phut: https://cuongtan66666666.streamlit.app/
echo Tab "Nha May AI" - Xem status indicators moi!
echo.
echo Status hien thi:
echo - 🟢 XANH = Dang chay
echo - 🔴 DO = Khong chay
echo.
pause
