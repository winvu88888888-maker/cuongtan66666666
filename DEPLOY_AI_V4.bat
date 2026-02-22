@echo off
chcp 65001 >nul
echo ========================================
echo   DEPLOY AI V4.1 - Fix Calendar Date
echo ========================================
echo.

cd /d "C:\Users\GHC\Desktop\python1 - Copy"

echo [1/3] Copy app.py sang UPLOAD_TO_STREAMLIT...
copy /Y app.py "UPLOAD_TO_STREAMLIT\app.py"

echo [2/3] Copy app.py sang UPLOAD_LEN_GITHUB...
copy /Y app.py "UPLOAD_LEN_GITHUB\app.py"

echo [3/3] Push len GitHub...
git add .
git commit -m "AI V4.1 - Fix calendar timezone VN + Can Chi ngay"
git push

echo.
echo ========================================
echo   HOAN TAT! Reload web de kiem tra.
echo ========================================
pause
