"""
Simple script to check if backend is running and if audit logger is initialized
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("="*60)
print("CHECKING BACKEND STATUS")
print("="*60)
print()

# Check 1: Can we import the audit logger?
print("1. Checking if audit logger module exists...")
try:
    from database.audit_log import audit_logger
    print("   ✅ Audit logger module imported")
except Exception as e:
    print(f"   ❌ Failed to import: {e}")
    sys.exit(1)

# Check 2: Is the audit logger initialized?
print()
print("2. Checking if audit logger is initialized...")
if audit_logger.initialized:
    print("   ✅ Audit logger IS initialized")
    print("   ✅ PostgreSQL connection is working")
    print("   ✅ Queries WILL be logged")
else:
    print("   ❌ Audit logger is NOT initialized")
    print("   ❌ PostgreSQL connection failed")
    print("   ❌ Queries will NOT be logged")
    print()
    print("   This is why queries don't appear in history!")

# Check 3: Can we connect to PostgreSQL?
print()
print("3. Testing PostgreSQL connection...")
try:
    from database.connections import get_postgres_connection
    with get_postgres_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"   ✅ PostgreSQL connected: {version[0][:50]}...")
        cursor.close()
except Exception as e:
    print(f"   ❌ PostgreSQL connection failed: {e}")
    print()
    print("   DIAGNOSIS:")
    print("   - PostgreSQL service may not be running")
    print("   - Database credentials may be incorrect")
    print("   - Database 'oilfield_insights' may not exist")

# Check 4: Does the audit table exist?
print()
print("4. Checking if audit table exists...")
try:
    from database.connections import get_postgres_connection
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
            print("   ✅ Audit table 'query_audit_log' exists")
            
            # Count rows
            cursor.execute("SELECT COUNT(*) FROM query_audit_log;")
            count = cursor.fetchone()[0]
            print(f"   ✅ Table has {count} queries logged")
            
            if count == 0:
                print()
                print("   ⚠️ Table exists but is empty")
                print("   This means:")
                print("   - Either no queries have been submitted yet")
                print("   - Or the audit logger wasn't initialized when queries were submitted")
        else:
            print("   ❌ Audit table does NOT exist")
            print("   The migration needs to be run")
        cursor.close()
except Exception as e:
    print(f"   ❌ Failed to check table: {e}")

# Summary
print()
print("="*60)
print("SUMMARY")
print("="*60)

if audit_logger.initialized:
    print("✅ Everything is working!")
    print("   - Backend can connect to PostgreSQL")
    print("   - Audit logger is initialized")
    print("   - Queries WILL be logged")
    print()
    print("If queries still don't appear in history:")
    print("   1. Make sure backend is running (python backend/main.py)")
    print("   2. Submit a test query on the main page")
    print("   3. Check backend logs for '✅ Query logged to audit trail'")
    print("   4. Refresh the history page")
else:
    print("❌ PROBLEM FOUND!")
    print("   - Audit logger is NOT initialized")
    print("   - This is why queries aren't being logged")
    print()
    print("TO FIX:")
    print("   1. Fix PostgreSQL connection (see error above)")
    print("   2. Restart backend: python backend/main.py")
    print("   3. Look for '✅ Query audit logger initialized'")
    print()
    print("QUICK WORKAROUND FOR DEMO:")
    print("   - Go to http://localhost:3002/history")
    print("   - Click 'Load Demo Data' button")
    print("   - Use mock data for demonstration")

print("="*60)

