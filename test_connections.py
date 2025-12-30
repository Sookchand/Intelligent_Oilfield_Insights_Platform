"""
Test database connections with current .env settings
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("="*60)
print("Testing Database Connections")
print("="*60)
print()

# Test PostgreSQL
print("1. Testing PostgreSQL...")
print(f"   Host: {os.getenv('POSTGRES_HOST')}")
print(f"   Port: {os.getenv('POSTGRES_PORT')}")
try:
    import psycopg2
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM production_data;")
    count = cursor.fetchone()[0]
    print(f"   ✅ Connected! Found {count} production records")
    conn.close()
except Exception as e:
    print(f"   ❌ Failed: {e}")

print()

# Test Neo4j
print("2. Testing Neo4j...")
print(f"   URI: {os.getenv('NEO4J_URI')}")
try:
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(
        os.getenv('NEO4J_URI'),
        auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
    )
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN count(n) as count")
        count = result.single()['count']
        print(f"   ✅ Connected! Found {count} nodes")
    driver.close()
except Exception as e:
    print(f"   ❌ Failed: {e}")

print()

# Test Qdrant
print("3. Testing Qdrant...")
print(f"   Host: {os.getenv('QDRANT_HOST')}")
print(f"   Port: {os.getenv('QDRANT_PORT')}")
try:
    from qdrant_client import QdrantClient
    client = QdrantClient(
        host=os.getenv('QDRANT_HOST'),
        port=int(os.getenv('QDRANT_PORT'))
    )
    collections = client.get_collections()
    print(f"   ✅ Connected! Found {len(collections.collections)} collections")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print()

# Test MinIO
print("4. Testing MinIO...")
print(f"   Endpoint: {os.getenv('MINIO_ENDPOINT')}")
try:
    from minio import Minio
    client = Minio(
        os.getenv('MINIO_ENDPOINT'),
        access_key=os.getenv('MINIO_ACCESS_KEY'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        secure=os.getenv('MINIO_USE_SSL', 'false').lower() == 'true'
    )
    buckets = client.list_buckets()
    print(f"   ✅ Connected! Found {len(buckets)} buckets")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print()
print("="*60)
print("Test Complete")
print("="*60)

