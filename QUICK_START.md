# Quick Start Guide

## 🚀 **TL;DR - Get Started in 3 Minutes**

```bash
# 1. Start databases
docker-compose up -d postgres neo4j qdrant minio
timeout /t 60

# 2. ⚠️ CRITICAL: Seed Neo4j with data (REQUIRED!)
docker exec -i oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass < data\seed_graph.cypher

# 3. Start backend (in new terminal, with venv activated)
venv\Scripts\activate
cd backend
python main.py

# 4. Start frontend (in another new terminal)
cd frontend
npm run dev

# 5. Open browser: http://localhost:3002
```

**That's it!** If you encounter issues, see the detailed troubleshooting sections below.

---

## ⚠️ **CRITICAL: Neo4j Must Be Seeded With Data**

After starting Neo4j for the first time, you **MUST** run this command to load the graph data:

```bash
docker exec -i oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass < data\seed_graph.cypher
```

**Without this step, the system will not work!** The backend will show "Neo4j: Connected" but queries will return no results.

---

## 🔄 RESTART BACKEND TO APPLY FIXES

### Latest Fix Applied

✅ **Follow-Up Question Intelligent Formatting** - Follow-up questions now return natural language answers instead of "Result: min"

### Step-by-Step Instructions

## **STEP 1: Start Databases First** ⚠️ IMPORTANT - Do this FIRST

1. **Open a terminal/command prompt**
2. **Navigate to the project**:

   ```bash
   cd C:\Project\IntelligentOilfieldInsightPlatform
   ```

3. **Start all databases**:

   ```bash
   docker-compose up -d postgres neo4j qdrant minio
   ```

4. **Wait 60 seconds for databases to initialize** (especially Neo4j):

   ```bash
   timeout /t 60
   ```

5. **Verify databases are running**:

   ```bash
   docker-compose ps
   ```

   You should see all 4 containers as "healthy":
   - ✅ oilfield-postgres (healthy)
   - ✅ oilfield-neo4j (healthy)
   - ✅ oilfield-qdrant (healthy or unhealthy - both OK)
   - ✅ oilfield-minio (healthy)

6. **⚠️ CRITICAL: Seed Neo4j with data** (Required for first-time setup):

   ```bash
   docker exec -i oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass < data\seed_graph.cypher
   ```

   **Expected output**: You should see "Added X labels, created Y nodes, set Z properties..."

   **If you get an error**: Neo4j might not be fully initialized yet. Wait 30 more seconds and try again.

---

## **STEP 2: Start Backend**

1. **Open a NEW terminal** (keep the first one open)

2. **Navigate to the project**:

   ```bash
   cd C:\Project\IntelligentOilfieldInsightPlatform
   ```

3. **Activate virtual environment**:

   ```bash
   venv\Scripts\activate
   ```

4. **Go to backend folder**:

   ```bash
   cd backend

   ```

5. **Start the backend**:

    ```bash
    python main.py
    ```

    **OR** to enable LangSmith LLMOps tracing:

    ```bash
    cd ..
    restart_with_langsmith.bat
    ```

6. **Wait for these messages**:

    ```log
    ✅ LangSmith LLMOps Enabled!  (if using restart_with_langsmith.bat)
    INFO:     Started server process [12345]
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://0.0.0.0:8000
    ```

    ⚠️ **Keep this terminal open!**

---

## **STEP 3: Start Frontend**

1. **Open a NEW terminal** (third terminal)

2. **Navigate to the project**:

    ```bash
    cd C:\Project\IntelligentOilfieldInsightPlatform
    ```

3. **Go to frontend folder**:

    ```bash
    cd frontend
    ```

4. **Start the frontend**:

    ```bash
    npm run dev
    ```

5. **Wait for this message**:

    ```log
    ✓ Ready in X.Xs
    - Local: http://localhost:3002
    ```

    ⚠️ **Keep this terminal open!**

---

## **STEP 4: Verify Everything is Working**

1. **Open browser** and go to: <http://localhost:3002>

2. **Check database connectivity** - All 4 indicators should turn **GREEN** after first query:
    - ✅ PostgreSQL: Connected
    - ✅ Neo4j: Connected
    - ✅ Qdrant: Connected
    - ✅ MinIO: Connected

    **Note:** Databases connect on-demand, so they may show as "not connected" until you run your first query.

3. **Test a query** in the dashboard:

    ```text
    Why is production dropping at Rig Alpha?
    ```

4. **You should get a detailed answer!** ✅

---

## 🚨 **Troubleshooting**

### **Neo4j Quick Diagnostic Checklist** ✅

Run these commands in order to diagnose Neo4j issues:

```bash
# 1. Is Neo4j container running?
docker ps --filter "name=oilfield-neo4j"
# Expected: STATUS shows "Up" and "(healthy)"

# 2. Can we connect to Neo4j?
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1 as test"
# Expected: "1" returned

# 3. Does Neo4j have data?
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (n) RETURN count(n) as node_count"
# Expected: node_count > 0 (should be around 50-100 nodes)

# 4. If node_count is 0, seed the data:
docker exec -i oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass < data\seed_graph.cypher
# Expected: "Added X labels, created Y nodes..."
```

