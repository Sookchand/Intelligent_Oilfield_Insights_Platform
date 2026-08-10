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


Interview Preparation
This **Technical Deep-Dive Cheat Sheet** is specifically designed for your interview with Halliburton. It bridges your project’s implementation with the specific technologies mentioned in the **AI Graph Engineer** job description, ensuring you speak their language and demonstrate "Senior-level" depth.

---

### **Halliburton Interview: Technical Deep-Dive & Cheat Sheet**

#### **1. GraphReader RAG & Hop Analysis (The "Graph" Expertise)**

* **The Halliburton Need:** Efficiently navigating massive asset hierarchies and subsurface data.
* **Your Talking Point:** *"Traditional RAG treats data as flat chunks. I implemented a **GraphReader** approach that treats the asset hierarchy (Rig → Well → Sensor) as a first-class citizen."*
* **Implementation Detail:** Explain that your **Graph Agent** doesn't just search for keywords; it uses **Cypher** to perform 1-hop and 2-hop traversals.
* *Example:* If a "Pump" is failing, the system automatically "hops" to find all connected "Wells" to assess the total production impact.



#### **2. LangGraph & Agentic Orchestration (The "AI Agent" Expertise)**

* **The Halliburton Need:** Robust, stateful workflows that can "self-correct" during complex queries.
* **Your Talking Point:** *"I used **LangGraph** because it allows for cyclic graphs and state management. Unlike linear chains, my agents can 'loop back' if the first SQL query doesn't provide enough context."*
* **Implementation Detail:** Mention your **Parser Agent** acts as the "Controller," decomposing a query like *"What is the safety risk at Well W-12?"* into tasks for the SQL, Graph, and Vector agents.

#### **3. Hybrid Retrieval (SQL + Graph + Vector)**

* **The Halliburton Need:** Unifying telemetry (SQL), relationships (Graph), and reports (Vector/Dark Data).
* **Your Talking Point:** *"In the energy sector, truth is distributed. My platform uses a **Triple-Retriever** pipeline: PostgreSQL for time-series telemetry, Neo4j for asset relationships, and Qdrant for semantic search in HSE reports"*.
* **Implementation Detail:** Discuss how the **Reasoning Agent** synthesizes these three streams into a single answer with a **Confidence Score**.

#### **4. Data Engineering & Infrastructure (The "Implementation" Expertise)**

* **The Halliburton Need:** Production-ready deployments using Docker, MinIO, and Cloud-native tools.
* **Your Talking Point:** *"I designed this for scalability. The entire stack is containerized with **Docker**, uses **MinIO** for object storage (HSE PDFs), and includes a **FastAPI** backend with automated health checks"*.
* **Implementation Detail:** Point out your **PostgreSQL** schema includes moving averages and production rate trends, which are critical for "Oilfield Insights".

---

### **Potential Halliburton "Gotcha" Questions & Your Responses**

| **Possible Question** | **Your "Senior Engineer" Answer** |
| --- | --- |
| *"How do you handle 'hallucinations' in the oilfield context?"* | *"Every answer is tied to a **Reasoning Trace**. I don't just provide text; I show the raw SQL results and the Graph path used, providing 100% auditability"*. |
| *"How would this scale to 10,000 wells?"* | *"The architecture is microservice-based. We can scale the SQL and Vector retrievers horizontally, and Neo4j is designed specifically for high-performance relationship queries at scale"*. |
| *"Why use Neo4j over a traditional relational DB for the hierarchy?"* | *"Relational databases struggle with deep joins. In oilfields, equipment relationships are complex. Neo4j allows us to traverse 5+ 'hops' in milliseconds to find root causes"*. |

---

### **Final Interview Tip for Friday:**

When you screen-share the **Explainability Dashboard**, emphasize the **"Source Attribution."** Halliburton engineers value "Source of Truth." Showing them that the AI can say, *"I found this in HSE Report #452 (Vector) and confirmed the pressure drop in the SCADA logs (SQL),"* will be your winning moment.

**You are fully prepared. Good luck on Friday, January 9th!**