@echo off
echo ====================================================
echo   QUICK UPDATE: Fix Manual Cycle Button
echo ====================================================
echo.

cd /d "%~dp0"

echo [1] Adding changes...
git add web/ai_factory_tabs.py

echo.
echo [2] Committing...
git commit -m "🔧 Fix: Nút 'CHẠY CHU KỲ THỦ CÔNG' giờ tự động tìm API key + thông báo rõ ràng hơn"

echo.
echo [3] Pushing to GitHub...
git push origin main

echo.
echo ====================================================
echo              UPDATE COMPLETE!
echo ====================================================
echo.
echo Streamlit sẽ tự động cập nhật trong 1-2 phút.
echo Sau đó vào web và thử lại nút "CHẠY CHU KỲ THỦ CÔNG"!
echo.
pause
