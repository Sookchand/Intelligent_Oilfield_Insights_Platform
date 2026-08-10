"""
Quick test script to check database connections
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Testing Database Connections")
print("=" * 60)

# Test Neo4j
print("\n1. Testing Neo4j...")
print(f"   URI: {os.getenv('NEO4J_URI')}")
print(f"   User: {os.getenv('NEO4J_USER')}")
print(f"   Password: {'*' * len(os.getenv('NEO4J_PASSWORD', ''))}")

try:
    from neo4j import GraphDatabase
    print("   - neo4j package imported successfully")

    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "oilfield_neo4j_pass")

    print(f"   - Connecting to {uri}...")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    print("   - Driver created")

    print("   - Testing query...")
    with driver.session() as session:
        result = session.run("RETURN 1 as test")
        value = result.single()
        print(f"   - Query result: {value}")

    print("   ✅ Neo4j: Connected!")
    driver.close()
except ImportError as e:
    print(f"   ❌ Neo4j: Package not installed - {str(e)}")
    print("   Run: pip install neo4j")
except Exception as e:
    print(f"   ❌ Neo4j: Failed - {type(e).__name__}: {str(e)}")
    import traceback
    print("   Full traceback:")
    traceback.print_exc()

# Test Qdrant
print("\n2. Testing Qdrant...")
print(f"   Host: {os.getenv('QDRANT_HOST')}")
print(f"   Port: {os.getenv('QDRANT_PORT')}")

try:
    from qdrant_client import QdrantClient
    print("   - qdrant_client package imported successfully")

    host = os.getenv("QDRANT_HOST", "localhost")
    port = int(os.getenv("QDRANT_PORT", "6333"))

    print(f"   - Connecting to {host}:{port}...")
    client = QdrantClient(host=host, port=port)
    print("   - Client created")

    print("   - Getting collections...")
    collections = client.get_collections()
    print(f"   ✅ Qdrant: Connected! ({len(collections.collections)} collections)")
except ImportError as e:
    print(f"   ❌ Qdrant: Package not installed - {str(e)}")
    print("   Run: pip install qdrant-client")
except Exception as e:
    print(f"   ❌ Qdrant: Failed - {type(e).__name__}: {str(e)}")
    import traceback
    print("   Full traceback:")
    traceback.print_exc()

# Test PostgreSQL
print("\n3. Testing PostgreSQL...")
print(f"   Host: {os.getenv('POSTGRES_HOST')}")
print(f"   Port: {os.getenv('POSTGRES_PORT')}")
print(f"   Database: {os.getenv('POSTGRES_DB')}")

try:
    import psycopg2
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "oilfield_production"),
        user=os.getenv("POSTGRES_USER", "oilfield_user"),
        password=os.getenv("POSTGRES_PASSWORD", "oilfield_pass")
    )
    cur = conn.cursor()
    cur.execute("SELECT 1")
    cur.close()
    conn.close()
    print("   ✅ PostgreSQL: Connected!")
except Exception as e:
    print(f"   ❌ PostgreSQL: Failed - {type(e).__name__}: {str(e)}")

# Test MinIO
print("\n4. Testing MinIO...")
print(f"   Endpoint: {os.getenv('MINIO_ENDPOINT')}")

try:
    from minio import Minio
    client = Minio(
        os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY", "minio_admin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "minio_admin_pass"),
        secure=os.getenv("MINIO_USE_SSL", "false").lower() == "true"
    )
    buckets = client.list_buckets()
    print(f"   ✅ MinIO: Connected! ({len(buckets)} buckets)")
except Exception as e:
    print(f"   ❌ MinIO: Failed - {type(e).__name__}: {str(e)}")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)

