# Neo4j Investigation Guide

## Current Status

Based on your output:
- ✅ PostgreSQL: Running (port 5433)
- ❌ **Neo4j: NOT in `docker-compose ps` output**
- ✅ Qdrant: Running (unhealthy but running)
- ✅ MinIO: Running

## Problem

**Neo4j container is not running!** When you ran `docker-compose up -d postgres neo4j qdrant minio`, it said "Started" but Neo4j is NOT in the `docker-compose ps` output.

This means Neo4j **started but immediately crashed**.

---

## Investigation Steps

### Step 1: Run Diagnostic Script

```bash
diagnose_neo4j.bat
```

This will check:
1. Container status
2. Neo4j logs (to see why it crashed)
3. Connection tests
4. Python packages

### Step 2: Check Neo4j Logs Manually

```bash
docker logs oilfield-neo4j --tail 50
```

**Common crash reasons:**
- Port 7474 or 7687 already in use
- Memory issues (needs 2GB heap)
- Corrupted data volume
- Plugin installation failed

### Step 3: Check if Neo4j container exists (stopped)

```bash
docker ps -a | findstr neo4j
```

If you see it with status "Exited", check the exit code.

---

## Quick Fixes

### Fix 1: Restart Neo4j

```bash
docker-compose restart neo4j
docker logs oilfield-neo4j --tail 30
```

### Fix 2: Recreate Neo4j (if corrupted)

```bash
# Stop and remove
docker-compose stop neo4j
docker-compose rm -f neo4j

# Remove old data volume
docker volume rm intelligentoilfieldinsightplatform_neo4j_data

# Start fresh
docker-compose up -d neo4j

# Wait 20 seconds
timeout /t 20

# Check logs
docker logs oilfield-neo4j --tail 30
```

### Fix 3: Check port conflicts

```bash
# Check if port 7474 is in use
netstat -ano | findstr :7474

# Check if port 7687 is in use
netstat -ano | findstr :7687
```

If ports are in use, kill the process or change ports in docker-compose.yml.

### Fix 4: Install Python packages

```bash
.\venv\Scripts\activate
pip install neo4j qdrant-client
```

---

## Automated Fix

Run this to fix everything:

```bash
fix_neo4j.bat
```

This will:
1. Install Python packages
2. Restart Neo4j
3. Wait for startup
4. Load graph data
5. Verify connection

---

## Manual Investigation Commands

### Check container status
```bash
docker ps -a | findstr neo4j
```

### Check logs
```bash
docker logs oilfield-neo4j --tail 50
```

### Check if Neo4j is responding
```bash
docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "RETURN 1"
```

### Check data volume
```bash
docker volume ls | findstr neo4j
```

### Inspect container
```bash
docker inspect oilfield-neo4j
```

---

## Expected Output After Fix

### `docker-compose ps` should show:
```
NAME                IMAGE                  COMMAND                  SERVICE    STATUS
oilfield-neo4j      neo4j:5.16-community   "tini -g -- /startup…"   neo4j      Up (healthy)
```

### `docker logs oilfield-neo4j` should show:
```
Started.
Remote interface available at http://localhost:7474/
Bolt enabled on localhost:7687
```

### Python test should show:
```python
{'postgres': True, 'neo4j': True, 'qdrant': True, 'minio': True}
```

---

## Next Steps After Fix

1. **Verify Neo4j has data:**
   ```bash
   docker exec oilfield-neo4j cypher-shell -u neo4j -p oilfield_neo4j_pass "MATCH (n) RETURN count(n)"
   ```
   Should return > 0 nodes.

2. **Restart backend:**
   ```bash
   cd backend
   ..\venv\Scripts\activate
   python main.py
   ```

3. **Test on main page:**
   - Query: "Show me all faulty equipment at Rig Alpha"
   - Should return results from Neo4j

---

## What to Report Back

Please run `diagnose_neo4j.bat` and share:
1. The full output
2. Specifically the Neo4j logs section
3. Any error messages

This will tell us exactly why Neo4j is crashing!

