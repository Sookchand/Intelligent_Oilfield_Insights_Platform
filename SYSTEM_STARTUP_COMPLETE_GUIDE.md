# 🚀 Complete System Startup & Testing Guide

## **Everything You Need to Start and Test the System**

---

## 📋 **Quick Start (3 Steps)**

### **Step 1: Start Backend** (Terminal 1)
```powershell
cd backend
python main.py
```
**Keep this terminal open!**

### **Step 2: Start Frontend** (Terminal 2 - NEW terminal)
```powershell
cd frontend
npm run dev
```
**Keep this terminal open!**

### **Step 3: Test Everything**
```powershell
# In Terminal 3 (NEW terminal)
.\test_system.ps1
```

---

## ✅ **Detailed Startup Instructions**

### **Terminal 1: Backend**

1. Make sure you're in the project root directory
2. Activate virtual environment (if not already activated):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
3. Start backend:
   ```powershell
   cd backend
   python main.py
   ```

**Expected Output**:
```
 * Serving Flask app 'main'
 * Debug mode: on
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
```

**✅ Verify**: Open http://localhost:5001/api/health in browser
Should see: `{"status": "healthy"}`

---

### **Terminal 2: Frontend**

1. Open a NEW terminal (Ctrl+Shift+` in VS Code)
2. Navigate to frontend:
   ```powershell
   cd frontend
   ```
3. Start frontend:
   ```powershell
   npm run dev
   ```

**Expected Output**:
```
- ready started server on 0.0.0.0:3002
- Local: http://localhost:3002
```

**✅ Verify**: Open http://localhost:3002 in browser
Should see: Dashboard with KPI cards and heat map

---

## 🧪 **Automated Testing**

### **Run the Test Script**:
```powershell
.\test_system.ps1
```

**This will test**:
- ✅ Backend health (port 5001)
- ✅ Frontend accessibility (port 3002)
- ✅ PostgreSQL status
- ✅ Neo4j accessibility (port 7474)
- ✅ API query functionality

---

## 🎯 **Manual Testing Checklist**

### **Test 1: Dashboard** ✅
1. Go to: http://localhost:3002
2. Verify KPI cards show:
   - Total Assets: 3,420
   - Avg Production Rate: ~850 bbl/day
   - System Health: 92%
   - Active Alerts: 8
3. Verify heat map shows 5 regions

**✅ PASS if all data displays correctly**

---

### **Test 2: AI Query** ✅
1. On dashboard, find query input
2. Enter: `show me all faulty equipment at Rig Alpha`
3. Press Enter

**Expected Response**:
```
Found 2 faulty equipment items at Rig Alpha:

1. PS-401 (Pressure Sensor)
   - Location: Well W-12
   - Status: FAULTY

2. TS-220 (Temperature Sensor)
   - Location: Well W-15
   - Status: FAULTY

Confidence: 90%
```

**✅ PASS if answer appears with confidence score**

---

### **Test 3: Explainability Page** ✅
1. Go to: http://localhost:3002/explainability
2. Enter: `show me production trends for Rig Alpha`
3. Click "Analyze"

**Expected**:
- Step 1: Parser Agent
- Step 2: SQL Agent (with SQL query in green)
- Step 3: Graph Agent (with Cypher query in purple)
- Step 4: Reasoning Agent
- Copy buttons next to queries
- Export Audit Log button

**✅ PASS if all steps shown with queries**

---

### **Test 4: Copy Button** ✅
1. On explainability page, expand Step 2
2. Click "Copy" button next to SQL query
3. Button should change to "Copied! ✓"
4. Open Notepad and paste (Ctrl+V)

**✅ PASS if SQL query is copied**

---

### **Test 5: Export Audit Log** ✅
1. On explainability page (with query analyzed)
2. Click "Export Audit Log"
3. Check Downloads folder
4. Open the JSON file

**Expected JSON Structure**:
```json
{
  "query_id": "q_...",
  "timestamp": "...",
  "natural_language_query": "...",
  "sql_queries": [...],
  "cypher_queries": [...],
  "answer": "...",
  "confidence": 0.90
}
```

**✅ PASS if JSON downloads with correct structure**

---

### **Test 6: PostgreSQL** ✅
1. Open pgAdmin: http://localhost:5050
2. Connect to PostgreSQL
3. Run query:
```sql
SELECT * FROM production_data 
WHERE rig_name = 'Rig Alpha' 
ORDER BY timestamp DESC 
LIMIT 5;
```

**✅ PASS if returns 5 rows**

4. Run EXPLAIN:
```sql
EXPLAIN ANALYZE
SELECT * FROM production_data 
WHERE rig_name = 'Rig Alpha' 
ORDER BY timestamp DESC 
LIMIT 30;
```

**✅ PASS if shows "Index Scan"**

---

### **Test 7: Neo4j** ✅
1. Open Neo4j Browser: http://localhost:7474
2. Login: neo4j / password
3. Run query:
```cypher
MATCH (r:Rig {name: 'Rig Alpha'})-[:HAS_EQUIPMENT]->(e:Equipment)
WHERE e.status = 'FAULTY'
RETURN r, e
```

**✅ PASS if shows visual graph with 2 equipment nodes**

---

## 🚨 **Troubleshooting**

### **Backend won't start**
```powershell
# Check if port 5001 is in use
Get-NetTCPConnection -LocalPort 5001 -ErrorAction SilentlyContinue

# Kill process if needed
Get-Process -Id (Get-NetTCPConnection -LocalPort 5001).OwningProcess | Stop-Process -Force

# Reinstall dependencies
cd backend
pip install -r requirements.txt

# Try again
python main.py
```

---

### **Frontend won't start**
```powershell
# Check if port 3002 is in use
Get-NetTCPConnection -LocalPort 3002 -ErrorAction SilentlyContinue

# Kill process if needed
Get-Process -Id (Get-NetTCPConnection -LocalPort 3002).OwningProcess | Stop-Process -Force

# Reinstall dependencies
cd frontend
npm install

# Try again
npm run dev
```

---

### **PostgreSQL not accessible**
```powershell
# Check service status
Get-Service -Name postgresql*

# Start service if stopped
Start-Service postgresql-x64-14  # Adjust version
```

---

### **Neo4j not accessible**
1. Open Neo4j Desktop application
2. Start the database
3. Verify it's running on port 7474

---

## ✅ **Success Criteria**

**System is READY when**:
- ✅ Backend running on http://localhost:5001
- ✅ Frontend running on http://localhost:3002
- ✅ Dashboard loads with correct data
- ✅ AI queries return answers
- ✅ Explainability page works
- ✅ Copy buttons work
- ✅ Export audit log works
- ✅ PostgreSQL accessible
- ✅ Neo4j accessible
- ✅ No errors in console

---

## 🎬 **Ready for Demo!**

Once all tests pass:

1. ✅ Review `MASTER_DEMO_GUIDE.md` for demo flow
2. ✅ Print `QUICK_REFERENCE_CHEAT_SHEET.md`
3. ✅ Practice with `HANDS_ON_TECHNICAL_EXERCISES.md`
4. ✅ Review `TECHNICAL_QA_PREPARATION.md` for Q&A

---

## 📞 **Quick Commands**

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

### **Test System**:
```powershell
.\test_system.ps1
```

### **Check Backend Health**:
```powershell
Invoke-WebRequest -Uri http://localhost:5001/api/health -UseBasicParsing
```

### **Test API Query**:
```powershell
$body = @{query = "show me faulty equipment at Rig Alpha"} | ConvertTo-Json
Invoke-WebRequest -Uri http://localhost:5001/api/query -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
```

---

## 🎯 **You're Ready!**

Follow the steps above, run all tests, and you'll have a fully functional system ready for demonstration! 🚀

