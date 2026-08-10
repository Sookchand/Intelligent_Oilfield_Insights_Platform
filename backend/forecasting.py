"""
Production Forecasting Module
Simple time-series forecasting for production trends
"""
import logging
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import statistics

logger = logging.getLogger(__name__)

class ProductionForecaster:
    """Simple production forecasting using linear regression and moving averages"""
    
    def __init__(self):
        self.forecast_days = 7
        
    def forecast_production(
        self,
        rig_name: str,
        production_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Forecast production for the next 7 days
        
        Args:
            rig_name: Name of the rig
            production_data: Historical production records
            
        Returns:
            Forecast with confidence intervals
        """
        if not production_data or len(production_data) < 3:
            return {
                "rig_name": rig_name,
                "error": "Insufficient data for forecasting (need at least 3 records)",
                "forecast": []
            }
        
        # Extract production values and timestamps
        sorted_data = sorted(production_data, key=lambda x: x.get('timestamp', ''))
        production_values = [float(r.get('production_bbl', 0)) for r in sorted_data]
        
        # Calculate trend using simple linear regression
        n = len(production_values)
        x_values = list(range(n))
        
        # Calculate slope and intercept
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(production_values)
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, production_values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        intercept = y_mean - slope * x_mean
        
        # Determine trend
        if slope > 1:
            trend = "increasing"
        elif slope < -1:
            trend = "declining"
        else:
            trend = "stable"
        
        # Calculate standard deviation for confidence intervals
        residuals = [y - (slope * x + intercept) for x, y in zip(x_values, production_values)]
        std_dev = statistics.stdev(residuals) if len(residuals) > 1 else 0
        
        # Generate forecast
        forecast_points = []
        last_timestamp = sorted_data[-1].get('timestamp', datetime.now().isoformat())
        
        try:
            last_date = datetime.fromisoformat(last_timestamp.replace('Z', '+00:00'))
        except:
            last_date = datetime.now()
        
        for i in range(1, self.forecast_days + 1):
            forecast_date = last_date + timedelta(days=i)
            forecast_value = slope * (n + i - 1) + intercept
            
            # Ensure non-negative production
            forecast_value = max(0, forecast_value)
            
            # Calculate confidence interval (95% = ~2 std devs)
            lower_bound = max(0, forecast_value - 2 * std_dev)
            upper_bound = forecast_value + 2 * std_dev
            
            forecast_points.append({
                "date": forecast_date.isoformat(),
                "production_bbl": round(forecast_value, 2),
                "lower_bound": round(lower_bound, 2),
                "upper_bound": round(upper_bound, 2),
                "confidence": 0.95
            })
        
        # Predict potential issues
        predicted_issues = []
        if trend == "declining" and slope < -5:
            predicted_issues.append("Significant production decline detected")
        if forecast_points[-1]["production_bbl"] < y_mean * 0.5:
            predicted_issues.append("Production may drop below 50% of average")
        if std_dev > y_mean * 0.3:
            predicted_issues.append("High variability in production data")
        
        # Calculate forecast accuracy metrics
        avg_production = statistics.mean(production_values)
        forecast_avg = statistics.mean([p["production_bbl"] for p in forecast_points])
        
        return {
            "rig_name": rig_name,
            "historical_data": [
                {
                    "date": r.get('timestamp', ''),
                    "production_bbl": float(r.get('production_bbl', 0))
                }
                for r in sorted_data
            ],
            "forecast": forecast_points,
            "trend": trend,
            "slope": round(slope, 4),
            "predicted_issues": predicted_issues,
            "statistics": {
                "historical_avg": round(avg_production, 2),
                "forecast_avg": round(forecast_avg, 2),
                "std_deviation": round(std_dev, 2),
                "data_points": n,
                "forecast_days": self.forecast_days
            }
        }
    
    def calculate_confidence_calibration(
        self,
        reasoning_trace: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Calculate how confidence evolves through the agent workflow
        
        Args:
            reasoning_trace: List of reasoning steps
            
        Returns:
            Confidence evolution timeline
        """
        confidence_history = []
        
        # Initial confidence (after parsing)
        confidence_history.append({
            "step": 0,
            "agent": "Parser",
            "confidence": 0.5,
            "reason": "Initial query understanding"
        })
        
        # Confidence increases with each data source
        for i, step in enumerate(reasoning_trace):
            agent = step.get("agent", "Unknown")
            
            if agent == "SQL":
                confidence_history.append({
                    "step": i + 1,
                    "agent": agent,
                    "confidence": 0.7,
                    "reason": "Structured data retrieved"
                })
            elif agent == "Graph":
                confidence_history.append({
                    "step": i + 1,
                    "agent": agent,
                    "confidence": 0.85,
                    "reason": "Relationship data added"
                })
            elif agent == "Reasoning":
                confidence_history.append({
                    "step": i + 1,
                    "agent": agent,
                    "confidence": 0.9,
                    "reason": "Multi-source synthesis complete"
                })
        
        return confidence_history

# Global instance
forecaster = ProductionForecaster()

