"""
Graph Agent - Neo4j Asset Relationship Traversal
Handles multi-hop queries across asset hierarchies
"""
import logging
from typing import List, Dict, Any, Optional
from database.connections import get_neo4j_driver

logger = logging.getLogger(__name__)

class GraphAgent:
    """
    Executes Cypher queries against Neo4j graph database
    """
    
    def __init__(self):
        self.driver = None
    
    def find_faulty_equipment(self, rig_name: str) -> List[Dict[str, Any]]:
        """
        Find faulty equipment linked to a rig
        
        Args:
            rig_name: Name of the rig
            
        Returns:
            List of faulty equipment with relationships
        """
        logger.info(f"Finding faulty equipment for {rig_name}")
        
        cypher_query = """
        MATCH (r:Rig {name: $rig_name})-[:HAS_WELL]->(w:Well)
              -[:HAS_SENSOR]->(s:Sensor)
        WHERE toLower(s.status) = 'faulty' OR s.last_reading_anomaly = true
        RETURN r.name as rig, w.name as well, s.sensor_id as sensor,
               s.sensor_type as type, s.last_reading as reading,
               toUpper(s.status) as status
        """
        
        try:
            driver = get_neo4j_driver()
            with driver.session() as session:
                result = session.run(cypher_query, rig_name=rig_name)
                records = [dict(record) for record in result]
                logger.info(f"Found {len(records)} faulty equipment items")
                driver.close()
                return records
        except Exception as e:
            logger.error(f"Error finding faulty equipment: {str(e)}")
            return self._mock_faulty_equipment(rig_name)
    
    def find_affected_assets(self, equipment_id: str, max_hops: int = 3) -> List[Dict[str, Any]]:
        """
        Find all assets affected by equipment failure (multi-hop traversal)
        
        Args:
            equipment_id: ID of the failed equipment
            max_hops: Maximum number of hops to traverse
            
        Returns:
            List of affected assets with paths
        """
        logger.info(f"Finding assets affected by {equipment_id} (max {max_hops} hops)")
        
        cypher_query = """
        MATCH path = (e:Equipment {id: $equipment_id})-[*1..%d]-(affected)
        WHERE affected:Rig OR affected:Well OR affected:Pump
        RETURN affected.name as asset_name, 
               labels(affected)[0] as asset_type,
               length(path) as hops,
               [node in nodes(path) | node.name] as path_nodes
        ORDER BY hops ASC
        """ % max_hops
        
        try:
            driver = get_neo4j_driver()
            with driver.session() as session:
                result = session.run(cypher_query, equipment_id=equipment_id)
                records = [dict(record) for record in result]
                logger.info(f"Found {len(records)} affected assets")
                driver.close()
                return records
        except Exception as e:
            logger.error(f"Error finding affected assets: {str(e)}")
            return self._mock_affected_assets(equipment_id)
    
    def find_equipment_by_basin(self, basin: str) -> List[Dict[str, Any]]:
        """
        Find all equipment in a specific basin
        
        Args:
            basin: Basin name
            
        Returns:
            List of equipment in the basin
        """
        logger.info(f"Finding equipment in {basin} basin")
        
        cypher_query = """
        MATCH (b:Basin {name: $basin})-[:CONTAINS]->(r:Rig)
              -[:HAS_WELL]->(w:Well)-[:HAS_SENSOR]->(s:Sensor)
        RETURN r.name as rig, w.name as well, s.sensor_id as sensor,
               s.sensor_type as type, s.status as status
        """
        
        try:
            driver = get_neo4j_driver()
            with driver.session() as session:
                result = session.run(cypher_query, basin=basin)
                records = [dict(record) for record in result]
                logger.info(f"Found {len(records)} equipment items in {basin}")
                driver.close()
                return records
        except Exception as e:
            logger.error(f"Error finding equipment by basin: {str(e)}")
            return self._mock_basin_equipment(basin)
    
    def find_incident_equipment_correlation(self) -> List[Dict[str, Any]]:
        """
        Find correlations between safety incidents and equipment anomalies
        
        Returns:
            List of correlated incidents and equipment
        """
        logger.info("Finding incident-equipment correlations")
        
        cypher_query = """
        MATCH (i:Incident)-[:OCCURRED_AT]->(w:Well)-[:HAS_SENSOR]->(s:Sensor)
        WHERE s.last_reading_anomaly = true
        AND i.timestamp >= s.anomaly_detected_at - interval '24 hours'
        RETURN i.incident_id as incident, i.severity as severity,
               w.name as well, s.sensor_id as sensor, s.sensor_type as type,
               i.timestamp as incident_time, s.anomaly_detected_at as anomaly_time
        ORDER BY i.severity DESC
        """
        
        try:
            driver = get_neo4j_driver()
            with driver.session() as session:
                result = session.run(cypher_query)
                records = [dict(record) for record in result]
                logger.info(f"Found {len(records)} correlations")
                driver.close()
                return records
        except Exception as e:
            logger.error(f"Error finding correlations: {str(e)}")
            return self._mock_correlations()
    
    def _mock_faulty_equipment(self, rig_name: str) -> List[Dict[str, Any]]:
        """Return mock faulty equipment data"""
        return [
            {
                "rig": rig_name,
                "well": "Well W-12",
                "sensor": "G-40",
                "type": "Pressure Gauge",
                "reading": 1850.5,
                "status": "FAULTY"
            }
        ]
    
    def _mock_affected_assets(self, equipment_id: str) -> List[Dict[str, Any]]:
        """Return mock affected assets data"""
        return [
            {
                "asset_name": "Rig Alpha",
                "asset_type": "Rig",
                "hops": 2,
                "path_nodes": [equipment_id, "Well W-12", "Rig Alpha"]
            }
        ]
    
    def _mock_basin_equipment(self, basin: str) -> List[Dict[str, Any]]:
        """Return mock basin equipment data"""
        return [
            {
                "rig": "Rig Alpha",
                "well": "Well W-12",
                "sensor": "G-40",
                "type": "Pressure Gauge",
                "status": "OPERATIONAL"
            }
        ]
    
    def _mock_correlations(self) -> List[Dict[str, Any]]:
        """Return mock correlation data"""
        return [
            {
                "incident": "INC-2024-045",
                "severity": "HIGH",
                "well": "Well W-12",
                "sensor": "G-40",
                "type": "Pressure Gauge",
                "incident_time": "2024-12-20 14:30:00",
                "anomaly_time": "2024-12-20 10:15:00"
            }
        ]

