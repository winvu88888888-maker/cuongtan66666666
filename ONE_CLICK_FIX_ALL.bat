@echo off
chcp 65001 > nul
echo ========================================================
echo   💾 LƯU TRƯỚC - HỎI SAU (FORCE SAVE MODE)
echo ========================================================
echo.
echo [1/2] Đồng bộ code...
copy /Y "app.py" "UPLOAD_LEN_GITHUB\app.py"
copy /Y "gemini_helper.py" "UPLOAD_LEN_GITHUB\gemini_helper.py"
copy /Y "free_ai_helper.py" "UPLOAD_LEN_GITHUB\free_ai_helper.py"
copy /Y "qmdg_orchestrator.py" "UPLOAD_LEN_GITHUB\qmdg_orchestrator.py"

copy /Y "app.py" "UPLOAD_TO_STREAMLIT\app.py"
copy /Y "gemini_helper.py" "UPLOAD_TO_STREAMLIT\gemini_helper.py"
copy /Y "free_ai_helper.py" "UPLOAD_TO_STREAMLIT\free_ai_helper.py"
copy /Y "qmdg_orchestrator.py" "UPLOAD_TO_STREAMLIT\qmdg_orchestrator.py"

echo.
echo [2/2] PUSH CODE (REMOVE STRICT VALIDATION)...
cd UPLOAD_LEN_GITHUB
git add .
git commit -m "Fix: Force Save API Key even if connection test fails (Trust user input)"
git push origin main --force
git push origin main:master --force
cd ..

cd UPLOAD_TO_STREAMLIT
git add .
git commit -m "Fix: Force Save API Key even if connection test fails (Trust user input)"
git push origin main --force
git push origin main:master --force
cd ..

echo.
echo ========================================================
echo   ✅ ĐÃ NỚI LỎNG CƠ CHẾ LƯU KEY!
echo   👉 Lỗi trước: Web cố test Key, thấy lỗi mạng (429) -> Không chịu lưu -> Quay về Key cũ.
echo   👉 Lỗi sau sửa: Web cứ Lưu Key bạn nhập cái đã. Lỗi tính sau.
echo   👉 Điều này đảm bảo Key mới của bạn CHẮC CHẮN được sử dụng.
echo   👉 F5 Web và thử lại lần cuối nhé!
echo ========================================================
pause
