@echo off
echo ====================================================
echo   SIMPLE FORCE PUSH
echo ====================================================
echo.

cd /d "%~dp0"

echo [1] Force adding all...
git add -A

echo.
echo [2] Force committing...
git commit -m "Status indicators update" || echo "OK"

echo.
echo [3] Force pushing (ignore conflicts)...
git push origin main --force

echo.
echo ====================================================
echo              DONE!
echo ====================================================
echo.
pause
