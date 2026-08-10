# 🚀 START SYSTEM NOW - Manual Steps

## **Quick Start Guide**

Follow these steps in order. Keep each terminal window open!

---

## ✅ **Step 1: Start Backend** (Terminal 1)

### **In your current terminal** (where venv is activated):

```powershell
cd backend
python main.py
```

### **Expected Output**:
```
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
```

### **✅ Verification**:
Open a browser and go to: http://localhost:5001/api/health

Should see: `{"status": "healthy"}`

**⚠️ KEEP THIS TERMINAL OPEN! Don't close it!**

---

## ✅ **Step 2: Start Frontend** (Terminal 2)

### **Open a NEW PowerShell terminal**:
1. Press `Ctrl+Shift+`` (backtick) in VS Code to open new terminal
2. OR: Click the `+` button in the terminal panel

### **In the NEW terminal, run**:

```powershell
cd frontend
npm run dev
```

### **Expected Output**:
```
- ready started server on 0.0.0.0:3002, url: http://localhost:3002
- event compiled client and server successfully
```

### **✅ Verification**:
Open a browser and go to: http://localhost:3002

Should see: Dashboard with KPI cards and heat map

**⚠️ KEEP THIS TERMINAL OPEN TOO!**

---

## ✅ **Step 3: Verify All Services**

### **Check Backend**:
```powershell
# In a NEW terminal (Terminal 3)
Invoke-WebRequest -Uri http://localhost:5001/api/health -UseBasicParsing
```

Expected: Status 200 OK

### **Check Frontend**:
Open browser: http://localhost:3002

Expected: Dashboard loads

### **Check PostgreSQL**:
```powershell
psql -U postgres -c "SELECT version();"
```

Expected: PostgreSQL version info

### **Check Neo4j**:
Open browser: http://localhost:7474

Expected: Neo4j Browser

---

## 🧪 **Step 4: Run First Test Query**

### **In the browser** (http://localhost:3002):

1. Find the query input box
2. Type: `show me all faulty equipment at Rig Alpha`
3. Press Enter or click Submit

### **Expected Result**:
```
Found 2 faulty equipment items at Rig Alpha:

1. PS-401 (Pressure Sensor)
   - Location: Well W-12
   - Status: FAULTY
   - Last Reading: 2,450 PSI

2. TS-220 (Temperature Sensor)
   - Location: Well W-15
   - Status: FAULTY
   - Last Reading: 185°F

Confidence: 90%
Data Sources: PostgreSQL, Neo4j
```

---

## 🔍 **Step 5: Test Explainability**

### **Navigate to Explainability Page**:
1. Go to: http://localhost:3002/explainability
2. Enter query: `show me production trends for Rig Alpha`
3. Click "Analyze"

### **Expected**:
- Step-by-step reasoning timeline
- SQL query visible in green
- Cypher query visible in purple
- Copy buttons next to each query
- Export Audit Log button

---

## ✅ **Step 6: Test Copy Button**

1. On explainability page, expand Step 2 (SQL Agent)
2. Click "Copy" button next to SQL query
3. Button should change to "Copied! ✓"
4. Open Notepad and paste (Ctrl+V)
5. SQL query should be pasted

---

## 💾 **Step 7: Test Export Audit Log**

1. On explainability page (with a query analyzed)
2. Click "Export Audit Log" button
3. Check your Downloads folder
4. File should be named: `audit_log_[timestamp].json`
5. Open the file - should contain complete audit trail

---

## 🗄️ **Step 8: Verify PostgreSQL**

### **Open pgAdmin**:
1. Go to: http://localhost:5050
2. Login (if needed)
3. Connect to PostgreSQL server

### **Run Test Query**:
```sql
SELECT * FROM production_data 
WHERE rig_name = 'Rig Alpha' 
ORDER BY timestamp DESC 
LIMIT 5;
```

Expected: 5 rows of production data

### **Check Index Usage**:
```sql
EXPLAIN ANALYZE
SELECT * FROM production_data 
WHERE rig_name = 'Rig Alpha' 
ORDER BY timestamp DESC 
LIMIT 30;
```

Expected: Shows "Index Scan" using `idx_production_rig_timestamp`

---

## 🕸️ **Step 9: Verify Neo4j**

### **Open Neo4j Browser**:
1. Go to: http://localhost:7474
2. Login: neo4j / password

### **Run Test Query**:
```cypher
MATCH (r:Rig {name: 'Rig Alpha'})-[:HAS_EQUIPMENT]->(e:Equipment)
WHERE e.status = 'FAULTY'
RETURN r, e
```

Expected: Visual graph showing Rig Alpha connected to 2 faulty equipment nodes

---

## 📊 **Step 10: Verify Data Consistency**

### **Check KPI Cards** (http://localhost:3002):
- Total Assets: 3,420
- Avg Production Rate: ~850 bbl/day
- System Health: 92%
- Active Alerts: 8

### **Check Heat Map**:
Sum of all regions should equal 3,420:
- Permian Basin: 850
- Eagle Ford: 720
- Bakken: 680
- Marcellus: 590
- Haynesville: 580
- **Total**: 3,420 ✅

---

## ✅ **Success Checklist**

- [ ] Backend running on http://localhost:5001
- [ ] Frontend running on http://localhost:3002
- [ ] Dashboard loads with correct KPI values
- [ ] AI query returns detailed answer
- [ ] Explainability page shows reasoning timeline
- [ ] SQL and Cypher queries visible
- [ ] Copy buttons work
- [ ] Export audit log works
- [ ] PostgreSQL accessible via pgAdmin
- [ ] Neo4j accessible via browser
- [ ] No errors in browser console
- [ ] No errors in backend terminal

---

## 🚨 **Troubleshooting**

### **Backend Error: "Address already in use"**
Another process is using port 5001. Kill it:
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5001).OwningProcess | Stop-Process -Force
```

### **Frontend Error: "Port 3002 is already in use"**
Kill the process:
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 3002).OwningProcess | Stop-Process -Force
```

### **PostgreSQL Connection Error**
Check if PostgreSQL is running:
```powershell
Get-Service -Name postgresql*
```

If not running:
```powershell
Start-Service postgresql-x64-14  # Adjust version number
```

### **Neo4j Connection Error**
Check if Neo4j is running:
```powershell
Get-Service -Name Neo4j
```

If not running, start Neo4j Desktop application.

---

## 🎯 **You're Ready for Demo!**

Once all steps pass, you have:
- ✅ Full system running
- ✅ All features working
- ✅ Data consistency verified
- ✅ Auditability features tested

**Now you can practice your demo! 🚀**

---

## 📋 **Quick Commands Reference**

### **Start Backend**:
```powershell
cd backend
python main.py
```

### **Start Frontend**:
```powershell
cd frontend
npm run dev
```

### **Check Backend Health**:
```powershell
Invoke-WebRequest -Uri http://localhost:5001/api/health -UseBasicParsing
```

### **Test Query via API**:
```powershell
$body = @{query = "show me faulty equipment at Rig Alpha"} | ConvertTo-Json
Invoke-WebRequest -Uri http://localhost:5001/api/query -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
```

---

## 🎬 **Next Steps**

1. ✅ Start all services (Steps 1-2)
2. ✅ Run all tests (Steps 3-10)
3. ✅ Practice demo flow from `MASTER_DEMO_GUIDE.md`
4. ✅ Review `QUICK_REFERENCE_CHEAT_SHEET.md`
5. ✅ You're ready! 🚀

