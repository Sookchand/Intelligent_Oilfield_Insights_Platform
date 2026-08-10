# 📚 Query Examples - AI-Powered System

## Sensor & Equipment Queries

### Find Specific Sensors
```
"What is the name and type of gauge at Well W-12?"
"Show me all sensors at Well W-13"
"List pressure gauges in the system"
"Which wells have temperature sensors?"
```

### Filter by Status
```
"What sensors are currently faulty?"
"Show me operational pressure gauges"
"Which equipment needs maintenance?"
"List all sensors with anomalies"
```

### Equipment Relationships
```
"What equipment is connected to Rig Alpha?"
"Show me all sensors monitoring Well W-12"
"Which rigs have the most sensors?"
"List all equipment in the Permian basin"
```

## Well Queries

### Basic Information
```
"List all wells"
"Show me wells in the Permian basin"
"What wells are currently active?"
"Which wells are in maintenance?"
```

### Filtering & Conditions
```
"Show me wells deeper than 8000 feet"
"List wells in Eagle Ford basin with depth over 7500 feet"
"Which wells are on Rig Beta?"
"Find wells with status 'Active' in Permian basin"
```

### Aggregations
```
"How many wells does each rig have?"
"What is the average depth of wells in Permian basin?"
"Which basin has the most wells?"
"Count wells by status"
```

## Rig Queries

### Basic Information
```
"List all rigs"
"Show me rigs in the Permian basin"
"What rigs are operated by XYZ Corp?"
"Which rig has the most wells?"
```

### Relationships
```
"What wells are on Rig Alpha?"
"Show me all equipment on Rig Beta"
"Which rigs have faulty sensors?"
"List rigs with wells in maintenance"
```

## Production Queries

### Current Production
```
"What is the current oil production at Well W-12?"
"Show me gas production for Rig Alpha"
"What is the water rate at Well W-13?"
"Display production metrics for all wells"
```

### Trends & Analysis
```
"What is the average oil production for Well W-12 in the last 7 days?"
"Show me production trends for Rig Alpha this month"
"Which well has the highest oil rate?"
"Compare production between Well W-12 and Well W-13"
```

### Anomalies & Issues
```
"Which wells have declining production?"
"Show me wells with production drops"
"What wells have abnormal pressure readings?"
"List wells with temperature anomalies"
```

## Complex Multi-Database Queries

### Combining Graph + Time-Series
```
"Show me production data for wells with faulty sensors"
"What is the average production of wells in Permian basin?"
"Which rigs have declining production and equipment issues?"
"List wells with both high production and maintenance needs"
```

### Correlation Analysis
```
"Do faulty sensors correlate with production drops?"
"Show me wells where sensor anomalies preceded production issues"
"Which equipment failures impacted production the most?"
"Analyze relationship between sensor status and production rates"
```

## Safety & Maintenance

### Equipment Status
```
"What equipment needs immediate attention?"
"Show me all faulty equipment"
"Which sensors haven't reported in 24 hours?"
"List overdue maintenance items"
```

### Risk Assessment
```
"Which wells have the most safety risks?"
"Show me equipment with multiple failures"
"What are the top 5 safety concerns?"
"List wells with both equipment issues and production problems"
```

## Advanced Queries

### Geospatial
```
"Show me all assets in the Permian basin"
"Which basin has the most equipment issues?"
"Compare production across different basins"
"List wells by basin and depth"
```

### Time-Based
```
"What happened in the last 24 hours?"
"Show me production changes over the last week"
"Which sensors were installed recently?"
"List maintenance completed this month"
```

### Aggregations & Statistics
```
"What is the total oil production across all wells?"
"Calculate average sensor uptime"
"Show me production statistics by rig"
"What percentage of sensors are operational?"
```

## Tips for Best Results

### ✅ DO:
- Be specific about what you want to know
- Mention entity names (Well W-12, Rig Alpha, etc.)
- Use clear time ranges when asking about trends
- Ask one question at a time for clarity

### ❌ DON'T:
- Use overly complex nested questions
- Mix multiple unrelated questions
- Use ambiguous pronouns without context
- Expect real-time data (system uses latest available)

## How to Test

### Via Frontend
1. Open http://localhost:3000
2. Type your question in the chat
3. View the answer and reasoning trace

### Via API
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What gauges are at Well W-12?"}'
```

### Via Test Script
```bash
python test_ai_flexible_queries.py
```

## Understanding the Response

Each response includes:
- **Answer**: Human-readable answer to your question
- **Confidence**: How confident the system is (0-1)
- **Reasoning Trace**: Step-by-step execution log
- **Data Sources**: Which databases were queried
- **AI Queries**: The actual Cypher/SQL generated (if AI was used)

Look for the 🤖 emoji in the trace to see AI-generated components!

