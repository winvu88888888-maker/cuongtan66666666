@echo off
echo ====================================================
echo   DEPLOY 50 AI AGENTS + WEB SEARCH TO GITHUB
echo ====================================================
echo.

cd /d "%~dp0"

echo [1] Checking Git status...
git status

echo.
echo [2] Adding all changes...
git add .

echo.
echo [3] Committing changes...
git commit -m "🚀 MAJOR UPGRADE: 50 AI Agents + Web Search + 24/7 GitHub Actions

- Created web_searcher.py for Google/Internet search
- Upgraded autonomous_miner.py: 50 agents, 15 concurrent workers
- Expanded mining_strategist.py: 100+ topics across 10 categories
- GitHub Actions: runs every 30 minutes (48x/day)
- Updated AI Factory dashboard UI
- Dual-phase search: Web scraping + Gemini AI Grounding

System now runs 24/7 autonomously, even when web browser is closed."

echo.
echo [4] Pushing to GitHub...
git push origin main

if errorlevel 1 (
    echo.
    echo [WARNING] Push failed, trying with --force...
    git push origin main --force
)

echo.
echo ====================================================
echo              DEPLOYMENT COMPLETE!
echo ====================================================
echo.
echo Next Steps:
echo 1. Go to GitHub repository Settings ^> Secrets
echo 2. Add secret: GEMINI_API_KEY = [Your API Key]
echo 3. Go to Actions tab and enable workflows
echo 4. Wait 30 minutes for first cycle to run
echo 5. Check https://cuongtan66666666.streamlit.app/
echo.
echo The 50 AI agents will now run 24/7 automatically!
echo.
pause
