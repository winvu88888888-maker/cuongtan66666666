@echo off
echo ====================================================
echo   KÍCH HOẠT 50 AI AGENTS NGAY (SỬ DỤNG API KEY CÓ SẴN)
echo ====================================================
echo.

cd /d "%~dp0"

echo [INFO] Đã tìm thấy API key trong factory_config.json
echo [INFO] Bắt đầu chạy 50 AI agents...
echo.

REM Chạy autonomous miner với API key có sẵn
python ai_modules\autonomous_miner.py

echo.
echo ====================================================
echo              HOÀN TẤT!
echo ====================================================
echo.
echo Kiểm tra kết quả:
echo - Xem file data_hub\hub_index.json
echo - Metrics "total_cycles" trong factory_config.json
echo - Vào web: https://cuongtan888888.streamlit.app/
echo.
pause
