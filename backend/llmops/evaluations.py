"""
LangSmith Evaluation Framework
Automated testing and quality metrics for LLM responses
"""

import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from langsmith import Client
from langsmith.schemas import Run, Example
from .test_dataset import get_all_test_cases, get_critical_test_cases

logger = logging.getLogger(__name__)

class LLMEvaluator:
    """Evaluates LLM responses against expected outputs"""
    
    def __init__(self):
        self.client = None
        self.dataset_name = "oilfield-intelligence-test-suite"
        
        # Initialize LangSmith client if enabled
        if os.getenv("LANGCHAIN_TRACING_V2") == "true":
            try:
                self.client = Client()
                logger.info("✅ LangSmith evaluator initialized")
            except Exception as e:
                logger.warning(f"⚠️ LangSmith client initialization failed: {e}")
    
    def create_dataset(self) -> Optional[str]:
        """Create or update test dataset in LangSmith"""
        if not self.client:
            logger.warning("LangSmith not enabled, skipping dataset creation")
            return None
        
        try:
            # Get all test cases
            test_cases = get_all_test_cases()
            
            # Create dataset
            dataset = self.client.create_dataset(
                dataset_name=self.dataset_name,
                description="Comprehensive test suite for Oilfield Intelligence Platform"
            )
            
            # Add examples to dataset
            for test_case in test_cases:
                self.client.create_example(
                    dataset_id=dataset.id,
                    inputs={"query": test_case["query"]},
                    outputs={
                        "expected_intent": test_case.get("expected_intent"),
                        "expected_entities": test_case.get("expected_entities"),
                        "expected_keywords": test_case.get("expected_keywords"),
                        "min_confidence": test_case.get("min_confidence")
                    },
                    metadata={
                        "test_id": test_case["id"],
                        "category": test_case.get("category"),
                        "created_at": datetime.now().isoformat()
                    }
                )
            
            logger.info(f"✅ Created dataset '{self.dataset_name}' with {len(test_cases)} test cases")
            return dataset.id
            
        except Exception as e:
            logger.error(f"❌ Failed to create dataset: {e}")
            return None
    
    def evaluate_intent_accuracy(self, actual: str, expected: str) -> float:
        """Evaluate if intent matches expected"""
        return 1.0 if actual == expected else 0.0
    
    def evaluate_entity_extraction(self, actual: Dict, expected: Dict) -> float:
        """Evaluate entity extraction accuracy"""
        score = 0.0
        total_categories = 0
        
        for entity_type in ["rigs", "wells", "sensors"]:
            if entity_type in expected:
                total_categories += 1
                expected_entities = set(expected[entity_type])
                actual_entities = set(actual.get(entity_type, []))
                
                if expected_entities == actual_entities:
                    score += 1.0
                elif expected_entities & actual_entities:  # Partial match
                    score += 0.5
        
        return score / total_categories if total_categories > 0 else 0.0
    
    def evaluate_keyword_presence(self, response: str, expected_keywords: List[str]) -> float:
        """Check if expected keywords are present in response"""
        if not expected_keywords:
            return 1.0
        
        response_lower = response.lower()
        matches = sum(1 for keyword in expected_keywords if keyword.lower() in response_lower)
        return matches / len(expected_keywords)
    
    def evaluate_confidence_threshold(self, actual_confidence: float, min_confidence: float) -> float:
        """Check if confidence meets minimum threshold"""
        return 1.0 if actual_confidence >= min_confidence else 0.0
    
    def evaluate_response(self, 
                         query: str,
                         response: Dict[str, Any],
                         expected: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive evaluation of a single response
        
        Args:
            query: User query
            response: Actual system response
            expected: Expected outputs from test case
            
        Returns:
            Evaluation metrics
        """
        metrics = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "scores": {},
            "overall_score": 0.0,
            "passed": False
        }
        
        # Evaluate intent
        if "expected_intent" in expected and "intent" in response:
            metrics["scores"]["intent_accuracy"] = self.evaluate_intent_accuracy(
                response["intent"],
                expected["expected_intent"]
            )
        
        # Evaluate entity extraction
        if "expected_entities" in expected and "entities" in response:
            metrics["scores"]["entity_accuracy"] = self.evaluate_entity_extraction(
                response["entities"],
                expected["expected_entities"]
            )
        
        # Evaluate keyword presence
        if "expected_keywords" in expected and "answer" in response:
            metrics["scores"]["keyword_coverage"] = self.evaluate_keyword_presence(
                response["answer"],
                expected["expected_keywords"]
            )
        
        # Evaluate confidence
        if "min_confidence" in expected and "confidence" in response:
            metrics["scores"]["confidence_threshold"] = self.evaluate_confidence_threshold(
                response.get("confidence", 0.0),
                expected["min_confidence"]
            )
        
        # Calculate overall score
        if metrics["scores"]:
            metrics["overall_score"] = sum(metrics["scores"].values()) / len(metrics["scores"])
            metrics["passed"] = metrics["overall_score"] >= 0.75  # 75% threshold
        
        return metrics
    
    def run_evaluation_suite(self, query_function) -> Dict[str, Any]:
        """
        Run full evaluation suite
        
        Args:
            query_function: Function that takes a query string and returns response dict
            
        Returns:
            Evaluation results summary
        """
        test_cases = get_critical_test_cases()
        results = []
        
        logger.info(f"🧪 Running evaluation suite with {len(test_cases)} test cases...")
        
        for test_case in test_cases:
            try:
                # Run query
                response = query_function(test_case["query"])
                
                # Evaluate response
                evaluation = self.evaluate_response(
                    test_case["query"],
                    response,
                    test_case
                )
                
                evaluation["test_id"] = test_case["id"]
                evaluation["category"] = test_case.get("category")
                results.append(evaluation)
                
            except Exception as e:
                logger.error(f"❌ Test {test_case['id']} failed: {e}")
                results.append({
                    "test_id": test_case["id"],
                    "query": test_case["query"],
                    "error": str(e),
                    "passed": False
                })
        
        # Calculate summary statistics
        summary = self._calculate_summary(results)
        
        logger.info(f"✅ Evaluation complete: {summary['pass_rate']}% pass rate")
        
        return {
            "summary": summary,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_summary(self, results: List[Dict]) -> Dict[str, Any]:
        """Calculate summary statistics from evaluation results"""
        total = len(results)
        passed = sum(1 for r in results if r.get("passed", False))
        
        avg_scores = {}
        for result in results:
            for metric, score in result.get("scores", {}).items():
                if metric not in avg_scores:
                    avg_scores[metric] = []
                avg_scores[metric].append(score)
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": round((passed / total * 100) if total > 0 else 0, 2),
            "average_scores": {
                metric: round(sum(scores) / len(scores), 3)
                for metric, scores in avg_scores.items()
            }
        }

