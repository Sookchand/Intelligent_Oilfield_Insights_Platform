@echo off
echo ========================================
echo Installing Python Requirements
echo ========================================

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing requirements from requirements.txt...
pip install -r requirements.txt

REM Verify installation
echo.
echo ========================================
echo Installed packages:
echo ========================================
pip list

echo.
echo ========================================
echo Installation complete!
echo ========================================
pause

