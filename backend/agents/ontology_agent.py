"""
Ontology-Driven Reasoning Agent
Provides semantic reasoning and causal inference using domain ontology
"""
import logging
from typing import Dict, List, Any, Optional
from database.connections import get_neo4j_driver

logger = logging.getLogger(__name__)

class OntologyAgent:
    """
    Semantic reasoning agent that uses domain ontology for causal inference
    """
    
    def __init__(self):
        self.ontology = self._load_oilfield_ontology()
        logger.info("✅ Ontology Agent initialized")
    
    def _load_oilfield_ontology(self) -> Dict[str, Any]:
        """
        Load oilfield domain ontology
        
        This defines:
        - Concepts (classes): Equipment, Fault, Anomaly, Production
        - Relationships: CAUSES, AFFECTS, IS_A, HAS_COMPONENT
        - Rules: Causal relationships and inference rules
        """
        return {
            "concepts": {
                "Equipment": {
                    "subclasses": ["Sensor", "Pump", "Valve", "Compressor"],
                    "properties": ["status", "reading", "location", "type"]
                },
                "Anomaly": {
                    "subclasses": ["ProductionDrop", "PressureSpike", "TemperatureAnomaly"],
                    "properties": ["severity", "timestamp", "affected_asset"]
                },
                "Fault": {
                    "subclasses": ["EquipmentFault", "CalibrationError", "CommunicationFailure"],
                    "properties": ["fault_type", "detected_at", "impact"]
                },
                "Production": {
                    "properties": ["rate", "volume", "efficiency", "timestamp"]
                }
            },
            
            "causal_rules": [
                {
                    "id": "R1",
                    "name": "FaultySensorCausesProductionDrop",
                    "cause": {
                        "concept": "Sensor",
                        "condition": "status = 'FAULTY'"
                    },
                    "effect": {
                        "concept": "ProductionDrop",
                        "likelihood": 0.85
                    },
                    "explanation": "Faulty sensors provide incorrect readings, leading to suboptimal control decisions and reduced production efficiency.",
                    "domain_knowledge": "In oilfield operations, pressure and flow sensors are critical for maintaining optimal production rates."
                },
                {
                    "id": "R2",
                    "name": "PressureAnomalyCausesShutdown",
                    "cause": {
                        "concept": "PressureGauge",
                        "condition": "reading > safety_threshold"
                    },
                    "effect": {
                        "concept": "EmergencyShutdown",
                        "likelihood": 0.95
                    },
                    "explanation": "High pressure readings trigger automatic safety shutdowns to prevent equipment damage and safety hazards.",
                    "domain_knowledge": "Safety protocols require immediate shutdown when pressure exceeds operational limits."
                },
                {
                    "id": "R3",
                    "name": "MultipleEquipmentFaultsIndicateSystemicIssue",
                    "cause": {
                        "concept": "Equipment",
                        "condition": "COUNT(status = 'FAULTY') > 2"
                    },
                    "effect": {
                        "concept": "SystemicFailure",
                        "likelihood": 0.75
                    },
                    "explanation": "Multiple simultaneous equipment failures often indicate a systemic issue such as power supply problems or environmental factors.",
                    "domain_knowledge": "Correlated failures suggest common root cause rather than independent failures."
                }
            ],
            
            "relationships": {
                "CAUSES": {
                    "description": "Causal relationship between events",
                    "examples": ["EquipmentFault CAUSES ProductionDrop"]
                },
                "AFFECTS": {
                    "description": "Influence relationship",
                    "examples": ["Sensor AFFECTS Production"]
                },
                "IS_A": {
                    "description": "Class hierarchy",
                    "examples": ["Sensor IS_A Equipment"]
                },
                "HAS_COMPONENT": {
                    "description": "Composition relationship",
                    "examples": ["Rig HAS_COMPONENT Well"]
                }
            }
        }
    
    def infer_cause(self, observation: Dict[str, Any], evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Use ontology to infer causal relationships
        
        Args:
            observation: The observed anomaly (e.g., production drop)
            evidence: Available evidence from data queries
            
        Returns:
            Causal explanation with confidence score
        """
        logger.info(f"🧠 Inferring cause for observation: {observation}")
        
        # Match observation to ontology concepts
        observation_concept = self._classify_observation(observation)
        
        # Find applicable causal rules
        applicable_rules = []
        for rule in self.ontology["causal_rules"]:
            if self._rule_matches_evidence(rule, evidence):
                applicable_rules.append(rule)
        
        if not applicable_rules:
            return {
                "causal_explanation": "No causal relationship found in ontology",
                "confidence": 0.0,
                "reasoning": "Insufficient evidence to match ontology rules"
            }
        
        # Select best matching rule
        best_rule = max(applicable_rules, key=lambda r: r["effect"]["likelihood"])
        
        return {
            "causal_explanation": best_rule["explanation"],
            "domain_knowledge": best_rule["domain_knowledge"],
            "confidence": best_rule["effect"]["likelihood"],
            "rule_id": best_rule["id"],
            "rule_name": best_rule["name"],
            "reasoning": f"Applied ontology rule {best_rule['id']}: {best_rule['name']}"
        }
    
    def _classify_observation(self, observation: Dict[str, Any]) -> str:
        """Classify observation into ontology concept"""
        # Simple classification based on keywords
        obs_text = str(observation).lower()
        
        if "production" in obs_text and ("drop" in obs_text or "decrease" in obs_text):
            return "ProductionDrop"
        elif "pressure" in obs_text and ("spike" in obs_text or "high" in obs_text):
            return "PressureSpike"
        elif "temperature" in obs_text:
            return "TemperatureAnomaly"
        else:
            return "UnknownAnomaly"
    
    def _rule_matches_evidence(self, rule: Dict[str, Any], evidence: List[Dict[str, Any]]) -> bool:
        """Check if evidence matches rule conditions"""
        cause_concept = rule["cause"]["concept"]
        condition = rule["cause"]["condition"]
        
        # Check if any evidence matches the rule
        for item in evidence:
            if cause_concept.lower() in str(item).lower():
                # Simple condition matching (can be enhanced)
                if "FAULTY" in condition and item.get("status") == "FAULTY":
                    return True
        
        return False
    
    def explain_relationship(self, entity1: str, entity2: str) -> Optional[str]:
        """
        Explain the semantic relationship between two entities using ontology
        
        Args:
            entity1: First entity (e.g., "Sensor G-40")
            entity2: Second entity (e.g., "Production Rate")
            
        Returns:
            Explanation of relationship or None
        """
        # This would query Neo4j for ontology relationships
        # For now, return based on ontology knowledge
        
        if "sensor" in entity1.lower() and "production" in entity2.lower():
            return "Sensors monitor critical parameters that directly affect production rates. Faulty sensors can lead to incorrect control decisions, reducing production efficiency."
        
        return None

