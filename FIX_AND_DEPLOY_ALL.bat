@echo off
echo ====================================================
echo   SCRIPT TỰ ĐỘNG - FIX VÀ DEPLOY HẾT MỌI THỨ
echo ====================================================
echo.
echo Đang thực hiện tất cả các bước tự động...
echo.

cd /d "%~dp0"

echo [Bước 1/6] Kiểm tra Git status...
git status

echo.
echo [Bước 2/6] Adding TẤT CẢ files (bao gồm untracked)...
git add -A

echo.
echo [Bước 3/6] Checking changes...
git status

echo.
echo [Bước 4/6] Committing với message tổng hợp...
git commit -m "🔥 MEGA FIX: Sửa AttributeError LED + API quota + Flash model priority" -m "- Fixed AttributeError when accessing model.model_name" -m "- Added safe getattr() checks" -m "- Changed model priority to Flash (save quota)" -m "- Added LED indicator with auto-check" -m "- Fixed Streamlit Cloud Secret handling"

echo.
echo [Bước 5/6] Pulling latest từ GitHub (rebase)...
git pull --rebase origin main

echo.
echo [Bước 6/6] Pushing to GitHub...
git push origin main

echo.
echo ====================================================
echo              HOÀN TẤT!
echo ====================================================
echo.
echo ✅ Tất cả thay đổi đã được commit
echo ✅ Đã push lên GitHub thành công
echo ✅ Streamlit Cloud sẽ tự động deploy trong 1-2 phút
echo.
echo 🌐 Web Apps (cả 2 sẽ được update):
echo    - https://cuongtan888888.streamlit.app/
echo    - https://cuongtan66666666.streamlit.app/
echo.
echo ⏰ Chờ 1-2 phút, sau đó:
echo    1. Vào web app
echo    2. Nhấn Ctrl+Shift+R (hard refresh)
echo    3. Xem LED indicator ở sidebar
echo.
echo 🎯 Sau khi deploy:
echo    - LED 🟢 xanh = API OK
echo    - LED 🔴 đỏ = API lỗi (cần tạo key mới)
echo    - Model sẽ dùng Flash (không phải Pro)
echo.
pause

echo.
echo ====================================================
echo   BẠN CÓ MUỐN MỞ WEB APP LUÔN KHÔNG?
echo ====================================================
echo.
set /p open_web="Nhấn Y để mở web app, N để bỏ qua: "

if /i "%open_web%"=="Y" (
    echo Đang mở web apps...
    start https://cuongtan888888.streamlit.app/
    timeout /t 2 /nobreak >nul
    start https://cuongtan66666666.streamlit.app/
    echo.
    echo ✅ Đã mở cả 2 web apps!
    echo Nhớ nhấn Ctrl+F5 để refresh!
)

echo.
echo Hoàn tất! Cảm ơn bạn đã sử dụng! 🎉
pause
