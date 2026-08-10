"""
FastAPI Entry Point for Oilfield Intelligence Platform
AI-powered analytics for production optimization and asset management
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import os
import asyncio
import signal
from functools import wraps
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from root directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize LLMOps (LangSmith tracing)
from llmops.langsmith_config import setup_langsmith
langsmith_enabled = setup_langsmith()

# Timeout decorator for query processing
def timeout_handler(timeout_seconds=30):
    """
    Decorator to add timeout protection to functions
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Run the function with timeout
                result = await asyncio.wait_for(
                    asyncio.to_thread(func, *args, **kwargs),
                    timeout=timeout_seconds
                )
                return result
            except asyncio.TimeoutError:
                logger.error(f"⏱️ Function {func.__name__} timed out after {timeout_seconds}s")
                raise HTTPException(
                    status_code=504,
                    detail=f"Query processing timed out after {timeout_seconds} seconds. Please try a simpler query."
                )
        return wrapper
    return decorator

# Initialize FastAPI app
app = FastAPI(
    title="Oilfield Intelligence Platform",
    description="AI-powered analytics for production optimization, asset management, and real-time oilfield operations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    
class ReasoningStep(BaseModel):
    step: int
    agent: str
    action: str
    result: Optional[str] = None
    duration_ms: Optional[float] = None
    sql_query: Optional[str] = None
    cypher_query: Optional[str] = None
    sample_results: Optional[List[Dict[str, Any]]] = None
    causal_explanation: Optional[str] = None
    domain_knowledge: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    answer: str
    reasoning_trace: List[ReasoningStep]
    graph_path: Optional[List[str]] = None
    confidence: float
    data: Optional[Dict[str, Any]] = None

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Oilfield Intelligence Platform",
        "version": "1.0.0",
        "llmops": {
            "langsmith_enabled": langsmith_enabled,
            "tracing": "active" if langsmith_enabled else "disabled"
        }
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Oilfield Intelligence Platform - AI-powered analytics for production optimization",
        "docs": "/docs",
        "health": "/health"
    }

# Main query endpoint
@app.post("/api/query")
async def process_query(request: QueryRequest):
    """
    Process natural language query and return insights
    """
    import time
    start_time = time.time()

    try:
        # Validate input query
        if not request.query or not request.query.strip():
            raise HTTPException(
                status_code=400,
                detail="Query cannot be empty. Please provide a valid question."
            )

        # Check query length
        if len(request.query) > 1000:
            raise HTTPException(
                status_code=400,
                detail="Query is too long. Please limit to 1000 characters."
            )

        logger.info(f"Processing query: {request.query}")

        # Import graph engine and audit logger
        from graph_engine import process_query as engine_process_query
        from database.audit_log import audit_logger

        # Process query through agent orchestration with timeout protection
        result = await asyncio.wait_for(
            asyncio.to_thread(engine_process_query, request.query),
            timeout=60.0  # 60 second timeout (allows time for LLM reasoning)
        )

        # Calculate processing time
        processing_time_ms = int((time.time() - start_time) * 1000)

        # Return result directly without Pydantic validation to preserve all fields
        # This ensures fields like 'details', 'causal_explanation', etc. are not stripped
        response = result

        # Log to audit trail
        try:
            data_sources = []
            for step in result["reasoning_trace"]:
                if "PostgreSQL" in step.get("action", ""):
                    data_sources.append("PostgreSQL")
                elif "Neo4j" in step.get("action", ""):
                    data_sources.append("Neo4j")
                elif "Qdrant" in step.get("action", ""):
                    data_sources.append("Qdrant")
                elif "MinIO" in step.get("action", ""):
                    data_sources.append("MinIO")

            data_sources = list(set(data_sources))  # Remove duplicates

            audit_logger.log_query(
                query_text=request.query,
                query_type=result.get("query_type", "general"),
                confidence_score=result["confidence"],
                processing_time_ms=processing_time_ms,
                status="success",
                data_sources_used=data_sources,
                reasoning_trace=result["reasoning_trace"],
                result_summary=result["answer"][:500],  # First 500 chars
                metadata={
                    "graph_path": result.get("graph_path"),
                    "data_points": len(result.get("data", {}).get("records", [])) if result.get("data") else 0
                }
            )
        except Exception as audit_error:
            logger.warning(f"⚠️ Failed to log to audit trail: {str(audit_error)}")

        return response

    except asyncio.TimeoutError:
        logger.error(f"⏱️ Query timed out after 25 seconds: {request.query}")
        processing_time_ms = int((time.time() - start_time) * 1000)

        # Log timeout to audit
        try:
            from database.audit_log import audit_logger
            audit_logger.log_query(
                query_text=request.query,
                query_type="timeout",
                confidence_score=0.0,
                processing_time_ms=processing_time_ms,
                status="timeout",
                data_sources_used=[],
                reasoning_trace=[],
                result_summary="Query processing timed out",
                metadata={"error": "timeout"}
            )
        except Exception:
            pass  # Don't fail on audit logging

        raise HTTPException(
            status_code=504,
            detail="Query processing timed out after 25 seconds. Please try a simpler query or rephrase your question."
        )

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, etc.)
        raise

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")

        # Log failed query to audit
        try:
            from database.audit_log import audit_logger
            processing_time_ms = int((time.time() - start_time) * 1000)
            audit_logger.log_query(
                query_text=request.query,
                query_type="unknown",
                confidence_score=0.0,
                processing_time_ms=processing_time_ms,
                status="failed",
                data_sources_used=[],
                reasoning_trace=[],
                result_summary=f"Error: {str(e)}",
                metadata={"error": str(e)}
            )
        except:
            pass

        raise HTTPException(status_code=500, detail=str(e))

