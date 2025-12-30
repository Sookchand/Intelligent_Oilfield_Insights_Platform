"""
Reasoning Agent - Final Synthesis & Grounding
Combines data from multiple sources and generates coherent answers
"""
import logging
from typing import List, Dict, Any, Optional

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
                self.llm = ChatOpenAI(model="gpt-4", temperature=0)
                self.llm_available = True
                logger.info("LLM initialized successfully")
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
        
        # Create prompt
        prompt = f"""
        Based on the following data, answer this question: {query}
        
        Production Data:
        {context['sql']}
        
        Asset Relationships:
        {context['graph']}
        
        HSE Reports:
        {context['vector']}
        
        Provide a clear, concise answer with specific data points and confidence level.
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
        
        answer_parts = []
        confidence = 0.7
        
        # Analyze SQL results
        if sql_results:
            sql_summary = self._summarize_sql_results(sql_results)
            answer_parts.append(sql_summary)
            confidence += 0.1
        
        # Analyze Graph results
        if graph_results:
            graph_summary = self._summarize_graph_results(graph_results)
            answer_parts.append(graph_summary)
            confidence += 0.1
        
        # Analyze Vector results
        if vector_results:
            vector_summary = self._summarize_vector_results(vector_results)
            answer_parts.append(vector_summary)
            confidence += 0.1
        
        # Combine summaries
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
    
    def _summarize_sql_results(self, results: List[Dict[str, Any]]) -> str:
        """Summarize SQL query results"""
        if not results:
            return ""
        
        # Simple summary logic
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

