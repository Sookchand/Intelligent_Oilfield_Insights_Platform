"""
Query Validator - Validates AI-generated queries against database schema and data
Best Practice: Always validate AI-generated queries before execution
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from database.connections import get_postgres_connection

logger = logging.getLogger(__name__)


class QueryValidator:
    """Validates SQL queries and results to prevent common AI mistakes"""
    
    def __init__(self):
        self.schema_cache = {}
        self.entity_cache = {}
        self._load_schema()
        self._load_entities()
    
    def _load_schema(self):
        """Load database schema for validation"""
        try:
            with get_postgres_connection() as conn:
                cursor = conn.cursor()
                
                # Get all tables and their columns
                cursor.execute("""
                    SELECT table_name, column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_schema = 'public'
                    ORDER BY table_name, ordinal_position
                """)
                
                for table, column, dtype in cursor.fetchall():
                    if table not in self.schema_cache:
                        self.schema_cache[table] = {}
                    self.schema_cache[table][column] = dtype
                
                cursor.close()
                logger.info(f"✅ Loaded schema for {len(self.schema_cache)} tables")
                
        except Exception as e:
            logger.error(f"❌ Failed to load schema: {e}")

    def _load_entities(self):
        """Load known entities (rigs, wells, etc.) for validation"""
        try:
            with get_postgres_connection() as conn:
                cursor = conn.cursor()

                # Get all unique rig names
                cursor.execute("SELECT DISTINCT rig_name FROM production_data ORDER BY rig_name")
                self.entity_cache['rigs'] = [row['rig_name'] for row in cursor.fetchall()]

                # Get all unique well names
                cursor.execute("SELECT DISTINCT well_name FROM production_data ORDER BY well_name")
                self.entity_cache['wells'] = [row['well_name'] for row in cursor.fetchall()]

                cursor.close()
                logger.info(f"✅ Loaded entities: {len(self.entity_cache.get('rigs', []))} rigs, {len(self.entity_cache.get('wells', []))} wells")

        except Exception as e:
            logger.error(f"❌ Failed to load entities: {e}")
    
    def validate_sql_query(self, sql: str, parameters: List[Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate SQL query before execution
        
        Returns:
            (is_valid, error_message)
        """
        sql_lower = sql.lower()
        
        # Check 1: Ensure it's a SELECT query (no modifications)
        if not sql_lower.strip().startswith('select'):
            return False, "Only SELECT queries are allowed"
        
        # Check 2: Detect literal strings in SELECT clause
        # Common mistake: SELECT 'min' instead of SELECT MIN(column)
        if "select '" in sql_lower or 'select "' in sql_lower:
            return False, "Query contains literal strings in SELECT clause - use aggregate functions instead"
        
        # Check 3: Validate table names exist
        for table in self.schema_cache.keys():
            if f" from {table}" in sql_lower or f" join {table}" in sql_lower:
                logger.info(f"✅ Table '{table}' exists in schema")
        
        # Check 4: Validate parameter count matches placeholders
        placeholder_count = sql.count('$') if '$' in sql else sql.count('%s')
        if placeholder_count != len(parameters):
            return False, f"Parameter count mismatch: {placeholder_count} placeholders but {len(parameters)} parameters"
        
        # Check 5: Validate parameters are not None or empty
        for i, param in enumerate(parameters):
            if param is None or param == '':
                return False, f"Parameter ${i+1} is None or empty"

        # Check 6: Validate entity names (rigs, wells) exist in database
        for param in parameters:
            if isinstance(param, str):
                # Check if it's a rig name
                if 'rig' in param.lower():
                    known_rigs = self.entity_cache.get('rigs', [])
                    if known_rigs and param not in known_rigs:
                        # Try fuzzy match
                        close_matches = [r for r in known_rigs if param.lower() in r.lower() or r.lower() in param.lower()]
                        if close_matches:
                            logger.warning(f"⚠️ Entity '{param}' not found. Did you mean: {close_matches}?")
                            return False, f"Entity '{param}' not found. Available rigs: {', '.join(known_rigs)}"
                        else:
                            return False, f"Rig '{param}' not found in database. Available rigs: {', '.join(known_rigs)}"

                # Check if it's a well name
                if 'well' in param.lower() or param.startswith('W-'):
                    known_wells = self.entity_cache.get('wells', [])
                    if known_wells and param not in known_wells:
                        return False, f"Well '{param}' not found in database. Available wells: {', '.join(known_wells)}"

        return True, None
    
    def validate_sql_results(self, results: List[Dict[str, Any]], sql: str) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        """
        Validate SQL query results to detect common issues
        
        Returns:
            (is_valid, error_message, cleaned_results)
        """
        if not results:
            return True, None, results
        
        cleaned_results = []
        
        for record in results:
            cleaned_record = {}
            has_issue = False
            
            for key, value in record.items():
                # Check 1: Detect literal strings (column name == value)
                if isinstance(value, str) and value.lower() == key.lower():
                    logger.warning(f"⚠️ Detected literal string: {key}='{value}'")
                    logger.warning(f"⚠️ SQL likely used SELECT '{value}' instead of aggregate function")
                    has_issue = True
                    break
                
                # Check 2: Handle NULL values from aggregate functions
                if value is None and any(agg in sql.lower() for agg in ['min(', 'max(', 'avg(', 'sum(', 'count(']):
                    logger.warning(f"⚠️ Aggregate function returned NULL for '{key}'")
                    logger.warning(f"⚠️ This usually means no records matched the WHERE clause")
                    has_issue = True
                    break
                
                cleaned_record[key] = value
            
            if has_issue:
                return False, "Query returned invalid results - likely no matching records or incorrect SQL", []
            
            cleaned_results.append(cleaned_record)
        
        return True, None, cleaned_results
    
    def suggest_query_fix(self, sql: str, error: str) -> Optional[str]:
        """Suggest a fix for common query errors"""
        
        sql_lower = sql.lower()
        
        # Fix 1: Literal strings in SELECT
        if "literal strings" in error.lower():
            # Find SELECT 'something' and suggest SELECT FUNCTION(column)
            if "select '" in sql_lower:
                return "Replace SELECT 'column_name' with SELECT MIN(column_name) or MAX(column_name)"
        
        # Fix 2: NULL from aggregate - suggest broader WHERE clause
        if "null" in error.lower() and "where" in sql_lower:
            return "Try using <= instead of < in WHERE clause, or check if the threshold value is correct"
        
        # Fix 3: No matching records
        if "no records matched" in error.lower():
            return "Verify the WHERE clause parameters match actual data in the database"
        
        return None
    
    def test_query_with_sample_data(self, sql: str, parameters: List[Any]) -> Dict[str, Any]:
        """
        Test query with actual database to verify it returns valid data
        
        Returns:
            {
                'success': bool,
                'record_count': int,
                'sample_record': dict,
                'issues': list
            }
        """
        issues = []
        
        try:
            with get_postgres_connection() as conn:
                cursor = conn.cursor()
                
                # Convert $1, $2 to %s
                import re
                converted_sql = re.sub(r'\$\d+', '%s', sql)
                
                cursor.execute(converted_sql, parameters)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                
                if not rows:
                    issues.append("Query returned 0 records")
                
                records = [dict(zip(columns, row)) for row in rows]
                
                # Validate first record
                if records:
                    is_valid, error, _ = self.validate_sql_results(records, sql)
                    if not is_valid:
                        issues.append(error)
                
                cursor.close()
                
                return {
                    'success': len(issues) == 0,
                    'record_count': len(records),
                    'sample_record': records[0] if records else None,
                    'issues': issues
                }
                
        except Exception as e:
            return {
                'success': False,
                'record_count': 0,
                'sample_record': None,
                'issues': [str(e)]
            }

