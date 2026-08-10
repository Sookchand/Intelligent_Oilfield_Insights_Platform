"""
Test AI-Powered Flexible Query System
Demonstrates how OpenAI enables arbitrary natural language queries
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/query"

# Test queries that demonstrate flexibility
TEST_QUERIES = [
    # Original question from user
    {
        "query": "What is the name and type of gauge at Well W-12?",
        "description": "Find specific sensor types at a specific well"
    },
    
    # Variations to test flexibility
    {
        "query": "Show me all pressure gauges in the system",
        "description": "Filter sensors by type"
    },
    
    {
        "query": "Which wells have temperature sensors?",
        "description": "Find wells with specific sensor types"
    },
    
    {
        "query": "What sensors are currently faulty?",
        "description": "Filter by sensor status"
    },
    
    {
        "query": "List all equipment at Rig Alpha",
        "description": "Find all equipment for a specific rig"
    },
    
    {
        "query": "What is the average oil production for Well W-12 in the last 7 days?",
        "description": "Time-series query with aggregation"
    },
    
    {
        "query": "Show me wells in the Permian basin with depth greater than 8000 feet",
        "description": "Complex filtering on well properties"
    },
    
    {
        "query": "Which rigs have the most wells?",
        "description": "Aggregation across relationships"
    }
]

def test_query(query_data: dict, index: int):
    """Test a single query"""
    print(f"\n{'='*80}")
    print(f"Test {index + 1}: {query_data['description']}")
    print(f"{'='*80}")
    print(f"Query: \"{query_data['query']}\"")
    print()
    
    try:
        start_time = time.time()
        response = requests.post(BASE_URL, json={"query": query_data['query']}, timeout=30)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ SUCCESS (took {duration:.2f}s)")
            print(f"\n📊 Answer:")
            print("-" * 80)
            print(result['answer'])
            print("-" * 80)
            
            print(f"\n🔍 Confidence: {result.get('confidence', 'N/A')}")
            
            print(f"\n🧠 Reasoning Trace:")
            for step in result.get('reasoning_trace', []):
                agent = step.get('agent', 'Unknown')
                action = step.get('action', 'Unknown')
                duration_ms = step.get('duration_ms', 0)
                
                print(f"  {step.get('step', '?')}. [{agent}] {action} ({duration_ms:.1f}ms)")
                
                # Show AI-generated queries
                if 'cypher_query' in step:
                    print(f"     Cypher: {step['cypher_query'][:100]}...")
                if 'sql_query' in step:
                    print(f"     SQL: {step['sql_query'][:100]}...")
                
                # Show AI details
                details = step.get('details', {})
                if details.get('ai_generated'):
                    print(f"     🤖 AI-Generated Query")
                    if 'explanation' in details:
                        print(f"     Explanation: {details['explanation']}")
            
            # Show data sources
            if 'data_sources' in result:
                print(f"\n📁 Data Sources:")
                for source in result['data_sources']:
                    ai_tag = " 🤖" if source.get('ai_generated') else ""
                    print(f"  - {source.get('type', 'unknown')} ({source.get('database', 'unknown')}){ai_tag}")
            
            return True
            
        else:
            print(f"❌ ERROR: HTTP {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏱️ TIMEOUT: Query took longer than 30 seconds")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION ERROR: Cannot connect to {BASE_URL}")
        print("Make sure the backend is running!")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🤖 AI-Powered Flexible Query System Test")
    print("=" * 80)
    print("This demonstrates how OpenAI enables arbitrary natural language queries")
    print("without needing predefined patterns or rules.")
    print()
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("⚠️ Backend health check failed!")
            return
    except:
        print("❌ Cannot connect to backend at http://localhost:8000")
        print("Please start the backend first:")
        print("  cd backend")
        print("  python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    print("✅ Backend is running\n")
    
    # Run tests
    results = []
    for i, query_data in enumerate(TEST_QUERIES):
        success = test_query(query_data, i)
        results.append(success)
        
        # Small delay between queries
        if i < len(TEST_QUERIES) - 1:
            time.sleep(1)
    
    # Summary
    print(f"\n{'='*80}")
    print("📊 Test Summary")
    print(f"{'='*80}")
    print(f"Total tests: {len(results)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")
    print(f"Success rate: {sum(results)/len(results)*100:.1f}%")

if __name__ == "__main__":
    main()

