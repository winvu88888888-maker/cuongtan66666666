@echo off
echo ====================================================
echo   HOTFIX: Sửa lỗi AttributeError trong LED Indicator
echo ====================================================
echo.

cd /d "%~dp0"

echo [1] Adding fix...
git add app.py

echo.
echo [2] Committing hotfix...
git commit -m "🔥 HOTFIX: Sửa lỗi AttributeError khi truy cập model.model_name"

echo.
echo [3] Pulling latest...
git pull --rebase origin main

echo.
echo [4] Pushing urgently...
git push origin main

echo.
echo ====================================================
echo              HOTFIX DEPLOYED!
echo ====================================================
echo.
echo ✅ Đã sửa lỗi crash AttributeError
echo ✅ App sẽ không còn crash khi hiển thị model name
echo.
echo Web: https://cuongtan888888.streamlit.app/
echo Chờ 1-2 phút để deploy, sau đó F5!
echo.
pause
