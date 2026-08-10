"""
Test script to verify the faulty equipment query fix
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from agents.parser import QueryParser

def test_parser_fix():
    """Test that the parser correctly identifies faulty equipment queries"""
    
    parser = QueryParser()
    
    # Test cases
    test_queries = [
        {
            "query": "Show me all faulty equipment at Rig Alpha",
            "expected_intent": "equipment_fault_analysis",
            "expected_entities": {"rigs": ["Rig Alpha"]},
            "expected_plan": ["sql_retriever", "graph_retriever", "reasoning"]
        },
        {
            "query": "What faulty sensors are at Well W-12?",
            "expected_intent": "equipment_fault_analysis",
            "expected_entities": {"wells": ["Well W-12"]},
            "expected_plan": ["sql_retriever", "graph_retriever", "reasoning"]
        },
        {
            "query": "Find broken equipment at Rig Alpha",
            "expected_intent": "equipment_fault_analysis",
            "expected_entities": {"rigs": ["Rig Alpha"]},
            "expected_plan": ["sql_retriever", "graph_retriever", "reasoning"]
        },
        {
            "query": "List all wells",
            "expected_intent": "list_wells",
            "expected_entities": {},
            "expected_plan": ["graph_list", "reasoning"]
        }
    ]
    
    print("=" * 80)
    print("TESTING PARSER FIX FOR FAULTY EQUIPMENT QUERIES")
    print("=" * 80)
    
    all_passed = True
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n{'='*80}")
        print(f"Test {i}: {test['query']}")
        print(f"{'='*80}")
        
        result = parser.parse(test['query'])
        
        # Check intent
        intent_match = result['intent'] == test['expected_intent']
        print(f"\n✓ Intent: {result['intent']}")
        if not intent_match:
            print(f"  ❌ EXPECTED: {test['expected_intent']}")
            all_passed = False
        else:
            print(f"  ✅ CORRECT")
        
        # Check entities
        print(f"\n✓ Entities: {result['entities']}")
        for key, expected_values in test['expected_entities'].items():
            if result['entities'].get(key) != expected_values:
                print(f"  ❌ EXPECTED {key}: {expected_values}")
                all_passed = False
            else:
                print(f"  ✅ {key}: CORRECT")
        
        # Check plan
        plan_match = result['plan'] == test['expected_plan']
        print(f"\n✓ Plan: {result['plan']}")
        if not plan_match:
            print(f"  ❌ EXPECTED: {test['expected_plan']}")
            all_passed = False
        else:
            print(f"  ✅ CORRECT")
    
    print("\n" + "=" * 80)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("=" * 80)
        print("\nThe parser now correctly identifies faulty equipment queries!")
        print("Intent: equipment_fault_analysis")
        print("Plan: sql_retriever → graph_retriever → reasoning")
        print("\nThis will trigger the correct graph traversal path.")
    else:
        print("❌ SOME TESTS FAILED")
        print("=" * 80)
    
    return all_passed

if __name__ == "__main__":
    success = test_parser_fix()
    sys.exit(0 if success else 1)

