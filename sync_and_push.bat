@echo off
setlocal
echo ====================================================
echo      DONG BO VA CAP NHAT WEBSITE (SIEU TOC)
echo ====================================================

:: Thu muc chua Git chuyen dung de upload
set REPO_DIR=..\UPLOAD_LEN_GITHUB

echo [1] Dang sao chep tat ca cac file da sua sang thu muc %REPO_DIR%...
if not exist "%REPO_DIR%" (
    echo [LOI] Khong tim thay thu muc %REPO_DIR%. Hay kiem tra lai ten thu muc.
    pause
    exit /b
)

:: Copy tat ca file code goc
copy /Y "app.py" "%REPO_DIR%\app.py"
copy /Y "gemini_helper.py" "%REPO_DIR%\gemini_helper.py"
copy /Y "phan_tich_da_tang.py" "%REPO_DIR%\phan_tich_da_tang.py"
copy /Y "database_tuong_tac.py" "%REPO_DIR%\database_tuong_tac.py"
copy /Y "qmdg_data.py" "%REPO_DIR%\qmdg_data.py"
copy /Y "qmdg_calc.py" "%REPO_DIR%\qmdg_calc.py"
copy /Y "mai_hoa_dich_so.py" "%REPO_DIR%\mai_hoa_dich_so.py"
copy /Y "luc_hao_kinh_dich.py" "%REPO_DIR%\luc_hao_kinh_dich.py"
copy /Y "free_ai_helper.py" "%REPO_DIR%\free_ai_helper.py"
copy /Y "n8n_integration.py" "%REPO_DIR%\n8n_integration.py"
copy /Y "requirements.txt" "%REPO_DIR%\requirements.txt"

:: Copy cac folder can thiet
if not exist "%REPO_DIR%\web" mkdir "%REPO_DIR%\web"
xcopy /S /E /I /Y "web" "%REPO_DIR%\web"

if not exist "%REPO_DIR%\ai_modules" mkdir "%REPO_DIR%\ai_modules"
xcopy /S /E /I /Y "ai_modules" "%REPO_DIR%\ai_modules"

if not exist "%REPO_DIR%\n8n_workflows" mkdir "%REPO_DIR%\n8n_workflows"
xcopy /S /E /I /Y "n8n_workflows" "%REPO_DIR%\n8n_workflows"

if not exist "%REPO_DIR%\data_hub" mkdir "%REPO_DIR%\data_hub"
xcopy /S /E /I /Y "data_hub" "%REPO_DIR%\data_hub"

echo.
echo [2] Dang vao thu muc %REPO_DIR%...
cd /d "%REPO_DIR%"

echo.
echo.
echo [3] Dang day code len Server (Push)...

:: Su dung remote origin da duoc cau hinh tu truoc hoac boi update_website.bat
git push origin main
if errorlevel 1 (
    echo [INFO] Thu push voi --force...
    git push origin main --force
)

echo.
echo ====================================================
echo             MOI THU DA XONG!
echo ====================================================
echo Web cua ban dang duoc cap nhat tại link cuongtan12345678.
echo (Doi khoang 2 phut de he thong cap nhat xong)
echo.
pause
