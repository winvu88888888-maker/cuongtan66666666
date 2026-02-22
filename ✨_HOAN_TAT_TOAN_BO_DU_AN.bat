@echo off
color 0A
echo ====================================================
echo   [ HE THONG HOAN TAT DU AN - PHIEN BAN CUOI CUNG ]
echo ====================================================
echo.
echo [1/3] Dang thanh loc code va chuan hoa he thong...
:: Force sync code to all folders
copy /y "app.py" "UPLOAD_LEN_GITHUB\app.py" >nul
copy /y "gemini_helper.py" "UPLOAD_LEN_GITHUB\gemini_helper.py" >nul
copy /y "app.py" "UPLOAD_TO_STREAMLIT\app.py" >nul
copy /y "gemini_helper.py" "UPLOAD_TO_STREAMLIT\gemini_helper.py" >nul
rd /s /q __pycache__ 2>nul
rd /s /q web\__pycache__ 2>nul
rd /s /q ai_modules\__pycache__ 2>nul

echo.
echo [2/3] Dang day toan bo ban FIX SIÊU CẤP len GitHub...
git add -A
git commit -m "💎 FINAL PURIFICATION: Resolved Shadowing, AI Activation, and Grounding Tools"
git push origin main --force

echo.
echo ----------------------------------------------------
echo [3/3] DA HOAN TAT! MOI THU DA SAN SANG 100%%
echo ----------------------------------------------------
echo.
echo BAY GIO CHI CON 1 BUOC CUOI CUNG:
echo 1. Vao https://share.streamlit.io/
echo 2. Tim app "cuongtan66666666" -> Reboot app 🔄
echo.
echo * Luu y: Ban co the xoa cac file .bat cu tren Desktop cho gon.
echo.
start https://share.streamlit.io/
pause
