# 🎯 QUICK REFERENCE CHEAT SHEET

## **Print This Out and Keep It Next to You During the Demo**

---

## 🗄️ **PostgreSQL Quick Reference**

### **Key Files**:
- `backend/agents/sql_agent.py` - SQL query generation
- `data/seed_sql.sql` - Database schema

### **Important Queries**:
```sql
-- Production trends (Line 30 in sql_agent.py)
SELECT * FROM production_data 
WHERE rig_name = %s 
ORDER BY timestamp DESC LIMIT 30;

-- Check index usage
EXPLAIN ANALYZE SELECT * FROM production_data WHERE rig_name = 'Rig Alpha';

-- Show all indexes
SELECT * FROM pg_indexes WHERE tablename = 'production_data';
```

### **Key Talking Points**:
- ✅ Parameterized queries prevent SQL injection
- ✅ Composite index `(rig_name, timestamp DESC)` for performance
- ✅ EXPLAIN ANALYZE shows query optimization

---

## 🕸️ **Neo4j Quick Reference**

### **Key Files**:
- `backend/agents/graph_agent.py` - Cypher query generation
- `data/seed_neo4j.cypher` - Graph schema

### **Important Queries**:
```cypher
// Find faulty equipment (Line 50 in graph_agent.py)
MATCH (r:Rig {name: $rig_name})-[:HAS_EQUIPMENT]->(e:Equipment)
WHERE e.status = 'FAULTY'
RETURN e;

// Visualize relationships
MATCH path = (r:Rig {name: 'Rig Alpha'})-[*1..2]->(e)
RETURN path;

// Count nodes
MATCH (n) RETURN labels(n), count(n);
```

### **Key Talking Points**:
- ✅ O(1) relationship traversal vs O(n) SQL joins
- ✅ Pattern matching with MATCH clause
- ✅ Variable-length paths with `[*1..3]`

---

## 🤖 **Multi-Agent Architecture**

### **Key Files**:
- `backend/graph_engine.py` - Orchestration
- `backend/agents/parser.py` - Intent classification
- `backend/agents/sql_agent.py` - SQL generation
- `backend/agents/graph_agent.py` - Cypher generation
- `backend/agents/reasoning_agent.py` - Answer synthesis

### **Agent Flow**:
```
User Query
    ↓
Parser Agent (classify intent, extract entities)
    ↓
SQL Agent (query PostgreSQL)
    ↓
Graph Agent (query Neo4j)
    ↓
Reasoning Agent (synthesize answer)
    ↓
Response (with confidence score)
```

### **Key Talking Points**:
- ✅ Each agent is specialized for one task
- ✅ Sequential execution with reasoning trace
- ✅ LangGraph for orchestration (optional mode)

---

## 🎨 **Frontend Architecture**

### **Key Files**:
- `frontend/app/page.tsx` - Main dashboard
- `frontend/app/explainability/page.tsx` - Explainability page
- `frontend/lib/groundedData.ts` - Single source of truth
- `frontend/components/explainability/ReasoningTimeline.tsx` - Timeline component

### **Key Technologies**:
- Next.js 13 App Router
- TanStack Query (React Query)
- TypeScript
- Tailwind CSS

### **Key Talking Points**:
- ✅ Server-side rendering for performance
- ✅ TanStack Query for data fetching and caching
- ✅ TypeScript for type safety
- ✅ Grounded data prevents inconsistencies

---

## 🔍 **Explainability & Auditability**

### **Key Features**:
1. **Reasoning Timeline**: Shows every step the AI took
2. **Query Display**: Shows exact SQL and Cypher queries
3. **Copy Button**: One-click copy for verification
4. **Export Audit Log**: Download complete JSON audit trail

### **Demo Flow**:
1. Go to http://localhost:3002/explainability
2. Enter: "show me faulty equipment at Rig Alpha"
3. Click "Analyze"
4. Expand Step 2 (SQL Agent) - show SQL query
5. Click "Copy" - paste into pgAdmin
6. Click "Export Audit Log" - show JSON

### **Key Talking Points**:
- ✅ Every query is traceable and verifiable
- ✅ Auditors can copy queries to verify independently
- ✅ Complete audit trail for regulatory compliance

---

## 📊 **Data Grounding**

### **Problem**:
- KPI cards showed different values than heat map
- AI responses didn't match critical alerts

### **Solution**:
- Created `frontend/lib/groundedData.ts` as single source of truth
- All components reference this file
- No hardcoded values

