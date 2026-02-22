@echo off
echo --- DANG KHAC PHUC LOI DEPLOY ---
echo 1. Dang lay code moi nhat tu tren mang ve (Git Pull)...
git pull origin main --no-edit
echo.
echo 2. Dang day code len lai (Git Push)...
git push origin main
echo.
echo --- NEU VAN LOI, HAY CHAY FILE 'force_deploy.bat' (EM SE TAO NGAY SAU DAY) ---
pause
