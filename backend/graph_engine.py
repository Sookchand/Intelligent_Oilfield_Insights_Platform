"""
LangGraph State Machine for Agent Orchestration
Implements the stateful reasoning loop for multi-agent coordination
"""
import logging
from typing import TypedDict, List, Annotated, Dict, Any
import operator

logger = logging.getLogger(__name__)

# Try to import LangGraph
try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    logger.warning("LangGraph not available. Using simplified orchestration.")
    LANGGRAPH_AVAILABLE = False

from agents import QueryParser, SQLAgent, GraphAgent, ReasoningAgent

class AgentState(TypedDict):
    """State shared across all agents"""
    query: str
    intent: str
    entities: Dict[str, List[str]]
    plan: List[str]
    sql_results: Annotated[List[Dict[str, Any]], operator.add]
    graph_results: Annotated[List[Dict[str, Any]], operator.add]
    vector_results: Annotated[List[Dict[str, Any]], operator.add]
    final_answer: str
    confidence: float
    reasoning_trace: Annotated[List[Dict[str, Any]], operator.add]

class OilfieldOrchestrator:
    """
    Orchestrates multiple agents to answer complex queries
    """
    
    def __init__(self):
        self.parser = QueryParser()
        self.sql_agent = SQLAgent()
        self.graph_agent = GraphAgent()
        self.reasoning_agent = ReasoningAgent()
        
        if LANGGRAPH_AVAILABLE:
            self.workflow = self._build_langgraph_workflow()
        else:
            self.workflow = None
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a natural language query through the agent workflow
        
        Args:
            query: Natural language query string
            
        Returns:
            Dictionary with answer, reasoning trace, and supporting data
        """
        logger.info(f"Processing query: {query}")
        
        if LANGGRAPH_AVAILABLE and self.workflow:
            return self._process_with_langgraph(query)
        else:
            return self._process_sequential(query)
    
    def _process_sequential(self, query: str) -> Dict[str, Any]:
        """
        Process query using sequential agent execution (fallback)
        """
        reasoning_trace = []
        
        # Step 1: Parse query
        parse_result = self.parser.parse(query)
        reasoning_trace.append({
            "step": 1,
            "agent": "Parser",
            "action": "Query decomposition",
            "result": f"Intent: {parse_result['intent']}"
        })
        
        sql_results = []
        graph_results = []
        
        # Step 2: Execute SQL queries if needed
        if "sql_retriever" in parse_result["plan"]:
            if parse_result["entities"].get("rigs"):
                rig_name = parse_result["entities"]["rigs"][0]
                sql_results = self.sql_agent.query_production_trends(rig_name)
                reasoning_trace.append({
                    "step": len(reasoning_trace) + 1,
                    "agent": "SQL",
                    "action": f"Queried production trends for {rig_name}",
                    "result": f"Retrieved {len(sql_results)} records"
                })
        
        # Step 3: Execute Graph queries if needed
        if "graph_retriever" in parse_result["plan"]:
            if parse_result["entities"].get("rigs"):
                rig_name = parse_result["entities"]["rigs"][0]
                graph_results = self.graph_agent.find_faulty_equipment(rig_name)
                reasoning_trace.append({
                    "step": len(reasoning_trace) + 1,
                    "agent": "Graph",
                    "action": f"Searched for faulty equipment at {rig_name}",
                    "result": f"Found {len(graph_results)} items"
                })
        
        # Step 4: Synthesize results
        synthesis = self.reasoning_agent.synthesize(
            query=query,
            sql_results=sql_results,
            graph_results=graph_results
        )
        
        reasoning_trace.append({
            "step": len(reasoning_trace) + 1,
            "agent": "Reasoning",
            "action": "Synthesized final answer",
            "result": f"Confidence: {synthesis['confidence']}"
        })
        
        # Extract graph path if available
        graph_path = None
        if graph_results:
            graph_path = [
                graph_results[0].get("rig"),
                graph_results[0].get("well"),
                graph_results[0].get("sensor")
            ]
        
        return {
            "answer": synthesis["answer"],
            "reasoning_trace": reasoning_trace,
            "graph_path": graph_path,
            "confidence": synthesis["confidence"],
            "data": {
                "sql_results": sql_results,
                "graph_results": graph_results
            }
        }
    
    def _build_langgraph_workflow(self):
        """Build LangGraph workflow (when available)"""
        # TODO: Implement full LangGraph workflow
        logger.info("LangGraph workflow building not yet implemented")
        return None
    
    def _process_with_langgraph(self, query: str) -> Dict[str, Any]:
        """Process query using LangGraph (when available)"""
        # For now, fall back to sequential processing
        return self._process_sequential(query)

# Global orchestrator instance
orchestrator = OilfieldOrchestrator()

def process_query(query: str) -> Dict[str, Any]:
    """
    Convenience function to process queries
    """
    return orchestrator.process_query(query)