### **Key File**:
```typescript
// frontend/lib/groundedData.ts
export const REGIONS = [
  { name: 'Permian Basin', totalAssets: 850, ... },
  { name: 'Eagle Ford', totalAssets: 720, ... },
  // ...
];

export const GLOBAL_KPIS = {
  totalAssets: REGIONS.reduce((sum, r) => sum + r.totalAssets, 0),
  avgProductionRate: REGIONS.reduce(...) / REGIONS.reduce(...),
  // All computed from REGIONS
};
```

### **Key Talking Points**:
- ✅ Single source of truth prevents inconsistencies
- ✅ All KPIs are computed, not hardcoded
- ✅ Heat map, KPI cards, and AI responses all use same data

---

## 🎯 **Common Questions & Quick Answers**

### **Q: Why PostgreSQL over MySQL?**
**A**: JSONB, advanced indexing, window functions, full ACID compliance

### **Q: How do you prevent SQL injection?**
**A**: Parameterized queries with `%s` placeholders (see `sql_agent.py` line 35)

### **Q: Why use a graph database?**
**A**: O(1) relationship traversal vs O(n) SQL joins, pattern matching

### **Q: How do you handle AI hallucinations?**
**A**: Data grounding, confidence scoring, cross-checking, audit trails

### **Q: How would you scale this?**
**A**: Connection pooling, read replicas, Redis caching, Kubernetes

### **Q: What's the biggest challenge?**
**A**: Data consistency - solved with `groundedData.ts` as single source of truth

---

## 🛠️ **Quick Commands**

### **Start Services**:
```bash
# PostgreSQL (should already be running)
# Check: psql -U postgres -c "SELECT version();"

# Neo4j (should already be running)
# Check: http://localhost:7474

# Backend
cd backend
python app.py

# Frontend
cd frontend
npm run dev
```

### **Verify Everything is Running**:
```bash
# PostgreSQL
curl http://localhost:5001/api/health

# Frontend
curl http://localhost:3002

# Neo4j
# Open http://localhost:7474 in browser
```

### **Run a Test Query**:
```bash
curl -X POST http://localhost:5001/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "show me faulty equipment at Rig Alpha"}'
```

---

## 📁 **File Locations (Quick Access)**

### **Backend**:
- `backend/app.py` - Flask API server
- `backend/graph_engine.py` - Multi-agent orchestration
- `backend/agents/parser.py` - Intent classification (Line 82)
- `backend/agents/sql_agent.py` - SQL queries (Line 30)
- `backend/agents/graph_agent.py` - Cypher queries (Line 50)

### **Frontend**:
- `frontend/app/page.tsx` - Main dashboard (Line 63 for KPI cards)
- `frontend/app/explainability/page.tsx` - Explainability page
- `frontend/lib/groundedData.ts` - Single source of truth
- `frontend/components/explainability/ReasoningTimeline.tsx` - Timeline

### **Data**:
- `data/seed_sql.sql` - PostgreSQL schema and seed data
- `data/seed_neo4j.cypher` - Neo4j graph schema and seed data

---

## 🎬 **Demo Checklist**

### **Before Demo**:
- [ ] All services running (PostgreSQL, Neo4j, Backend, Frontend)
- [ ] pgAdmin open and connected
- [ ] Neo4j Browser open and connected
- [ ] VS Code open with key files
- [ ] Browser tabs open (dashboard, explainability, pgAdmin, Neo4j)

### **During Demo**:
- [ ] Start with high-level overview (5 min)
- [ ] Show multi-agent architecture (8 min)
- [ ] Demonstrate explainability (7 min)
- [ ] Explain data grounding (5 min)
- [ ] Live coding exercise (5 min)

### **Key Points to Hit**:
- [ ] Parameterized queries prevent SQL injection
- [ ] Composite indexes optimize performance
- [ ] Graph databases excel at relationship traversal
- [ ] Multi-agent architecture provides specialization
- [ ] Full explainability builds trust
- [ ] Data grounding ensures consistency

---

## 🚀 **Final Reminders**

1. **Be Confident**: You built this - you know it
2. **Show Code**: Don't just talk - open files and show
3. **Run Queries**: Demonstrate live in pgAdmin and Neo4j Browser
4. **Explain Trade-offs**: "I chose X because Y"
5. **Admit Limitations**: "In production, I'd use X"

**You've got this! 🎯**

