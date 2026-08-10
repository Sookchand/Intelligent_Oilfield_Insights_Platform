"""
Test script for list query functionality
"""
import requests
import json

def test_list_wells():
    """Test listing all wells"""
    url = "http://localhost:8000/api/query"
    payload = {
        "query": "list the Well"
    }
    
    print("Testing: 'list the Well'")
    print("=" * 60)
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS!\n")
        print(f"Answer:\n{result['answer']}\n")
        print(f"Confidence: {result['confidence']}")
        print(f"\nReasoning Trace:")
        for step in result['reasoning_trace']:
            print(f"  {step['step']}. {step['agent']}: {step['action']}")
            if 'cypher_query' in step:
                print(f"     Cypher: {step['cypher_query'][:100]}...")
    else:
        print(f"❌ ERROR: {response.status_code}")
        print(response.text)

def test_list_rigs():
    """Test listing all rigs"""
    url = "http://localhost:8000/api/query"
    payload = {
        "query": "show all rigs"
    }
    
    print("\n\nTesting: 'show all rigs'")
    print("=" * 60)
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS!\n")
        print(f"Answer:\n{result['answer']}\n")
        print(f"Confidence: {result['confidence']}")
    else:
        print(f"❌ ERROR: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print("Testing List Query Functionality")
    print("=" * 60)
    
    try:
        test_list_wells()
        test_list_rigs()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend at http://localhost:8000")
        print("Make sure the backend is running!")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

