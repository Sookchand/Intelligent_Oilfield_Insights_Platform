# 🔧 Fix Database Connectivity Status

## **Current Issue**: Database indicators showing RED (not connected)

---

## ✅ **Solution: Start the Databases**

### **Step 1: Run the Database Startup Script**

In a **NEW terminal** (or PowerShell), run:

```cmd
START_DATABASES.bat
```

This will:
- ✅ Start PostgreSQL on port 5433
- ✅ Start Neo4j on ports 7474 and 7687
- ✅ Start Qdrant on port 6333
- ✅ Start MinIO on ports 9002 and 9003
- ✅ Wait 30 seconds for initialization
- ✅ Show you the status

**Wait for the script to complete!**

---

### **Step 2: Restart the Backend**

Once databases are running:

1. **Go to your backend terminal** (where you ran `python main.py`)
2. **Press Ctrl+C** to stop the backend
3. **Run it again**:
   ```powershell
   python main.py
   ```

You should now see **successful** database connections in the logs!

---

### **Step 3: Refresh the Frontend**

1. Go to your browser at http://localhost:3002
2. **Refresh the page** (F5 or Ctrl+R)
3. The database connectivity indicators should now be **GREEN** ✅

---

## 🐳 **If You Don't Have Docker**

### **Install Docker Desktop**:

1. Download from: https://www.docker.com/products/docker-desktop
2. Install and start Docker Desktop
3. Wait for Docker to fully start (whale icon in system tray)
4. Run `START_DATABASES.bat` again

---

## 🧪 **Verify Databases are Running**

### **Check Docker containers**:

```powershell
docker-compose ps
```

You should see:
- ✅ oilfield-postgres (healthy)
- ✅ oilfield-neo4j (healthy)
- ✅ oilfield-qdrant (healthy)
- ✅ oilfield-minio (healthy)

---

### **Test PostgreSQL**:

```powershell
docker exec -it oilfield-postgres psql -U oilfield_user -d oilfield_production -c "SELECT COUNT(*) FROM rigs;"
```

Should return a count of rigs.

---

### **Test Neo4j**:

Open browser: http://localhost:7474

- Username: `neo4j`
- Password: `oilfield_neo4j_pass`

Run query: `MATCH (n) RETURN count(n)`

---

### **Test Qdrant**:

```powershell
Invoke-WebRequest -Uri http://localhost:6333/health -UseBasicParsing
```

Should return: `{"status":"ok"}`

---

### **Test MinIO**:

Open browser: http://localhost:9003

- Username: `minio_admin`
- Password: `minio_admin_pass`

---

## 📊 **Expected Backend Logs After Restart**

Once you restart the backend with databases running, you should see:

```
INFO - Testing PostgreSQL connection...
INFO - PostgreSQL connection successful ✅
INFO - Testing Neo4j connection...
INFO - Neo4j connection successful ✅
INFO - Testing Qdrant connection...
INFO - Qdrant connection successful ✅
INFO - Testing MinIO connection...
INFO - MinIO connection successful ✅
```

---

## 🎯 **Frontend Dashboard Should Show**

After refreshing the frontend:

- ✅ PostgreSQL: Connected (GREEN)
- ✅ Neo4j: Connected (GREEN)
- ✅ Qdrant: Connected (GREEN)
- ✅ MinIO: Connected (GREEN)

---

## 🚨 **Troubleshooting**

### **Error: "Docker daemon is not running"**

1. Open Docker Desktop
2. Wait for it to fully start
3. Run `START_DATABASES.bat` again

---

### **Error: "Port already in use"**

Check what's using the ports:

```powershell
# Check port 5433 (PostgreSQL)
Get-NetTCPConnection -LocalPort 5433 -ErrorAction SilentlyContinue

# Check port 7687 (Neo4j)
Get-NetTCPConnection -LocalPort 7687 -ErrorAction SilentlyContinue
```

If something is using these ports, either:
- Stop that service, OR
- Change the ports in `docker-compose.yml`

---

### **Error: "Container already exists"**

Stop and remove old containers:

```powershell
docker-compose down
docker-compose up -d postgres neo4j qdrant minio
```

---

### **Databases start but backend still can't connect**

Check the backend `.env` file has correct ports:

```
POSTGRES_PORT=5433
NEO4J_URI=bolt://localhost:7687
QDRANT_PORT=6333
MINIO_ENDPOINT=localhost:9002
```

---

## 🎬 **Complete Startup Sequence**

### **Terminal 1: Databases**
```cmd
START_DATABASES.bat
```
Wait for completion.

---

### **Terminal 2: Backend**
```powershell
cd backend
python main.py
```
Wait for "Uvicorn running on http://0.0.0.0:8000"

---

### **Terminal 3: Frontend**
```powershell
cd frontend
npm run dev
```
Wait for "ready started server on 0.0.0.0:3002"

---

### **Browser**
Open: http://localhost:3002

**All database indicators should be GREEN!** ✅

---

## ✅ **Success Checklist**

- [ ] Docker Desktop is running
- [ ] `docker-compose ps` shows 4 healthy containers
- [ ] Backend logs show successful database connections
- [ ] Frontend shows GREEN database indicators
- [ ] Can submit queries and get answers
- [ ] Explainability page works

---

## 🎯 **You're Production-Ready!**

Once all databases are connected:
- ✅ Real PostgreSQL data
- ✅ Real Neo4j graph queries
- ✅ Real vector search with Qdrant
- ✅ Real document storage with MinIO
- ✅ Full explainability with actual queries
- ✅ Production-grade demo system

**Ready to impress! 🚀**

