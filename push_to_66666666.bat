@echo off
echo ====================================================
echo   PUSH TRUC TIEP LEN cuongtan888888
echo ====================================================
echo.

cd /d "%~dp0"

echo [1] Adding all changes...
git add -A

echo.
echo [2] Committing...
git commit -m "🚀 Update UI + ⚡ Auto-Merge Miner Data" || echo "Nothing new to commit"

echo.
echo [3] Fetching latest data from remote...
git pull --rebase origin main

echo.
echo [4] Pushing to GitHub...
git push origin main

echo.
echo ====================================================
echo              DONE!
echo ====================================================
echo.
echo Web: https://cuongtan888888.streamlit.app/
echo Doi 1-2 phut de cap nhat!
echo.
pause
