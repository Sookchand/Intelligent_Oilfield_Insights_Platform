@echo off
echo ========================================
echo Intelligent Oilfield Insights Platform
echo Local Development Setup
echo ========================================
echo.

REM Step 1: Activate virtual environment
echo [Step 1/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated successfully!
echo.

REM Step 2: Upgrade pip
echo [Step 2/5] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)
echo Pip upgraded successfully!
echo.

REM Step 3: Install requirements
echo [Step 3/5] Installing Python packages from requirements.txt...
echo This may take several minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)
echo All packages installed successfully!
echo.

REM Step 4: Verify installation
echo [Step 4/5] Verifying installation...
pip list
echo.

REM Step 5: Create .env file if it doesn't exist
echo [Step 5/5] Setting up environment variables...
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your OPENAI_API_KEY
    echo.
) else (
    echo .env file already exists
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your OPENAI_API_KEY
echo 2. Run: docker-compose up -d
echo 3. Wait for services to start (about 30 seconds)
echo 4. Initialize databases with seed data
echo.
pause

