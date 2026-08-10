"""
LangSmith Test Dataset for Oilfield Intelligence Platform
Comprehensive test cases for reliability and accuracy validation
"""

from typing import List, Dict, Any
from datetime import datetime

# Test dataset with expected outputs
TEST_QUERIES = [
    {
        "id": "prod_drop_001",
        "query": "Why is production dropping at Rig Alpha?",
        "expected_intent": "production_analysis",
        "expected_entities": {
            "rigs": ["Rig Alpha"],
            "wells": [],
            "sensors": []
        },
        "expected_keywords": ["production", "dropping", "faulty", "sensor", "G-40", "Well W-12"],
        "expected_data_sources": ["sql", "graph"],
        "min_confidence": 0.85,
        "category": "production_analysis"
    },
    {
        "id": "faulty_equip_001",
        "query": "Show me all faulty equipment at Rig Alpha",
        "expected_intent": "equipment_status",
        "expected_entities": {
            "rigs": ["Rig Alpha"],
            "wells": [],
            "sensors": []
        },
        "expected_keywords": ["faulty", "equipment", "G-40", "Pressure Gauge"],
        "expected_data_sources": ["graph"],
        "min_confidence": 0.90,
        "category": "equipment_analysis"
    },
    {
        "id": "safety_001",
        "query": "Are there any safety risks at Rig Beta?",
        "expected_intent": "safety_analysis",
        "expected_entities": {
            "rigs": ["Rig Beta"],
            "wells": [],
            "sensors": []
        },
        "expected_keywords": ["safety", "risk", "HSE"],
        "expected_data_sources": ["sql", "vector"],
        "min_confidence": 0.80,
        "category": "safety_analysis"
    },
    {
        "id": "prod_trend_001",
        "query": "What is the production trend for Rig Alpha over the last 30 days?",
        "expected_intent": "production_analysis",
        "expected_entities": {
            "rigs": ["Rig Alpha"],
            "wells": [],
            "time_periods": ["30 days"]
        },
        "expected_keywords": ["production", "trend", "30 days"],
        "expected_data_sources": ["sql"],
        "min_confidence": 0.85,
        "category": "production_analysis"
    },
    {
        "id": "well_status_001",
        "query": "What is the status of Well W-12?",
        "expected_intent": "equipment_status",
        "expected_entities": {
            "rigs": [],
            "wells": ["Well W-12"],
            "sensors": []
        },
        "expected_keywords": ["Well W-12", "status"],
        "expected_data_sources": ["sql", "graph"],
        "min_confidence": 0.85,
        "category": "equipment_analysis"
    },
    {
        "id": "sensor_reading_001",
        "query": "What is the current reading for sensor G-40?",
        "expected_intent": "equipment_status",
        "expected_entities": {
            "rigs": [],
            "wells": [],
            "sensors": ["G-40"]
        },
        "expected_keywords": ["G-40", "sensor", "reading"],
        "expected_data_sources": ["graph"],
        "min_confidence": 0.90,
        "category": "equipment_analysis"
    },
    {
        "id": "multi_rig_001",
        "query": "Compare production between Rig Alpha and Rig Beta",
        "expected_intent": "production_analysis",
        "expected_entities": {
            "rigs": ["Rig Alpha", "Rig Beta"],
            "wells": [],
            "sensors": []
        },
        "expected_keywords": ["compare", "production", "Rig Alpha", "Rig Beta"],
        "expected_data_sources": ["sql"],
        "min_confidence": 0.80,
        "category": "production_analysis"
    },
    {
        "id": "forecast_001",
        "query": "What will production be next week at Rig Alpha?",
        "expected_intent": "forecasting",
        "expected_entities": {
            "rigs": ["Rig Alpha"],
            "wells": [],
            "time_periods": ["next week"]
        },
        "expected_keywords": ["forecast", "prediction", "next week"],
        "expected_data_sources": ["sql"],
        "min_confidence": 0.75,
        "category": "forecasting"
    },
    {
        "id": "root_cause_001",
        "query": "What caused the production drop at Rig Alpha?",
        "expected_intent": "production_analysis",
        "expected_entities": {
            "rigs": ["Rig Alpha"],
            "wells": [],
            "sensors": []
        },
        "expected_keywords": ["caused", "production drop", "faulty", "sensor"],
        "expected_data_sources": ["sql", "graph", "ontology"],
        "min_confidence": 0.85,
        "category": "root_cause_analysis"
    },
    {
        "id": "time_query_001",
        "query": "When did production first drop below 850 barrels per day for Rig Alpha?",
        "expected_intent": "production_analysis",
        "expected_entities": {
            "rigs": ["Rig Alpha"],
            "wells": [],
            "time_periods": []
        },
        "expected_keywords": ["when", "850", "barrels"],
        "expected_data_sources": ["sql"],
        "min_confidence": 0.85,
        "category": "production_analysis"
    }
]

# Additional edge cases and stress tests
EDGE_CASE_QUERIES = [
    {
        "id": "edge_ambiguous_001",
        "query": "Show me the data",
        "expected_intent": "unclear",
        "expected_behavior": "should_ask_clarification",
        "category": "edge_case"
    },
    {
        "id": "edge_no_entity_001",
        "query": "What is the production?",
        "expected_intent": "production_analysis",
        "expected_behavior": "should_ask_which_rig",
        "category": "edge_case"
    },
    {
        "id": "edge_invalid_rig_001",
        "query": "Show production for Rig XYZ",
        "expected_intent": "production_analysis",
        "expected_behavior": "should_return_no_data_found",
        "category": "edge_case"
    }
]

def get_all_test_cases() -> List[Dict[str, Any]]:
    """Get all test cases including edge cases"""
    return TEST_QUERIES + EDGE_CASE_QUERIES

def get_test_cases_by_category(category: str) -> List[Dict[str, Any]]:
    """Get test cases filtered by category"""
    return [tc for tc in TEST_QUERIES if tc.get("category") == category]

def get_critical_test_cases() -> List[Dict[str, Any]]:
    """Get only critical test cases (high confidence required)"""
    return [tc for tc in TEST_QUERIES if tc.get("min_confidence", 0) >= 0.85]

