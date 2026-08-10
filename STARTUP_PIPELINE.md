# 🚀 Startup Pipeline - Complete System

**From Zero to Running in 5 Minutes**

---

## 📋 Prerequisites Check

Before starting, verify you have:
- [ ] Docker Desktop running
- [ ] Command Prompt (cmd.exe) ready - **NOT PowerShell**
- [ ] Project location: `C:\Project\IntelligentOilfieldInsightPlatform`

---

## ⚡ Complete Startup Pipeline

### 🎯 Terminal 1: Databases

**Open Command Prompt #1:**

```cmd
cd C:\Project\IntelligentOilfieldInsightPlatform
docker-compose up -d
```

**Wait 30 seconds**, then verify:
```cmd
docker ps
```

✅ **Success:** You should see 4 containers running

---

### 🎯 Terminal 2: Backend (with venv)

**Open Command Prompt #2:**

```cmd
cd C:\Project\IntelligentOilfieldInsightPlatform\backend
venv\Scripts\activate
uvicorn main:app --reload
```

✅ **Success:** You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Verify:** Open http://localhost:8000/docs in browser

---

### 🎯 Terminal 3: Frontend

**Open Command Prompt #3:**

```cmd
cd C:\Project\IntelligentOilfieldInsightPlatform\frontend
npm run dev
```

✅ **Success:** You should see:
```
✓ Ready in 2.9s
```

**IMPORTANT:** Terminal should **stay open** (not return to prompt)

**Verify:** Open http://localhost:3000 in browser

---

## ✅ Verification Checklist

### Step 1: Check Databases
Open: http://localhost:3000

You should see:
- ✅ "All Systems Operational" (green banner)
- ✅ PostgreSQL: Connected
- ✅ Neo4j: Connected
- ✅ Qdrant: Connected
- ✅ MinIO: Connected

### Step 2: Test a Query
1. Click demo query: "Why is production dropping at Rig Alpha?"
2. Click "Ask AI"
3. Wait 5-10 seconds
4. ✅ See AI response with reasoning

### Step 3: Check Explainability
1. Click "View Explainability" button
2. ✅ See agent workflow
3. ✅ See reasoning timeline
4. ✅ See SQL/Cypher queries

---

## 🛑 Shutdown Pipeline

### Stop in Reverse Order:

**Terminal 3 (Frontend):**
```cmd
Ctrl + C
```

**Terminal 2 (Backend):**
```cmd
Ctrl + C
deactivate
```

**Terminal 1 (Databases):**
```cmd
docker-compose down
```

---

## 🔧 One-Command Startup (Alternative)

If you want to start everything at once, use the master script:

**Double-click:** `START_ALL.bat`

This will:
1. ✅ Start Docker containers
2. ✅ Open Terminal 2 with backend (venv activated)
3. ✅ Open Terminal 3 with frontend
4. ✅ Open browser to http://localhost:3000

---

## 🐛 Quick Troubleshooting

### Issue: "venv not found"
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Port already in use"
```cmd
# Kill port 8000 (backend)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Kill port 3000 (frontend)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Issue: "Docker not running"
1. Open Docker Desktop
2. Wait for it to fully start
3. Try again

### Issue: Frontend exits immediately
❌ You're using PowerShell!
✅ Use Command Prompt (cmd.exe)

---

## 📊 Visual Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Start Databases (Terminal 1)                        │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ docker-compose up -d                                     │ │
│ │ ✅ PostgreSQL, Neo4j, Qdrant, MinIO running             │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Start Backend with venv (Terminal 2)                │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ cd backend                                               │ │
│ │ venv\Scripts\activate                                    │ │
│ │ uvicorn main:app --reload                                │ │
│ │ ✅ FastAPI running on http://localhost:8000             │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Start Frontend (Terminal 3)                         │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ cd frontend                                              │ │
│ │ npm run dev                                              │ │
│ │ ✅ Next.js running on http://localhost:3000             │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: Verify & Test                                       │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ ✅ All databases connected                              │ │
│ │ ✅ Demo queries working                                 │ │
│ │ ✅ Explainability dashboard functional                  │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## ⏱️ Expected Timeline

| Step | Action | Time | Status Check |
|------|--------|------|--------------|
| 1 | Start databases | 30s | `docker ps` shows 4 containers |
| 2 | Activate venv + start backend | 10s | http://localhost:8000/docs loads |
| 3 | Start frontend | 5s | Terminal shows "✓ Ready" |
| 4 | Verify system | 5s | http://localhost:3000 shows green status |
| **TOTAL** | **Full system running** | **~50s** | **All systems operational** |

---

## 🎯 Success Indicators

When everything is running correctly:

### Terminal 1 (Databases):
```
✅ Returned to prompt (containers running in background)
```

### Terminal 2 (Backend):
```
✅ Shows: "Uvicorn running on http://127.0.0.1:8000"
✅ Terminal stays open (process running)
✅ Shows: "Application startup complete"
```

### Terminal 3 (Frontend):
```
✅ Shows: "✓ Ready in 2.9s"
✅ Terminal stays open (process running)
✅ Does NOT return to prompt
```

### Browser (http://localhost:3000):
```
✅ Page loads
✅ "All Systems Operational" banner
✅ All 4 databases show "Connected" (green)
✅ Demo queries are clickable
```

---

## 📝 Quick Command Reference

```cmd
# Start everything
docker-compose up -d                    # Databases
cd backend && venv\Scripts\activate     # Activate venv
uvicorn main:app --reload               # Backend
cd frontend && npm run dev              # Frontend (in new terminal)

# Check status
docker ps                               # Database containers
curl http://localhost:8000/docs         # Backend API
curl http://localhost:3000              # Frontend

# Stop everything
Ctrl+C                                  # Stop backend/frontend
docker-compose down                     # Stop databases
```

---

## 🎉 You're Done!

Once all three terminals show success indicators:
1. ✅ Open http://localhost:3000
2. ✅ Try a demo query
3. ✅ Explore the explainability dashboard
4. ✅ Start building!

**Need help?** See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for troubleshooting.

