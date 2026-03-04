@echo off
echo ================================================
echo    PDF RAG System - Easy Installer
echo ================================================
echo.
echo This will install all required packages...
echo.
pause

echo Installing packages with --user flag and increased timeout...
pip install --user --timeout 120 -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo Installation had some issues. Trying minimal install...
    echo.
    pip install --user --timeout 120 pypdf faiss-cpu gradio transformers sentence-transformers
)

echo.
echo ================================================
echo Installation complete!
echo ================================================
echo.
echo To start the app, run: python app.py
echo.
pause
