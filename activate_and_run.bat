@echo off
echo ========================================
echo Activating Virtual Environment
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Creating virtual environment...
    python -m venv venv
    echo.
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo.
    echo Virtual environment created and dependencies installed!
) else (
    echo Virtual environment found, activating...
    call venv\Scripts\activate.bat
)

echo.
echo ========================================
echo Virtual Environment Activated
echo ========================================
echo.
echo Python location: 
where python
echo.
echo Installed packages:
pip list | findstr -i "fastapi uvicorn sqlalchemy neo4j"
echo.

REM Check Docker services
echo ========================================
echo Checking Docker Services
echo ========================================
docker-compose ps 2>nul
if errorlevel 1 (
    echo.
    echo Starting Docker services...
    docker-compose up -d postgres neo4j qdrant minio
    echo.
    echo Waiting 15 seconds for databases to initialize...
    timeout /t 15 /nobreak
) else (
    echo Docker services are running
)

echo.
echo ========================================
echo Starting Backend Server
echo ========================================
echo.
echo Backend will be available at:
echo   - API: http://localhost:8000
echo   - Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

