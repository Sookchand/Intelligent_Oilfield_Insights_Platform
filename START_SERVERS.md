# 🚀 Quick Start Guide - Intelligent Oilfield Insights Platform

## Prerequisites

- ✅ Docker Desktop running (for databases)
- ✅ Python 3.11+ installed
- ✅ Node.js 18+ installed
- ✅ Command Prompt (not PowerShell)

---

## Step 1: Start Database Services

Open **Command Prompt** and run:

```cmd
cd C:\Project\IntelligentOilfieldInsightPlatform
docker-compose up -d
```

**Verify databases are running:**

```cmd
docker ps
```

You should see 4 containers:

- PostgreSQL (port 5432)
- Neo4j (port 7687, 7474)
- Qdrant (port 6333)
- MinIO (port 9000, 9001)

---

## Step 2: Start Backend API Server

### Option A: Using Command Prompt (Recommended)

1. **Open a NEW Command Prompt window**
2. **Navigate to backend:**

   ```cmd
   cd C:\Project\IntelligentOilfieldInsightPlatform\backend
   ```

3. **Activate virtual environment:**

   ```cmd
   venv\Scripts\activate
   ```

4. **Start the server:**

   ```cmd
   uvicorn main:app --reload
   ```

5. **Verify it's running:**
   - You should see: `Uvicorn running on http://127.0.0.1:8000`
   - Open: <http://localhost:8000/docs> (FastAPI Swagger UI)

### Option B: Using the Batch File

1. Navigate to `backend` folder
2. Double-click `start-backend.bat` (if exists)

---

## Step 3: Start Frontend Development Server ✅ VERIFIED WORKING

### ⚠️ CRITICAL: Must Use Command Prompt (cmd.exe), NOT PowerShell

PowerShell will cause the Node.js process to exit immediately. Always use Command Prompt.

### Option A: Using Command Prompt (RECOMMENDED - 100% Working!)

1. **Open a NEW Command Prompt window**
   - Press `Win + R`
   - Type `cmd`
   - Press Enter

2. **Navigate to frontend:**

   ```cmd
   cd C:\Project\IntelligentOilfieldInsightPlatform\frontend
   ```

3. **Start the server:**

   ```cmd
   npm run dev
   ```

4. **Verify it's running:**
   - You should see: `✓ Ready in 2.9s`
   - **IMPORTANT:** The terminal should **stay open** (NOT return to prompt)
   - If it returns to prompt, you're using PowerShell - close it and use cmd.exe
   - Open: <http://localhost:3000>

5. **Confirm it's working:**
   - ✅ Page shows "All Systems Operational"
   - ✅ All 4 databases show "Connected" (green status)
   - ✅ Demo query cards are visible and clickable
   - ✅ Query input box is ready

### Option B: Using the Batch File

1. Open File Explorer
2. Navigate to `C:\Project\IntelligentOilfieldInsightPlatform\frontend`
3. **Double-click** `start-dev.bat`
4. A Command Prompt window will open automatically
5. Wait for "✓ Ready" message
6. Open browser to <http://localhost:3000>

---

## Step 4: Access the Application

### Frontend (User Interface)

- **URL**: <http://localhost:3000>
- **Pages**:
  - `/` - Query Dashboard
  - `/explainability` - AI Explainability Dashboard
  - `/business` - Business Impact (placeholder)
  - `/data` - Data Explorer (placeholder)
  - `/system` - System Monitor (placeholder)

### Backend (API Documentation)

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>
- **Health Check**: <http://localhost:8000/health>

### Database UIs

- **Neo4j Browser**: <http://localhost:7474>
  - Username: `neo4j`
  - Password: `password123`
- **MinIO Console**: <http://localhost:9001>
  - Username: `minioadmin`
  - Password: `minioadmin`

---

## Quick Test

1. **Open**: <http://localhost:3000>
2. **Click a demo query** like "Why is production dropping at Rig Alpha?"
3. **Click "Ask AI"**
4. **View the results** with full explainability
5. **Click "View Explainability"** to see the detailed reasoning trace

---

## Stopping the Servers

### Stop Frontend

- Press `Ctrl + C` in the Command Prompt running the frontend

### Stop Backend

- Press `Ctrl + C` in the Command Prompt running the backend

### Stop Databases

```cmd
cd C:\Project\IntelligentOilfieldInsightPlatform
docker-compose down
```

---

## Troubleshooting

### "Port already in use" Error

**Frontend (port 3000):**

```cmd
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Backend (port 8000):**

```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### "Module not found" Error

**Backend:**

```cmd
cd backend
pip install -r requirements.txt
```

**Frontend:**

```cmd
cd frontend
npm install
```

### Database Connection Error

**Check if Docker is running:**

```cmd
docker ps
```

**Restart databases:**

```cmd
docker-compose down
docker-compose up -d
```

### PowerShell Issues

**Always use Command Prompt (cmd.exe), NOT PowerShell!**

The Python virtual environment activation doesn't work properly in PowerShell.

---

## Development Workflow

### Making Backend Changes

1. Edit Python files in `backend/`
2. Server auto-reloads (thanks to `--reload` flag)
3. Test at <http://localhost:8000/docs>

### Making Frontend Changes

1. Edit TypeScript/React files in `frontend/`
2. Browser auto-refreshes (hot reload)
3. View at <http://localhost:3000>

### Adding Dependencies

**Backend:**

```cmd
cd backend
pip install <package-name>
pip freeze > requirements.txt
```

**Frontend:**

```cmd
cd frontend
npm install <package-name>
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Browser                              │
│                  http://localhost:3000                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Next.js Frontend (Port 3000)                    │
│  - Query Dashboard                                           │
│  - Explainability Dashboard                                  │
│  - Business Impact (placeholder)                             │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                     │
│  - Multi-Agent System                                        │
│  - Business Metrics                                          │
│  - Query Processing                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┬──────────────┐
         ▼               ▼               ▼              ▼
    PostgreSQL        Neo4j          Qdrant         MinIO
    (Port 5432)    (Port 7687)    (Port 6333)   (Port 9000)
```

---

## Next Steps

1. ✅ Start all services using this guide
2. ✅ Test the Query Dashboard
3. ✅ Explore the Explainability features
4. ✅ Review the API documentation
5. 🚧 Implement placeholder pages (Business/Data/System)
6. 🚧 Add authentication
7. 🚧 Deploy to production

---

**Need Help?** Check the README files in `backend/` and `frontend/` directories.