---

### **If Neo4j shows OFFLINE (red) or "No data found"**

**Common Issue**: Neo4j container is running but has no data seeded.

**Solution - Seed Neo4j with data**:

```bash
# Step 1: Verify Neo4j is running
docker ps --filter "name=oilfield-neo4j"

# Step 2: Wait for Neo4j to fully initialize (if just started)
timeout /t 30

# Step 3: Test connection
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1 as test"

# Step 4: Seed with data (CRITICAL STEP)
docker exec -i oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass < data\seed_graph.cypher

# Step 5: Verify data was loaded
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (n) RETURN count(n) as node_count"

# Step 6: Restart backend (Ctrl+C in backend terminal, then python main.py)
```

**If Neo4j container keeps exiting**:

```bash
# Step 1: Remove the broken container
docker rm -f oilfield-neo4j

# Step 2: Remove the data volume (fresh start)
docker volume rm intelligentoilfieldinsightplatform_neo4j_data

# Step 3: Recreate Neo4j
docker-compose up -d neo4j

# Step 4: Wait 60 seconds for initialization
timeout /t 60

# Step 5: Seed with data
docker exec -i oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass < data\seed_graph.cypher
```

### **If databases won't start**

```bash
# Stop everything
docker-compose down

# Remove Neo4j data volume (if corrupted)
docker volume rm intelligentoilfieldinsightplatform_neo4j_data

# Start fresh
docker-compose up -d postgres neo4j qdrant minio

# Wait 60 seconds
timeout /t 60
```

### **Quick Status Check**

```bash
# Check what's running
docker-compose ps

# Check Neo4j logs
docker logs oilfield-neo4j --tail 30

# Test Neo4j connection
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1"
```

---

## 🎯 **Quick Startup (After First Time)**

Once everything is set up, you can use these shortcuts:

### **Terminal 1 - Databases**

```bash
docker-compose up -d
```

### **Terminal 2 - Backend**

```bash
venv\Scripts\activate
cd backend
python main.py
```

### **Terminal 3 - Frontend**

```bash
cd frontend
npm run dev
```

Then open: <http://localhost:3002>

---

## 🛑 **Shutdown**

To stop everything:

```bash
# Stop databases
docker-compose down

# Stop backend: Press Ctrl+C in backend terminal
# Stop frontend: Press Ctrl+C in frontend terminal
```

---

## 🧪 Test Follow-Up Questions

### In the Frontend (<http://localhost:3002>)

#### Test 1: Production Drop Query + Follow-Up

1. **Ask**: "Why is production dropping at Rig Alpha?"
2. **Expected**: Answer mentions production drop and faulty equipment
3. **Click**: "When did it start?" (quick follow-up button)
4. **Expected**: "It started on [formatted date and time]" ✅

#### Test 2: Equipment Query + Follow-Up

1. **Ask**: "Show me all faulty equipment at Rig Alpha"
2. **Expected**: Lists faulty equipment (Gauge G-40, etc.)
3. **Click**: "What caused this?" (quick follow-up button)
4. **Expected**: Analyzes root cause ✅

#### Test 3: Direct Time Query

1. **Ask**: "When did production first drop below 850 barrels per day for Rig Alpha?"
2. **Expected**: "It started on January 15, 2024 at 02:30 PM" ✅

---

## ✅ What to Look For

### In the Backend Logs

```log
✅ Extracted follow-up question: When did it start?
✅ Extracted rigs from context: ['Rig Alpha']
🤖 Using AI-powered query generation (follow-up question)
✅ Query type determined: sql
✅ Generated SQL query: SELECT MIN(timestamp) FROM production_data WHERE...
✅ Converted PostgreSQL parameters to psycopg2 format
✅ SQL query returned 1 records
✅ AI-formatted answer: It started on January 15, 2024...
```

### In the Frontend

- ✅ Natural language answers (not "Result: min")
- ✅ Formatted dates like "January 15, 2024 at 02:30 PM"
- ✅ Formatted numbers like "1,234.56"
- ✅ All quick follow-up buttons work correctly
- ✅ No errors about "$1" parameters

---

## 🚀 Complete System Startup (Recommended)

### Prerequisites

- ✅ Docker Desktop is running
- ✅ Python 3.11+ installed
- ✅ Node.js 18+ installed (for frontend)

### One-Command Startup (PowerShell)

The easiest way to start the entire system:

```powershell
.\start_system.ps1
```

This will:

- ✅ Start all database containers (PostgreSQL, Neo4j, Qdrant, MinIO)
- ✅ Wait for databases to initialize (15 seconds)
- ✅ Start the FastAPI backend on port 8000
- ✅ Start the Next.js frontend on port 3002

**Access Points:**

- **Frontend UI**: <http://localhost:3002>
- **Backend API**: <http://localhost:8000>
- **API Docs**: <http://localhost:8000/docs>
- **Neo4j Browser**: <http://localhost:7474>

---

## 🔧 Manual Startup (Step-by-Step)

