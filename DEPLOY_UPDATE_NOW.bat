@echo off
chcp 65001 >nul
echo ============================================
echo  🛡️ DEPLOY: Xóa AI Dọn Dẹp + Thêm 30 chủ đề
echo ============================================
echo.

cd /d "%~dp0"

echo [1/3] Copy files sang UPLOAD_LEN_GITHUB...
copy /Y "ai_modules\maintenance_manager.py" "UPLOAD_LEN_GITHUB\ai_modules\maintenance_manager.py"
copy /Y "web\ai_factory_tabs.py" "UPLOAD_LEN_GITHUB\web\ai_factory_tabs.py"
copy /Y "web\ai_factory_view.py" "UPLOAD_LEN_GITHUB\web\ai_factory_view.py"
copy /Y "qmdg_data.py" "UPLOAD_LEN_GITHUB\qmdg_data.py"
echo ✅ Done!

echo.
echo [2/3] Copy files sang UPLOAD_TO_STREAMLIT...
copy /Y "ai_modules\maintenance_manager.py" "UPLOAD_TO_STREAMLIT\ai_modules\maintenance_manager.py"
copy /Y "web\ai_factory_tabs.py" "UPLOAD_TO_STREAMLIT\web\ai_factory_tabs.py"
copy /Y "web\ai_factory_view.py" "UPLOAD_TO_STREAMLIT\web\ai_factory_view.py"
copy /Y "qmdg_data.py" "UPLOAD_TO_STREAMLIT\qmdg_data.py"
echo ✅ Done!

echo.
echo [3/3] Push lên GitHub...
git add -A
git commit -m "🛡️ Disable AI Cleanup + Add 30 new topics"
git push origin main --force
echo.
echo ============================================
echo  ✅ HOÀN TẤT! Chờ Streamlit Cloud reload...
echo ============================================
pause
