@echo off
echo ====================================================
echo   FORCE PUSH - DEPLOY EVERYTHING
echo ====================================================
echo.

cd /d "%~dp0"

echo [1] Pulling with merge strategy...
git pull origin main --no-rebase --allow-unrelated-histories

echo.
echo [2] Adding all changes...
git add -A

echo.
echo [3] Committing...
git commit -m "🚀 Complete 50 AI Agents System + API Key" || echo "Already committed"

echo.
echo [4] Force pushing...
git push origin main --force

echo.
echo ====================================================
echo              DONE!
echo ====================================================
echo.
echo Vào web sau 1-2 phút: https://cuongtan66666666.streamlit.app/
echo.
pause