If you prefer to start components individually or troubleshoot:

### Step 1: Setup Virtual Environment (First Time Only)

Open **PowerShell** and run:

```powershell
cd c:\Project\IntelligentOilfieldInsightPlatform
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 2: Start Database Containers

```powershell
docker-compose up -d postgres neo4j qdrant minio
```

**Wait 30 seconds** for databases to initialize, especially Neo4j.

### Step 3: Verify Database Status

```powershell
docker ps --filter "name=oilfield"
```

All containers should show "Up" status and "(healthy)" or "(health: starting)".

**Important**: If Neo4j shows "Exited", restart it:

```powershell
docker rm -f oilfield-neo4j
docker-compose up -d neo4j
Start-Sleep -Seconds 30
```

### Step 4: Start Backend

```powershell
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 5: Start Frontend (New Terminal)

```powershell
cd frontend
npm run dev
```

## 🌐 Access the System

Once all services are running:

- **Frontend UI**: <http://localhost:3000>
- **Backend API**: <http://localhost:8000>
- **API Documentation**: <http://localhost:8000/docs>
- **Health Check**: <http://localhost:8000/health>
- **Neo4j Browser**: <http://localhost:7474> (user: neo4j, password: oilfield123)

## 🧪 Test the System

### Option 1: Use the Frontend UI

1. Open <http://localhost:3000>
2. Click any demo query button
3. View the AI-generated response with reasoning trace

### Option 2: Use the API Directly

Run the test script:

```powershell
python test_backend.py
```

Or use Swagger UI at <http://localhost:8000/docs>:

1. Click on `POST /api/query`
2. Click "Try it out"
3. Enter: `{"query": "Why is production dropping at Rig Alpha?"}`
4. Click "Execute"

## ❌ Troubleshooting

### Neo4j Shows "Disconnected" in Frontend

**Cause**: Neo4j container failed to start or exited with error

**Solution**:

```powershell
# Remove and recreate Neo4j container
docker rm -f oilfield-neo4j
docker-compose up -d neo4j

# Wait for it to initialize (important!)
Start-Sleep -Seconds 30

# Verify it's running
docker ps --filter "name=oilfield-neo4j"
```

You should see status: "Up X seconds (healthy)"

### "ERR_CONNECTION_REFUSED" on Backend

**Cause**: Backend not running or virtual environment not activated

**Solution**:

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Start backend
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### "Module not found" Errors

**Cause**: Dependencies not installed in virtual environment

**Solution**:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "Port already in use"

**Solution**:

```powershell
# Find process using the port
netstat -ano | findstr :8000

# Kill the process (replace <PID> with actual process ID)
taskkill /PID <PID> /F
```

### Frontend Not Loading

**Cause**: Frontend server not started or wrong port

**Solution**:

```powershell
cd frontend
npm install  # First time only
npm run dev
```

Frontend should start on <http://localhost:3000>

### Database Connection Errors

**Check all databases are running**:

```powershell
docker ps --filter "name=oilfield"
```

Expected output:

- `oilfield-postgres` - Up (healthy)
- `oilfield-neo4j` - Up (healthy)
- `oilfield-qdrant` - Up
- `oilfield-minio` - Up (healthy)

**Restart all databases**:

```powershell
docker-compose down
docker-compose up -d postgres neo4j qdrant minio
Start-Sleep -Seconds 30
```

## ✅ Verification Checklist

Before starting the system, verify:

- [ ] Docker Desktop is running
- [ ] Virtual environment exists: `venv\` folder present
- [ ] Dependencies installed: `pip list | findstr fastapi`
- [ ] Ports are free: 8000 (backend), 3000 (frontend), 5433 (postgres), 7474/7687 (neo4j)
- [ ] All database containers are healthy: `docker ps`

## 🎯 What You Should See

### Successful Backend Startup

```log
INFO:     Will watch for changes in these directories: ['C:\\Project\\IntelligentOilfieldInsightPlatform\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Successful Frontend Startup

```log
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
- event compiled client and server successfully
```

### Healthy Database Status

```powershell
docker ps --filter "name=oilfield"
```

All containers should show:

- STATUS: "Up X minutes (healthy)" or "Up X minutes (health: starting)"
- PORTS: Properly mapped

## 📚 Additional Resources

- **Full Documentation**: See `STARTUP_GUIDE.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **Architecture**: See `ARCHITECTURE.md`

## 🆘 Still Having Issues?

1. **Check Docker**: `docker-compose ps` - all services should be "Up"
2. **Check Logs**: `docker logs oilfield-neo4j` (or other container name)
3. **Verify Python**: `python --version` (should be 3.11+)
4. **Verify Node**: `node --version` (should be 18+)
5. **Check virtual environment**: You should see `(venv)` in your prompt
6. **Test backend**: `python test_backend.py`
7. **Restart everything**: Use `start_system.ps1` for a fresh start

## 🔄 Clean Restart

If everything is broken, do a complete restart:

```powershell
# Stop all services
docker-compose down

# Remove Neo4j container (if problematic)
docker rm -f oilfield-neo4j

# Start fresh
.\start_system.ps1
```
