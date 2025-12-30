@echo off
echo ========================================
echo Setting Up Virtual Environment
echo ========================================
echo.

REM Check if venv exists
if exist "venv" (
    echo Virtual environment already exists
    echo Activating...
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
    echo Activating...
    call venv\Scripts\activate.bat
)

echo.
echo ========================================
echo Installing Dependencies
echo ========================================
echo.

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing requirements...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Virtual environment is ready at: %CD%\venv
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
echo.
echo To start the backend, run:
echo   activate_and_run.bat
echo.
pause

