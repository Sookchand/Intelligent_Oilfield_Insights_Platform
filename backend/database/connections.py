"""
Database connection managers for PostgreSQL, Neo4j, Qdrant, and MinIO
"""
import os
import logging
from typing import Optional
from contextlib import contextmanager

# Database imports
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None

try:
    from neo4j import GraphDatabase
except ImportError:
    GraphDatabase = None

try:
    from qdrant_client import QdrantClient
except ImportError:
    QdrantClient = None

try:
    from minio import Minio
except ImportError:
    Minio = None

logger = logging.getLogger(__name__)

# PostgreSQL Connection
@contextmanager
def get_postgres_connection():
    """
    Get PostgreSQL database connection
    """
    if psycopg2 is None:
        raise ImportError("psycopg2 not installed. Run: pip install psycopg2-binary")
    
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            database=os.getenv("POSTGRES_DB", "oilfield_production"),
            user=os.getenv("POSTGRES_USER", "oilfield_user"),
            password=os.getenv("POSTGRES_PASSWORD", "oilfield_pass"),
            cursor_factory=RealDictCursor
        )
        logger.info("PostgreSQL connection established")
        yield conn
    except Exception as e:
        logger.error(f"PostgreSQL connection error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info("PostgreSQL connection closed")

# Neo4j Connection
def get_neo4j_driver():
    """
    Get Neo4j graph database driver
    """
    if GraphDatabase is None:
        raise ImportError("neo4j not installed. Run: pip install neo4j")
    
    try:
        driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(
                os.getenv("NEO4J_USER", "neo4j"),
                os.getenv("NEO4J_PASSWORD", "oilfield_neo4j_pass")
            )
        )
        logger.info("Neo4j driver created")
        return driver
    except Exception as e:
        logger.error(f"Neo4j connection error: {str(e)}")
        raise

# Qdrant Connection
def get_qdrant_client():
    """
    Get Qdrant vector database client
    """
    if QdrantClient is None:
        raise ImportError("qdrant-client not installed. Run: pip install qdrant-client")
    
    try:
        client = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", "6333"))
        )
        logger.info("Qdrant client created")
        return client
    except Exception as e:
        logger.error(f"Qdrant connection error: {str(e)}")
        raise

# MinIO Connection
def get_minio_client():
    """
    Get MinIO object storage client
    """
    if Minio is None:
        raise ImportError("minio not installed. Run: pip install minio")
    
    try:
        client = Minio(
            os.getenv("MINIO_ENDPOINT", "localhost:9000"),
            access_key=os.getenv("MINIO_ACCESS_KEY", "minio_admin"),
            secret_key=os.getenv("MINIO_SECRET_KEY", "minio_admin_pass"),
            secure=os.getenv("MINIO_USE_SSL", "false").lower() == "true"
        )
        logger.info("MinIO client created")
        return client
    except Exception as e:
        logger.error(f"MinIO connection error: {str(e)}")
        raise

# Test all connections
def test_all_connections():
    """
    Test connectivity to all databases
    """
    results = {
        "postgres": False,
        "neo4j": False,
        "qdrant": False,
        "minio": False
    }
    
    # Test PostgreSQL
    try:
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                results["postgres"] = True
    except Exception as e:
        logger.error(f"PostgreSQL test failed: {str(e)}")
    
    # Test Neo4j
    try:
        logger.info("Testing Neo4j connection...")
        driver = get_neo4j_driver()
        logger.info("Neo4j driver created, verifying connectivity...")
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            result.single()
            results["neo4j"] = True
            logger.info("Neo4j connection successful!")
        driver.close()
    except Exception as e:
        logger.error(f"Neo4j test failed: {type(e).__name__}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    
    # Test Qdrant
    try:
        logger.info("Testing Qdrant connection...")
        client = get_qdrant_client()
        client.get_collections()
        results["qdrant"] = True
        logger.info("Qdrant connection successful!")
    except Exception as e:
        logger.error(f"Qdrant test failed: {type(e).__name__}: {str(e)}")
    
    # Test MinIO
    try:
        logger.info("Testing MinIO connection...")
        client = get_minio_client()
        client.list_buckets()
        results["minio"] = True
        logger.info("MinIO connection successful!")
    except Exception as e:
        logger.error(f"MinIO test failed: {type(e).__name__}: {str(e)}")
    
    return results

