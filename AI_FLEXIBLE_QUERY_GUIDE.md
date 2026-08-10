# 🤖 AI-Powered Flexible Query System

## Overview

The system now uses **OpenAI GPT-4** to dynamically generate database queries from natural language, enabling it to handle **arbitrary questions** without predefined patterns.

## How It Works

### 1. **Hybrid Architecture**

```
User Question
    ↓
Query Parser (Rule-based)
    ↓
AI Router (Determines: Cypher, SQL, or Both)
    ↓
┌─────────────────┬─────────────────┐
│  AI Cypher Gen  │   AI SQL Gen    │
│  (Neo4j Graph)  │  (PostgreSQL)   │
└─────────────────┴─────────────────┘
    ↓
Flexible Executor
    ↓
AI Formatter
    ↓
Answer to User
```

### 2. **When AI is Used**

The system automatically uses AI-powered query generation when:
- The query is classified as "general_query" (no specific pattern match)
- No specific entities are detected in the query
- OpenAI API is available

Otherwise, it falls back to rule-based query execution.

### 3. **Components**

#### **AIQueryGenerator** (`backend/agents/ai_query_generator.py`)
- Converts natural language to Cypher queries
- Converts natural language to SQL queries
- Routes queries to appropriate database
- Uses GPT-4o-mini for fast, cost-effective generation

#### **FlexibleExecutor** (`backend/agents/flexible_executor.py`)
- Executes AI-generated Cypher queries against Neo4j
- Executes AI-generated SQL queries against PostgreSQL
- Formats results into human-readable answers

#### **Updated Orchestrator** (`backend/graph_engine.py`)
- Detects when to use AI vs rule-based approach
- Coordinates AI query generation and execution
- Maintains reasoning trace for transparency

## Example Queries

### ✅ Now Supported (AI-Powered)

```
"What is the name and type of gauge at Well W-12?"
→ Generates: MATCH (w:Well {name: 'W-12'})-[:HAS_SENSOR]->(s:Sensor) 
             WHERE s.sensor_type CONTAINS 'Gauge' 
             RETURN s.sensor_id, s.sensor_type

"Show me all pressure gauges in the system"
→ Generates: MATCH (s:Sensor) 
             WHERE s.sensor_type CONTAINS 'Pressure' 
             RETURN s.sensor_id, s.sensor_type, s.status

"Which wells have temperature sensors?"
→ Generates: MATCH (w:Well)-[:HAS_SENSOR]->(s:Sensor) 
             WHERE s.sensor_type CONTAINS 'Temperature' 
             RETURN DISTINCT w.name

"What sensors are currently faulty?"
→ Generates: MATCH (s:Sensor) 
             WHERE s.status = 'Faulty' 
             RETURN s.sensor_id, s.sensor_type, s.status

"Show me wells in Permian basin deeper than 8000 feet"
→ Generates: MATCH (w:Well) 
             WHERE w.basin = 'Permian' AND w.depth_ft > 8000 
             RETURN w.name, w.depth_ft, w.status

"What is the average oil production for Well W-12?"
→ Generates: SELECT AVG(oil_rate_bbl_day) 
             FROM production 
             WHERE well_name = 'W-12'
```

## Benefits

### 🎯 **Flexibility**
- Handle questions you didn't anticipate
- No need to predefine every query pattern
- Natural language understanding

### 🔍 **Transparency**
- AI-generated queries are shown in reasoning trace
- Users can see exactly what query was executed
- Explanations provided for each query

### 🛡️ **Safety**
- Queries are validated before execution
- Falls back to rule-based system if AI fails
- Error handling and logging

### ⚡ **Performance**
- Uses GPT-4o-mini for fast generation (~1-2 seconds)
- Caches schema information
- Parallel execution when possible

## Configuration

### Required Environment Variable

```bash
OPENAI_API_KEY=sk-...
```

Already configured in `backend/.env`

### Cost Optimization

- Uses **GPT-4o-mini** instead of GPT-4 (10x cheaper)
- Structured JSON output for reliability
- Low temperature (0.1) for consistency
- Schema context provided to reduce tokens

## Testing

### Run the test suite:

```bash
python test_ai_flexible_queries.py
```

This will test 8 different query types including:
- Specific sensor lookups
- Filtering by type/status
- Aggregations
- Complex multi-condition queries

### Manual Testing

Start the backend:
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Try queries in the frontend or via API:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What gauges are at Well W-12?"}'
```

## Monitoring

Check the reasoning trace in the response to see:
- Whether AI was used (`ai_powered: true`)
- Generated Cypher/SQL queries
- Execution time for each step
- Confidence scores

Example trace:
```json
{
  "step": 2,
  "agent": "AI Graph Query",
  "action": "Generated and executed Cypher query",
  "cypher_query": "MATCH (w:Well {name: 'W-12'})-[:HAS_SENSOR]->(s:Sensor)...",
  "details": {
    "ai_generated": true,
    "explanation": "Finding all sensors connected to Well W-12",
    "records_count": 3
  }
}
```

## Fallback Behavior

If OpenAI is unavailable:
1. System logs warning
2. Falls back to rule-based query parsing
3. Uses predefined patterns and templates
4. Still functional, just less flexible

## Future Enhancements

- [ ] Query result caching
- [ ] Learning from user feedback
- [ ] Multi-turn conversations
- [ ] Query optimization suggestions
- [ ] Natural language explanations of results

