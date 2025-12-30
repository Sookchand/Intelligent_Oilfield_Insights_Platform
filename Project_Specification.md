# Specification: Intelligent Oilfield Insights Platform

## 1. Intent & Goals
- **Problem Statement**: Oil & Gas data is siloed across relational databases (production), knowledge graphs (assets/hierarchy), and unstructured reports (HSE/Safety). Decision-makers lack a unified interface to correlate these sources.
- **Business Value**: Reduce Mean Time to Knowledge (MTTK) for engineers by providing an agentic reasoning layer that identifies correlations (e.g., pressure spikes vs. equipment failure).
- **Success Criteria (SMART)**: 
  - Accuracy > 90% on NL-to-SQL and NL-to-Cypher translations.
  - End-to-end query latency < 5 seconds for multi-agent retrieval.

## 2. Scope & Constraints
- **In-Scope**: LangGraph orchestration, Hybrid retrieval (SQL, Graph, Vector), and a Reasoning agent for data synthesis.
- **Out-of-Scope**: Real-time SCADA streaming (V1 uses batch data); Integration with proprietary PPDM schemas (V1 uses simplified industry models).

## 3. Interfaces & Data Requirements
- **Input**: Natural Language Query (NLQ) via FastAPI endpoint.
- **Output**: JSON containing a structured summary, data tables, and reasoning logs.
- **Data Sources**: PostgreSQL (Production), Neo4j (Ontology), Pinecone (HSE Reports).

4. Demonstration Scenarios & Test Questions
- The following scenarios must be implemented to prove the system's ability to handle multi-step reasoning, context retention, and cross-domain entity linking.

- **Scenario A**: Operational Performance & Root Cause Analysis
- Goal: Demonstrate SQL-to-Graph-to-Vector "Hop Analysis."
- **Question**: "Why is production dropping at Rig Alpha?"
- Expected Path: SQL Agent identifies the trend ➔ Graph Agent identifies linked faulty sensors ➔ Vector Agent retrieves recent repair logs.
- "Which wells in the Permian Basin are currently producing below their 30-day average?"
- Expected Path: SQL Agent performs time-series aggregation and filtering.
- "Identify all assets currently affected by the pump failure at Block-12."

- Expected Path: Graph Agent performs multi-hop traversal from the failed equipment to all downstream wells.

- **Scenario B**: Safety, Compliance, and Risk Exposure
- Goal: Demonstrate semantic retrieval grounded in physical asset ontologies. 4. "Are there any recurring safety incidents linked to the pressure gauge anomalies we saw last week?" * Expected Path: Graph Agent links timestamps of anomalies to specific equipment ➔ Vector Agent retrieves correlated HSE reports. 5. "Show me high-severity incidents for wells that are currently in 'Maintenance' status." * Expected Path: SQL Agent filters by status ➔ Vector Agent retrieves and ranks reports by severity.

- **Scenario C**: Maintenance Optimization & Reliability
- Goal: Demonstrate the system's ability to translate industry-specific use cases into actionable insights. 6. "Which rigs have overdue preventive maintenance tasks and have also reported mechanical vibrations?" * Expected Path: SQL Agent finds overdue dates ➔ Vector Agent retrieves vibration mentions from operator notes. 7. "What is the correlation between downtime at Rig Delta and historical sensor malfunctions?" * Expected Path: Hybrid retrieval aggregating downtime logs (SQL) and sensor history (Graph/Vector).

5. Success Criteria for Demonstration (KPIs)
- Explainability: Every answer must be accompanied by a Reasoning Trace showing which databases were queried and why.
- Visual Grounding: Knowledge Graph "hops" must be visualized on the frontend to prove the GraphReader logic.
- Domain Accuracy: All responses must correctly use industry terminology (e.g., BOP, SCADA, Wellbore, PPDM).