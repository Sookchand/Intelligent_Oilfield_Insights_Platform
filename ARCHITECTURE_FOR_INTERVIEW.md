# 🏗️ System Architecture - Halliburton Interview

**Use this to explain the technical architecture during the interview**

---

## 📊 **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js 14)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Main Query   │  │Explainability│  │  Dashboard   │          │
│  │   Page       │  │    Page      │  │   (Future)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI + Python)                    │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │           LangGraph Orchestration Engine                  │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │ │
│  │  │ Parser  │→ │   SQL   │→ │  Graph  │→ │Reasoning│     │ │
│  │  │  Agent  │  │  Agent  │  │  Agent  │  │  Agent  │     │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘     │ │
│  │       ↓            ↓            ↓            ↓           │ │
│  │  [Intent]    [SQL Query]  [Cypher]    [Synthesis]       │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
           │                │                │
           │                │                │
           ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ PostgreSQL   │  │    Neo4j     │  │   Qdrant     │
│              │  │              │  │              │
│ Time-Series  │  │ Asset Graph  │  │Vector Search │
│ Production   │  │ Relationships│  │ HSE Reports  │
│ Telemetry    │  │ Equipment    │  │ Documents    │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## 🔄 **Query Flow (Step-by-Step)**

### **Example: "Why is production dropping at Rig Alpha?"**

```
1. USER QUERY
   ↓
2. PARSER AGENT
   - Detects intent: "production_analysis"
   - Extracts entities: ["Rig Alpha"]
   - Creates plan: [SQL, Graph, Reasoning]
   ↓
3. SQL AGENT
   - Executes: SELECT * FROM production_data WHERE rig_name = 'Rig Alpha'
   - Returns: 70 records with production trends
   ↓
4. GRAPH AGENT
   - Executes: MATCH (r:Rig)-[:HAS_WELL]->(w:Well)-[:HAS_SENSOR]->(s:Sensor)
   - Returns: 1 faulty sensor (G-40 at Well W-12)
   ↓
5. REASONING AGENT
   - Synthesizes SQL + Graph results
   - Calculates: avg_production = 943.2 bbl/day
   - Identifies: 1 faulty equipment contributing to decline
   - Generates: Natural language answer with 85% confidence
   ↓
6. RESPONSE TO USER
   - Answer with reasoning trace
   - Graph path visualization
   - Source attribution
```

---

## 🎯 **Multi-Hop Graph Traversal**

### **Traditional RAG (Flat Chunks)**
```
Query: "Why is production dropping?"
  ↓
Vector Search: Find documents with "production" + "dropping"
  ↓
Return: Text chunks (no relationships)
```

### **GraphReader RAG (Relationship-Aware)**
```
Query: "Why is production dropping at Rig Alpha?"
  ↓
Graph Traversal:
  Rig Alpha (node)
    ↓ [:HAS_WELL] (1-hop)
  Well W-12 (node)
    ↓ [:HAS_SENSOR] (2-hop)
  Sensor G-40 (node, status: FAULTY)
  ↓
Return: Relationship path + context
```

**Key Advantage:** Finds root causes through relationships, not just keywords

---

## 🗄️ **Database Schema Design**

### **PostgreSQL (Time-Series)**
```sql
CREATE TABLE production_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    rig_name VARCHAR(100),
    well_name VARCHAR(100),
    basin VARCHAR(100),
    production_rate DECIMAL(10,2),  -- bbl/day
    pressure DECIMAL(10,2),         -- psi
    temperature DECIMAL(10,2),      -- °F
    moving_avg DECIMAL(10,2)        -- 30-day moving average
);

-- Optimized for time-series queries
CREATE INDEX idx_rig_timestamp ON production_data(rig_name, timestamp DESC);
```

### **Neo4j (Asset Graph)**
```cypher
// Node Types
(:Rig {name, location, basin})
(:Well {name, depth, type})
(:Sensor {sensor_id, type, status, last_reading})

// Relationships
(Rig)-[:HAS_WELL]->(Well)
(Well)-[:HAS_SENSOR]->(Sensor)
(Sensor)-[:MONITORS]->(Equipment)

// Example Query (2-hop traversal)
MATCH (r:Rig {name: 'Rig Alpha'})-[:HAS_WELL]->(w:Well)
      -[:HAS_SENSOR]->(s:Sensor)
WHERE toLower(s.status) = 'faulty'
RETURN r.name, w.name, s.sensor_id, s.status
```

---

## 🧠 **Agent Responsibilities**

| Agent | Input | Output | Database |
|-------|-------|--------|----------|
| **Parser** | Natural language query | Intent, entities, execution plan | None |
| **SQL** | Rig/well name, time range | Production trends, telemetry | PostgreSQL |
| **Graph** | Rig/well/sensor name | Asset relationships, faulty equipment | Neo4j |
| **Vector** | Semantic query | HSE reports, documents | Qdrant |
| **Reasoning** | All agent results | Synthesized answer, confidence | None |

---

## 🔐 **Data Consistency Strategy**

### **Problem:** Different databases return different formats
- PostgreSQL: Tuples `(timestamp, production_rate, pressure)`
- Neo4j: Dictionaries `{rig: "Rig Alpha", well: "Well W-12"}`
- Qdrant: Vectors with metadata

### **Solution:** Unified Data Extractors
```python
# backend/utils/data_extractors.py

def extract_production_value(record):
    """Single source of truth for production extraction"""
    if isinstance(record, dict):
        return float(record.get('production_rate', 0))
    elif isinstance(record, tuple):
        return float(record[1])  # Production is 2nd element
    return 0.0

def calculate_average_production(records):
    """Consistent averaging across all agents"""
    return sum(extract_production_value(r) for r in records) / len(records)
```

**Result:** All agents report the same production value (943.2 bbl/day)

---

## 📈 **Scalability Design**

### **Current (Development)**
- Single Docker Compose stack
- 4 containers (Frontend, Backend, PostgreSQL, Neo4j)
- Local development environment

### **Production (Halliburton Scale)**
```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                        │
└─────────────────────────────────────────────────────────┘
         │                │                │
    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
    │Backend 1│      │Backend 2│      │Backend 3│
    └─────────┘      └─────────┘      └─────────┘
         │                │                │
    ┌────▼────────────────▼────────────────▼────┐
    │         PostgreSQL Cluster (Sharded)      │
    │  Shard 1: Permian Basin                   │
    │  Shard 2: Eagle Ford Basin                │
    │  Shard 3: Bakken Basin                    │
    └───────────────────────────────────────────┘
         │                │                │
    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
    │ Neo4j   │      │ Qdrant  │      │  MinIO  │
    │Cluster  │      │Cluster  │      │Cluster  │
    └─────────┘      └─────────┘      └─────────┘
```

**Scaling Strategy:**
- **Horizontal:** Add more backend instances
- **Database Sharding:** Partition by basin/region
- **Caching:** Redis for frequent queries
- **CDN:** Static assets on CloudFront

---

## 🎯 **Key Differentiators for Halliburton**

1. **GraphReader RAG** - Not just vector search
2. **Multi-hop traversal** - Find root causes through relationships
3. **Hybrid retrieval** - SQL + Graph + Vector unified
4. **100% auditability** - Every answer traceable to source
5. **Production-ready** - Docker, health checks, error handling
6. **Domain-specific** - Built for oilfield operations

---

**This is what sets you apart from other candidates!** 🚀

