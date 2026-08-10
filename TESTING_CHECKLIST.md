# ✅ Testing Checklist - Intelligent Oilfield Insights Platform

## 🚀 Pre-Testing Setup

### Step 1: Verify All Services Are Running

- [ ] **Docker containers running**
  ```cmd
  docker ps
  ```
  Should show 4 containers: postgres, neo4j, qdrant, minio

- [ ] **Backend running**
  - Open: http://localhost:8000/docs
  - Should see FastAPI Swagger UI

- [ ] **Frontend running**
  - Terminal shows: `✓ Ready in 2.9s`
  - Terminal stays open (doesn't return to prompt)
  - Open: http://localhost:3000
  - Should see Query Dashboard

---

## 🎨 Frontend Tests

### Test 1: Page Load
- [ ] Page loads without errors
- [ ] Navigation bar displays correctly
- [ ] Logo and title visible: "🛢️ Intelligent Oilfield Insights"
- [ ] All navigation links present (5 items)
- [ ] No console errors (except browser extension warnings)

### Test 2: Database Status
- [ ] "Database Connectivity" section visible
- [ ] Shows "All Systems Operational" (green)
- [ ] PostgreSQL shows "Connected" (green)
- [ ] Neo4j shows "Connected" (green)
- [ ] Qdrant shows "Connected" (green)
- [ ] MinIO shows "Connected" (green)

### Test 3: Demo Queries
- [ ] 4 demo query cards visible
- [ ] Card 1: "Why is production dropping at Rig Alpha?"
- [ ] Card 2: "Show me all faulty equipment at Rig Alpha"
- [ ] Card 3: "What is the safety risk at Well W-12?"
- [ ] Card 4: "Predict production for next week"
- [ ] Cards are clickable
- [ ] Clicking a card populates the query input

### Test 4: Query Input
- [ ] Query input box visible
- [ ] Placeholder text: "Ask about production, equipment, safety, or forecasts..."
- [ ] Can type in the input
- [ ] "Ask AI" button visible and clickable
- [ ] Quick stats cards visible (Multi-Agent System, Data Sources, AI Transparency)

### Test 5: Query Execution
- [ ] Click demo query "Why is production dropping at Rig Alpha?"
- [ ] Click "Ask AI" button
- [ ] Loading spinner appears
- [ ] "Processing your query..." message shows
- [ ] Response appears after 5-10 seconds
- [ ] Typewriter effect works
- [ ] Confidence score displays
- [ ] Data sources shown
- [ ] "View Explainability" button appears

### Test 6: Query History & Bookmarks
- [ ] Click in query input box
- [ ] Dropdown appears with history
- [ ] Click bookmark icon (⭐) on a query
- [ ] Query appears in BOOKMARKS section
- [ ] Recent queries appear in RECENT section
- [ ] Clicking a history item populates input
- [ ] Refresh page - bookmarks persist

### Test 7: Navigation
- [ ] Click "Explainability" in nav
- [ ] Redirects to `/explainability`
- [ ] Click "Business Impact" - shows placeholder
- [ ] Click "Data Explorer" - shows placeholder
- [ ] Click "System Monitor" - shows placeholder
- [ ] Click "Query Dashboard" - returns to home

---

## 🧠 Explainability Dashboard Tests

### Test 8: Explainability Page Load
- [ ] Navigate to `/explainability`
- [ ] Page loads correctly
- [ ] "AI Explainability Dashboard" title visible
- [ ] "Understanding How AI Reaches Conclusions" subtitle visible

### Test 9: Agent Workflow Visualization
- [ ] "Agent Workflow" section visible
- [ ] 4 agent cards displayed:
  - [ ] Parser Agent (purple)
  - [ ] SQL Agent (blue)
  - [ ] Graph Agent (teal)
  - [ ] Reasoning Agent (pink)
- [ ] Each card shows status and description
- [ ] Visual flow arrows between agents

### Test 10: Reasoning Timeline
- [ ] "Detailed Reasoning Timeline" section visible
- [ ] Multiple reasoning steps shown
- [ ] Each step has:
  - [ ] Step number
  - [ ] Agent name
  - [ ] Description
  - [ ] Timestamp
  - [ ] Expand/collapse button
- [ ] Clicking expand shows SQL/Cypher queries
- [ ] Syntax highlighting works

### Test 11: Confidence Breakdown
- [ ] "Confidence Analysis" section visible
- [ ] Overall confidence score displayed
- [ ] Breakdown by component:
  - [ ] Data Quality
  - [ ] Query Complexity
  - [ ] Agent Consensus
  - [ ] Historical Accuracy
- [ ] Progress bars show percentages
- [ ] Colors indicate confidence levels

### Test 12: Data Source Attribution
- [ ] "Data Source Attribution" section visible
- [ ] Shows contribution from each database:
  - [ ] PostgreSQL
  - [ ] Neo4j
  - [ ] Qdrant
  - [ ] MinIO
- [ ] Percentages add up to 100%
- [ ] Visual indicators (bars/charts)

### Test 13: Knowledge Graph Visualization
- [ ] "Knowledge Graph" section visible
- [ ] Graph visualization displays
- [ ] Nodes represent entities
- [ ] Edges represent relationships
- [ ] Interactive (can zoom/pan if implemented)

---

## 🔌 Backend API Tests

### Test 14: API Documentation
- [ ] Open http://localhost:8000/docs
- [ ] Swagger UI loads
- [ ] All endpoints visible:
  - [ ] POST /api/query
  - [ ] GET /api/business/downtime-cost/{rig_name}
  - [ ] GET /api/business/maintenance-roi/{equipment_id}
  - [ ] GET /api/business/safety-risk/{rig_name}
  - [ ] GET /api/business/forecast/{rig_name}
  - [ ] GET /api/system/metrics
  - [ ] GET /api/status/databases

### Test 15: Query Endpoint
- [ ] Expand POST /api/query
- [ ] Click "Try it out"
- [ ] Enter: `{"query": "Why is production dropping at Rig Alpha?"}`
- [ ] Click "Execute"
- [ ] Response code: 200
- [ ] Response includes:
  - [ ] `answer` field
  - [ ] `confidence` field
  - [ ] `reasoning_trace` array
  - [ ] `data_sources` object
  - [ ] `query_metadata` object

### Test 16: Business Metrics Endpoints
- [ ] Test downtime-cost endpoint with "Rig Alpha"
- [ ] Response includes cost calculation
- [ ] Test maintenance-roi endpoint with equipment ID
- [ ] Response includes ROI calculation
- [ ] Test safety-risk endpoint with "Rig Alpha"
- [ ] Response includes risk score

### Test 17: Database Status
- [ ] Open http://localhost:8000/api/status/databases
- [ ] Response shows all 4 databases
- [ ] All show `"status": "connected"`
- [ ] Response time < 1 second

---

## 🗄️ Database Tests

### Test 18: PostgreSQL
- [ ] Can connect to PostgreSQL
- [ ] Production data exists
- [ ] Queries return results

### Test 19: Neo4j
- [ ] Open http://localhost:7474
- [ ] Login with neo4j / password123
- [ ] Run: `MATCH (n) RETURN count(n)`
- [ ] Returns node count > 0

### Test 20: Qdrant
- [ ] Qdrant accessible on port 6333
- [ ] Collections exist

### Test 21: MinIO
- [ ] Open http://localhost:9001
- [ ] Login with minioadmin / minioadmin
- [ ] Buckets visible

---

## 🎯 End-to-End Tests

### Test 22: Complete Query Flow
- [ ] Open http://localhost:3000
- [ ] Click "Why is production dropping at Rig Alpha?"
- [ ] Click "Ask AI"
- [ ] Wait for response
- [ ] Response mentions equipment issues
- [ ] Click "View Explainability"
- [ ] See full reasoning trace
- [ ] See SQL queries executed
- [ ] See Neo4j queries executed
- [ ] Confidence score > 80%

### Test 23: All Demo Queries
- [ ] Test query 1: Production dropping
- [ ] Test query 2: Faulty equipment
- [ ] Test query 3: Safety risk
- [ ] Test query 4: Production forecast
- [ ] All return valid responses
- [ ] All show explainability

---

## ✅ Success Criteria

All tests should pass with:
- ✅ No critical errors in browser console
- ✅ All databases showing "Connected"
- ✅ All demo queries returning responses
- ✅ Explainability dashboard showing full traces
- ✅ Response times < 10 seconds
- ✅ UI is responsive and interactive

---

## 📊 Test Results Summary

**Date:** _____________  
**Tester:** _____________

| Category | Tests Passed | Tests Failed | Notes |
|----------|--------------|--------------|-------|
| Frontend | ___/7 | ___ | |
| Explainability | ___/6 | ___ | |
| Backend API | ___/4 | ___ | |
| Databases | ___/4 | ___ | |
| End-to-End | ___/2 | ___ | |
| **TOTAL** | **___/23** | **___** | |

**Overall Status:** ⬜ PASS ⬜ FAIL

**Notes:**
_____________________________________________
_____________________________________________
_____________________________________________

