@echo off
echo ====================================================
echo   50 AI AGENTS - CHAY MAI MAI TREN MAY BAN
echo ====================================================
echo.

cd /d "%~dp0"

:LOOP
echo.
echo [%date% %time%] Bat dau chu ky moi...
python ai_modules\autonomous_miner.py

echo.
echo [%date% %time%] Hoan tat! Doi 30 phut...
timeout /t 1800 /nobreak

goto LOOP
