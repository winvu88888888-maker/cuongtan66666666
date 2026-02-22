@echo off
chcp 65001 >nul
echo ============================================
echo  🔧 FIX: Import error + Push + Re-trigger
echo ============================================
echo.

cd /d "%~dp0"

echo [1/3] Đồng bộ autonomous_miner.py...
copy /Y "ai_modules\autonomous_miner.py" "UPLOAD_LEN_GITHUB\ai_modules\autonomous_miner.py"
copy /Y "ai_modules\autonomous_miner.py" "UPLOAD_TO_STREAMLIT\ai_modules\autonomous_miner.py"
echo ✅ Done!

echo.
echo [2/3] Push fix lên GitHub...
git add -A
git commit -m "🔧 Fix: MiningStrategist import error in GitHub Actions"
git push origin main --force
echo.

echo [3/3] Kích hoạt lại Mining...
timeout /t 5 /nobreak >nul
python deploy_helper.py trigger

echo.
echo ============================================
echo  ✅ Fix đã push! Mining sẽ chạy lại...
echo  👉 https://github.com/winvu88888888-maker/cuongtan66666666/actions
echo ============================================
pause
