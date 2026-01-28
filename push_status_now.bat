@echo off
cd /d "%~dp0"
git add web/ai_factory_tabs.py
git commit -m "✨ Add status indicators to data hub tab"
git push origin main
echo.
echo DONE! Refresh web sau 1-2 phut!
pause
