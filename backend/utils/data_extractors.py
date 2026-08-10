"""
Data Extraction Utilities for Database Consistency
Provides unified methods to extract values from different database result formats
"""
from typing import Any, Union, Dict, List, Tuple
from decimal import Decimal


def extract_production_value(record: Union[Dict, List, Tuple]) -> float:
    """
    Extract production value from SQL result (dict or tuple format)
    
    CONSISTENCY STRATEGY: Single source of truth for production extraction
    
    Args:
        record: Database record (dict from ORM or tuple from raw SQL)
        
    Returns:
        Production value as float
        
    Examples:
        >>> extract_production_value({'production_rate': 850.5})
        850.5
        >>> extract_production_value((timestamp, 850.5, 2500, 180))
        850.5
        >>> extract_production_value({'production_bbl': Decimal('850.5')})
        850.5
    """
    if isinstance(record, dict):
        # Try multiple field names for flexibility
        value = record.get('production_rate') or record.get('production_bbl') or 0
        # Handle Decimal types from PostgreSQL
        return float(value) if value else 0.0
    elif isinstance(record, (list, tuple)) and len(record) >= 2:
        # SQL tuple format: (timestamp, production_rate, moving_avg, pressure, temperature)
        value = record[1]
        return float(value) if value is not None else 0.0
    return 0.0


def extract_timestamp(record: Union[Dict, List, Tuple]) -> Any:
    """
    Extract timestamp from SQL result
    
    Args:
        record: Database record
        
    Returns:
        Timestamp value
    """
    if isinstance(record, dict):
        return record.get('timestamp')
    elif isinstance(record, (list, tuple)) and len(record) >= 1:
        return record[0]
    return None


def extract_pressure(record: Union[Dict, List, Tuple]) -> float:
    """
    Extract pressure value from SQL result
    
    Args:
        record: Database record
        
    Returns:
        Pressure value as float
    """
    if isinstance(record, dict):
        value = record.get('pressure', 0)
        return float(value) if value else 0.0
    elif isinstance(record, (list, tuple)) and len(record) >= 4:
        # SQL tuple format: (timestamp, production_rate, moving_avg, pressure, temperature)
        value = record[3]
        return float(value) if value is not None else 0.0
    return 0.0


def extract_temperature(record: Union[Dict, List, Tuple]) -> float:
    """
    Extract temperature value from SQL result
    
    Args:
        record: Database record
        
    Returns:
        Temperature value as float
    """
    if isinstance(record, dict):
        value = record.get('temperature', 0)
        return float(value) if value else 0.0
    elif isinstance(record, (list, tuple)) and len(record) >= 5:
        # SQL tuple format: (timestamp, production_rate, moving_avg, pressure, temperature)
        value = record[4]
        return float(value) if value is not None else 0.0
    return 0.0


def normalize_graph_result(graph_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize graph database results to consistent format
    
    Args:
        graph_record: Raw Neo4j result
        
    Returns:
        Normalized dictionary with consistent keys
    """
    return {
        'rig': graph_record.get('rig', 'Unknown'),
        'well': graph_record.get('well', 'Unknown'),
        'sensor': graph_record.get('sensor', 'Unknown'),
        'type': graph_record.get('type', 'Unknown'),
        'status': graph_record.get('status', 'UNKNOWN'),
        'reading': float(graph_record.get('reading', 0)) if graph_record.get('reading') else None
    }


def calculate_average_production(records: List[Union[Dict, List, Tuple]]) -> float:
    """
    Calculate average production from a list of records
    
    CONSISTENCY STRATEGY: Use same extraction logic everywhere
    
    Args:
        records: List of database records
        
    Returns:
        Average production as float
    """
    if not records:
        return 0.0
    
    total = sum(extract_production_value(r) for r in records)
    return float(total / len(records))


def calculate_recent_average(records: List[Union[Dict, List, Tuple]], n: int = 7) -> float:
    """
    Calculate average of most recent N records
    
    Args:
        records: List of database records (assumed sorted by timestamp DESC)
        n: Number of recent records to average
        
    Returns:
        Recent average as float
    """
    if not records:
        return 0.0
    
    recent = records[:n] if len(records) >= n else records
    return calculate_average_production(recent)

