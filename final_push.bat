@echo off
echo ====================================================
echo   FORCE PUSH - GIAI QUYET CONFLICT
echo ====================================================
echo.

cd /d "%~dp0"

echo [1] Stashing unstaged changes...
git stash

echo.
echo [2] Pulling with merge...
git pull origin main --no-rebase

echo.
echo [3] Applying stashed changes...
git stash pop

echo.
echo [4] Adding ALL changes...
git add -A

echo.
echo [5] Committing everything...
git commit -m "🤖 AI Factory: Data from 50 agents + Cycle #2" || echo "Already committed"

echo.
echo [6] Force pushing...
git push origin main --force

echo.
echo ====================================================
echo              SUCCESS!
echo ====================================================
echo.
echo Du lieu da len GitHub!
echo Vao web: https://cuongtan66666666.streamlit.app/
echo Doi 1-2 phut roi xem tab "Nha May AI"
echo.
pause
