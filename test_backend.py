#!/usr/bin/env python
"""Quick test script to verify backend is working"""
import requests
import json

url = "http://localhost:8000/api/query"
payload = {"query": "Why is production dropping at Rig Alpha?"}

print("Testing backend API...")
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print("\nSending request...")

try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS!")
        result = response.json()
        print(f"\nAnswer: {result['answer']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Graph Path: {result.get('graph_path')}")
        print(f"\nReasoning Trace:")
        for step in result['reasoning_trace']:
            print(f"  {step['step']}. {step['agent']}: {step['action']}")
    else:
        print(f"\n❌ ERROR {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ EXCEPTION: {str(e)}")
    import traceback
    traceback.print_exc()

