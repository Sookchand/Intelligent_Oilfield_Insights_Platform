"""
Flexible Query Executor
Executes AI-generated queries against databases
"""
import logging
import os
from typing import Dict, Any, List, Optional
from database.connections import get_neo4j_driver, get_postgres_connection
from agents.query_validator import QueryValidator

logger = logging.getLogger(__name__)

class FlexibleExecutor:
    """
    Executes dynamically generated queries against databases
    """

    def __init__(self):
        self.validator = QueryValidator()
        logger.info("✅ Query validator initialized")
    
    def execute_cypher(self, cypher: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query against Neo4j
        
        Args:
            cypher: Cypher query string
            parameters: Query parameters
            
        Returns:
            List of result records
        """
        if not cypher:
            logger.error("No Cypher query provided")
            return []
        
        logger.info(f"Executing Cypher: {cypher[:100]}...")
        
        try:
            driver = get_neo4j_driver()
            with driver.session() as session:
                result = session.run(cypher, parameters or {})
                records = [dict(record) for record in result]
                logger.info(f"✅ Cypher query returned {len(records)} records")
                driver.close()
                return records
        except Exception as e:
            logger.error(f"❌ Error executing Cypher query: {str(e)}")
            logger.error(f"Query was: {cypher}")
            logger.error(f"Parameters: {parameters}")
            return []
    
    def execute_sql(self, sql: str, parameters: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a SQL query against PostgreSQL

        Args:
            sql: SQL query string (can use $1, $2 or %s style parameters)
            parameters: Query parameters (list for positional params)

        Returns:
            List of result records
        """
        if not sql:
            logger.error("No SQL query provided")
            return []

        # STEP 1: Validate query before execution
        is_valid, error = self.validator.validate_sql_query(sql, parameters or [])
        if not is_valid:
            logger.error(f"❌ Query validation failed: {error}")
            suggestion = self.validator.suggest_query_fix(sql, error)
            if suggestion:
                logger.info(f"💡 Suggestion: {suggestion}")
            return []

        # BEST PRACTICE: Convert PostgreSQL-style parameters ($1, $2) to psycopg2-style (%s)
        # This allows AI to generate standard PostgreSQL syntax while ensuring compatibility
        import re
        converted_sql = sql
        if parameters and '$' in sql:
            # Replace $1, $2, $3, etc. with %s in order
            # Use regex to find all $N patterns and replace them
            def replace_param(match):
                return '%s'
            converted_sql = re.sub(r'\$\d+', replace_param, sql)
            logger.info(f"Converted PostgreSQL parameters to psycopg2 format")

        logger.info(f"Executing SQL: {converted_sql[:100]}...")

        try:
            with get_postgres_connection() as conn:
                cursor = conn.cursor()

                # Execute query
                if parameters:
                    cursor.execute(converted_sql, parameters)
                else:
                    cursor.execute(converted_sql)

                # Fetch results
                rows = cursor.fetchall()

                logger.info(f"🔍 DEBUG - Raw rows (type: {type(rows[0]) if rows else 'empty'}): {rows}")

                # RealDictCursor already returns dict-like objects, just convert to regular dicts
                records = [dict(row) for row in rows] if rows else []

                logger.info(f"🔍 DEBUG - Converted records: {records}")

                cursor.close()

                # STEP 2: Validate results
                is_valid, error, cleaned_records = self.validator.validate_sql_results(records, sql)
                if not is_valid:
                    logger.error(f"❌ Result validation failed: {error}")
                    suggestion = self.validator.suggest_query_fix(sql, error)
                    if suggestion:
                        logger.info(f"💡 Suggestion: {suggestion}")
                    return []

                logger.info(f"✅ SQL query returned {len(cleaned_records)} valid records")
                return cleaned_records

        except Exception as e:
            logger.error(f"❌ Error executing SQL query: {str(e)}")
            logger.error(f"Original query: {sql}")
            logger.error(f"Converted query: {converted_sql}")
            logger.error(f"Parameters: {parameters}")
            return []
    
    def format_results(self, results: List[Dict[str, Any]], question: str) -> str:
        """
        Format query results into a human-readable answer using AI

        Args:
            results: Query results
            question: Original question

        Returns:
            Formatted answer string
        """
        if not results:
            return "No results found for your query."

        # Log what we're formatting
        logger.info(f"🔍 Formatting results for question: '{question}'")
        logger.info(f"🔍 Results to format: {results}")

        # Use AI to format the results into a natural language answer
        try:
            logger.info("🤖 Calling OpenAI to format results...")
            from openai import OpenAI
            import json
            import os

            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            # Prepare results for AI
            results_json = json.dumps(results[:20], default=str)  # Limit to first 20 results

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that formats database query results into clear, concise natural language answers. Be specific and include key data points."},
                    {"role": "user", "content": f"Question: {question}\n\nQuery Results:\n{results_json}\n\nProvide a clear, concise answer to the question based on these results."}
                ],
                temperature=0,
                max_tokens=500
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.warning(f"⚠️ AI formatting failed, using fallback: {str(e)}")
            # Fallback to simple formatting
            return self._fallback_format(results, question)

    def _fallback_format(self, results: List[Dict[str, Any]], question: str) -> str:
        """Fallback formatting when AI is not available - with intelligent interpretation"""
        if len(results) == 1 and len(results[0]) == 1:
            # Single value result - interpret based on key and question
            key = list(results[0].keys())[0]
            value = list(results[0].values())[0]

            # Intelligent interpretation based on aggregate functions
            question_lower = question.lower()

            if key == 'min' and ('when' in question_lower or 'start' in question_lower or 'first' in question_lower):
                # Timestamp question
                from datetime import datetime
                try:
                    if isinstance(value, str):
                        dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                        return f"It started on {dt.strftime('%B %d, %Y at %I:%M %p')}"
                    else:
                        return f"It started at: {value}"
                except:
                    return f"The earliest timestamp is: {value}"

            elif key == 'max' and ('when' in question_lower or 'last' in question_lower or 'latest' in question_lower):
                # Latest timestamp
                from datetime import datetime
                try:
                    if isinstance(value, str):
                        dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                        return f"The latest occurrence was on {dt.strftime('%B %d, %Y at %I:%M %p')}"
                    else:
                        return f"The latest timestamp is: {value}"
                except:
                    return f"The latest timestamp is: {value}"

            elif key == 'avg' or key == 'average':
                return f"The average is {value:,.2f}" if isinstance(value, (int, float)) else f"The average is {value}"

            elif key == 'count':
                return f"There are {value} results"

            elif key == 'sum' or key == 'total':
                return f"The total is {value:,.2f}" if isinstance(value, (int, float)) else f"The total is {value}"

            else:
                # Generic single value
                return f"{key.replace('_', ' ').title()}: {value}"

        elif len(results) <= 10:
            # Small result set - show all details
            answer_parts = [f"Found {len(results)} result(s):\n"]

            for i, record in enumerate(results, 1):
                parts = []
                for key, value in record.items():
                    if value is not None:
                        parts.append(f"{key}: {value}")
                answer_parts.append(f"{i}. {', '.join(parts)}")

            return "\n".join(answer_parts)

        else:
            # Large result set - summarize
            answer_parts = [f"Found {len(results)} results. Showing first 10:\n"]

            for i, record in enumerate(results[:10], 1):
                # Show only first 3 fields
                parts = []
                for key, value in list(record.items())[:3]:
                    if value is not None:
                        parts.append(f"{key}: {value}")
                answer_parts.append(f"{i}. {', '.join(parts)}")

            answer_parts.append(f"\n... and {len(results) - 10} more results")
            return "\n".join(answer_parts)

