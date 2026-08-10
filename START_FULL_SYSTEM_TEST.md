# 🚀 Full System Startup & Testing Guide

## **Step-by-Step System Startup**

Follow these steps to start all services and test the complete system.

---

## ✅ **Step 1: Verify Prerequisites**

### **Check PostgreSQL**:
```bash
psql -U postgres -c "SELECT version();"
```
Expected: PostgreSQL version info

### **Check Neo4j**:
Open browser: http://localhost:7474
Expected: Neo4j Browser login page

---

## ✅ **Step 2: Start Backend**

### **Option A: Using PowerShell Script**
```powershell
.\start-backend.ps1
```

### **Option B: Manual Start**
```bash
cd backend
python main.py
```

**Expected Output**:
```
 * Running on http://127.0.0.1:5001
 * Connected to PostgreSQL
 * Connected to Neo4j
```

**Keep this terminal open!**

---

## ✅ **Step 3: Start Frontend**

### **Open a NEW terminal** and run:
```bash
cd frontend
npm run dev
```

**Expected Output**:
```
- ready started server on 0.0.0.0:3002
- Local: http://localhost:3002
```

**Keep this terminal open!**

---

## ✅ **Step 4: Verify All Services**

### **Check Backend Health**:
```bash
curl http://localhost:5001/api/health
```
Expected: `{"status": "healthy"}`

### **Check Frontend**:
Open browser: http://localhost:3002
Expected: Dashboard with KPI cards and heat map

---

## 🧪 **Step 5: Run Comprehensive Tests**

Now let's test every feature systematically.

---

## 📊 **Test 1: Dashboard & KPI Cards**

### **What to Check**:
1. Navigate to http://localhost:3002
2. Verify KPI cards show:
   - Total Assets: 3,420
   - Avg Production Rate: ~850 bbl/day
   - System Health: 92%
   - Active Alerts: 8

3. Verify heat map shows 5 regions with correct asset counts

**✅ PASS if all numbers match**

---

## 🤖 **Test 2: AI Query - Faulty Equipment**

### **Test Query**:
```
show me all faulty equipment at Rig Alpha
```

