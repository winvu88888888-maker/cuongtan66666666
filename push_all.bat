@echo off
echo ====================================================
echo   PUSH TAT CA THAY DOI LEN WEB
echo ====================================================
echo.

cd /d "%~dp0"

echo [1] Adding all changes...
git add -A

echo.
echo [2] Committing...
git commit -m "🧹 Cleanup + ✨ Status indicators" || echo "No new changes"

echo.
echo [3] Pushing to cuongtan888888...
git push origin main

echo.
echo ====================================================
echo              DONE!
echo ====================================================
echo.
echo Web: https://cuongtan888888.streamlit.app/
echo Doi 1-2 phut, nhan Ctrl+F5, vao tab "Nha May AI"!
echo.
pause
