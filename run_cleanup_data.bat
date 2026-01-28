@echo off
cd /d "%~dp0"
echo ====================================================
echo   TIEN HANH DON DEP CAC CHU DE SAI/DAI
echo ====================================================

python cleanup_bad_titles.py

echo.
echo [1] Dang lay du lieu moi nhat tu Cloud de tranh conflict...
git pull --rebase origin main

echo.
echo [2] Dang cap nhat danh sach da don dep len Cloud...
git add data_hub/*.json
git commit -m "🧹 Cleanup: Removed technical/long titles from Data Hub"
git push origin main

echo.
echo ====================================================
echo             DA DON DEP XONG! 
echo      Refresh Web de thay danh sach sach se!
echo ====================================================
pause