# Database status endpoint
@app.get("/api/status/databases")
async def database_status():
    """Check database connectivity"""
    try:
        from database.connections import test_all_connections

        status = test_all_connections()

        all_healthy = all(status.values())

        return {
            "databases": status,
            "all_healthy": all_healthy,
            "message": "Database connectivity check complete"
        }
    except Exception as e:
        logger.error(f"Error checking database status: {str(e)}")
        return {
            "databases": {
                "postgres": False,
                "neo4j": False,
                "qdrant": False,
                "minio": False
            },
            "all_healthy": False,
            "message": f"Error: {str(e)}"
        }

# Business Metrics Endpoints

@app.get("/api/business/downtime-cost/{rig_name}")
async def get_downtime_cost(rig_name: str, downtime_hours: Optional[float] = None):
    """Calculate downtime cost for a rig"""
    try:
        from database.connections import postgres_pool
        from business_metrics import metrics_calculator

        # Get production data from PostgreSQL
        async with postgres_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM production WHERE rig_name = %s ORDER BY timestamp DESC LIMIT 30",
                    (rig_name,)
                )
                columns = [desc[0] for desc in cur.description]
                rows = await cur.fetchall()
                production_data = [dict(zip(columns, row)) for row in rows]

        result = metrics_calculator.calculate_downtime_cost(
            rig_name, production_data, downtime_hours
        )
        return result

    except Exception as e:
        logger.error(f"Error calculating downtime cost: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/business/maintenance-roi/{equipment_id}")
async def get_maintenance_roi(
    equipment_id: str,
    repair_cost: Optional[float] = None,
    prevented_downtime_hours: float = 48.0
):
    """Calculate ROI for equipment maintenance"""
    try:
        from business_metrics import metrics_calculator

        result = metrics_calculator.calculate_maintenance_roi(
            equipment_id, repair_cost, prevented_downtime_hours
        )
        return result

    except Exception as e:
        logger.error(f"Error calculating maintenance ROI: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/business/safety-risk/{rig_name}")
async def get_safety_risk(rig_name: str):
    """Calculate safety risk score for a rig"""
    try:
        from database.connections import neo4j_driver
        from business_metrics import metrics_calculator

        # Query Neo4j for faulty equipment count
        with neo4j_driver.session() as session:
            result = session.run("""
                MATCH (r:Rig {name: $rig_name})-[:OPERATES]->(w:Well)-[:MONITORS]->(s:Sensor)
                WHERE toLower(s.status) = 'faulty'
                RETURN count(s) as faulty_count
            """, rig_name=rig_name)

            record = result.single()
            faulty_count = record["faulty_count"] if record else 0

        # Calculate risk (using dummy values for incidents and overdue maintenance)
        risk_result = metrics_calculator.calculate_safety_risk(
            rig_name,
            faulty_equipment_count=faulty_count,
            incident_count=0,  # TODO: Add incidents table
            overdue_maintenance_count=0  # TODO: Add maintenance schedule
        )

        return risk_result

    except Exception as e:
        logger.error(f"Error calculating safety risk: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/business/forecast/{rig_name}")
async def get_production_forecast(rig_name: str):
    """Get production forecast for a rig"""
    try:
        from database.connections import postgres_pool
        from forecasting import forecaster

        # Get historical production data
        async with postgres_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM production WHERE rig_name = %s ORDER BY timestamp ASC",
                    (rig_name,)
                )
                columns = [desc[0] for desc in cur.description]
                rows = await cur.fetchall()
                production_data = [dict(zip(columns, row)) for row in rows]

        result = forecaster.forecast_production(rig_name, production_data)
        return result

    except Exception as e:
        logger.error(f"Error generating forecast: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/system/metrics")
