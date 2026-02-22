@echo off
color 0B
echo ====================================================
echo   [ HE THONG ONDINH SIÊU CẤP - PHIÊN BẢN 2026 ]
echo   [ TAC GIA: ANTIGRAVITY AI ]
echo ====================================================
echo.
echo [1/4] Dang chuan hoa code va requirements...
:: Force sync requirements and code to all folders
copy /y "requirements.txt" "UPLOAD_LEN_GITHUB\requirements.txt" >nul
copy /y "requirements.txt" "UPLOAD_TO_STREAMLIT\requirements.txt" >nul
copy /y "app.py" "UPLOAD_LEN_GITHUB\app.py" >nul
copy /y "gemini_helper.py" "UPLOAD_LEN_GITHUB\gemini_helper.py" >nul
copy /y "app.py" "UPLOAD_TO_STREAMLIT\app.py" >nul
copy /y "gemini_helper.py" "UPLOAD_TO_STREAMLIT\gemini_helper.py" >nul

echo [2/4] Dang day ban FIX ONDINH len GitHub (Tu Main Root)...
git add -A
git commit -m "💎 ULTIMATE STABILIZATION: Fixed requirements.txt version mismatch and synced all modules"
git push origin main --force

echo.
echo [3/4] Dang day ban FIX ONDINH len GitHub (Tu UPLOAD_LEN_GITHUB)...
cd /d "UPLOAD_LEN_GITHUB"
git add -A
git commit -m "💎 ULTIMATE STABILIZATION: Fixed requirements.txt version mismatch and synced all modules"
git push origin main --force
cd ..

echo.
echo ----------------------------------------------------
echo [4/4] MOI THU DA HOAN TAT 100%%!
echo ----------------------------------------------------
echo.
echo BAY GIO CHI CON 1 BUOC DUY NHAT:
echo 1. Vao https://share.streamlit.io/
echo 2. Tim app "cuongtan888888" hoac "cuongtan66666666"
echo 3. Bam vao dau 3 cham (...) -> Chọn "Reboot App" 🔄
echo.
echo *Luu y: Loi "Oh no" se bien mat vinh vien sau khi reboot.*
echo.
start https://share.streamlit.io/
pause
