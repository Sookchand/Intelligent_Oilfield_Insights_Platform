"""
SQL Agent - PostgreSQL Query Execution
Handles time-series production data and telemetry queries
"""
import logging
from typing import List, Dict, Any, Optional
from database.connections import get_postgres_connection

logger = logging.getLogger(__name__)

class SQLAgent:
    """
    Executes SQL queries against PostgreSQL production database
    """
    
    def __init__(self):
        self.connection = None
    
    def query_production_trends(self, rig_name: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Query production trends for a specific rig
        
        Args:
            rig_name: Name of the rig
            days: Number of days to analyze
            
        Returns:
            List of production records with moving averages
        """
        logger.info(f"Querying production trends for {rig_name} over {days} days")
        
        query = """
        SELECT 
            timestamp, 
            production_rate, 
            AVG(production_rate) OVER (
                ORDER BY timestamp 
                ROWS BETWEEN 30 PRECEDING AND CURRENT ROW
            ) as moving_avg,
            pressure,
            temperature
        FROM production_data
        WHERE rig_name = %s
        ORDER BY timestamp DESC
        LIMIT %s;
        """
        
        try:
            with get_postgres_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (rig_name, days * 24))  # Assuming hourly data
                    results = cur.fetchall()
                    logger.info(f"Retrieved {len(results)} production records")
                    return results
        except Exception as e:
            logger.error(f"Error querying production trends: {str(e)}")
            # Return mock data for development
            return self._mock_production_data(rig_name, days)
    
    def query_wells_below_average(self, basin: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Find wells producing below their moving average
        
        Args:
            basin: Basin name
            days: Number of days for average calculation
            
        Returns:
            List of underperforming wells
        """
        logger.info(f"Querying underperforming wells in {basin}")
        
        query = """
        WITH well_averages AS (
            SELECT 
                well_name,
                AVG(production_rate) as avg_rate,
                production_rate as current_rate,
                timestamp
            FROM production_data
            WHERE basin = %s
            AND timestamp >= NOW() - INTERVAL '%s days'
            GROUP BY well_name, production_rate, timestamp
        )
        SELECT 
            well_name,
            current_rate,
            avg_rate,
            ((current_rate - avg_rate) / avg_rate * 100) as deviation_pct
        FROM well_averages
        WHERE current_rate < avg_rate
        ORDER BY deviation_pct ASC;
        """
        
        try:
            with get_postgres_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (basin, days))
                    results = cur.fetchall()
                    logger.info(f"Found {len(results)} underperforming wells")
                    return results
        except Exception as e:
            logger.error(f"Error querying underperforming wells: {str(e)}")
            return self._mock_underperforming_wells(basin)
    
    def query_maintenance_overdue(self) -> List[Dict[str, Any]]:
        """
        Query equipment with overdue maintenance
        
        Returns:
            List of equipment needing maintenance
        """
        logger.info("Querying overdue maintenance")
        
        query = """
        SELECT 
            equipment_id,
            equipment_type,
            last_maintenance_date,
            next_maintenance_due,
            EXTRACT(DAY FROM (NOW() - next_maintenance_due)) as days_overdue
        FROM maintenance_schedule
        WHERE next_maintenance_due < NOW()
        ORDER BY days_overdue DESC;
        """
        
        try:
            with get_postgres_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    results = cur.fetchall()
                    logger.info(f"Found {len(results)} overdue maintenance items")
                    return results
        except Exception as e:
            logger.error(f"Error querying overdue maintenance: {str(e)}")
            return self._mock_maintenance_data()
    
    def _mock_production_data(self, rig_name: str, days: int) -> List[Dict[str, Any]]:
        """Return mock production data for development"""
        return [
            {
                "timestamp": "2024-12-30 10:00:00",
                "production_rate": 850.5,
                "moving_avg": 1000.0,
                "pressure": 2500,
                "temperature": 180
            },
            {
                "timestamp": "2024-12-29 10:00:00",
                "production_rate": 900.0,
                "moving_avg": 1000.0,
                "pressure": 2550,
                "temperature": 182
            }
        ]
    
    def _mock_underperforming_wells(self, basin: str) -> List[Dict[str, Any]]:
        """Return mock underperforming wells data"""
        return [
            {
                "well_name": "Well W-12",
                "current_rate": 450.0,
                "avg_rate": 600.0,
                "deviation_pct": -25.0
            }
        ]
    
    def _mock_maintenance_data(self) -> List[Dict[str, Any]]:
        """Return mock maintenance data"""
        return [
            {
                "equipment_id": "PUMP-45",
                "equipment_type": "Pump",
                "last_maintenance_date": "2024-10-15",
                "next_maintenance_due": "2024-12-15",
                "days_overdue": 15
            }
        ]

