@echo off
chcp 65001 >nul
echo Starting Essay Corrector System...
cd /d "C:\Users\Era\Documents\EssayCorrector"
"C:\Users\Era\Documents\EssayCorrector\.venv\Scripts\python.exe" "C:\Users\Era\Documents\EssayCorrector\app.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application crashed. Please check the error messages above.
    pause
)
