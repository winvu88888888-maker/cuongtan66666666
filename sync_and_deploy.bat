@echo off
echo Syncing files to UPLOAD_LEN_GITHUB...
copy gemini_helper.py ..\UPLOAD_LEN_GITHUB\ /Y
copy qmdg_knowledge_complete.py ..\UPLOAD_LEN_GITHUB\ /Y
copy qmdg_advanced_rules.py ..\UPLOAD_LEN_GITHUB\ /Y
copy qmdg_inference_rules.py ..\UPLOAD_LEN_GITHUB\ /Y
copy qmdg_response_template.py ..\UPLOAD_LEN_GITHUB\ /Y
copy auto_knowledge_updater.py ..\UPLOAD_LEN_GITHUB\ /Y
copy qmdg_data.py ..\UPLOAD_LEN_GITHUB\ /Y

echo Deploying from UPLOAD_LEN_GITHUB...
cd ..\UPLOAD_LEN_GITHUB
git add .
git commit -m "feat: Auto-sync comprehensive QMDG knowledge system"
git push origin main --force

echo DONE! Please restart Streamlit.
