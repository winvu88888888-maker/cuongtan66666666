@echo off
echo ====================================================
echo   FIX LỖI API QUOTA - CHUYỂN SANG FLASH MODEL 
echo ====================================================  
echo.

cd /d "%~dp0"

echo [1] Adding changes...
git add -A

echo.
echo [2] Committing...
git commit -m "🔧 FIX: Sửa lỗi 429 Quota - Ưu tiên Gemini Flash thay vì Pro"

echo.
echo [3] Pulling latest changes...
git pull --rebase origin main

echo.
echo [4] Pushing to GitHub...
git push origin main

echo.
echo ====================================================
echo              DONE!
echo ====================================================
echo.
echo Web: https://cuongtan66666666.streamlit.app/
echo Chờ 1-2 phút để Streamlit Cloud deploy lại!
echo.
pause
