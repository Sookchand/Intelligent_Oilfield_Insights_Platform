# 🛠️ Hands-On Technical Exercises

## **Goal**: Demonstrate Deep Technical Knowledge Through Live Coding

These exercises will prove you **understand the technologies**, not just copied code.

---

## 🎯 **Exercise 1: Modify a SQL Query Live** (5 minutes)

### **Scenario**:
> "Show me how you'd modify the system to track production by **basin** instead of by **rig**."

### **What to Do**:

#### **Step 1: Open `backend/agents/sql_agent.py`**

**Current Code** (Line 30):
```python
def query_production_trends(self, rig_name: str) -> List[Dict[str, Any]]:
    query = """
        SELECT timestamp, rig_name, production_rate
        FROM production_data
        WHERE rig_name = %s
        ORDER BY timestamp DESC
        LIMIT 30
    """
    cursor.execute(query, (rig_name,))
```

**Modify to**:
```python
def query_production_by_basin(self, basin_name: str) -> List[Dict[str, Any]]:
    query = """
        SELECT 
            basin,
            DATE(timestamp) as date,
            SUM(production_rate) as total_production,
            AVG(production_rate) as avg_production,
            COUNT(DISTINCT rig_name) as active_rigs
        FROM production_data
        WHERE basin = %s
        GROUP BY basin, DATE(timestamp)
        ORDER BY date DESC
        LIMIT 30
    """
    cursor.execute(query, (basin_name,))
    return cursor.fetchall()
```

### **What to Explain**:
- "I added **GROUP BY** to aggregate by basin and date"
- "Used **SUM()** and **AVG()** for aggregations"
- "Used **COUNT(DISTINCT rig_name)** to count unique rigs"
- "This shows I understand **SQL aggregation functions**"

---

## 🎯 **Exercise 2: Write a New Cypher Query** (5 minutes)

### **Scenario**:
> "Show me how you'd find all equipment that shares a **common failure pattern**."

### **What to Do**:

#### **Step 1: Open Neo4j Browser**

**Write This Query**:
```cypher
// Find equipment with similar failure patterns
MATCH (e1:Equipment)-[:LOCATED_AT]->(w1:Well)<-[:HAS_WELL]-(r:Rig)
WHERE e1.status = 'FAULTY'

MATCH (e2:Equipment)-[:LOCATED_AT]->(w2:Well)<-[:HAS_WELL]-(r)
WHERE e2.status = 'FAULTY' AND e1 <> e2

RETURN 
    r.name AS rig,
    COLLECT(DISTINCT e1.type) AS faulty_equipment_types,
    COUNT(DISTINCT e1) AS failure_count
ORDER BY failure_count DESC
```

### **What to Explain**:
- "This uses **two MATCH clauses** to find co-located failures"
- "The `e1 <> e2` ensures we don't match the same equipment"
- "**COLLECT()** aggregates the equipment types"
- "This pattern helps identify **systemic failures** vs isolated incidents"

#### **Step 2: Add to `backend/agents/graph_agent.py`**

```python
def find_failure_patterns(self, rig_name: str) -> List[Dict[str, Any]]:
    """Find common failure patterns at a rig"""
    
    cypher_query = """
        MATCH (r:Rig {name: $rig_name})-[:HAS_WELL]->(w:Well)<-[:LOCATED_AT]-(e:Equipment)
        WHERE e.status = 'FAULTY'
        WITH r, w, COLLECT(e.type) AS equipment_types, COUNT(e) AS failure_count
        WHERE failure_count > 1
        RETURN 
            w.name AS well,
            equipment_types,
            failure_count
        ORDER BY failure_count DESC
    """
    
    with self.driver.session() as session:
        result = session.run(cypher_query, rig_name=rig_name)
        return [dict(record) for record in result]
```

### **What to Explain**:
- "I use **WITH** to create an intermediate result set"
- "The **WHERE failure_count > 1** filters for multiple failures"
- "This demonstrates understanding of **Cypher's pipeline model**"

---

## 🎯 **Exercise 3: Add a New Agent** (10 minutes)