### **Expected Response**:
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
```

### **What to Verify**:
- ✅ Answer appears with typewriter effect
- ✅ Confidence score shown (should be ~0.85-0.95)
- ✅ Data sources listed (PostgreSQL + Neo4j)
- ✅ No errors in console

**✅ PASS if answer is detailed and accurate**

---

## 🔍 **Test 3: Explainability Page**

### **Steps**:
1. Navigate to http://localhost:3002/explainability
2. Enter query: `show me production trends for Rig Alpha`
3. Click "Analyze"

### **Expected Results**:

#### **Step 1: Parser Agent**
- Action: "Parsed query and identified intent"
- Result: "Intent: production_analysis, Entities: Rig Alpha"

#### **Step 2: SQL Agent**
- Action: "Queried production trends for Rig Alpha"
- SQL Query displayed in green:
```sql
SELECT * FROM production_data 
WHERE rig_name = 'Rig Alpha' 
ORDER BY timestamp DESC LIMIT 30
```
- ✅ **Copy button** visible
- Result: "Retrieved 10 records"

#### **Step 3: Graph Agent**
- Action: "Queried knowledge graph for Rig Alpha"
- Cypher Query displayed in purple:
```cypher
MATCH (r:Rig {name: $rig_name})-[:HAS_EQUIPMENT]->(e:Equipment)
RETURN e
```
- ✅ **Copy button** visible
- Result: "Found 5 equipment nodes"

#### **Step 4: Reasoning Agent**
- Action: "Synthesized final answer"
- Result: Natural language answer

### **What to Verify**:
- ✅ All 4 steps shown
- ✅ SQL and Cypher queries visible
- ✅ Copy buttons work (click and verify "Copied!" appears)
- ✅ Export Audit Log button visible

**✅ PASS if all steps shown with queries**

---

## 📋 **Test 4: Copy Button Functionality**

### **Steps**:
1. On explainability page, expand Step 2 (SQL Agent)
2. Click "Copy" button next to SQL query
3. Open Notepad and paste (Ctrl+V)

### **Expected**:
- Button changes to "Copied! ✓" for 2 seconds
- Query is in clipboard
- Can paste into Notepad

**✅ PASS if query copied successfully**

---

## 💾 **Test 5: Export Audit Log**

### **Steps**:
1. On explainability page (with a query analyzed)
2. Click "Export Audit Log" button
3. Check Downloads folder

### **Expected**:
- File downloaded: `audit_log_[timestamp].json`
- File contains:
  - `query_id`
  - `timestamp`
  - `natural_language_query`
  - `sql_queries` array
  - `cypher_queries` array
  - `answer`
  - `confidence`

### **Verify JSON Structure**:
```json
{
  "query_id": "q_...",
  "timestamp": "2024-...",
  "natural_language_query": "show me production trends for Rig Alpha",
  "sql_queries": [...],
  "cypher_queries": [...],
  "answer": "...",
  "confidence": 0.90
}
```

**✅ PASS if JSON file downloads and has correct structure**

---

## 🗄️ **Test 6: PostgreSQL Verification**

### **Steps**:
1. Open pgAdmin (http://localhost:5050)
2. Connect to PostgreSQL
3. Run this query:
```sql
SELECT * FROM production_data 
WHERE rig_name = 'Rig Alpha' 
ORDER BY timestamp DESC 
LIMIT 5;
```

### **Expected**:
- Returns 5 rows
- Columns: id, timestamp, rig_name, well_name, production_rate, pressure, temperature

### **Run EXPLAIN**:
```sql
EXPLAIN ANALYZE
SELECT * FROM production_data 
WHERE rig_name = 'Rig Alpha' 
ORDER BY timestamp DESC 
LIMIT 30;
```

### **Expected**:
- Shows "Index Scan" (not Seq Scan)
- Uses `idx_production_rig_timestamp`
- Cost should be low (~0.42..8.44)

**✅ PASS if index is being used**

---

## 🕸️ **Test 7: Neo4j Verification**

### **Steps**:
1. Open Neo4j Browser (http://localhost:7474)
2. Login with credentials (neo4j/password)
3. Run this query:
```cypher
MATCH (r:Rig {name: 'Rig Alpha'})-[:HAS_EQUIPMENT]->(e:Equipment)
WHERE e.status = 'FAULTY'
RETURN r, e
```

### **Expected**:
- Visual graph showing Rig Alpha node
- Connected to 2 Equipment nodes (PS-401, TS-220)
- Both equipment nodes have status: 'FAULTY'

### **Run Count Query**:
```cypher
MATCH (n) RETURN labels(n) AS type, count(n) AS count
```

### **Expected**:
- Rig: 5 nodes
- Well: 15 nodes
- Equipment: 30+ nodes

**✅ PASS if graph visualizes correctly**

---

## 🎨 **Test 8: Data Consistency**

### **Verify Grounded Data**:

1. **Check KPI Card**: Total Assets = 3,420
2. **Check Heat Map**: Sum of all regions = 3,420
   - Permian Basin: 850
   - Eagle Ford: 720
   - Bakken: 680
   - Marcellus: 590
   - Haynesville: 580
   - **Total**: 3,420 ✅

3. **Check AI Response**: Should reference same numbers

**✅ PASS if all numbers match across components**

---

## 🚨 **Test 9: Critical Alerts**

### **Steps**:
1. On dashboard, check "Critical Alerts" section
2. Verify 8 alerts shown

### **Expected Alerts**:
1. High Pressure - Rig Alpha - Well W-12
2. Equipment Failure - Rig Alpha - PS-401
3. Temperature Spike - Rig Beta - Well W-23
4. Low Production - Rig Gamma - Well W-34
5. Maintenance Due - Rig Delta - Pump P-15
6. Gas Leak Detected - Rig Epsilon - Well W-45
7. Vibration Alert - Rig Alpha - Motor M-08
8. Pressure Drop - Rig Beta - Well W-28

**✅ PASS if 8 alerts shown**

---

## 🧪 **Test 10: Multiple Query Types**

### **Test Different Queries**:

#### **Query 1: Production Analysis**
```
show me production trends for Rig Alpha
```
Expected: Production data with rates and trends

#### **Query 2: Equipment Status**
```
what equipment is faulty at Rig Alpha?
```
Expected: List of 2 faulty equipment items

#### **Query 3: Safety Query**
```
show me safety incidents in the last month
```
Expected: HSE report data

#### **Query 4: Maintenance Query**
```
what maintenance is scheduled for Rig Beta?
```
Expected: Maintenance schedule information

**✅ PASS if all queries return relevant answers**

---

## ✅ **Final Verification Checklist**

- [ ] Backend running on port 5001
- [ ] Frontend running on port 3002
- [ ] PostgreSQL accessible
- [ ] Neo4j accessible
- [ ] Dashboard loads correctly
- [ ] KPI cards show correct data (3,420 assets)
- [ ] Heat map shows 5 regions
- [ ] AI queries return answers
- [ ] Explainability page shows reasoning timeline
- [ ] SQL queries visible with copy button
- [ ] Cypher queries visible with copy button
- [ ] Export audit log works
- [ ] pgAdmin can query PostgreSQL
- [ ] Neo4j Browser can query graph
- [ ] Data is consistent across all components
- [ ] No errors in browser console
- [ ] No errors in backend terminal

---

## 🎯 **Success Criteria**

**System is READY for demo if**:
- ✅ All 10 tests pass
- ✅ All services running without errors
- ✅ All features working as expected
- ✅ Data is consistent

---

## 🚨 **Troubleshooting**

### **Backend won't start**:
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### **Frontend won't start**:
```bash
cd frontend
npm install
npm run dev
```

### **PostgreSQL connection error**:
Check if PostgreSQL is running:
```bash
psql -U postgres -c "SELECT 1;"
```

### **Neo4j connection error**:
Check if Neo4j is running:
Open http://localhost:7474

---

## 🎬 **Ready for Demo!**

Once all tests pass, you're ready to demonstrate the system! 🚀

