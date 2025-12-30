"""
FastAPI Entry Point for Intelligent Oilfield Insights Platform
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Intelligent Oilfield Insights Platform",
    description="Enterprise-Grade Agentic RAG system for Oil & Gas data unification",
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
        "service": "Intelligent Oilfield Insights Platform",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Intelligent Oilfield Insights Platform",
        "docs": "/docs",
        "health": "/health"
    }

# Main query endpoint
@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process natural language query and return insights
    """
    try:
        logger.info(f"Processing query: {request.query}")

        # Import graph engine
        from graph_engine import process_query as engine_process_query

        # Process query through agent orchestration
        result = engine_process_query(request.query)

        # Convert to response model
        response = QueryResponse(
            answer=result["answer"],
            reasoning_trace=[
                ReasoningStep(**step) for step in result["reasoning_trace"]
            ],
            graph_path=result.get("graph_path"),
            confidence=result["confidence"],
            data=result.get("data")
        )

        return response

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

