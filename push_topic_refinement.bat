@echo off
cd /d "%~dp0"
git add ai_modules/autonomous_miner.py app.py
git commit -m "✨ Improved: Two-level topic selection (Category -> Topic) + better AI categorization"
git push origin main
echo.
echo DONE! Refresh web sau 1-2 phut!
echo Bay gio ban co the lọc chu de theo Phân loai chuan (Kinh Dich, Ky Mon...) trong dropdown!
pause
