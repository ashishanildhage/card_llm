@echo off
SETLOCAL EnableDelayedExpansion

:: Store the current directory
set "ORIGINAL_DIR=%CD%"

:: Check if virtual environment exists
if not exist "venv_dev" (
    echo Virtual environment not found!
    echo Please run install_dependencies.bat first
    pause
    exit /b 1
)

:: Navigate to the virtual environment Scripts folder
cd venv_dev\Scripts

:: Activate the virtual environment
call activate
if errorlevel 1 (
    echo Failed to activate virtual environment
    cd "%ORIGINAL_DIR%"
    pause
    exit /b 1
)

:: Return to the original directory
cd "%ORIGINAL_DIR%"

:: Clear the screen
cls

:: Show helpful information
echo Virtual environment activated successfully!
echo.
echo Available commands:
echo - streamlit run streamlit_app.py    (Start the application)
echo - pytest tests/                     (Run tests)
echo - mlflow server --host 0.0.0.0 --port 5000   (Start MLflow server)
echo.
echo Current directory: %CD%
echo.

:: Start a new command prompt in the current directory
cmd /k