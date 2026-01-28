@echo off
echo ====================================================
echo   FORCE PUSH STATUS INDICATORS
echo ====================================================
echo.

cd /d "%~dp0"

echo [1] Pulling with merge...
git pull origin main --no-rebase --allow-unrelated-histories

echo.
echo [2] Adding all...
git add -A

echo.
echo [3] Committing...
git commit -m "✨ Status indicators + Latest updates" || echo "Already committed"

echo.
echo [4] Force pushing...
git push origin main --force

echo.
echo ====================================================
echo              SUCCESS!
echo ====================================================
echo.
echo Vao web sau 1-2 phut: https://cuongtan66666666.streamlit.app/
echo Tab "Nha May AI" - Xem 3 status indicators:
echo - 🟢 50 AI AGENTS (xanh = dang chay)
echo - 🟢 AI DON DEP (xanh = dang chay)
echo - 🟢 GITHUB ACTIONS (xanh = 24/7 active)
echo.
pause
