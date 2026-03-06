@echo off
echo ================================================
echo    Preparing Files for Hugging Face Spaces
echo ================================================
echo.

REM Create deployment folder
if not exist "hf_deploy" mkdir hf_deploy

REM Copy necessary files
echo Copying files...
copy app_simple.py hf_deploy\app.py
copy simple_rag.py hf_deploy\simple_rag.py
copy requirements_hf.txt hf_deploy\requirements.txt
copy README_HF.md hf_deploy\README.md

REM Copy data folder
if not exist "hf_deploy\data" mkdir hf_deploy\data
copy data\sample.pdf hf_deploy\data\sample.pdf

echo.
echo ================================================
echo    Files Ready in hf_deploy folder!
echo ================================================
echo.
echo Next Steps:
echo 1. Go to https://huggingface.co/new-space
echo 2. Create a new Space (choose Gradio)
echo 3. Upload files from hf_deploy folder
echo 4. Your app will be live in 2-3 minutes!
echo.
echo Detailed instructions in DEPLOY_TO_HUGGINGFACE.md
echo.
pause
