# Quick Start Guide

## 🚀 Start the Backend in 3 Steps

### Step 1: Setup Virtual Environment (First Time Only)

Open **Command Prompt** (not PowerShell) and run:

```cmd
cd c:\Project\IntelligentOilfieldInsightPlatform
setup_venv.bat
```

This will:
- ✅ Create a virtual environment in `venv/`
- ✅ Install all Python dependencies
- ✅ Prepare the environment for running

**Note**: You only need to do this once!

### Step 2: Ensure Docker is Running

Make sure Docker Desktop is running on your machine.

### Step 3: Run the Backend

In **Command Prompt**, run:

```cmd
activate_and_run.bat
```

This will:
- ✅ Activate the virtual environment
- ✅ Check if Docker services are running
- ✅ Start databases if needed
- ✅ Start the FastAPI backend

## 🌐 Access the API

Once you see this message:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Open your browser to:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🧪 Test a Query

In the Swagger UI (http://localhost:8000/docs):

1. Click on `POST /api/query`
2. Click "Try it out"
3. Enter: `{"query": "Why is production dropping at Rig Alpha?"}`
4. Click "Execute"

## ❌ Troubleshooting

### "ERR_CONNECTION_REFUSED"

**Most Common Cause**: Virtual environment not activated or dependencies not installed

**Solution**:
```cmd
REM Step 1: Setup venv (if you haven't already)
setup_venv.bat

REM Step 2: Run with venv activated
activate_and_run.bat
```

### "Module not found" errors

**Cause**: Dependencies not installed in venv

**Solution**:
```cmd
venv\Scripts\activate.bat
pip install -r requirements.txt
```

### "Port already in use"

**Solution**:
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Backend starts but crashes immediately

**Check the error message** in the Command Prompt window. Common issues:
- Database not running: `docker-compose up -d postgres neo4j qdrant minio`
- Wrong Python version: Need Python 3.11+
- Missing .env file: `copy .env.example .env`

## 📋 Manual Steps (Alternative)

If the batch files don't work, here's the manual process:

```cmd
REM 1. Activate venv
venv\Scripts\activate.bat

REM 2. Start databases
docker-compose up -d postgres neo4j qdrant minio

REM 3. Wait for databases
timeout /t 30

REM 4. Start backend
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ Verification Checklist

Before starting the backend, verify:

- [ ] Docker Desktop is running
- [ ] Virtual environment exists: `venv\` folder present
- [ ] Dependencies installed: Run `venv\Scripts\pip.exe list`
- [ ] Port 8000 is free: `netstat -ano | findstr :8000` returns nothing
- [ ] Using Command Prompt (not PowerShell)

## 🎯 What You Should See

When the backend starts successfully:

```
INFO:     Will watch for changes in these directories: ['C:\\Project\\IntelligentOilfieldInsightPlatform\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Then you can access http://localhost:8000/docs

## 📚 More Help

- **Full Documentation**: See `STARTUP_GUIDE.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`

## 🆘 Still Having Issues?

1. Make sure you're using **Command Prompt**, not PowerShell
2. Check that the virtual environment is activated (you should see `(venv)` in your prompt)
3. Verify dependencies: `pip list | findstr fastapi`
4. Check Docker: `docker-compose ps`
5. Look for error messages in the terminal output

