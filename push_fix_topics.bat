@echo off
cd /d "%~dp0"
git add web/ai_factory_tabs.py
git commit -m "🔧 Fix: Smart topic detection using category instead of random text"
git push origin main
echo.
echo DONE! Refresh web sau 1-2 phut!
echo Top 5 chu de se hien thi dung chu de nghien cuu, khong phai text ngau nhien!
pause
