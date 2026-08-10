# 🔧 Fix Neo4j Showing Offline

## **Issue**: Neo4j shows offline/red on the homepage

From your terminal output, I can see:
- ✅ PostgreSQL: Running and healthy
- ✅ MinIO: Running and healthy
- ⚠️ Qdrant: Running but unhealthy (this is OK)
- ❌ **Neo4j: Started but not showing in status**

---

## ✅ **Quick Fix - Option 1: Restart Neo4j**

### **Run this command**:

```cmd
FIX_NEO4J.bat
```

This will:
1. Restart the Neo4j container
2. Wait 30 seconds for initialization
3. Test the connection
4. Seed the database with data

**Then restart your backend!**

---

## ✅ **Quick Fix - Option 2: Manual Restart**

### **Step 1: Restart Neo4j**

```powershell
docker restart oilfield-neo4j
```

### **Step 2: Wait 30 seconds**

Neo4j takes time to start up. Wait at least 30 seconds.

### **Step 3: Check if it's running**

```powershell
docker ps --filter "name=oilfield-neo4j"
```

You should see it with status "Up" and "(healthy)"

### **Step 4: Test the connection**

```powershell
# Test HTTP endpoint
Invoke-WebRequest -Uri http://localhost:7474 -UseBasicParsing

# Test Bolt endpoint
Test-NetConnection -ComputerName localhost -Port 7687
```

### **Step 5: Restart the backend**

Go to your backend terminal:
1. Press **Ctrl+C**
2. Run: `python main.py`

### **Step 6: Refresh the frontend**

In your browser at http://localhost:3002:
- Press **F5** or **Ctrl+R**
- Neo4j should now show **GREEN**

---

## 🔍 **Diagnostic: Check Neo4j Logs**

If Neo4j is still not working, check the logs:

```powershell
docker logs oilfield-neo4j --tail 50
```

Look for:
- ✅ "Started" or "Remote interface available"
- ❌ Any error messages about memory, ports, or configuration

---

## 🚨 **If Neo4j Keeps Failing**

### **Option A: Full Reset**

```powershell
# Stop all containers
docker-compose down

# Remove Neo4j data volume (this will delete Neo4j data)
docker volume rm intelligentoilfieldinsightplatform_neo4j_data

# Start Neo4j fresh
docker-compose up -d neo4j

# Wait 60 seconds
Start-Sleep -Seconds 60

# Check status
docker-compose ps neo4j
```

---

### **Option B: Check Port Conflicts**

Make sure nothing else is using ports 7474 or 7687:

```powershell
# Check port 7474 (HTTP)
Get-NetTCPConnection -LocalPort 7474 -ErrorAction SilentlyContinue

# Check port 7687 (Bolt)
Get-NetTCPConnection -LocalPort 7687 -ErrorAction SilentlyContinue
```

If something else is using these ports, you'll need to stop that service.

---

### **Option C: Increase Memory**

Neo4j might need more memory. Check Docker Desktop:
1. Open Docker Desktop
2. Go to Settings → Resources
3. Increase Memory to at least **4GB**
4. Click "Apply & Restart"
5. Run `docker-compose up -d neo4j` again

---

## 🧪 **Verify Neo4j is Working**

### **Test 1: HTTP Endpoint**

Open browser: http://localhost:7474

You should see the Neo4j Browser interface.

Login with:
- Username: `neo4j`
- Password: `oilfield_neo4j_pass`

---

### **Test 2: Run a Query**

In Neo4j Browser, run:

```cypher
MATCH (n) RETURN count(n) as total_nodes
```

If you get a number back, Neo4j is working!

---

### **Test 3: Check from Backend**

In your backend terminal, after restarting, look for:

```
INFO - Testing Neo4j connection...
INFO - Neo4j driver created
INFO - Neo4j connection successful ✅
```

Instead of connection errors.

---

## 📊 **Expected Status After Fix**

### **Docker Status**:
```powershell
docker-compose ps
```

Should show:
```
oilfield-neo4j   neo4j:5.16-community   Up X minutes (healthy)
```

---

### **Frontend Dashboard**:

All database indicators should be **GREEN**:
- ✅ PostgreSQL: Connected
- ✅ Neo4j: Connected
- ✅ Qdrant: Connected (or yellow if unhealthy, that's OK)
- ✅ MinIO: Connected

---

## 🎯 **Quick Commands Summary**

### **Restart Neo4j**:
```cmd
FIX_NEO4J.bat
```

### **Check Neo4j status**:
```powershell
docker ps --filter "name=oilfield-neo4j"
```

### **View Neo4j logs**:
```powershell
docker logs oilfield-neo4j --tail 50
```

### **Test Neo4j connection**:
```powershell
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1"
```

### **Full restart**:
```powershell
docker-compose restart neo4j
```

---

## ✅ **After Neo4j is Fixed**

1. **Restart backend**: Ctrl+C, then `python main.py`
2. **Refresh frontend**: F5 in browser
3. **Test a query**: Try "show me equipment at Rig Alpha"
4. **Check explainability**: Should show Cypher queries

---

## 💡 **Why This Happens**

Neo4j sometimes takes longer to start than other databases because:
- It needs to initialize the graph database
- It loads plugins (APOC, GDS)
- It allocates memory for the heap
- It verifies data integrity

**Solution**: Just give it more time (30-60 seconds) and restart if needed.

---

## 🎬 **You're Almost There!**

Once Neo4j shows green, your system will be **100% production-ready** with:
- ✅ Full graph query capabilities
- ✅ Asset hierarchy visualization
- ✅ Relationship-based queries
- ✅ Complete explainability with Cypher queries

Run `FIX_NEO4J.bat` and let me know what you see! 🚀

