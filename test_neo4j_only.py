"""Test Neo4j connection only"""
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Neo4j connection...")
print(f"URI: {os.getenv('NEO4J_URI')}")
print(f"User: {os.getenv('NEO4J_USER')}")

try:
    from neo4j import GraphDatabase
    
    driver = GraphDatabase.driver(
        os.getenv('NEO4J_URI'),
        auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
    )
    
    print("Driver created, testing connection...")
    
    # Verify connectivity with a simple query
    with driver.session() as session:
        result = session.run("RETURN 1 as test")
        record = result.single()
        print(f"✅ Connection successful! Test result: {record['test']}")
    
    driver.close()
    print("✅ Driver closed successfully")
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

