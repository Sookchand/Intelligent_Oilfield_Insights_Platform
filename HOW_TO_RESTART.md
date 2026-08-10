# 🔄 How to Restart the Backend - Step by Step

## ⚡ **METHOD 1: Use the Restart Script (EASIEST!)**

I've created a restart script for you!

### **Just double-click this file:**
```
RESTART_BACKEND.bat
```

**What it does:**
1. ✅ Stops any running Python processes
2. ✅ Activates the virtual environment
3. ✅ Starts the backend with the updated code

**Wait for:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Then go to **Step 3: Test the Fix** below.

---

## 🔧 **METHOD 2: Manual Restart**

### **Step 1: Stop the Backend**

**Option A - If you see the backend terminal:**
1. Click on the terminal window running the backend
2. Press `Ctrl + C`

**Option B - If you can't find it:**
1. Press `Ctrl + Shift + Esc` (opens Task Manager)
2. Find "Python" processes
3. Right-click → End Task on all Python processes
4. Close Task Manager

### **Step 2: Start the Backend**

1. Open a **NEW** Command Prompt or PowerShell
2. Navigate to your project:
   ```powershell
   cd c:\Project\IntelligentOilfieldInsightPlatform
   ```
3. Run these commands:
   ```powershell
   cd backend
   ..\venv\Scripts\activate
   python main.py
   ```

### **Step 3: Wait for Startup**

You should see:
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🧪 **Step 3: Test the Fix**

### **1. Open the Frontend**

Go to: **http://localhost:3000**

### **2. Enter the Test Query**

Type in the search box:
```
Show me all faulty equipment at Rig Alpha
```

### **3. Click "Ask AI"**

### **4. Verify the Result**

You should now see:

✅ **Confidence: 85-90%** (not 30%!)

✅ **Answer should include:**
- Found 1 faulty equipment
- Gauge G-40 (Pressure Gauge)
- At Well W-12
- Status: FAULTY
- Production Impact: 943.2 bbl/day

✅ **Processing Steps should show:**
1. Parser - Query decomposition
2. SQL - Queried production trends for Rig Alpha
3. Graph - Searched for faulty equipment at Rig Alpha
4. Reasoning - Synthesized results

✅ **Data Sources should show:**
- PostgreSQL ✓ (70 records)
- Neo4j ✓ (1 faulty item found)

---

## ✅ **Success Checklist**

After testing, verify:

- [ ] Backend is running (terminal shows "Application startup complete")
- [ ] Frontend is accessible at http://localhost:3000
- [ ] Query returns **85-90% confidence** (not 30%)
- [ ] Shows **1 faulty equipment** (Gauge G-40)
- [ ] Shows **Well W-12**
- [ ] Shows **production impact** (943.2 bbl/day)
- [ ] Processing shows **4 steps** (Parser, SQL, Graph, Reasoning)
- [ ] Data sources show **PostgreSQL ✓ and Neo4j ✓**

---

## 🚨 **Troubleshooting**

### **Problem: Port 8000 already in use**

**Solution:**
1. Open Task Manager (Ctrl + Shift + Esc)
2. Find all "Python" processes
3. End them all
4. Try starting again

### **Problem: "venv not found"**

**Solution:**
Make sure you're in the right directory:
```powershell
cd c:\Project\IntelligentOilfieldInsightPlatform
cd backend
..\venv\Scripts\activate
```

### **Problem: Still getting 30% confidence**

**Solution:**
1. Make sure you **restarted** the backend (not just refreshed the page)
2. Check the backend terminal for errors
3. Verify databases are running:
   ```powershell
   docker ps --filter "name=oilfield"
   ```
   Should show 4 containers running

### **Problem: Frontend not loading**

**Solution:**
1. Check if frontend is running
2. If not, open a new terminal:
   ```powershell
   cd c:\Project\IntelligentOilfieldInsightPlatform\frontend
   npm run dev
   ```

---

## 📞 **Quick Commands Reference**

### **Stop Backend:**
```powershell
# Press Ctrl+C in the backend terminal
# OR
taskkill /F /IM python.exe
```

### **Start Backend:**
```powershell
cd c:\Project\IntelligentOilfieldInsightPlatform\backend
..\venv\Scripts\activate
python main.py
```

### **Check Databases:**
```powershell
docker ps --filter "name=oilfield"
```

### **Check Backend Health:**
Open in browser: http://localhost:8000/health

---

## 🎯 **What You're Testing**

**The Fix:**
- Parser now detects "faulty equipment" queries correctly
- Routes through: SQL Agent → Graph Agent → Reasoning Agent
- Returns high confidence with complete data

**Before Fix:**
- 30% confidence
- No data found
- Wrong processing path

**After Fix:**
- 85-90% confidence
- 1 faulty equipment found
- Correct processing path

---

## 🎉 **You're Ready!**

Once you see **85-90% confidence**, the fix is working!

**Next steps:**
1. Test the other 4 demo queries
2. Practice your demo flow
3. You're ready for the interview! 🚀

---

**Need help? Check the terminal output for error messages and let me know what you see!**

