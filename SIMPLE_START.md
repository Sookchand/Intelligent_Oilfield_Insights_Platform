# 🚀 SIMPLE START GUIDE

## **Just 2 Commands to Start Everything**

---

## ✅ **Step 1: Start Backend**

### **In your current terminal** (where you see the error):

```powershell
cd backend
python main.py
```

**Wait for this message**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Then test it**: Open http://localhost:8000/docs in your browser
You should see the FastAPI documentation page!

**⚠️ KEEP THIS TERMINAL OPEN!**

---

## ✅ **Step 2: Start Frontend**

### **Open a NEW terminal** (Ctrl+Shift+` in VS Code):

```powershell
cd frontend
npm run dev
```

**Wait for this message**:
```
- ready started server on 0.0.0.0:3002
```

✅ **Then test it**: Open http://localhost:3002 in your browser
You should see the dashboard!

**⚠️ KEEP THIS TERMINAL OPEN TOO!**

---

## 🎯 **That's It! Now Test**

### **Go to**: http://localhost:3002

1. You should see the dashboard with KPI cards
2. Find the query input box
3. Type: `show me all faulty equipment at Rig Alpha`
4. Press Enter
5. You should get a detailed answer!

---

## 🔍 **Test Explainability**

### **Go to**: http://localhost:3002/explainability

1. Enter: `show me production trends for Rig Alpha`
2. Click "Analyze"
3. You should see step-by-step reasoning with SQL and Cypher queries!

---

## 🚨 **If Backend Won't Start**

### **Error: "Address already in use"**

Someone is already using port 8000. Kill it:

```powershell
# Find what's using port 8000
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

# Kill it
$pid = (Get-NetTCPConnection -LocalPort 8000).OwningProcess
Stop-Process -Id $pid -Force

# Try starting backend again
cd backend
python main.py
```

---

### **Error: "No module named 'fastapi'"**

Install dependencies:

```powershell
cd backend
pip install -r requirements.txt

# Try again
python main.py
```

---

## 🚨 **If Frontend Won't Start**

### **Error: "Port 3002 is already in use"**

Kill it:

```powershell
$pid = (Get-NetTCPConnection -LocalPort 3002).OwningProcess
Stop-Process -Id $pid -Force

# Try again
cd frontend
npm run dev
```

---

### **Error: "npm: command not found"**

Install Node.js from: https://nodejs.org/

Then:
```powershell
cd frontend
npm install
npm run dev
```

---

## ✅ **Success Checklist**

- [ ] Backend terminal shows: "Uvicorn running on http://0.0.0.0:8000"
- [ ] Frontend terminal shows: "ready started server on 0.0.0.0:3002"
- [ ] http://localhost:8000/docs shows FastAPI docs
- [ ] http://localhost:3002 shows dashboard
- [ ] Can submit a query and get an answer
- [ ] Explainability page works

---

## 🎬 **You're Ready!**

Once both are running, you can:
1. ✅ Test queries on the dashboard
2. ✅ Check explainability page
3. ✅ Practice your demo
4. ✅ Review `MASTER_DEMO_GUIDE.md` for demo flow

**The system is ready! 🚀**

