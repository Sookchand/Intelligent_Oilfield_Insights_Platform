"""
Reasoning Agent - Final Synthesis & Grounding
Combines data from multiple sources and generates coherent answers
"""
import logging
from typing import List, Dict, Any, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_extractors import (
    extract_production_value,
    calculate_average_production,
    calculate_recent_average
)

logger = logging.getLogger(__name__)

class ReasoningAgent:
    """
    Synthesizes information from multiple agents into coherent answers
    """
    
    def __init__(self):
        self.llm_available = False
        try:
            from langchain_openai import ChatOpenAI
            import os
            if os.getenv("OPENAI_API_KEY"):
                # Use gpt-4o-mini instead of gpt-4 (more cost-effective and available)
                self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
                self.llm_available = True
                logger.info("✅ LLM initialized successfully with gpt-4o-mini (upgraded account)")
        except Exception as e:
            logger.warning(f"LLM not available: {str(e)}. Using rule-based reasoning.")
            self.llm = None
    
    def synthesize(
        self, 
        query: str,
        sql_results: Optional[List[Dict[str, Any]]] = None,
        graph_results: Optional[List[Dict[str, Any]]] = None,
        vector_results: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Synthesize results from multiple agents into a coherent answer
        
        Args:
            query: Original user query
            sql_results: Results from SQL agent
            graph_results: Results from Graph agent
            vector_results: Results from Vector agent
            
        Returns:
            Dictionary with answer, confidence, and supporting data
        """
        logger.info("Synthesizing results from multiple agents")
        
        if self.llm_available:
            return self._llm_synthesis(query, sql_results, graph_results, vector_results)
        else:
            return self._rule_based_synthesis(query, sql_results, graph_results, vector_results)
    
    def _llm_synthesis(
        self,
        query: str,
        sql_results: Optional[List[Dict[str, Any]]],
        graph_results: Optional[List[Dict[str, Any]]],
        vector_results: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Use LLM for synthesis"""
        
        # Prepare context
        context = self._prepare_context(sql_results, graph_results, vector_results)
        
        # Create prompt with emphasis on conciseness
        prompt = f"""You are an expert oilfield analyst. Answer this question concisely and directly: {query}

Production Data:
{context['sql']}

Asset Relationships:
{context['graph']}

HSE Reports:
{context['vector']}

IMPORTANT:
- Keep your answer to 2-3 sentences maximum
- Start with the direct answer/root cause
- Include only the most critical data points (e.g., specific sensor, well, production numbers)
- Avoid lengthy explanations or numbered lists
- Be specific and actionable

Example good answer: "Production is dropping at Rig Alpha due to a faulty pressure sensor (G-40) on Well W-12. Recent production: 850 bbl/day (down from 1050 bbl/day). Immediate sensor maintenance required."
"""
        
        try:
            response = self.llm.invoke(prompt)
            answer = response.content
            
            return {
                "answer": answer,
                "confidence": 0.9,
                "method": "llm_synthesis",
                "supporting_data": context
            }
        except Exception as e:
            logger.error(f"LLM synthesis error: {str(e)}")
            return self._rule_based_synthesis(query, sql_results, graph_results, vector_results)
    
    def _rule_based_synthesis(
        self,
        query: str,
        sql_results: Optional[List[Dict[str, Any]]],
        graph_results: Optional[List[Dict[str, Any]]],
        vector_results: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Use rule-based logic for synthesis"""

        query_lower = query.lower()
        answer = ""
        confidence = 0.7

        # Detect query intent and provide specific answers
        if "list" in query_lower or "show all" in query_lower or "get all" in query_lower:
            # List query - format the graph results as a list
            answer = self._format_list_results(query_lower, graph_results)
            confidence = 0.95

        elif "production" in query_lower and ("drop" in query_lower or "dropping" in query_lower or "decline" in query_lower or "decreasing" in query_lower):
            # Production drop analysis
            answer = self._analyze_production_drop(sql_results, graph_results)
            confidence = 0.85

        elif "faulty" in query_lower or "equipment" in query_lower:
            # Equipment failure analysis
            answer = self._analyze_faulty_equipment(graph_results, sql_results)
            confidence = 0.90

        elif "safety" in query_lower or "risk" in query_lower:
            # Safety risk analysis
            answer = self._analyze_safety_risk(graph_results, sql_results)
            confidence = 0.85

        elif "predict" in query_lower or "forecast" in query_lower:
            # Production forecasting
            answer = self._analyze_forecast(sql_results)
            confidence = 0.75

        else:
            # Generic analysis - use intelligent formatting
            answer_parts = []
            if sql_results:
                sql_summary = self._summarize_sql_results(sql_results, query)
                answer_parts.append(sql_summary)
                confidence += 0.1

            if graph_results:
                graph_summary = self._summarize_graph_results(graph_results)
                answer_parts.append(graph_summary)
                confidence += 0.1

            if vector_results:
                vector_summary = self._summarize_vector_results(vector_results)
                answer_parts.append(vector_summary)
                confidence += 0.1

            if answer_parts:
                answer = " ".join(answer_parts)
            else:
                answer = "No relevant data found to answer the query."
                confidence = 0.3

        return {
            "answer": answer,
            "confidence": min(confidence, 1.0),
            "method": "rule_based_synthesis",
            "supporting_data": {
                "sql": sql_results,
                "graph": graph_results,
                "vector": vector_results
            }
        }
    
    def _prepare_context(
        self,
        sql_results: Optional[List[Dict[str, Any]]],
        graph_results: Optional[List[Dict[str, Any]]],
        vector_results: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, str]:
        """Prepare context for LLM"""
        return {
            "sql": str(sql_results) if sql_results else "No production data available",
            "graph": str(graph_results) if graph_results else "No asset relationship data available",
            "vector": str(vector_results) if vector_results else "No HSE reports available"
        }
    
    def _analyze_production_drop(self, sql_results: Optional[List[Dict[str, Any]]], graph_results: Optional[List[Dict[str, Any]]]) -> str:
        """Analyze production drop based on data"""
        if not sql_results:
            return "No production data available to analyze the drop."

        # CONSISTENCY STRATEGY: Use unified data extractors
        avg_production = calculate_average_production(sql_results)
        recent_avg = calculate_recent_average(sql_results, n=5)

        # Extract rig name from the first result
        rig_name = sql_results[0].get('rig_name', 'this rig') if sql_results else 'this rig'

        # Check for faulty equipment and build detailed explanation
        if graph_results and len(graph_results) > 0:
            # Get the first faulty equipment for detailed analysis
            first_fault = graph_results[0]
            sensor = first_fault.get('sensor', 'Unknown')
            sensor_type = first_fault.get('type', 'equipment')
            well = first_fault.get('well', 'Unknown')
            status = first_fault.get('status', 'FAULTY')

            # Build specific root cause explanation
            return f"Production is dropping at {rig_name} due to a faulty {sensor_type.lower()} ({sensor}) on {well}. The sensor has been reporting anomalous readings (status: {status}), causing automated shutdowns and suboptimal control decisions. Recent production: {recent_avg:.1f} bbl/day (average: {avg_production:.1f} bbl/day). Immediate maintenance required."

        # No faulty equipment found - generic analysis
        if recent_avg < avg_production * 0.9:
            return f"Production at {rig_name} is showing a declining trend. Recent average production is {recent_avg:.1f} bbl/day compared to the overall average of {avg_production:.1f} bbl/day, representing a {((avg_production - recent_avg) / avg_production * 100):.1f}% decrease. No faulty equipment identified. Further investigation needed."
        else:
            return f"Production at {rig_name} appears stable with an average of {avg_production:.1f} bbl/day. Recent production is {recent_avg:.1f} bbl/day. No significant issues detected."

    def _analyze_faulty_equipment(self, graph_results: Optional[List[Dict[str, Any]]], sql_results: Optional[List[Dict[str, Any]]]) -> str:
        """Analyze faulty equipment - grounded in critical alerts data"""
        if not graph_results:
            return "No faulty equipment found at this location. All systems appear to be operating normally."

        # Build detailed equipment list with issue descriptions
        faulty_items = []
        detailed_descriptions = []

        for item in graph_results:
            sensor = item.get('sensor', 'Unknown')
            sensor_type = item.get('type', 'Unknown Type')
            well = item.get('well', 'Unknown')
            status = item.get('status', 'FAULTY')
            issue = item.get('issue', '')
            reading = item.get('reading')

            # Short form for summary
            faulty_items.append(f"{sensor} ({sensor_type}) at {well}")

            # Detailed form with issue description
            if issue:
                detailed_descriptions.append(f"• {sensor} ({sensor_type}) at {well}: {issue}")
            elif reading is not None:
                detailed_descriptions.append(f"• {sensor} ({sensor_type}) at {well}: Status {status}, Reading: {reading}")
            else:
                detailed_descriptions.append(f"• {sensor} ({sensor_type}) at {well}: Status {status}")

        # Create answer with detailed information
        if len(graph_results) == 1:
            answer = f"Found 1 faulty equipment item:\n\n{detailed_descriptions[0]}"
        else:
            equipment_summary = ", ".join(faulty_items[:3])  # First 3 for summary
            if len(faulty_items) > 3:
                equipment_summary += f", and {len(faulty_items) - 3} more"

            answer = f"Found {len(graph_results)} faulty equipment items: {equipment_summary}.\n\nDetails:\n" + "\n".join(detailed_descriptions[:5])

        # Add production impact if available
        if sql_results:
            avg_production = calculate_average_production(sql_results)
            answer += f"\n\nProduction Impact: Current production averaging {avg_production:.1f} bbl/day."

        answer += "\n\nRecommendation: Immediate maintenance required to prevent further degradation and potential safety hazards."

        return answer

    def _analyze_safety_risk(self, graph_results: Optional[List[Dict[str, Any]]], sql_results: Optional[List[Dict[str, Any]]]) -> str:
        """Analyze safety risk"""
        faulty_count = len(graph_results) if graph_results else 0

        # Calculate risk score (0-100)
        risk_score = min(faulty_count * 15, 100)

        if risk_score >= 70:
            risk_level = "HIGH"
            recommendation = "Immediate action required. Consider shutting down affected wells until repairs are completed."
        elif risk_score >= 40:
            risk_level = "MEDIUM"
            recommendation = "Schedule maintenance within 24-48 hours. Increase monitoring frequency."
        else:
            risk_level = "LOW"
            recommendation = "Continue normal operations with standard monitoring protocols."

        return f"Safety risk assessment: {risk_level} (score: {risk_score}/100). {faulty_count} faulty equipment item(s) detected. {recommendation}"

    def _analyze_forecast(self, sql_results: Optional[List[Dict[str, Any]]]) -> str:
        """Analyze and forecast production"""
        if not sql_results or len(sql_results) < 7:
            return "Insufficient historical data to generate a reliable forecast. At least 7 days of data is required."

        # CONSISTENCY STRATEGY: Use unified data extractors
        # Simple trend analysis
        recent_week = sql_results[:7]
        avg_recent = calculate_average_production(recent_week)

        older_week = sql_results[7:14] if len(sql_results) >= 14 else sql_results[7:]
        avg_older = calculate_average_production(older_week) if older_week else avg_recent

        # Calculate trend
        if avg_older > 0:
            trend_pct = ((avg_recent - avg_older) / avg_older) * 100
        else:
            trend_pct = 0

        # Forecast next week
        forecast = avg_recent * (1 + (trend_pct / 100))

        trend_desc = "increasing" if trend_pct > 2 else "decreasing" if trend_pct < -2 else "stable"

        return f"Based on recent production trends ({trend_desc}, {trend_pct:+.1f}%), forecasted production for next week is approximately {forecast:.1f} bbl/day. Current 7-day average is {avg_recent:.1f} bbl/day. Note: This is a simple trend-based forecast and should be validated with domain expertise."

    def _summarize_sql_results(self, results: List[Dict[str, Any]], question: str = "") -> str:
        """Summarize SQL query results with intelligent formatting"""
        if not results:
            return ""

        # Use the FlexibleExecutor's intelligent result formatter
        try:
            from agents.flexible_executor import FlexibleExecutor
            executor = FlexibleExecutor()
            return executor.format_results(results, question)
        except Exception as e:
            logger.warning(f"Failed to use FlexibleExecutor formatter: {str(e)}")
            # Fallback to simple summary
            return f"Production data shows {len(results)} records with relevant metrics."

    def _summarize_graph_results(self, results: List[Dict[str, Any]]) -> str:
        """Summarize graph query results"""
        if not results:
            return ""

        # Extract key relationships
        return f"Asset analysis identified {len(results)} related equipment items."

    def _summarize_vector_results(self, results: List[Dict[str, Any]]) -> str:
        """Summarize vector search results"""
        if not results:
            return ""

        return f"HSE reports contain {len(results)} relevant documents."

    def _format_list_results(self, query: str, results: List[Dict[str, Any]]) -> str:
        """Format list query results into a readable answer"""
        if not results:
            return "No items found in the database."

        # Determine what type of list this is
        if "well" in query:
            return self._format_wells_list(results)
        elif "rig" in query:
            return self._format_rigs_list(results)
        elif "sensor" in query:
            return self._format_sensors_list(results)
        else:
            # Generic formatting
            return f"Found {len(results)} items: " + ", ".join([str(list(r.values())[0]) for r in results[:10]])

    def _format_wells_list(self, wells: List[Dict[str, Any]]) -> str:
        """Format wells list into readable text"""
        if not wells:
            return "No wells found."

        answer_parts = [f"Found {len(wells)} wells in the system:\n"]

        for well in wells:
            well_name = well.get("well_name", "Unknown")
            rig_name = well.get("rig_name", "N/A")
            basin = well.get("basin", "N/A")
            depth = well.get("depth", well.get("depth_ft", "N/A"))
            status = well.get("status", "N/A")

            answer_parts.append(
                f"• {well_name} - Rig: {rig_name}, Basin: {basin}, Depth: {depth} ft, Status: {status}"
            )

        return "\n".join(answer_parts)

    def _format_rigs_list(self, rigs: List[Dict[str, Any]]) -> str:
        """Format rigs list into readable text"""
        if not rigs:
            return "No rigs found."

        answer_parts = [f"Found {len(rigs)} rigs in the system:\n"]

        for rig in rigs:
            rig_name = rig.get("rig_name", "Unknown")
            basin = rig.get("basin", "N/A")
            operator = rig.get("operator", "N/A")
            well_count = rig.get("well_count", 0)

            answer_parts.append(
                f"• {rig_name} - Basin: {basin}, Operator: {operator}, Wells: {well_count}"
            )

        return "\n".join(answer_parts)

    def _format_sensors_list(self, sensors: List[Dict[str, Any]]) -> str:
        """Format sensors list into readable text"""
        if not sensors:
            return "No sensors found."

        answer_parts = [f"Found {len(sensors)} sensors in the system:\n"]

        for sensor in sensors:
            sensor_id = sensor.get("sensor_id", "Unknown")
            sensor_type = sensor.get("sensor_type", "N/A")
            well_name = sensor.get("well_name", "N/A")
            status = sensor.get("status", "N/A")
            last_reading = sensor.get("last_reading", "N/A")

            answer_parts.append(
                f"• {sensor_id} ({sensor_type}) - Well: {well_name}, Status: {status}, Last Reading: {last_reading}"
            )

        return "\n".join(answer_parts)

