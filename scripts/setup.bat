@echo off
REM Environment Setup Script Launcher - Essay Corrector System
REM 
REM This script is used to launch the environment setup script on Windows systems.
REM 
REM @author: Biubush

echo Starting environment setup script...

REM Get script directory and project root
SET SCRIPT_DIR=%~dp0
SET PROJECT_ROOT=%SCRIPT_DIR%\..

REM Change to project root directory
cd /d "%PROJECT_ROOT%"

REM Check if Python is installed
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not detected. Please install Python 3.7 or higher.
    echo You can download Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Execute setup.py script with absolute path
python "%SCRIPT_DIR%\setup.py" %*

REM If there's an error, pause
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred during installation. Please check the error messages above.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Environment setup completed. You can close this window.
pause 