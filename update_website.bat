@echo off
echo ==============================================
echo      TU DONG CAP NHAT WEBSITE LEN GITHUB
echo ==============================================

echo 1. Dang cau hinh Git...
git config --global user.email "winvu88888888@gmail.com"
git config --global user.name "winvu88888888-maker"

echo.
echo 2. Dang luu thay doi (Commit)...
:: Xoa git cu de dam bao khong bi dinh loi Secret History
if exist .git (
    echo [INFO] Dang lam sach lich su Git cu...
    rmdir /s /q .git
)

git init
git add .
git commit -m "Auto update: Fix UI and Errors (Clean Push)"

echo.
echo 3. Dang ket noi Server GitHub...
git remote remove origin
git remote add origin https://github.com/winvu88888888-maker/cuongtan66666666.git

echo.
echo 4. Dang day code len Server (Push)...
git branch -M main
:: Luon su dung Force Push de dam bao ghi de code cu
git push -u origin main --force

echo.
echo ==============================================
echo             HOAN TAT QUA TRINH
echo ==============================================
echo Hay kiem tra lai web sau 1-2 phut:
echo https://cuongtan66666666.streamlit.app/
echo.
pause
