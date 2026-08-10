# 🚀 Quick Reference Guide - Halliburton Demo

## 📁 **Important Files & Locations**

### **Architecture Diagram**

- **HTML Version:** `ARCHITECTURE_DIAGRAM.html` (double-click to open in browser)
- **Documentation:** `SCALABILITY_ARCHITECTURE.md`
- **Location:** Project root directory

### **Demo Documentation**

- **Main Demo Script:** `SCALABILITY_DEMO_READY.md`
- **Scalability Features:** `SCALABILITY_ARCHITECTURE.md`
- **Query History Fix:** `QUERY_HISTORY_FIXED.md`
- **Hydration Error Fix:** `HYDRATION_ERROR_FIX.md`

### **Key Components**

- **Cluster Map:** `frontend/components/AssetMap/AssetClusterMap.tsx`
- **Critical Alerts:** `frontend/components/AssetMap/CriticalAlertsSidebar.tsx`
- **History Page:** `frontend/app/history/page.tsx`
- **API Client:** `frontend/lib/api.ts`

---

## 🔧 **Common Issues & Fixes**

### **Issue 1: Query History Page Not Loading**

**Symptoms:**

- History page shows "No queries found"
- Backend not being called

**Fix:**
✅ **Already Fixed!** The history page now uses the centralized API client.

**To Test:**

1. Submit a query on the main page
2. Navigate to <http://localhost:3002/history>
3. Query should appear in the table

**If Still Not Working:**

- Check if backend is running on port 8000
- Check browser console for errors
- Verify the audit table exists in PostgreSQL

---

### **Issue 2: React Hydration Error**

**Symptoms:**

- Error: "Prop `cx` did not match. Server: '217.5982112579092' Client: '217.5982112579091'"
- Floating-point precision differences

**Fix:**
✅ **FINALLY FIXED!** Component now uses client-only rendering to avoid SSR hydration issues.

**How It Works:**

- Shows loading spinner during SSR
- Renders full component only on client
- No hydration errors

**Details:** See `HYDRATION_ERROR_FINAL_FIX.md`

---

### **Issue 3: Backend Not Running**

**Symptoms:**

- Frontend shows connection errors
- API calls fail
- History page shows error message

**Fix:**

```bash
cd backend
python main.py
```

**Verify:**

- Backend should start on <http://localhost:8000>
- Check for "✅ Query audit logger initialized"

---

## 🎯 **Pre-Demo Checklist**

### **1. Start Backend**

```bash
cd backend
python main.py
```

**Expected Output:**

```
✅ Connected to PostgreSQL
✅ Connected to Neo4j
✅ Connected to Qdrant
✅ Query audit logger initialized
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### **2. Start Frontend**

```bash
cd frontend
npm run dev
```

**Expected Output:**

```
- ready started server on 0.0.0.0:3002
- Local:        http://localhost:3002
```

### **3. Test Main Page**

- [ ] Navigate to <http://localhost:3002>
- [ ] Database Health Matrix shows 4 green LEDs
- [ ] KPI cards display correctly
- [ ] Cluster map shows 5 colored regions
- [ ] Critical alerts sidebar shows 10 alerts
- [ ] Hover over cluster shows tooltip

### **4. Test Query Functionality**

- [ ] Type a query: "Why is production declining?"
- [ ] Submit and wait for answer
- [ ] Reasoning trace displays
- [ ] Confidence score shows

### **5. Test History Page**

- [ ] Navigate to <http://localhost:3002/history>
- [ ] Query appears in the table
- [ ] Search filter works
- [ ] Status filter works
- [ ] Confidence badges display

---

## 📊 **Demo Flow (5 Minutes)**

### **1. Opening (30s)**
>
> "This is Halliburton's Command & Control Center - handling thousands of assets using intelligent clustering and multi-agent reasoning."

**Show:** Main dashboard

---

### **2. Scalability (1m)**
>
> "We're showing 3,420 assets, but you only see 5 clusters. This prevents information overload."

**Hover over Permian Basin cluster:**

- Show the "Glass Box" tooltip
- Point to the 4 agent icons

---

### **3. Exception-Based Intelligence (1m)**
>
> "The Critical Alerts Sidebar shows only the Top 10 failing assets."

**Click on "Rig Alpha":**

- Show the expanded reasoning
- Point to the 94% confidence score

---

### **4. Query & Explainability (2m)**
>
> "Now let's ask a question."

**Type:** "Why is production declining in the Permian Basin?"

- Show the answer
- Show the reasoning trace

---

### **5. Audit Trail (30s)**
>
> "Every query is logged for compliance."

**Navigate to:** <http://localhost:3002/history>

- Show the query history table

---

## 🌍 **Architecture Diagram**

### **How to View:**

**Option 1: Browser (Recommended)**

1. Double-click `ARCHITECTURE_DIAGRAM.html`
2. Or open in browser: `file:///c:/Project/IntelligentOilfieldInsightPlatform/ARCHITECTURE_DIAGRAM.html`

**Option 2: VS Code**

1. Open `SCALABILITY_ARCHITECTURE.md`
2. Look for the Mermaid code block
3. Use Mermaid preview extension

**What It Shows:**

- Tier 1: Global View (Cluster Map)
- Tier 2: Exception View (Critical Alerts)
- Tier 3: Detail View (Individual Asset)
- Multi-Agent Intelligence Layer

---

## 💡 **Key Talking Points**

### **For Executives:**
>
> "We don't visualize data - we visualize **anomalies**. The cluster map shows 3,420 assets, but the AI filters it down to the 10 that matter most."

### **For Engineers:**
>
> "The SQL Agent scans all 3,420 wells in the background. The Graph Agent identifies systemic faults. The Vector Agent finds historical context. All before you even click a button."

### **For Data Scientists:**
>
> "The clustering uses spatial indexing with O(n log n) complexity. The color-coding is driven by multi-agent consensus - not just a simple threshold."

---

## 🚨 **Emergency Fallbacks**

### **If History Page Fails:**

- Show backend logs with query processing
- Query the audit table directly in PostgreSQL
- Explain the architecture instead

### **If Cluster Map Doesn't Load:**

- Refresh the page
- Show the KPI dashboard instead
- Focus on the critical alerts sidebar

### **If Query Takes Too Long:**

- Say: "The AI is analyzing data across all 4 databases"
- Show a previous query's reasoning trace
- Have a pre-recorded video ready

---

## ✅ **Final Status**

- ✅ Cluster map with 3,420 assets
- ✅ Critical alerts sidebar with Top 10
- ✅ Query history page working
- ✅ No React errors
- ✅ No hydration errors
- ✅ Architecture diagram ready
- ✅ Documentation complete

---

## 📞 **Quick Commands**

### **Start Everything:**

```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### **Test Backend:**

```bash
curl http://localhost:8000/api/status/databases
```

### **Test Frontend:**

Open <http://localhost:3002> in browser

### **View Architecture Diagram:**

Double-click `ARCHITECTURE_DIAGRAM.html`

---

**You're 100% ready for the Halliburton demo on Friday!** 🚀
