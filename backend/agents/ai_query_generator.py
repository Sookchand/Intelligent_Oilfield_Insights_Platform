"""
AI-Powered Query Generator using OpenAI
Dynamically generates Cypher and SQL queries from natural language
"""
import logging
import os
from typing import Dict, Any, Optional, List
import json
import time

logger = logging.getLogger(__name__)

class AIQueryGenerator:
    """
    Uses OpenAI to generate database queries from natural language
    """

    def __init__(self):
        self.openai_available = False
        self.client = None
        self.max_retries = 2  # Limit retries to prevent hanging
        self.timeout = 10  # 10 second timeout per request

        try:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")

            if api_key and api_key.startswith("sk-"):
                # Configure client with timeout and retry limits
                self.client = OpenAI(
                    api_key=api_key,
                    timeout=self.timeout,
                    max_retries=self.max_retries
                )
                self.openai_available = True
                logger.info("✅ OpenAI client initialized successfully")
            else:
                logger.warning("⚠️ OpenAI API key not found or invalid")
        except Exception as e:
            logger.warning(f"⚠️ OpenAI not available: {str(e)}")
    
    def generate_cypher_query(self, question: str, schema_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a Cypher query from natural language
        
        Args:
            question: Natural language question
            schema_context: Optional schema information
            
        Returns:
            Dictionary with cypher query, explanation, and parameters
        """
        if not self.openai_available:
            return {"error": "OpenAI not available", "cypher": None}
        
        # Default schema if not provided
        if not schema_context:
            schema_context = self._get_default_neo4j_schema()
        
        system_prompt = f"""You are an expert in Neo4j Cypher query language for an oilfield asset management system.

Database Schema:
{schema_context}

Your task is to convert natural language questions into valid Cypher queries.

Rules:
1. Return ONLY valid Cypher syntax
2. Use parameterized queries when possible
3. Include appropriate RETURN clauses
4. Use OPTIONAL MATCH for relationships that might not exist
5. Order results when appropriate
6. Limit results to reasonable numbers (e.g., LIMIT 100)

Return your response as JSON with this structure:
{{
    "cypher": "MATCH (n:Node) RETURN n",
    "explanation": "Brief explanation of what the query does",
    "parameters": {{"param_name": "value"}},
    "return_fields": ["field1", "field2"]
}}
"""
        
        try:
            start_time = time.time()
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate a Cypher query for: {question}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            elapsed = time.time() - start_time

            result = json.loads(response.choices[0].message.content)
            logger.info(f"✅ Generated Cypher query in {elapsed:.2f}s: {result.get('cypher', '')[:100]}...")
            return result

        except Exception as e:
            error_msg = str(e)
            # Check for rate limit or timeout errors
            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                logger.warning(f"⚠️ OpenAI rate limit hit, falling back to rule-based query")
            elif "timeout" in error_msg.lower():
                logger.warning(f"⚠️ OpenAI request timed out, falling back to rule-based query")
            else:
                logger.error(f"❌ Error generating Cypher query: {error_msg[:100]}")
            return {"error": error_msg, "cypher": None}
    
    def generate_sql_query(self, question: str, schema_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a SQL query from natural language
        
        Args:
            question: Natural language question
            schema_context: Optional schema information
            
        Returns:
            Dictionary with SQL query, explanation, and parameters
        """
        if not self.openai_available:
            return {"error": "OpenAI not available", "sql": None}
        
        # Default schema if not provided
        if not schema_context:
            schema_context = self._get_default_postgres_schema()
        
        system_prompt = f"""You are an expert in PostgreSQL for an oilfield production database.

Database Schema:
{schema_context}

Your task is to convert natural language questions into valid SQL queries.

Rules:
1. Return ONLY valid PostgreSQL syntax
2. Use parameterized queries with $1, $2, etc. for values
3. Extract actual values from the question/context for parameters
4. If the question mentions specific entities (rigs, wells, etc.), extract their names
5. If the question has context about production rates or other values, use those values
6. Include appropriate WHERE clauses
7. Use JOINs when needed
8. Order results when appropriate
9. Limit results to reasonable numbers (e.g., LIMIT 100)

CRITICAL - Aggregate Functions (COMMON MISTAKE - READ CAREFULLY):
- For "when did it start" questions, use: SELECT MIN(timestamp) AS min_time FROM production_data WHERE ...
- For "when was the latest" questions, use: SELECT MAX(timestamp) AS max_time FROM production_data WHERE ...
- For "what is the average" questions, use: SELECT AVG(production_rate) AS avg_rate FROM production_data WHERE ...
- For "how many" questions, use: SELECT COUNT(*) AS count FROM production_data WHERE ...
- NEVER EVER use SELECT 'min' or SELECT 'max' - these return literal strings "min" and "max", NOT actual data!
- ALWAYS use the actual aggregate function with parentheses: MIN(column), MAX(column), AVG(column), COUNT(*)

CRITICAL - "When did it start?" Questions:
- If context mentions "average production is X" and "recent production is Y" (where Y < X), find when production dropped BELOW the average
- Use the AVERAGE value as the threshold, NOT the recent/current value
- Example: If average is 943.2 and recent is 850.5, use: WHERE production_rate < 943.2 (NOT < 850.5)
- This finds when the decline STARTED, not when it reached the current low point

Examples to avoid mistakes:
✅ CORRECT: SELECT MIN(timestamp) AS min_time FROM production_data WHERE rig_name = $1
❌ WRONG: SELECT 'min' AS min_time FROM production_data WHERE rig_name = $1
✅ CORRECT: SELECT MAX(production_rate) AS max_rate FROM production_data WHERE rig_name = $1
❌ WRONG: SELECT 'max' AS max_rate FROM production_data WHERE rig_name = $1
✅ CORRECT (when did drop start): SELECT MIN(timestamp) WHERE production_rate < $1 (where $1 = average, e.g. 943.2)
❌ WRONG (when did drop start): SELECT MIN(timestamp) WHERE production_rate < $1 (where $1 = current low, e.g. 850.5)

IMPORTANT: The "parameters" array must contain the ACTUAL VALUES to substitute for $1, $2, etc.
- If the question mentions "Rig Alpha", parameters should include "Rig Alpha"
- If the question mentions a production rate like "850.5", parameters should include 850.5
- DO NOT put placeholder strings like "$1" or "your_rig_name" in the parameters array

Return your response as JSON with this structure:
{{
    "sql": "SELECT MIN(timestamp) AS min_time FROM production_data WHERE rig_name = $1",
    "explanation": "Finds the earliest timestamp for the specified rig",
    "parameters": ["Rig Alpha"],
    "return_fields": ["min_time"]
}}
"""
        
        try:
            start_time = time.time()
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate a SQL query for: {question}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            elapsed = time.time() - start_time

            result = json.loads(response.choices[0].message.content)

            # BEST PRACTICE: Validate and log the generated query
            sql_query = result.get('sql', '')
            parameters = result.get('parameters', [])

            # Validate that parameters is a list
            if not isinstance(parameters, list):
                logger.warning(f"Parameters is not a list: {parameters}, converting to list")
                if isinstance(parameters, dict):
                    parameters = list(parameters.values())
                else:
                    parameters = [parameters] if parameters else []
                result['parameters'] = parameters

            # Log for debugging
            logger.info(f"✅ Generated SQL query in {elapsed:.2f}s: {sql_query[:100]}...")
            logger.info(f"✅ Parameters ({len(parameters)}): {parameters}")

            return result

        except Exception as e:
            error_msg = str(e)
            # Check for rate limit or timeout errors
            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                logger.warning(f"⚠️ OpenAI rate limit hit, falling back to rule-based query")
            elif "timeout" in error_msg.lower():
                logger.warning(f"⚠️ OpenAI request timed out, falling back to rule-based query")
            else:
                logger.error(f"❌ Error generating SQL query: {error_msg[:100]}")
            return {"error": error_msg, "sql": None}

    def _get_default_neo4j_schema(self) -> str:
        """Get default Neo4j schema description"""
        return """
Node Types:
- Rig: Properties: name (string), basin (string), operator (string)
- Well: Properties: name (string), basin (string), depth_ft (integer), status (string)
- Sensor: Properties: sensor_id (string), sensor_type (string), status (string), last_reading (float), last_reading_anomaly (boolean)

Relationships:
- (Rig)-[:HAS_WELL]->(Well)
- (Well)-[:HAS_SENSOR]->(Sensor)
- (Sensor)-[:MONITORS]->(Well)

Common sensor types: "Pressure Gauge", "Temperature", "Flow Meter", "Vibration Sensor"
Common statuses: "Operational", "Faulty", "Maintenance", "Active"

Examples:
- Find all sensors at a well: MATCH (w:Well {name: $well_name})-[:HAS_SENSOR]->(s:Sensor) RETURN s
- Find gauges at a well: MATCH (w:Well {name: $well_name})-[:HAS_SENSOR]->(s:Sensor) WHERE s.sensor_type CONTAINS 'Gauge' RETURN s.sensor_id, s.sensor_type
- List all wells: MATCH (w:Well) RETURN w.name, w.basin, w.depth_ft ORDER BY w.name
"""

    def _get_default_postgres_schema(self) -> str:
        """Get default PostgreSQL schema description"""
        return """
Tables:
1. production_data
   - id (serial primary key)
   - rig_name (varchar)
   - well_name (varchar)
   - basin (varchar)
   - timestamp (timestamp)
   - production_rate (decimal) - oil production in bbl/day
   - pressure (decimal) - pressure in psi
   - temperature (decimal) - temperature in Fahrenheit

2. maintenance_schedule
   - id (serial primary key)
   - equipment_id (varchar)
   - equipment_type (varchar)
   - last_maintenance_date (date)
   - next_maintenance_due (date)
   - status (varchar)

3. incidents
   - id (serial primary key)
   - incident_id (varchar)
   - severity (varchar)
   - description (text)
   - timestamp (timestamp)
   - location (varchar)

Examples:
- Get production for a rig: SELECT * FROM production_data WHERE rig_name = $1 ORDER BY timestamp DESC LIMIT 30
- Average production: SELECT AVG(production_rate) FROM production_data WHERE rig_name = $1
- Find when production dropped: SELECT MIN(timestamp) FROM production_data WHERE production_rate < $1 AND rig_name = $2
"""

    def determine_query_type(self, question: str) -> str:
        """
        Determine whether to use Cypher (graph) or SQL (time-series)

        Args:
            question: Natural language question

        Returns:
            "cypher", "sql", or "both"
        """
        if not self.openai_available:
            # Fallback to simple keyword matching
            question_lower = question.lower()

            # Graph-oriented keywords
            if any(kw in question_lower for kw in ["sensor", "gauge", "equipment", "relationship", "connected", "linked"]):
                return "cypher"

            # Time-series keywords
            if any(kw in question_lower for kw in ["production", "rate", "trend", "average", "forecast"]):
                return "sql"

            return "both"

        try:
            start_time = time.time()
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a database query router. Determine which database to query:
- "cypher" for Neo4j graph queries (assets, relationships, equipment, sensors, wells, rigs)
- "sql" for PostgreSQL time-series queries (production data, rates, trends, forecasts)
- "both" if both databases are needed

Respond with ONLY one word: cypher, sql, or both"""
                    },
                    {"role": "user", "content": question}
                ],
                temperature=0
            )
            elapsed = time.time() - start_time

            result = response.choices[0].message.content.strip().lower()
            logger.info(f"Query type determined in {elapsed:.2f}s: {result}")
            return result if result in ["cypher", "sql", "both"] else "both"

        except Exception as e:
            error_msg = str(e)
            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                logger.warning(f"⚠️ OpenAI rate limit hit, using fallback routing")
            elif "timeout" in error_msg.lower():
                logger.warning(f"⚠️ OpenAI request timed out, using fallback routing")
            else:
                logger.error(f"❌ Error determining query type: {error_msg[:100]}")
            return "both"  # Safe fallback

