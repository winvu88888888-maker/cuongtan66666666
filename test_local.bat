@echo off
echo ====================================================
echo   TEST STATUS INDICATORS LOCAL
echo ====================================================
echo.

cd /d "%~dp0"

echo Starting Streamlit app locally...
echo Vao trinh duyet: http://localhost:8501
echo Tab "Nha May AI" de xem status indicators!
echo.
echo Nhan Ctrl+C de dung.
echo.

streamlit run app.py
