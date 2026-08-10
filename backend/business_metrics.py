"""
Business Metrics Calculator
Calculates downtime costs, ROI, safety risk, and forecasting
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import statistics

logger = logging.getLogger(__name__)

class BusinessMetricsCalculator:
    """Calculate business impact metrics for oil & gas operations"""
    
    def __init__(self):
        # Default values (can be configured)
        self.oil_price_per_bbl = 75.0  # USD per barrel
        self.avg_production_per_hour = 50.0  # barrels per hour
        self.sensor_repair_cost = 5000.0  # USD
        self.well_maintenance_cost = 15000.0  # USD
        
    def calculate_downtime_cost(
        self, 
        rig_name: str, 
        production_data: List[Dict[str, Any]],
        downtime_hours: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculate financial impact of production downtime
        
        Args:
            rig_name: Name of the rig
            production_data: List of production records
            downtime_hours: Optional manual downtime hours
            
        Returns:
            Dictionary with cost analysis
        """
        if not production_data:
            return {
                "rig_name": rig_name,
                "error": "No production data available",
                "total_cost_usd": 0
            }
        
        # Calculate production loss
        production_values = [float(r.get('production_bbl', 0)) for r in production_data]
        avg_production = statistics.mean(production_values) if production_values else 0
        
        # Estimate downtime if not provided
        if downtime_hours is None:
            # Look for zero or very low production periods
            downtime_hours = sum(1 for p in production_values if p < avg_production * 0.1)
        
        production_loss_bbl = downtime_hours * self.avg_production_per_hour
        total_cost = production_loss_bbl * self.oil_price_per_bbl
        
        return {
            "rig_name": rig_name,
            "production_loss_bbl": round(production_loss_bbl, 2),
            "oil_price_per_bbl": self.oil_price_per_bbl,
            "downtime_hours": round(downtime_hours, 2),
            "total_cost_usd": round(total_cost, 2),
            "avg_production_bbl": round(avg_production, 2),
            "period_days": len(production_data),
            "cost_per_hour": round(total_cost / max(downtime_hours, 1), 2)
        }
    
    def calculate_maintenance_roi(
        self,
        equipment_id: str,
        repair_cost: Optional[float] = None,
        prevented_downtime_hours: float = 48.0
    ) -> Dict[str, Any]:
        """
        Calculate ROI for equipment maintenance
        
        Args:
            equipment_id: Equipment identifier
            repair_cost: Cost to repair (defaults to sensor cost)
            prevented_downtime_hours: Estimated downtime prevented
            
        Returns:
            ROI analysis
        """
        if repair_cost is None:
            repair_cost = self.sensor_repair_cost
        
        # Calculate revenue saved
        production_saved = prevented_downtime_hours * self.avg_production_per_hour
        revenue_saved = production_saved * self.oil_price_per_bbl
        
        # Calculate ROI
        roi_percentage = ((revenue_saved - repair_cost) / repair_cost) * 100
        payback_period_days = (repair_cost / (revenue_saved / prevented_downtime_hours)) / 24
        
        return {
            "equipment_id": equipment_id,
            "repair_cost_usd": round(repair_cost, 2),
            "prevented_downtime_hours": prevented_downtime_hours,
            "production_saved_bbl": round(production_saved, 2),
            "revenue_saved_usd": round(revenue_saved, 2),
            "roi_percentage": round(roi_percentage, 2),
            "payback_period_days": round(payback_period_days, 2),
            "net_benefit_usd": round(revenue_saved - repair_cost, 2)
        }
    
    def calculate_safety_risk(
        self,
        rig_name: str,
        faulty_equipment_count: int,
        incident_count: int = 0,
        overdue_maintenance_count: int = 0
    ) -> Dict[str, Any]:
        """
        Calculate safety risk score for a rig
        
        Args:
            rig_name: Name of the rig
            faulty_equipment_count: Number of faulty equipment items
            incident_count: Number of recent incidents
            overdue_maintenance_count: Number of overdue maintenance items
            
        Returns:
            Safety risk analysis
        """
        # Calculate risk factors (0-100 scale)
        equipment_risk = min(faulty_equipment_count * 25, 100)
        incident_risk = min(incident_count * 20, 100)
        maintenance_risk = min(overdue_maintenance_count * 15, 100)
        
        # Weighted average
        total_risk = (
            equipment_risk * 0.5 +
            incident_risk * 0.3 +
            maintenance_risk * 0.2
        )
        
        # Determine risk level
        if total_risk >= 75:
            risk_level = "critical"
        elif total_risk >= 50:
            risk_level = "high"
        elif total_risk >= 25:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Generate recommendations
        recommendations = []
        if equipment_risk > 50:
            recommendations.append("Immediate equipment inspection required")
        if incident_risk > 50:
            recommendations.append("Review safety protocols and training")
        if maintenance_risk > 50:
            recommendations.append("Schedule overdue maintenance immediately")
        if total_risk > 75:
            recommendations.append("Consider temporary shutdown for safety assessment")
        
        return {
            "rig_name": rig_name,
            "risk_score": round(total_risk, 2),
            "risk_level": risk_level,
            "factors": {
                "faulty_equipment": round(equipment_risk, 2),
                "incident_history": round(incident_risk, 2),
                "maintenance_overdue": round(maintenance_risk, 2)
            },
            "counts": {
                "faulty_equipment": faulty_equipment_count,
                "incidents": incident_count,
                "overdue_maintenance": overdue_maintenance_count
            },
            "recommendations": recommendations
        }

# Global instance
metrics_calculator = BusinessMetricsCalculator()

