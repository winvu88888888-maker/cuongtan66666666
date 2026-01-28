@echo off
cd /d "%~dp0"
git add web/ai_factory_tabs.py
git commit -m "🗑️ Remove: Top 5 topics section (incorrect data)"
git push origin main
echo.
echo DONE! Refresh web sau 1-2 phut!
echo Phan Top 5 chu de da duoc xoa hoan toan!
pause
