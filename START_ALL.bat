@echo off
title Intelligent Oilfield Insights Platform - Startup
color 0A

echo.
echo ========================================
echo  🛢️  Intelligent Oilfield Insights
echo  Complete System Startup Pipeline
echo ========================================
echo.

REM Step 1: Check Docker
echo [1/4] Checking Docker Desktop...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Docker not found!
    echo Please install Docker Desktop and try again.
    pause
    exit /b 1
)
echo ✅ Docker is available
echo.

REM Step 2: Start Databases
echo [2/4] Starting Database Containers...
echo     - PostgreSQL (port 5432)
echo     - Neo4j (port 7687, 7474)
echo     - Qdrant (port 6333)
echo     - MinIO (port 9000, 9001)
echo.
docker-compose up -d
if %errorlevel% neq 0 (
    echo ❌ ERROR: Failed to start Docker containers
    echo Make sure Docker Desktop is running!
    pause
    exit /b 1
)
echo ✅ Database containers started
echo.
echo Waiting 10 seconds for databases to initialize...
timeout /t 10 /nobreak >nul
echo.

REM Step 3: Start Backend with venv
echo [3/4] Starting Backend API Server (with venv)...
echo     - Activating Python virtual environment
echo     - Starting FastAPI with Uvicorn
echo     - API will be available at http://localhost:8000
echo.

if not exist backend\venv (
    echo ⚠️  WARNING: Virtual environment not found!
    echo Creating virtual environment...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
)

start "🔧 Backend API Server (Port 8000)" cmd /k "cd backend && call venv\Scripts\activate && echo ✅ Virtual environment activated && echo Starting FastAPI server... && uvicorn main:app --reload"
echo ✅ Backend server starting in new window...
echo.

echo Waiting 5 seconds for backend to initialize...
timeout /t 5 /nobreak >nul
echo.

REM Step 4: Start Frontend
echo [4/4] Starting Frontend Development Server...
echo     - Starting Next.js development server
echo     - Frontend will be available at http://localhost:3000
echo.

if not exist frontend\node_modules (
    echo ⚠️  WARNING: Node modules not found!
    echo Installing dependencies...
    cd frontend
    call npm install
    cd ..
)

start "🎨 Frontend Dev Server (Port 3000)" cmd /k "cd frontend && echo Starting Next.js... && npm run dev"
echo ✅ Frontend server starting in new window...
echo.

echo Waiting 8 seconds for frontend to build...
timeout /t 8 /nobreak >nul
echo.

REM Success Summary
echo ========================================
echo  ✅ All Services Started Successfully!
echo ========================================
echo.
echo  📊 Access URLs:
echo  ┌────────────────────────────────────────────────┐
echo  │ Frontend UI:    http://localhost:3000         │
echo  │ Backend API:    http://localhost:8000/docs    │
echo  │ Neo4j Browser:  http://localhost:7474         │
echo  │ MinIO Console:  http://localhost:9001         │
echo  └────────────────────────────────────────────────┘
echo.
echo  🪟 Two new windows opened:
echo     1. Backend API Server (with venv activated)
echo     2. Frontend Dev Server
echo.
echo  ✅ Verification Steps:
echo     1. Check backend window shows: "Uvicorn running on..."
echo     2. Check frontend window shows: "✓ Ready in X.Xs"
echo     3. Frontend window should STAY OPEN (not return to prompt)
echo.
echo  Press any key to open the frontend in your browser...
pause >nul

start http://localhost:3000

echo.
echo  🎉 System is ready! Enjoy your Intelligent Oilfield Insights Platform!
echo.
echo  🛑 To stop all services:
echo     1. Press Ctrl+C in Backend window
echo     2. Press Ctrl+C in Frontend window
echo     3. Run: docker-compose down
echo.
echo  📚 Documentation:
echo     - STARTUP_PIPELINE.md - Complete startup guide
echo     - QUICK_REFERENCE.md  - Quick reference card
echo     - TESTING_CHECKLIST.md - Testing guide
echo.
pause

