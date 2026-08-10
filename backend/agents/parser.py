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
            "relationship": ["linked", "connected", "affected", "related", "caused"],
            "forecast": ["predict", "forecast", "projection", "future", "next week", "next month"],
            "list": ["list", "show all", "get all", "display all", "what are", "which"]
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

        # For follow-up questions, extract just the question part (ignore context)
        actual_question = query

        # Check if this is a follow-up with context
        if "Question:" in query:
            parts = query.split("Question:")
            if len(parts) > 1:
                actual_question = parts[1].strip().lower()
                logger.info(f"🔍 Extracted question from context: '{actual_question}'")
            else:
                actual_question = query.lower()
        else:
            actual_question = query.lower()

        # Check for "what caused" or "why" questions FIRST (HIGHEST PRIORITY for follow-ups)
        if "what caused" in actual_question or "why is" in actual_question or "why did" in actual_question or "why" in actual_question:
            return "production_analysis"

        # Check for faulty/broken equipment queries
        if ("faulty" in actual_question or "broken" in actual_question or "failed" in actual_question or "failure" in actual_question) and \
           ("equipment" in actual_question or "sensor" in actual_question or "gauge" in actual_question):
            return "equipment_fault_analysis"

        # Check for list intent (most specific)
        if any(kw in actual_question for kw in self.keywords["list"]):
            # Determine what to list
            if "well" in actual_question:
                return "list_wells"
            elif "rig" in actual_question and "equipment" not in actual_question:
                return "list_rigs"
            elif "sensor" in actual_question:
                return "list_sensors"
            elif "equipment" in actual_question:
                return "list_equipment"
            return "list_query"

        # Check for forecast intent (more specific)
        if any(kw in actual_question for kw in self.keywords["forecast"]):
            return "production_forecast"

        if any(kw in actual_question for kw in self.keywords["production"]):
            if any(kw in actual_question for kw in self.keywords["trend"]):
                return "production_analysis"
            return "production_query"

        if any(kw in actual_question for kw in self.keywords["safety"]):
            return "safety_analysis"

        if any(kw in actual_question for kw in self.keywords["maintenance"]):
            return "maintenance_query"

        if any(kw in actual_question for kw in self.keywords["relationship"]):
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

        # Extract rig names (e.g., "Rig Alpha", "Rig Alpha 2", "Rig-12")
        # Use word boundary and specific patterns to avoid false matches like "rig appears"
        # Match: Rig + Name + optional space + optional number/suffix
        rig_pattern = r'\bRig\s+([A-Z][A-Za-z0-9-]+(?:\s+\d+)?|\d+[A-Za-z0-9-]*)'
        rig_matches = re.findall(rig_pattern, query)
        entities["rigs"] = [f"Rig {match}" for match in rig_matches]
        
        # Extract well names (e.g., "Well W-12", "Well Alpha", "Well Alpha 2")
        # Match: Well + Name + optional space + optional number/suffix
        well_pattern = r'\bWell\s+([A-Z][A-Za-z0-9-]+(?:\s+\d+)?|\d+[A-Za-z0-9-]*|W-\d+)'
        well_matches = re.findall(well_pattern, query)
        entities["wells"] = [f"Well {match}" for match in well_matches]
        
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

        if intent == "equipment_fault_analysis":
            # NEW: Handle faulty equipment queries
            plan.append("sql_retriever")  # Get production data to show impact
            plan.append("graph_retriever")  # Find faulty equipment via graph traversal

        elif intent in ["list_wells", "list_rigs", "list_sensors", "list_equipment", "list_query"]:
            plan.append("graph_list")  # Use graph to list entities

        elif intent == "production_forecast":
            plan.append("sql_retriever")  # Get historical production data for forecasting

        elif intent == "production_analysis":
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

