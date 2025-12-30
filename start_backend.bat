@echo off
echo ========================================
echo Intelligent Oilfield Insights Platform
echo Backend Server Startup
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo Virtual environment activated!
) else (
    echo WARNING: No virtual environment found
    echo Using system Python
)
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if databases are running
echo Checking database services...
docker ps | findstr oilfield-postgres >nul 2>&1
if errorlevel 1 (
    echo WARNING: PostgreSQL container not running
    echo Starting database services...
    docker-compose up -d postgres neo4j qdrant minio
    echo Waiting 10 seconds for databases to initialize...
    timeout /t 10 /nobreak >nul
)

echo.
echo Starting FastAPI backend on http://localhost:8000
echo API Documentation will be available at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