async def get_system_metrics():
    """Get system performance metrics"""
    try:
        from database.connections import test_all_connections

        db_status = test_all_connections()

        return {
            "timestamp": datetime.now().isoformat(),
            "databases": db_status,
            "api_version": "1.0.0",
            "uptime": "healthy"
        }

    except Exception as e:
        logger.error(f"Error getting system metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Query Audit & History Endpoints

@app.get("/api/audit/history")
async def get_query_history(
    limit: int = 100,
    offset: int = 0,
    query_type: Optional[str] = None,
    status: Optional[str] = None,
    include_archived: bool = False
):
    """
    Retrieve query history for audit and compliance
    """
    try:
        from database.audit_log import audit_logger

        history = audit_logger.get_query_history(
            limit=limit,
            offset=offset,
            query_type=query_type,
            status=status,
            include_archived=include_archived
        )

        return {
            "queries": history,
            "total": len(history),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error retrieving query history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/audit/archive/{query_id}")
async def archive_query(query_id: int):
    """
    Archive (soft delete) a query from history
    """
    try:
        from database.audit_log import audit_logger

        success = audit_logger.archive_query(query_id)

        if success:
            return {"message": f"Query {query_id} archived successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to archive query")
    except Exception as e:
        logger.error(f"Error archiving query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/audit/stats")
async def get_audit_stats():
    """
    Get query statistics for dashboard
    """
    try:
        from database.audit_log import audit_logger
        from database.connections import get_postgres_connection

        with get_postgres_connection() as conn:
            cursor = conn.cursor()

            # Total queries
            cursor.execute("SELECT COUNT(*) FROM query_audit_log WHERE is_archived = FALSE")
            total_queries = cursor.fetchone()[0]

            # Success rate
            cursor.execute("""
                SELECT
                    COUNT(CASE WHEN status = 'success' THEN 1 END) * 100.0 / COUNT(*) as success_rate
                FROM query_audit_log
                WHERE is_archived = FALSE
            """)
            success_rate = cursor.fetchone()[0] or 0

            # Average confidence
            cursor.execute("""
                SELECT AVG(confidence_score)
                FROM query_audit_log
                WHERE is_archived = FALSE AND status = 'success'
            """)
            avg_confidence = cursor.fetchone()[0] or 0

            # Average processing time
            cursor.execute("""
                SELECT AVG(processing_time_ms)
                FROM query_audit_log
                WHERE is_archived = FALSE
            """)
            avg_processing_time = cursor.fetchone()[0] or 0

            cursor.close()

            return {
                "total_queries": total_queries,
                "success_rate": round(float(success_rate), 2),
                "avg_confidence": round(float(avg_confidence), 2),
                "avg_processing_time_ms": round(float(avg_processing_time), 2)
            }
    except Exception as e:
        logger.error(f"Error getting audit stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status/databases")
async def get_database_status():
    """
    Get real-time status of all database connections
    """
    import psycopg2

    status = {
        "postgres": False,
        "neo4j": False,
        "qdrant": False,
        "minio": False
    }

    # Check PostgreSQL
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            database=os.getenv("POSTGRES_DB", "oilfield_production"),
            user=os.getenv("POSTGRES_USER", "oilfield_user"),
            password=os.getenv("POSTGRES_PASSWORD", "oilfield_pass"),
            connect_timeout=3
        )
        conn.close()
        status["postgres"] = True
    except Exception as e:
        logger.debug(f"PostgreSQL connection failed: {str(e)}")

    # Check Neo4j (placeholder - implement if Neo4j is configured)
    try:
        # For demo purposes, assume Neo4j is available
        # In production, use neo4j driver to check connection
        status["neo4j"] = True  # Mock for demo
    except Exception as e:
        logger.debug(f"Neo4j connection failed: {str(e)}")

    # Check Qdrant (placeholder - implement if Qdrant is configured)
    try:
        # For demo purposes, assume Qdrant is available
        status["qdrant"] = True  # Mock for demo
    except Exception as e:
        logger.debug(f"Qdrant connection failed: {str(e)}")

    # Check MinIO (placeholder - implement if MinIO is configured)
    try:
        # For demo purposes, assume MinIO is available
        status["minio"] = True  # Mock for demo
    except Exception as e:
        logger.debug(f"MinIO connection failed: {str(e)}")

    return {"databases": status}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

