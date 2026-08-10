# 🧪 Testing Guide - Intelligent Oilfield Insights Platform

## ✅ Frontend is Working!

Based on your browser output, the frontend is successfully running and displaying:
- ✅ Navigation bar with logo
- ✅ Page title "Ask Anything About Your Oilfield"
- ✅ Database connectivity status
- ✅ 4 Demo query cards
- ✅ Query input box
- ✅ Quick stats cards

---

## 🎯 Quick Tests to Try

### Test 1: Database Status Check

**What to look for:**
- The 4 database cards (PostgreSQL, Neo4j, Qdrant, MinIO)
- Should show "Checking..." initially
- After a few seconds, should show either:
  - ✅ Green "Connected" status
  - ❌ Red "Disconnected" status

**If showing "Disconnected":**
- Make sure backend is running: http://localhost:8000/docs
- Check Docker containers: `docker ps`

---

### Test 2: Try a Demo Query

**Steps:**
1. Click on the first demo query card: **"Why is production dropping at Rig Alpha?"**
2. The query should appear in the input box
3. Click the blue **"Ask AI"** button
4. You should see:
   - Loading spinner with "Processing your query..."
   - After a few seconds, results appear with typewriter effect
   - Confidence score displayed
   - Data sources shown
   - "View Explainability" button

**Expected Result:**
```
The AI should analyze production data and provide an answer about
why production is dropping, mentioning equipment failures or other issues.
```

---

### Test 3: View Explainability

**Steps:**
1. After getting a query result, click **"View Explainability"**
2. You should be redirected to `/explainability` page
3. You should see:
   - Agent Workflow Visualization (4 agent cards)
   - Detailed Reasoning Timeline (expandable steps)
   - Confidence Analysis (with breakdown)
   - Data Source Attribution
   - Knowledge Graph Visualization (if applicable)

**What to check:**
- ✅ Can you expand/collapse reasoning steps?
- ✅ Do you see SQL queries in the timeline?
- ✅ Do you see Cypher queries in the timeline?
- ✅ Is the confidence score displayed?
- ✅ Are data sources shown with percentages?

---

### Test 4: Navigation

**Steps:**
1. Click on different navigation items:
   - Query Dashboard
   - Explainability
   - Business Impact
   - Data Explorer
   - System Monitor

**Expected:**
- Query Dashboard and Explainability should work fully
- Business Impact, Data Explorer, System Monitor show "Coming soon" placeholders

---

### Test 5: Query History & Bookmarks

**Steps:**
1. Enter a query in the input box
2. Click the bookmark icon (⭐)
3. Click in the input box again
4. You should see a dropdown with:
   - BOOKMARKS section (showing your bookmarked query)
   - RECENT section (showing recent queries)

**Test:**
- Try clicking a query from history - it should populate the input
- Try bookmarking multiple queries
- Refresh the page - bookmarks should persist (localStorage)

---

## 🐛 Known Issues (Non-Critical)

### 1. Browser Console Errors

**Error:** `layout.js:192 Uncaught SyntaxError`
- **Cause:** Browser extension (Smart Unit Converter)
- **Impact:** None - page works fine
- **Fix:** Disable browser extensions or ignore

**Error:** `favicon.ico 404`
- **Cause:** Missing favicon file
- **Impact:** None - just a missing icon
- **Fix:** Already added `app/icon.tsx` - will work after rebuild

### 2. Database Status Shows "Checking..."

**Cause:** Backend not running or not accessible
**Fix:**
```cmd
# Check backend
curl http://localhost:8000/api/status/databases

# If not running, start it
cd backend
start-backend.bat
```

---

## ✅ Success Criteria

Your frontend is working correctly if:

- [x] Page loads and displays content
- [x] Navigation bar is visible
- [x] Demo queries are clickable
- [x] Query input accepts text
- [x] "Ask AI" button is clickable
- [ ] Database status shows "Connected" (requires backend)
- [ ] Queries return results (requires backend)
- [ ] Explainability page shows reasoning (requires backend)

---

## 🔧 Testing with Backend

To test the full system:

### 1. Make sure backend is running:
```cmd
# Check if backend is accessible
curl http://localhost:8000/docs
```

### 2. Test the API directly:
```cmd
# Test query endpoint
curl -X POST http://localhost:8000/api/query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"Why is production dropping at Rig Alpha?\"}"
```

### 3. Test from frontend:
1. Open http://localhost:3000
2. Click a demo query
3. Click "Ask AI"
4. Should get a response within 5-10 seconds

---

## 📊 What Each Feature Does

### Query Dashboard (`/`)
- **Purpose:** Main interface for asking questions
- **Features:**
  - Natural language query input
  - Demo queries for quick testing
  - Real-time database status
  - Query history and bookmarks
  - Results with typewriter effect
  - Confidence scoring

### Explainability Dashboard (`/explainability`)
- **Purpose:** Show how AI reaches conclusions
- **Features:**
  - Agent workflow visualization
  - Step-by-step reasoning trace
  - SQL/Cypher query display
  - Confidence breakdown
  - Data source attribution
  - Knowledge graph visualization

---

## 🎯 Demo Queries Explained

### 1. "Why is production dropping at Rig Alpha?"
- **Tests:** Production analysis, SQL queries, time-series data
- **Expected:** Analysis of production trends with equipment issues

### 2. "Show me all faulty equipment at Rig Alpha"
- **Tests:** Graph traversal, Neo4j queries, relationship mapping
- **Expected:** List of faulty equipment with graph visualization

### 3. "What is the safety risk at Well W-12?"
- **Tests:** Business metrics, risk calculation, multi-source data
- **Expected:** Safety risk score with contributing factors

### 4. "Predict production for next week"
- **Tests:** Forecasting, confidence calibration, trend analysis
- **Expected:** Production forecast with confidence intervals

---

## 🚀 Next Steps

1. ✅ Verify frontend is displaying correctly (DONE!)
2. ⏳ Start backend server
3. ⏳ Test database connectivity
4. ⏳ Try demo queries
5. ⏳ Explore explainability features
6. ⏳ Test all navigation pages

---

## 📝 Reporting Issues

If something doesn't work:

1. **Check browser console** (F12) for errors
2. **Check terminal** running frontend for errors
3. **Check backend** is running (http://localhost:8000/docs)
4. **Check Docker** containers are running (`docker ps`)
5. **Try refreshing** the page (Ctrl + F5)

---

**Your frontend is working! 🎉**

The page is loading correctly and displaying all content. The only errors are:
- Browser extension interference (ignore)
- Missing favicon (cosmetic, already fixed)

To test the full functionality, make sure the backend is running!

