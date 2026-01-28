@echo off
cd /d "%~dp0"
git add web/ai_factory_tabs.py
git commit -m "🔧 Fix: Status indicators indentation"
git push origin main --force
echo.
echo DONE! Doi 1-2 phut roi vao web xem!
pause
