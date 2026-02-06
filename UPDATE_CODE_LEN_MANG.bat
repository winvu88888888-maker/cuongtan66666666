@echo off
chcp 65001 > nul
echo ========================================================
echo   🚀 TỰ ĐỘNG CẬP NHẬT CODE LÊN GITHUB (STREAMLIT CLOUD)
echo ========================================================
echo.
echo 1. Đang thêm các file thay đổi...
git add .
echo.
echo 2. Đang ghi lại nhật ký thay đổi (Fix AI Logic)...
git commit -m "Critical Fix: AI Secretary Logic V2.0"
echo.
echo 3. Đang đẩy lên Mây (Cloud)...
git push
echo.
echo ========================================================
echo   ✅ XONG! HÃY CHỜ 1 PHÚT RỒI F5 TRANG WEB CỦA BẠN.
echo ========================================================
pause
