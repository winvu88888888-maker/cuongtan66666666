@echo off
echo ====================================================
echo   DON DEP - XOA FILE KHONG CAN THIET
echo ====================================================
echo.

cd /d "%~dp0"

echo Dang xoa cac file .bat khong can thiet...

:: Xoa cac script deploy cu/trung lap
del /F /Q deploy_50_agents.bat 2>nul
del /F /Q deploy_api_key.bat 2>nul
del /F /Q deploy_status.bat 2>nul
del /F /Q final_push.bat 2>nul
del /F /Q fix_push.bat 2>nul
del /F /Q force_deploy.bat 2>nul
del /F /Q force_push_status.bat 2>nul
del /F /Q push_data.bat 2>nul
del /F /Q quick_update.bat 2>nul
del /F /Q simple_push.bat 2>nul
del /F /Q run_forever.bat 2>nul
del /F /Q test_local.bat 2>nul

:: Xoa script cu lien quan den repo khac
del /F /Q sync_and_push.bat 2>nul
del /F /Q update_website.bat 2>nul

echo.
echo Dang xoa cac file Python test/backup...
del /F /Q test_mining.py 2>nul
del /F /Q luc_hao_v2.py 2>nul
del /F /Q mai_hoa_v2.py 2>nul

echo.
echo ====================================================
echo   CAC FILE CON LAI (CAN THIET)
echo ====================================================
echo.
echo SCRIPTS:
echo - activate_now.bat        (Chay 1 chu ky local)
echo - push_to_66666666.bat    (Push len web)
echo - push_status_now.bat     (Push nhanh)
echo - run_ai_factory_247.bat  (Chay 24/7 local)
echo.
echo PYTHON FILES:
echo - app.py                  (Main web app)
echo - gemini_helper.py        (Gemini AI)
echo - qmdg_*.py               (QMDG core)
echo - database_tuong_tac.py   (Database)
echo - n8n_integration.py      (n8n)
echo - free_ai_helper.py       (Free AI)
echo - mai_hoa_dich_so.py      (Mai Hoa)
echo - luc_hao_kinh_dich.py    (Luc Hao)
echo - phan_tich_da_tang.py    (Analysis)
echo.
echo FOLDERS:
echo - ai_modules/             (50 AI agents)
echo - web/                    (Web UI)
echo - data_hub/               (Data storage)
echo - .github/                (GitHub Actions)
echo.
echo ====================================================
echo              HOAN TAT!
echo ====================================================
echo.
pause
