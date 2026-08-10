"""
Test script to verify audit logging is working
"""
import sys
sys.path.append('backend')

from database.audit_log import audit_logger
from database.connections import get_postgres_connection

print("=" * 60)
print("TESTING AUDIT LOGGING SYSTEM")
print("=" * 60)

# Test 1: Check if table exists
print("\n1. Checking if audit table exists...")
try:
    with get_postgres_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'query_audit_log'
            );
        """)
        exists = cursor.fetchone()[0]
        if exists:
            print("   ✅ Table 'query_audit_log' exists")
        else:
            print("   ❌ Table 'query_audit_log' does NOT exist")
            print("   Creating table...")
            # Try to create it
            with open('backend/database/migrations/001_create_audit_log.sql', 'r') as f:
                cursor.execute(f.read())
            conn.commit()
            print("   ✅ Table created successfully")
        cursor.close()
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Check current row count
print("\n2. Checking current row count...")
try:
    with get_postgres_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM query_audit_log")
        count = cursor.fetchone()[0]
        print(f"   📊 Current rows in audit log: {count}")
        cursor.close()
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Insert a test query
print("\n3. Inserting a test query...")
try:
    query_id = audit_logger.log_query(
        query_text="Test query: Why is production declining?",
        query_type="production_query",
        confidence_score=0.95,
        processing_time_ms=1234,
        status="success",
        data_sources_used=["PostgreSQL", "Neo4j"],
        reasoning_trace=[
            {"step": 1, "agent": "Parser", "action": "Parsed query"},
            {"step": 2, "agent": "SQL", "action": "Queried production data"}
        ],
        result_summary="Production is declining due to equipment failure",
        user_name="Test User",
        metadata={"test": True}
    )
    if query_id:
        print(f"   ✅ Test query logged successfully (ID: {query_id})")
    else:
        print("   ❌ Failed to log test query")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Retrieve recent queries
print("\n4. Retrieving recent queries...")
try:
    history = audit_logger.get_query_history(limit=5)
    print(f"   📊 Retrieved {len(history)} queries:")
    for q in history:
        print(f"      - [{q['id']}] {q['query_text'][:50]}... (confidence: {q['confidence_score']})")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Check if audit logger is initialized
print("\n5. Checking audit logger initialization...")
print(f"   Initialized: {audit_logger.initialized}")

print("\n" + "=" * 60)
print("AUDIT LOGGING TEST COMPLETE")
print("=" * 60)

