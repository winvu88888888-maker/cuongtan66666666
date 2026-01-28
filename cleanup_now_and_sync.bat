@echo off
echo ======================================================
echo AI FACTORY: DEEP CLEANUP AND SYNC
echo ======================================================
echo.

echo 1. Pulling latest data from GitHub...
git pull origin main

echo.
echo 2. Running aggressive cleanup of technical titles...
:: First, make sure we add the scripts so Python can see them if they were just created
git add cleanup_bad_titles.py ai_modules/shard_manager.py
python cleanup_bad_titles.py

echo.
echo 3. Synchronizing and pushing clean data + new AI logic...
:: Add EVERYTHING to ensure new scripts and AI prompt changes are pushed
git add .
git commit -m "✨ Improved: Fortune-Telling AI style + Deep Cleanup of technical titles"
git push origin main

echo.
echo ======================================================
echo ✅ DONE! Refresh your web app in 1-2 minutes.
echo ======================================================
pause
