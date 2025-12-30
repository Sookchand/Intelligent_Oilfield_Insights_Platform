"""
Query Parser Agent - NLQ Intent & Planning
Decomposes natural language queries into sub-tasks for specialized agents
"""
import logging
from typing import List, Dict, Any
import re

logger = logging.getLogger(__name__)

class QueryParser:
    """
    Analyzes natural language queries and creates execution plans
    """
    
    def __init__(self):
        self.keywords = {
            "production": ["production", "output", "yield", "rate", "volume"],
            "safety": ["safety", "incident", "hse", "accident", "injury"],
            "maintenance": ["maintenance", "repair", "downtime", "service"],
            "equipment": ["rig", "well", "pump", "sensor", "gauge", "equipment"],
            "trend": ["trend", "average", "dropping", "increasing", "below", "above"],
            "relationship": ["linked", "connected", "affected", "related", "caused"]
        }
    
    def parse(self, query: str) -> Dict[str, Any]:
        """
        Parse query and determine execution plan
        
        Args:
            query: Natural language query string
            
        Returns:
            Dictionary containing intent, entities, and execution plan
        """
        logger.info(f"Parsing query: {query}")
        
        query_lower = query.lower()
        
        # Detect intent
        intent = self._detect_intent(query_lower)
        
        # Extract entities
        entities = self._extract_entities(query)
        
        # Create execution plan
        plan = self._create_plan(intent, entities)
        
        result = {
            "query": query,
            "intent": intent,
            "entities": entities,
            "plan": plan
        }
        
        logger.info(f"Parse result: {result}")
        return result
    
    def _detect_intent(self, query: str) -> str:
        """Detect primary intent of the query"""
        
        if any(kw in query for kw in self.keywords["production"]):
            if any(kw in query for kw in self.keywords["trend"]):
                return "production_analysis"
            return "production_query"
        
        if any(kw in query for kw in self.keywords["safety"]):
            return "safety_analysis"
        
        if any(kw in query for kw in self.keywords["maintenance"]):
            return "maintenance_query"
        
        if any(kw in query for kw in self.keywords["relationship"]):
            return "relationship_analysis"
        
        return "general_query"
    
    def _extract_entities(self, query: str) -> Dict[str, List[str]]:
        """Extract named entities from query"""
        
        entities = {
            "rigs": [],
            "wells": [],
            "sensors": [],
            "basins": [],
            "time_periods": []
        }
        
        # Extract rig names (e.g., "Rig Alpha", "Rig-12")
        rig_pattern = r'Rig\s+[A-Za-z0-9-]+'
        entities["rigs"] = re.findall(rig_pattern, query, re.IGNORECASE)
        
        # Extract well names (e.g., "Well W-12", "Well Alpha")
        well_pattern = r'Well\s+[A-Za-z0-9-]+'
        entities["wells"] = re.findall(well_pattern, query, re.IGNORECASE)
        
        # Extract basin names
        basin_keywords = ["Permian", "Eagle Ford", "Bakken", "Marcellus"]
        entities["basins"] = [b for b in basin_keywords if b.lower() in query.lower()]
        
        # Extract time periods
        time_keywords = ["30-day", "weekly", "monthly", "daily", "last week", "last month"]
        entities["time_periods"] = [t for t in time_keywords if t.lower() in query.lower()]
        
        return entities
    
    def _create_plan(self, intent: str, entities: Dict[str, List[str]]) -> List[str]:
        """Create execution plan based on intent and entities"""
        
        plan = []
        
        if intent == "production_analysis":
            plan.append("sql_retriever")  # Get production data
            if entities.get("rigs") or entities.get("wells"):
                plan.append("graph_retriever")  # Get asset relationships
        
        elif intent == "safety_analysis":
            plan.append("vector_retriever")  # Search HSE reports
            plan.append("graph_retriever")  # Link to equipment
        
        elif intent == "maintenance_query":
            plan.append("sql_retriever")  # Get maintenance records
            plan.append("graph_retriever")  # Get equipment hierarchy
        
        elif intent == "relationship_analysis":
            plan.append("graph_retriever")  # Primary: graph traversal
            plan.append("sql_retriever")  # Supporting: time-series data
        
        else:
            # Default plan for general queries
            plan.append("sql_retriever")
            plan.append("graph_retriever")
        
        plan.append("reasoning")  # Always end with synthesis
        
        return plan

