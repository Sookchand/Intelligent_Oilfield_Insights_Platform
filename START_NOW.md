# 🚀 START SYSTEM NOW - CORRECTED

## **IMPORTANT: Backend runs on port 8000, not 5001!**

---

## ✅ **Step 1: Start Backend**

### **Option A: Use the Batch File** (EASIEST)
```cmd
START_BACKEND.bat
```

This will:
- Activate virtual environment
- Kill any existing process on port 8000
- Start FastAPI backend
- Show you the URL: http://localhost:8000

**Keep this window open!**

---

### **Option B: Manual Start**

In your terminal (with venv activated):

```powershell
cd backend
python main.py
```

**Expected Output**:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!**

---

## ✅ **Step 2: Verify Backend is Running**

Open browser and go to:
- **API Health**: http://localhost:8000/api/health
- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)

You should see the FastAPI documentation page!

---

## ✅ **Step 3: Start Frontend**

### **Open a NEW terminal** and run:

```powershell
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

## ✅ **Step 4: Open the Application**

Open browser and go to:
- **Dashboard**: http://localhost:3002
- **Explainability**: http://localhost:3002/explainability

---

## 🧪 **Step 5: Test a Query**

### **On the Dashboard** (http://localhost:3002):

1. Find the query input box
2. Type: `show me all faulty equipment at Rig Alpha`
3. Press Enter

**Expected**: Detailed answer with confidence score

---

## 🔍 **Step 6: Test Explainability**

### **Go to**: http://localhost:3002/explainability

1. Enter: `show me production trends for Rig Alpha`
2. Click "Analyze"
3. You should see:
   - Step-by-step reasoning timeline
   - SQL queries in green
   - Cypher queries in purple
   - Copy buttons
   - Export Audit Log button

---

## 🚨 **Troubleshooting**

### **Backend Error: "Address already in use"**

Kill the process on port 8000:

```powershell
# Find the process
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

# Kill it
$pid = (Get-NetTCPConnection -LocalPort 8000).OwningProcess
Stop-Process -Id $pid -Force
```

Then start backend again.

---

### **Frontend Error: "Port 3002 already in use"**

Kill the process on port 3002:

```powershell
# Find and kill
$pid = (Get-NetTCPConnection -LocalPort 3002).OwningProcess
Stop-Process -Id $pid -Force
```

Then start frontend again.

---

### **Backend starts but frontend can't connect**

Check the frontend API configuration:

The frontend should be calling: `http://localhost:8000/api/query`

If you see errors in browser console, check:
1. Backend is running on port 8000
2. CORS is enabled (it should be by default)
3. No firewall blocking localhost

---

## ✅ **Quick Verification Checklist**

- [ ] Backend running: http://localhost:8000/docs shows FastAPI docs
- [ ] Frontend running: http://localhost:3002 shows dashboard
- [ ] KPI cards show: 3,420 total assets
- [ ] Heat map shows 5 regions
- [ ] Query input box is visible
- [ ] Can submit a query and get an answer

---

## 🎯 **Correct URLs**

| Service | URL |
|---------|-----|
| **Backend API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **API Health** | http://localhost:8000/api/health |
| **Frontend** | http://localhost:3002 |
| **Explainability** | http://localhost:3002/explainability |
| **pgAdmin** | http://localhost:5050 |
| **Neo4j Browser** | http://localhost:7474 |

---

## 🚀 **Quick Start Commands**

### **Start Backend**:
```cmd
START_BACKEND.bat
```
OR
```powershell
cd backend
python main.py
```

### **Start Frontend**:
```powershell
cd frontend
npm run dev
```

### **Test Backend**:
```powershell
Invoke-WebRequest -Uri http://localhost:8000/api/health -UseBasicParsing
```

### **Test Query**:
```powershell
$body = @{query = "show me faulty equipment at Rig Alpha"} | ConvertTo-Json
Invoke-WebRequest -Uri http://localhost:8000/api/query -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
```

---

## 🎬 **You're Ready!**

Once both services are running:
1. ✅ Backend on port 8000
2. ✅ Frontend on port 3002
3. ✅ Test a query
4. ✅ Check explainability page
5. ✅ Practice your demo!

**The system is ready for demonstration! 🚀**

