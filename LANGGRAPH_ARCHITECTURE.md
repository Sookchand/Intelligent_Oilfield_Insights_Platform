# 🔄 LangGraph Orchestration Architecture

## 🎯 **Why LangGraph Was Chosen**

### **The Challenge**
Oil & Gas data analytics requires **stateful, multi-step reasoning** across heterogeneous data sources:
- Complex queries need multiple database lookups (SQL → Graph → Vector)
- Context must be maintained across agent interactions
- Decisions depend on previous results (conditional branching)
- Failures require retry logic and graceful degradation

### **Why Not Simple Chains?**
Traditional LLM chains (LangChain LCEL) are **stateless** and **linear**:
```python
# ❌ Simple Chain - No Memory, No Branching
chain = prompt | llm | parser
result = chain.invoke(query)  # One-shot, no context retention
```

**Limitations:**
- ❌ No memory between steps
- ❌ No conditional logic (if/else based on results)
- ❌ No retry mechanisms
- ❌ No parallel execution
- ❌ No human-in-the-loop

### **Why LangGraph?**
LangGraph provides **stateful orchestration** with:
- ✅ **Persistent State** - Shared memory across all agents
- ✅ **Conditional Routing** - Dynamic paths based on results
- ✅ **Cycles & Loops** - Iterative refinement
- ✅ **Checkpointing** - Resume from failures
- ✅ **Human-in-the-Loop** - Approval gates for critical decisions

---

## 🏗️ **LangGraph Implementation in Our System**

### **State Management**
```python
# backend/graph_engine.py
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    """Shared state across all agents"""
    query: str                    # Original user query
    intent: str                   # Parsed intent (production_analysis, fault_detection)
    entities: Dict[str, List[str]] # Extracted entities (rigs, wells, equipment)
    plan: List[str]               # Execution plan
    sql_results: List[Dict]       # Accumulated SQL results
    graph_results: List[Dict]     # Accumulated graph results
    vector_results: List[Dict]    # Accumulated vector search results
    final_answer: str             # Synthesized answer
    confidence: float             # Confidence score
    reasoning_trace: List[Dict]   # Full audit trail
```

**Key Benefit:** Every agent reads/writes to shared state, enabling **context-aware decisions**.

---

### **Conditional Routing**
```python
def route_query(state: AgentState) -> str:
    """
    Dynamic routing based on query intent
    
    LangGraph enables conditional branching:
    - Production queries → SQL Agent
    - Equipment queries → Graph Agent
    - Document search → Vector Agent
    - Complex queries → All agents in parallel
    """
    intent = state["intent"]
    
    if intent == "production_analysis":
        return "sql_agent"
    elif intent == "equipment_fault":
        return "graph_agent"
    elif intent == "document_search":
        return "vector_agent"
    else:
        return "multi_agent"  # Parallel execution

# Build workflow with conditional edges
workflow = StateGraph(AgentState)
workflow.add_node("parser", parse_query)
workflow.add_node("sql_agent", query_sql)
workflow.add_node("graph_agent", query_graph)
workflow.add_node("vector_agent", query_vector)
workflow.add_node("synthesizer", synthesize_results)

# Conditional routing
workflow.add_conditional_edges(
    "parser",
    route_query,
    {
        "sql_agent": "sql_agent",
        "graph_agent": "graph_agent",
        "vector_agent": "vector_agent",
        "multi_agent": "sql_agent"  # Start parallel execution
    }
)
```

**Key Benefit:** Queries are routed to the **optimal agent(s)** based on intent, not hardcoded paths.

---

### **Memory & Context Retention**
```python
# LangGraph maintains state across steps
def sql_agent(state: AgentState) -> AgentState:
    """SQL agent reads previous context"""
    entities = state["entities"]  # ← Memory from parser
    rig_name = entities.get("rigs", ["Rig Alpha"])[0]
    
    # Query production data
    results = query_production(rig_name)
    
    # Update shared state
    state["sql_results"].extend(results)
    state["reasoning_trace"].append({
        "agent": "SQL",
        "action": f"Queried production for {rig_name}",
        "result": f"Retrieved {len(results)} records"
    })
    
    return state  # ← State flows to next agent

def graph_agent(state: AgentState) -> AgentState:
    """Graph agent uses SQL results for context"""
    rig_name = state["entities"]["rigs"][0]
    sql_results = state["sql_results"]  # ← Memory from SQL agent
    
    # Use SQL results to inform graph query
    if any(r["production_rate"] < 800 for r in sql_results):
        # Production is low → search for faulty equipment
        results = find_faulty_equipment(rig_name)
    
    state["graph_results"].extend(results)
    return state
```

