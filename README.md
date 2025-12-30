# **🛢️ Intelligent Oilfield Insights Platform**

An Enterprise-Grade Agentic RAG system built with **LangGraph**, **Neo4j**, and **PostgreSQL** to unify siloed Oil & Gas data into a single, natural-language reasoning interface.

## **🏗️ Project Structure**

This structure ensures **SRP (Single Responsibility Principle)** compliance and modularity for independent agent testing.

Plaintext

.  
├── backend/              \# FastAPI Application & Orchestration  
│   ├── agents/           \# Modular Agent Roles  
│   │   ├── parser.py     \# NLQ Intent & Planning  
│   │   ├── graph\_agent.py\# GraphReader / Neo4j Logic  
│   │   ├── sql\_agent.py  \# SQLAlchemy / Postgres Logic  
│   │   └── reasoning.py  \# Final Synthesis & Grounding  
│   ├── database/         \# Database Connections & Models  
│   ├── schemas/          \# Pydantic State & API Definitions  
│   ├── main.py           \# FastAPI Entry Point  
│   └── graph\_engine.py   \# LangGraph state machine definition  
├── frontend/             \# Next.js Application (App Router)  
│   ├── components/       \# ReasoningTrace, DataVisualizers, Charts  
│   └── app/              \# Dashboard Query Interface  
├── data/                 \# Data Synthesis & Seed Scripts  
│   ├── seed\_sql.sql      \# PostgreSQL production data  
│   └── seed\_graph.cypher \# Neo4j ontology & incidents  
├── tests/                \# Testing Suite (Unit & Integration)  
└── docker-compose.yml    \# Environment Orchestration

## ---

**🔄 Data Flow & Architecture**

The system unifies heterogeneous data sources through an **Orchestrated Agentic Workflow**.

1. **Ingestion**: Structured production telemetry (PostgreSQL), asset hierarchies (Neo4j), and HSE shift logs (Pinecone) are indexed.  
2. **Request**: A natural language query enters the **FastAPI** layer from the **Next.js** dashboard.  
3. **Planning**: The **Parser Node** decomposes the query into sub-tasks for specialized agents.  
4. **Retrieval**: The **SQL Agent** (telemetry) and **Graph Agent** (entities/hops) retrieve cross-domain context.  
5. **Reasoning**: **GraphReader** logic identifies if "more hops" are needed to link production drops to equipment failures.  
6. **Synthesis**: The **Reasoning Agent** generates a grounded answer with a visible **Reasoning Trace** for the user.

## ---

**🧠 Core Orchestration: graph\_engine.py**

This skeleton implements the **Stateful Reasoning Loop**, enabling autonomous decision-making.

Python

from typing import TypedDict, List, Annotated  
from langgraph.graph import StateGraph, END  
import operator

class AgentState(TypedDict):  
    query: str  
    plan: List\[str\]  
    context: Annotated\[List\[str\], operator.add\]  
    final\_answer: str

def planner(state: AgentState):  
    """Identifies if we need SQL (numbers) or Graph (relationships)."""  
    return {"plan": \["sql\_retriever", "graph\_retriever"\]}

def graph\_retriever(state: AgentState):  
    """Executes GraphReader 'Hop Analysis' for asset relationships."""  
    return {"context": \["Graph: Well W1 linked to faulty Pressure Gauge G-40."\]}

\# Define the workflow graph  
workflow \= StateGraph(AgentState)  
workflow.add\_node("planner", planner)  
workflow.add\_node("graph\_retriever", graph\_retriever)  
workflow.set\_entry\_point("planner")  
workflow.add\_edge("planner", "graph\_retriever")  
workflow.add\_edge("graph\_retriever", END)  
graph \= workflow.compile()

## ---

**🎨 Frontend: The "Glass Box" Dashboard**

The frontend is built for **Observability**, allowing users to audit the AI's logic.

### **1\. Agentic Trace (Explainability)**

A real-time timeline of LangGraph execution steps:

* 🔵 **Plan**: Intent decomposition.  
* 🟢 **SQL Action**: Querying production logs.  
* 🟡 **Graph Hop**: Linking rigs to gauge anomalies via the **GraphReader**.  
* ✅ **Synthesis**: Root-cause analysis generation.

### **2\. GraphReader Workspace (Visual Grounding)**

* **Node-Link Map**: Visualizes the specific "path" (e.g., Rig ➔ Well ➔ Gauge) the agent traversed.  
* **Metadata Tooltips**: Hover over nodes to see live readings from the relational database.

## ---

**🛠️ Step-by-Step Build Plan**

### **Phase 1: Environment & Infrastructure**

* **Isolation**: Configure .env for secure environment isolation.  
* **SQLAlchemy**: Define relational models for production time-series data.  
* **Neo4j Ontology**: Build the semantic layer (Rigs → Wells → Gauges → Incidents).

### **Phase 2: Individual Agent Development**

* **SQL Agent**: Implement NL-to-SQL for trend detection.  
* **GraphReader Agent**: Implement NL-to-Cypher for multi-hop asset traversal.  
* **Vector Agent**: Implement semantic search for HSE reports in Pinecone.

### **Phase 3: QA & Deployment**

* **FastAPI**: Wrap the workflow in microservices with structured JSON logging.  
* **Unit Testing**: Validate translation accuracy (\>90%) for SQL and Cypher.  
* **Containerization**: Dockerize the stack for production deployment.

---

**Next Step**: Would you like me to generate the **backend/database/models.py** file to define the SQLAlchemy schemas for your PostgreSQL layer?