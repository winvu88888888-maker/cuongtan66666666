@echo off
echo ====================================================
echo   FIX GIT CONFLICT + DEPLOY
echo ====================================================
echo.

cd /d "%~dp0"

echo [1] Pulling latest changes from GitHub...
git pull origin main --rebase

echo.
echo [2] Adding API key files...
git add custom_data.json .streamlit/secrets.toml activate_now.bat web/ai_factory_tabs.py

echo.
echo [3] Committing...
git commit -m "🔑 Add API key files + Fix manual cycle button" || echo "No new changes to commit"

echo.
echo [4] Pushing to GitHub...
git push origin main

echo.
echo ====================================================
echo              DEPLOYMENT COMPLETE!
echo ====================================================
echo.
echo Bây giờ có 2 cách:
echo.
echo [A] CHẠY LOCAL NGAY (Test nhanh):
echo     - Chạy activate_now.bat
echo     - 50 agents sẽ chạy trên máy bạn
echo.
echo [B] VÀO WEB (Tự động 24/7):
echo     - Vào https://cuongtan66666666.streamlit.app/
echo     - Tab "Nhà Máy AI"
echo     - Bật toggle 24/7
echo.
pause