**Key Benefit:** Agents make **context-aware decisions** based on previous results.

---

### **Tool Execution Framework**
```python
# LangGraph integrates with LangChain tools
from langchain.tools import Tool

# Define tools for each data source
sql_tool = Tool(
    name="query_production_database",
    func=lambda query: execute_sql(query),
    description="Query PostgreSQL for production time-series data"
)

graph_tool = Tool(
    name="query_knowledge_graph",
    func=lambda query: execute_cypher(query),
    description="Query Neo4j for asset relationships and equipment status"
)

vector_tool = Tool(
    name="search_documents",
    func=lambda query: search_qdrant(query),
    description="Search technical documents and manuals"
)

# LangGraph agent with tool access
def reasoning_agent(state: AgentState) -> AgentState:
    """Agent can dynamically select tools"""
    tools = [sql_tool, graph_tool, vector_tool]
    
    # LLM decides which tool to use
    agent_executor = create_agent_executor(llm, tools)
    result = agent_executor.invoke({
        "input": state["query"],
        "context": state["sql_results"] + state["graph_results"]
    })
    
    return state
```

**Key Benefit:** Agents can **dynamically select tools** based on query requirements.

---

## 🔄 **Planning & Multi-Step Reasoning**

### **Execution Plan Generation**
```python
def create_execution_plan(state: AgentState) -> AgentState:
    """
    LangGraph enables multi-step planning
    
    Example plan for: "Why is production dropping at Rig Alpha?"
    1. Query production trends (SQL)
    2. Identify anomalies (Analysis)
    3. Search for faulty equipment (Graph)
    4. Retrieve maintenance logs (Vector)
    5. Synthesize causal explanation (Reasoning)
    """
    intent = state["intent"]
    entities = state["entities"]
    
    if intent == "production_analysis":
        plan = [
            "query_production_trends",
            "detect_anomalies",
            "find_faulty_equipment",
            "search_maintenance_logs",
            "synthesize_answer"
        ]
    
    state["plan"] = plan
    return state
```

---

## 📊 **Comparison: LangGraph vs. Alternatives**

| Feature | LangChain LCEL | Custom Orchestration | **LangGraph** |
|---------|---------------|---------------------|---------------|
| **State Management** | ❌ Stateless | ✅ Manual | ✅ Built-in |
| **Conditional Routing** | ❌ Linear | ✅ Custom logic | ✅ Native support |
| **Memory** | ❌ None | ✅ Manual | ✅ Automatic |
| **Checkpointing** | ❌ No | ❌ Complex | ✅ Built-in |
| **Human-in-Loop** | ❌ No | ✅ Custom | ✅ Native |
| **Debugging** | ⚠️ Limited | ✅ Full control | ✅ LangSmith integration |
| **Production Ready** | ⚠️ For simple cases | ✅ Yes | ✅ Yes |

---

## 🎯 **Why This Matters for Oil & Gas**

### **Real-World Scenario:**
```
Query: "Analyze production drop at Rig Alpha and recommend actions"

LangGraph Workflow:
1. Parser → Extract: Rig Alpha, Intent: production_analysis
2. SQL Agent → Query production trends (last 30 days)
3. Conditional: IF production < threshold THEN
4.   Graph Agent → Find faulty equipment
5.   Vector Agent → Search maintenance procedures
6. Ontology Agent → Infer causal relationships
7. Reasoning Agent → Synthesize recommendations
8. Human-in-Loop → Approve shutdown recommendation
9. Return → Actionable insights with full audit trail
```

**Without LangGraph:** Would require complex custom orchestration with manual state management.

**With LangGraph:** Declarative workflow with built-in state, routing, and checkpointing.

---

## ✅ **Key Takeaways**

1. **LangGraph was chosen** for stateful, multi-step reasoning across heterogeneous data sources
2. **State management** enables context-aware agent decisions
3. **Conditional routing** optimizes query execution paths
4. **Tool execution** framework integrates SQL, Graph, and Vector databases
5. **Planning capabilities** support complex multi-step workflows
6. **Production-ready** with checkpointing, error handling, and human-in-the-loop

**This is not a prototype — it's an enterprise-grade agentic system built on LangGraph's orchestration framework.**

