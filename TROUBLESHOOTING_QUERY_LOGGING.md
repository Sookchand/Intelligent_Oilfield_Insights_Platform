# 🔧 Troubleshooting: Query Logging Not Working

## ❌ **Problem**

Queries are not appearing in the history page at http://localhost:3002/history

---

## 🔍 **Diagnosis Steps**

### **Step 1: Check if Backend is Running**

```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000
```

**Expected:** Should show a process listening on port 8000

**If not running:**
```bash
cd backend
python main.py
```

---

### **Step 2: Check Backend Logs**

When you start the backend, you should see:

```
✅ Connected to PostgreSQL
✅ Connected to Neo4j  
✅ Connected to Qdrant
✅ Query audit logger initialized
✅ Audit log table verified/created
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**If you see:**
```
❌ Failed to initialize audit logger: connection to server at "localhost" failed
```

**Then:** PostgreSQL is not connected or credentials are wrong.

---

### **Step 3: Test Backend API**

```bash
# Test if backend is responding
curl http://localhost:8000/api/status/databases
```

**Expected Response:**
```json
{
  "postgresql": {"status": "connected"},
  "neo4j": {"status": "connected"},
  "qdrant": {"status": "connected"}
}
```

---

### **Step 4: Submit a Test Query**

1. Go to http://localhost:3002
2. Type: "Why is production declining?"
3. Click Submit
4. Wait for the answer

**Check backend logs for:**
```
✅ Query logged to audit trail (ID: 1)
```

---

### **Step 5: Check History Page**

1. Navigate to http://localhost:3002/history
2. Your query should appear in the table

**If not appearing:**
- Check browser console for errors
- Check backend logs for audit logging errors
- Verify PostgreSQL connection

---

## 🔧 **Common Issues & Fixes**

### **Issue 1: PostgreSQL Not Connected**

**Symptoms:**
- Backend logs show: `❌ Failed to initialize audit logger`
- History page shows: "No queries logged yet"

**Fix:**

1. **Check PostgreSQL is running:**
   ```bash
   # Windows
   Get-Service -Name postgresql*
   
   # Should show "Running"
   ```

2. **Check credentials in `.env`:**
   ```bash
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=oilfield_insights
   POSTGRES_USER=oilfield_user
   POSTGRES_PASSWORD=your_password
   ```

3. **Test connection manually:**
   ```bash
   psql -h localhost -U oilfield_user -d oilfield_insights
   ```

---

### **Issue 2: Audit Table Doesn't Exist**

**Symptoms:**
- Backend logs show: `❌ Error creating audit table`
- Queries fail to log

**Fix:**

1. **Check if migration file exists:**
   ```bash
   ls backend/database/migrations/001_create_audit_log.sql
   ```

2. **Run migration manually:**
   ```bash
   psql -h localhost -U oilfield_user -d oilfield_insights -f backend/database/migrations/001_create_audit_log.sql
   ```

3. **Verify table exists:**
   ```sql
   \dt query_audit_log
   ```

---

### **Issue 3: Backend Running But Not Logging**

**Symptoms:**
- Backend is running
- Queries work on main page
- But nothing appears in history

**Fix:**

1. **Check audit_logger initialization:**
   
   Look for this in backend logs:
   ```
   ✅ Query audit logger initialized
   ```

2. **If not initialized, check PostgreSQL connection**

3. **Restart backend:**
   ```bash
   # Stop backend (Ctrl+C)
   # Start again
   python backend/main.py
   ```

---

### **Issue 4: Frontend Not Calling Backend**

**Symptoms:**
- No network requests in browser DevTools
- No backend logs when submitting query

**Fix:**

1. **Check API base URL in `frontend/lib/api.ts`:**
   ```typescript
   const api = axios.create({
     baseURL: 'http://localhost:8000',
   });
   ```

2. **Check CORS settings in backend:**
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3002"],
   )
   ```

3. **Check browser console for CORS errors**

---

## 🧪 **Manual Testing**

### **Test 1: Direct API Call**

```bash
# Submit a query directly to backend
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Why is production declining?"}'
```

**Expected:** Should return a JSON response with answer and reasoning

---

### **Test 2: Check Audit History**

```bash
# Get query history from backend
curl http://localhost:8000/api/audit/history?limit=10
```

**Expected:** Should return list of queries

---

### **Test 3: Query Database Directly**

```sql
-- Connect to PostgreSQL
psql -h localhost -U oilfield_user -d oilfield_insights

-- Check if table exists
\dt query_audit_log

-- Count rows
SELECT COUNT(*) FROM query_audit_log;

-- View recent queries
SELECT id, query_text, timestamp, status 
FROM query_audit_log 
ORDER BY timestamp DESC 
LIMIT 10;
```

---

## ✅ **Quick Fix Checklist**

- [ ] PostgreSQL is running
- [ ] Backend is running on port 8000
- [ ] Backend logs show "✅ Query audit logger initialized"
- [ ] Audit table exists in database
- [ ] Frontend is running on port 3002
- [ ] No CORS errors in browser console
- [ ] Test query submitted successfully
- [ ] Query appears in backend logs
- [ ] Query appears in history page

---

## 🚨 **Emergency Workaround**

If you can't get PostgreSQL working for the demo:

### **Option 1: Use Mock Data**

Modify `frontend/app/history/page.tsx` to show mock data:

```typescript
const mockQueries = [
  {
    id: 1,
    query_text: "Why is production declining at Rig Alpha?",
    timestamp: new Date().toISOString(),
    confidence_score: 0.94,
    status: "success",
    processing_time_ms: 1247,
    data_sources_used: ["PostgreSQL", "Neo4j", "Qdrant"],
    result_summary: "Production decline due to equipment failure"
  },
  // Add more mock queries...
];

// In fetchQueryHistory:
setQueries(mockQueries);
```

### **Option 2: Show Pre-recorded Demo**

Have a video or screenshots ready showing:
- Query being submitted
- Answer appearing
- History page with logged queries

---

## 📞 **Need Help?**

1. **Check backend logs** - Most issues show up here
2. **Check browser console** - Frontend errors appear here
3. **Check PostgreSQL logs** - Database connection issues
4. **Restart everything** - Sometimes fixes weird issues

---

**Most Common Fix:** Restart the backend after ensuring PostgreSQL is running!

