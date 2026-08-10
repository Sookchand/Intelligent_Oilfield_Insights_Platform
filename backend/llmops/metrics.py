"""
LLM Metrics and Evaluation Framework
Track quality, cost, and performance of LLM operations
"""
import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class LLMMetrics:
    """Track LLM performance metrics"""
    
    def __init__(self):
        self.query_metrics: List[Dict[str, Any]] = []
    
    def log_query(
        self,
        query: str,
        answer: str,
        model: str,
        latency_ms: float,
        tokens_used: int,
        cost_usd: float,
        confidence: float,
        metadata: Optional[Dict] = None
    ):
        """Log metrics for a single query"""
        
        metric = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "answer": answer,
            "model": model,
            "latency_ms": latency_ms,
            "tokens_used": tokens_used,
            "cost_usd": cost_usd,
            "confidence": confidence,
            "metadata": metadata or {}
        }
        
        self.query_metrics.append(metric)
        
        logger.info(f"""
        📊 LLM Query Metrics:
        - Model: {model}
        - Latency: {latency_ms:.0f}ms
        - Tokens: {tokens_used}
        - Cost: ${cost_usd:.4f}
        - Confidence: {confidence:.0%}
        """)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics"""
        
        if not self.query_metrics:
            return {"total_queries": 0}
        
        total_queries = len(self.query_metrics)
        total_cost = sum(m["cost_usd"] for m in self.query_metrics)
        avg_latency = sum(m["latency_ms"] for m in self.query_metrics) / total_queries
        avg_confidence = sum(m["confidence"] for m in self.query_metrics) / total_queries
        
        return {
            "total_queries": total_queries,
            "total_cost_usd": total_cost,
            "avg_latency_ms": avg_latency,
            "avg_confidence": avg_confidence,
            "cost_per_query": total_cost / total_queries if total_queries > 0 else 0
        }


class OilfieldLLMMetrics:
    """Domain-specific metrics for oilfield queries"""
    
    @staticmethod
    def check_numerical_accuracy(answer: str, ground_truth: Dict[str, Any]) -> float:
        """
        Check if numbers in answer match ground truth
        
        Returns:
            Accuracy score 0.0 to 1.0
        """
        # Extract numbers from answer
        answer_numbers = re.findall(r'\d+\.?\d*', answer)
        
        # Extract numbers from ground truth
        truth_numbers = []
        for value in ground_truth.values():
            if isinstance(value, (int, float)):
                truth_numbers.append(str(value))
        
        if not answer_numbers or not truth_numbers:
            return 0.0
        
        # Check how many answer numbers are in ground truth
        matches = sum(1 for num in answer_numbers if num in truth_numbers)
        
        return matches / len(answer_numbers) if answer_numbers else 0.0
    
    @staticmethod
    def check_entity_accuracy(answer: str, expected_entities: List[str]) -> float:
        """
        Check if expected entities (rigs, wells, sensors) are mentioned
        
        Returns:
            Accuracy score 0.0 to 1.0
        """
        if not expected_entities:
            return 1.0
        
        matches = sum(1 for entity in expected_entities if entity in answer)
        
        return matches / len(expected_entities)
    
    @staticmethod
    def measure_conciseness(answer: str, target_words: int = 50) -> float:
        """
        Measure how concise the answer is
        
        Returns:
            Score 0.0 to 1.0 (1.0 = perfect conciseness)
        """
        word_count = len(answer.split())
        
        if word_count <= target_words:
            return 1.0
        
        # Penalize verbosity
        excess_ratio = (word_count - target_words) / target_words
        score = max(0.0, 1.0 - (excess_ratio * 0.5))
        
        return score
    
    @staticmethod
    def detect_hallucinations(answer: str, data_sources: List[Dict]) -> Dict[str, Any]:
        """
        Detect potential hallucinations by checking if answer data exists in sources
        
        Returns:
            Dict with hallucination analysis
        """
        # Extract all numbers from answer
        answer_numbers = set(re.findall(r'\d+\.?\d*', answer))
        
        # Extract all numbers from data sources
        source_numbers = set()
        for source in data_sources:
            for value in source.values():
                if isinstance(value, (int, float)):
                    source_numbers.add(str(value))
        
        # Find numbers in answer not in sources
        hallucinated_numbers = answer_numbers - source_numbers
        
        hallucination_score = len(hallucinated_numbers) / len(answer_numbers) if answer_numbers else 0.0
        
        return {
            "hallucination_score": hallucination_score,
            "hallucinated_numbers": list(hallucinated_numbers),
            "total_numbers": len(answer_numbers),
            "verified_numbers": len(answer_numbers) - len(hallucinated_numbers)
        }


# Global metrics instance
llm_metrics = LLMMetrics()