### **Scenario**:
> "Show me how you'd add a **Weather Agent** that correlates weather with production."

### **What to Do**:

#### **Step 1: Create `backend/agents/weather_agent.py`**

```python
from typing import List, Dict, Any
import requests

class WeatherAgent:
    """Agent for querying weather data"""
    
    def __init__(self):
        self.api_key = "demo_key"  # In production, use env var
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_weather_for_location(self, lat: float, lng: float) -> Dict[str, Any]:
        """Get current weather for a location"""
        
        # Mock data for demo
        return {
            "temperature": 85.5,
            "conditions": "Clear",
            "wind_speed": 12.3,
            "humidity": 45
        }
    
    def correlate_weather_production(
        self, 
        rig_name: str, 
        production_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Correlate weather with production drops"""
        
        # Simple correlation logic
        avg_production = sum(d['production_rate'] for d in production_data) / len(production_data)
        
        # Check if weather is extreme
        weather = self.get_weather_for_location(32.0, -102.0)  # Permian Basin coords
        
        if weather['temperature'] > 100 or weather['wind_speed'] > 25:
            return {
                "correlation": "HIGH",
                "reason": f"Extreme weather detected: {weather['temperature']}°F, {weather['wind_speed']} mph wind",
                "impact": "Weather may be contributing to production issues"
            }
        else:
            return {
                "correlation": "LOW",
                "reason": "Weather conditions are normal",
                "impact": "Weather is not a significant factor"
            }
```

#### **Step 2: Integrate into `backend/graph_engine.py`**

```python
from agents.weather_agent import WeatherAgent

class GraphEngine:
    def __init__(self):
        # ... existing agents ...
        self.weather_agent = WeatherAgent()
    
    def _process_sequential(self, query: str):
        # ... existing code ...
        
        # Add weather correlation step
        if "production" in query.lower() and sql_results:
            weather_data = self.weather_agent.correlate_weather_production(
                rig_name=parse_result['entities']['rigs'][0],
                production_data=sql_results
            )
            
            reasoning_trace.append({
                "step": len(reasoning_trace) + 1,
                "agent": "Weather",
                "action": "Correlated weather with production",
                "result": weather_data['reason'],
                "duration_ms": 50,
                "details": weather_data
            })
```

### **What to Explain**:
- "I created a **new agent class** following the same pattern"
- "Integrated it into the **orchestration layer**"
- "Added it to the **reasoning trace** for explainability"
- "This shows I understand the **agent architecture**"

---

## 🎯 **Exercise 4: Optimize a Query** (5 minutes)

### **Scenario**:
> "This query is slow. Show me how you'd optimize it."

### **What to Do**:

#### **Step 1: Run EXPLAIN in pgAdmin**

**Slow Query**:
```sql
SELECT * FROM production_data
WHERE basin = 'Permian'
AND timestamp > NOW() - INTERVAL '7 days'
ORDER BY production_rate DESC;
```

**Run**:
```sql
EXPLAIN ANALYZE
SELECT * FROM production_data
WHERE basin = 'Permian'
AND timestamp > NOW() - INTERVAL '7 days'
ORDER BY production_rate DESC;
```

**Point Out**:
- "See the **Seq Scan** - that's bad, it's scanning the whole table"
- "Cost is high: ~1000..5000"

#### **Step 2: Add Index**

```sql
CREATE INDEX idx_production_basin_timestamp 
ON production_data(basin, timestamp DESC);
```

#### **Step 3: Run EXPLAIN Again**

**Point Out**:
- "Now it's using **Index Scan**"
- "Cost dropped to ~10..50"
- "This is a **100x improvement**"

### **What to Explain**:
- "I created a **composite index** on the WHERE clause columns"
- "The `DESC` matches the ORDER BY direction"
- "PostgreSQL can now use an **index-only scan**"
- "In production, I'd monitor with **pg_stat_statements**"

---

## 🎯 **Exercise 5: Debug a Frontend Issue** (5 minutes)

### **Scenario**:
> "The KPI card is showing the wrong value. Debug it."

