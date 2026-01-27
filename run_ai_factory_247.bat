@echo off
chcp 65001 >nul
title NHA MAY AI 24/7 - QUAN DOAN KHAI THAC
color 0A
cls

echo ========================================================
echo       🏭 KHOI DONG NHA MAY AI 24/7 (AI FACTORY)       
echo           Che do: AUTONOMOUS DAEMON (Non-Stop)        
echo ========================================================
echo.
echo [INFO] Dang kich hoat Quan Doan 50 AI + Ve Sinh Tu Dong...
echo [INFO] Nhan Ctrl+C bat cu luc nao de DUNG LAI.
echo.

cd /d "%~dp0"

:: Check python availability
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Khong tim thay Python! Vui long cai dat Python.
    pause
    exit /b
)

:: Run the miner in daemon mode
python ai_modules/autonomous_miner.py --daemon

if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Chuong trinh da dung dot ngot.
    pause
)
