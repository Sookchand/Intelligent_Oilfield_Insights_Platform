"""
Quick test script to verify backend is running and can log queries
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_backend_status():
    """Test if backend is running"""
    print("\n" + "="*60)
    print("TESTING BACKEND STATUS")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/status/databases", timeout=5)
        print(f"✅ Backend is running on {BASE_URL}")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Backend is NOT running on {BASE_URL}")
        print("   Please start the backend with: python backend/main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_query_submission():
    """Test submitting a query"""
    print("\n" + "="*60)
    print("TESTING QUERY SUBMISSION")
    print("="*60)
    
    test_query = "Why is production declining at Rig Alpha?"
    
    try:
        print(f"Submitting query: '{test_query}'")
        
        response = requests.post(
            f"{BASE_URL}/api/query",
            json={"query": test_query},
            timeout=30
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Query processed successfully!")
            print(f"   Answer: {data.get('answer', 'N/A')[:100]}...")
            print(f"   Confidence: {data.get('confidence', 'N/A')}")
            print(f"   Query Type: {data.get('query_type', 'N/A')}")
            return True
        else:
            print(f"❌ Query failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error submitting query: {str(e)}")
        return False

def test_query_history():
    """Test retrieving query history"""
    print("\n" + "="*60)
    print("TESTING QUERY HISTORY")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/audit/history?limit=10", timeout=5)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            queries = data.get('queries', [])
            total = data.get('total', 0)
            
            print(f"✅ Retrieved query history")
            print(f"   Total queries in database: {total}")
            print(f"   Queries returned: {len(queries)}")
            
            if queries:
                print(f"\n   Recent queries:")
                for i, q in enumerate(queries[:5], 1):
                    print(f"   {i}. {q.get('query_text', 'N/A')[:50]}...")
                    print(f"      Status: {q.get('status', 'N/A')}, Confidence: {q.get('confidence_score', 'N/A')}")
            else:
                print(f"\n   ⚠️ No queries found in history")
                print(f"   This means queries are not being logged to the database")
                
            return len(queries) > 0
        else:
            print(f"❌ Failed to retrieve history: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error retrieving history: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("BACKEND & QUERY LOGGING TEST")
    print("="*60)
    
    # Test 1: Backend status
    backend_ok = test_backend_status()
    
    if not backend_ok:
        print("\n❌ Backend is not running. Please start it first.")
        print("   Command: python backend/main.py")
        return
    
    # Test 2: Submit a query
    time.sleep(1)
    query_ok = test_query_submission()
    
    # Test 3: Check history
    time.sleep(1)
    history_ok = test_query_history()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Backend Running:     {'✅' if backend_ok else '❌'}")
    print(f"Query Submission:    {'✅' if query_ok else '❌'}")
    print(f"Query History:       {'✅' if history_ok else '❌'}")
    
    if backend_ok and query_ok and not history_ok:
        print("\n⚠️ DIAGNOSIS:")
        print("   - Backend is running")
        print("   - Queries are being processed")
        print("   - BUT queries are NOT being logged to the database")
        print("\n   Possible causes:")
        print("   1. PostgreSQL is not connected")
        print("   2. Audit logger failed to initialize")
        print("   3. Audit table doesn't exist")
        print("\n   Check backend logs for:")
        print("   - '✅ Query audit logger initialized'")
        print("   - '✅ Audit log table verified/created'")
        print("   - Any PostgreSQL connection errors")
    
    print("="*60)

if __name__ == "__main__":
    main()