### **What to Do**:

#### **Step 1: Open Chrome DevTools**

1. Right-click on KPI card → Inspect
2. Go to Console
3. Type:
```javascript
// Check the grounded data
import { GLOBAL_KPIS } from '@/lib/groundedData';
console.log(GLOBAL_KPIS);
```

#### **Step 2: Check the Component**

Open `frontend/app/page.tsx`:

```typescript
<KPICard
  title="Production Rate"
  value={GLOBAL_KPIS.avgProductionRate.toFixed(1)}  // ← Check this
  unit="bbl/day"
/>
```

#### **Step 3: Verify the Calculation**

Open `frontend/lib/groundedData.ts`:

```typescript
export const GLOBAL_KPIS = {
  avgProductionRate: REGIONS.reduce((sum, r) => sum + r.totalProduction, 0) / 
                     REGIONS.reduce((sum, r) => sum + r.totalAssets, 0),
  // ↑ This calculates weighted average
};
```

### **What to Explain**:
- "I used **DevTools** to inspect the component state"
- "Traced the data flow: Component → groundedData.ts → REGIONS"
- "Verified the **calculation logic** is correct"
- "This shows I understand **React data flow** and **debugging**"

---

## 🎯 **Exercise 6: Add Real-Time Updates** (10 minutes)

### **Scenario**:
> "Show me how you'd add real-time production updates using WebSockets."

### **What to Do**:

#### **Step 1: Create WebSocket Server** (`backend/websocket_server.py`)

```python
import asyncio
import websockets
import json
from datetime import datetime

async def production_stream(websocket, path):
    """Stream production data to clients"""
    
    while True:
        # Simulate real-time production data
        data = {
            "timestamp": datetime.now().isoformat(),
            "rig_name": "Rig Alpha",
            "production_rate": 850.5 + (random.random() - 0.5) * 20,
            "pressure": 2500 + (random.random() - 0.5) * 100,
        }
        
        await websocket.send(json.dumps(data))
        await asyncio.sleep(5)  # Update every 5 seconds

async def main():
    async with websockets.serve(production_stream, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
```

#### **Step 2: Create React Hook** (`frontend/hooks/useProductionStream.ts`)

```typescript
import { useEffect, useState } from 'react';

export function useProductionStream() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8765');
    
    ws.onmessage = (event) => {
      const newData = JSON.parse(event.data);
      setData(newData);
    };
    
    return () => ws.close();
  }, []);
  
  return data;
}
```

#### **Step 3: Use in Component**

```typescript
import { useProductionStream } from '@/hooks/useProductionStream';

export default function LiveProductionCard() {
  const liveData = useProductionStream();
  
  return (
    <div>
      <h3>Live Production</h3>
      {liveData && (
        <p>{liveData.production_rate.toFixed(1)} bbl/day</p>
      )}
    </div>
  );
}
```

### **What to Explain**:
- "I used **WebSockets** for bidirectional real-time communication"
- "Created a **custom React hook** for reusability"
- "Used **useEffect** for connection lifecycle management"
- "This demonstrates understanding of **async programming** and **React hooks**"

---

## ✅ **Summary: What These Exercises Prove**

| Exercise | Technology | Skill Demonstrated |
|----------|-----------|-------------------|
| **1. Modify SQL** | PostgreSQL | Aggregation, GROUP BY, window functions |
| **2. Write Cypher** | Neo4j | Graph traversal, pattern matching |
| **3. Add Agent** | Python/Architecture | OOP, design patterns, integration |
| **4. Optimize Query** | PostgreSQL | Performance tuning, indexing, EXPLAIN |
| **5. Debug Frontend** | React/TypeScript | DevTools, data flow, debugging |
| **6. WebSockets** | Full Stack | Real-time systems, async programming |

---

## 🎯 **How to Use This**

1. **Pick 2-3 exercises** based on what the interviewer asks
2. **Code them live** - don't just talk about it
3. **Explain your thinking** as you code
4. **Show the results** - run the code and prove it works

This proves you're not just reading slides - you **actually know the tech**! 🚀

