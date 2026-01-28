@echo off
echo ====================================================
echo   PUSH DU LIEU MOI LEN GITHUB
echo ====================================================
echo.

cd /d "%~dp0"

echo [1] Checking what changed...
git status

echo.
echo [2] Adding data_hub files...
git add data_hub/

echo.
echo [3] Committing...
git commit -m "🤖 AI Factory Cycle #2: 39 tasks completed by 50 agents" || echo "No changes"

echo.
echo [4] Pulling latest...
git pull origin main --rebase

echo.
echo [5] Pushing to GitHub...
git push origin main

echo.
echo ====================================================
echo              DONE!
echo ====================================================
echo.
echo Vao web sau 1-2 phut: https://cuongtan66666666.streamlit.app/
echo Tab "Nha May AI" - Xem metrics da tang!
echo.
pause
