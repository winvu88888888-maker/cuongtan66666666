@echo off
cd /d "%~dp0"
git add web/ai_factory_tabs.py
git commit -m "✨ Improved: Top 5 shows REAL research topics"
git push origin main
echo.
echo DONE! Refresh web sau 1-2 phut!
echo Top 5 se hien thi chu de THAT tu mining strategist!
pause
