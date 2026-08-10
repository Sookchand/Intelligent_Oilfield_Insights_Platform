"""
Query Audit Log Module
Handles logging of all queries for compliance and auditability
"""
import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from decimal import Decimal
import psycopg2
from psycopg2.extras import RealDictCursor
from database.connections import get_postgres_connection

logger = logging.getLogger(__name__)

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime and Decimal objects"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

class QueryAuditLogger:
    """
    Manages query audit logging for compliance and governance
    """
    
    def __init__(self):
        self.initialized = False
        try:
            self._ensure_table_exists()
            self.initialized = True
            logger.info("✅ Query audit logger initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize audit logger: {str(e)}")
    
    def _ensure_table_exists(self):
        """Ensure audit log table exists"""
        with get_postgres_connection() as conn:
            try:
                cursor = conn.cursor()

                # Read and execute migration SQL
                with open('database/migrations/001_create_audit_log.sql', 'r') as f:
                    cursor.execute(f.read())

                conn.commit()
                logger.info("✅ Audit log table verified/created")
            except Exception as e:
                logger.error(f"❌ Error creating audit table: {str(e)}")
                conn.rollback()
                raise
            finally:
                cursor.close()
    
    def log_query(
        self,
        query_text: str,
        query_type: str,
        confidence_score: float,
        processing_time_ms: int,
        status: str,
        data_sources_used: List[str],
        reasoning_trace: List[Dict[str, Any]],
        result_summary: str,
        user_id: Optional[str] = None,
        user_name: Optional[str] = None,
        session_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[int]:
        """
        Log a query to the audit trail
        
        Returns:
            The ID of the created audit log entry, or None if failed
        """
        if not self.initialized:
            logger.warning("⚠️ Audit logger not initialized, skipping log")
            return None

        with get_postgres_connection() as conn:
            try:
                cursor = conn.cursor()

                query = """
                    INSERT INTO query_audit_log (
                        query_text, query_type, user_id, user_name,
                        confidence_score, processing_time_ms, status,
                        data_sources_used, reasoning_trace, result_summary,
                        session_id, ip_address, metadata
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    RETURNING id
                """

                cursor.execute(query, (
                    query_text,
                    query_type,
                    user_id,
                    user_name,
                    confidence_score,
                    processing_time_ms,
                    status,
                    json.dumps(data_sources_used, cls=DateTimeEncoder),
                    json.dumps(reasoning_trace, cls=DateTimeEncoder),
                    result_summary,
                    session_id,
                    ip_address,
                    json.dumps(metadata, cls=DateTimeEncoder) if metadata else None
                ))

                result = cursor.fetchone()
                if result is None:
                    logger.error("❌ INSERT did not return an ID")
                    conn.rollback()
                    return None

                # Handle both dict-like and tuple-like results
                if isinstance(result, dict):
                    audit_id = result.get('id') or result.get(0)
                else:
                    audit_id = result[0] if len(result) > 0 else None

                if audit_id is None:
                    logger.error("❌ Could not extract audit ID from result")
                    conn.rollback()
                    return None

                conn.commit()

                logger.info(f"✅ Query logged to audit trail (ID: {audit_id})")
                return audit_id

            except Exception as e:
                logger.error(f"❌ Error logging query to audit: {type(e).__name__}: {str(e)}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                conn.rollback()
                return None
            finally:
                cursor.close()
    
    def get_query_history(
        self,
        limit: int = 100,
        offset: int = 0,
        user_id: Optional[str] = None,
        query_type: Optional[str] = None,
        status: Optional[str] = None,
        include_archived: bool = False,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve query history with filters
        """
        with get_postgres_connection() as conn:
            try:
                cursor = conn.cursor(cursor_factory=RealDictCursor)

                # Build query with filters
                conditions = []
                params = []

                if not include_archived:
                    conditions.append("is_archived = FALSE")

                if user_id:
                    conditions.append("user_id = %s")
                    params.append(user_id)

                if query_type:
                    conditions.append("query_type = %s")
                    params.append(query_type)

                if status:
                    conditions.append("status = %s")
                    params.append(status)

                if start_date:
                    conditions.append("timestamp >= %s")
                    params.append(start_date)

                if end_date:
                    conditions.append("timestamp <= %s")
                    params.append(end_date)

                where_clause = " AND ".join(conditions) if conditions else "TRUE"

                query = f"""
                    SELECT * FROM query_audit_log
                    WHERE {where_clause}
                    ORDER BY timestamp DESC
                    LIMIT %s OFFSET %s
                """

                params.extend([limit, offset])
                cursor.execute(query, params)

                results = [dict(row) for row in cursor.fetchall()]
                return results

            except Exception as e:
                logger.error(f"❌ Error retrieving query history: {str(e)}")
                return []
            finally:
                cursor.close()
    
    def archive_query(self, query_id: int, archived_by: Optional[str] = None) -> bool:
        """Archive (soft delete) a query"""
        with get_postgres_connection() as conn:
            try:
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE query_audit_log
                    SET is_archived = TRUE,
                        archived_at = NOW(),
                        archived_by = %s
                    WHERE id = %s
                """, (archived_by, query_id))

                conn.commit()
                logger.info(f"✅ Query {query_id} archived")
                return True

            except Exception as e:
                logger.error(f"❌ Error archiving query: {str(e)}")
                conn.rollback()
                return False
            finally:
                cursor.close()

# Global instance
audit_logger = QueryAuditLogger()

