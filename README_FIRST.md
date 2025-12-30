# 🚀 Getting Started - READ THIS FIRST!

## The Issue You're Experiencing

You're seeing **"ERR_CONNECTION_REFUSED"** because the backend isn't running. This is happening because:

1. ❌ The virtual environment wasn't activated
2. ❌ Dependencies aren't installed in the venv
3. ❌ You might be using PowerShell (which doesn't work well with Python venvs)

## ✅ The Solution (3 Simple Steps)

### Step 1: Open Command Prompt (NOT PowerShell!)

- Press `Win + R`
- Type `cmd`
- Press Enter

### Step 2: Setup the Virtual Environment (First Time Only)

```cmd
cd c:\Project\IntelligentOilfieldInsightPlatform
setup_venv.bat
```

Wait for it to finish installing all dependencies (~2-3 minutes).

### Step 3: Start the Backend

```cmd
activate_and_run.bat
```

This will:
- ✅ Activate the virtual environment
- ✅ Start Docker databases
- ✅ Start the FastAPI backend

### Step 4: Open Your Browser

Once you see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Go to: **http://localhost:8000/docs**

## 🎯 What You Should See

The Swagger UI should load with all the API endpoints:
- `GET /health` - Health check
- `POST /api/query` - Natural language queries
- `GET /api/status/databases` - Database status
- And more...

## 🧪 Test It

1. In Swagger UI, click `POST /api/query`
2. Click "Try it out"
3. Enter:
   ```json
   {
     "query": "Why is production dropping at Rig Alpha?"
   }
   ```
4. Click "Execute"

You should get a JSON response with analysis, reasoning trace, and confidence score!

## ❌ Still Not Working?

### Check 1: Is the venv activated?

Your command prompt should show `(venv)` at the beginning:
```
(venv) C:\Project\IntelligentOilfieldInsightPlatform>
```

If not, run:
```cmd
venv\Scripts\activate.bat
```

### Check 2: Are dependencies installed?

```cmd
venv\Scripts\pip.exe list | findstr fastapi
```

Should show:
```
fastapi                       0.115.6
```

If not, run:
```cmd
venv\Scripts\pip.exe install -r requirements.txt
```

### Check 3: Is Docker running?

```cmd
docker-compose ps
```

Should show all services running. If not:
```cmd
docker-compose up -d postgres neo4j qdrant minio
```

### Check 4: Is port 8000 free?

```cmd
netstat -ano | findstr :8000
```

Should return nothing. If something is using it:
```cmd
taskkill /PID <PID> /F
```

## 📁 Important Files

- **`setup_venv.bat`** - Sets up virtual environment (run once)
- **`activate_and_run.bat`** - Starts the backend (run every time)
- **`QUICK_START.md`** - Detailed quick start guide
- **`STARTUP_GUIDE.md`** - Comprehensive documentation

## 🎓 Understanding the Project

This is an **Intelligent Oilfield Insights Platform** with:

- **Backend**: FastAPI with multi-agent reasoning system
- **Databases**: PostgreSQL (structured data), Neo4j (graph), Qdrant (vectors), MinIO (files)
- **Frontend**: Next.js dashboard (to be built)

The backend uses AI agents to:
1. Parse natural language queries
2. Query SQL and graph databases
3. Perform vector similarity search
4. Reason about the results
5. Generate comprehensive answers

## 🔄 Daily Workflow

Every time you want to work on the project:

1. Open **Command Prompt**
2. Run `activate_and_run.bat`
3. Wait for "Uvicorn running..."
4. Open http://localhost:8000/docs
5. Start coding/testing!

To stop:
- Press `Ctrl+C` in the Command Prompt window

## 📞 Need More Help?

See the detailed guides:
- **Quick Start**: `QUICK_START.md`
- **Full Startup Guide**: `STARTUP_GUIDE.md`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`

---

**TL;DR**: Run `setup_venv.bat` once, then `activate_and_run.bat` every time. Use Command Prompt, not PowerShell!

