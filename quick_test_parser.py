"""Quick test of parser fix"""
import sys
sys.path.insert(0, 'backend')

from agents.parser import QueryParser

parser = QueryParser()

query = "Show me all faulty equipment at Rig Alpha"
result = parser.parse(query)

print(f"Query: {query}")
print(f"Intent: {result['intent']}")
print(f"Entities: {result['entities']}")
print(f"Plan: {result['plan']}")

expected_intent = "equipment_fault_analysis"
expected_plan = ["sql_retriever", "graph_retriever", "reasoning"]

if result['intent'] == expected_intent and result['plan'] == expected_plan:
    print("\n✅ FIX SUCCESSFUL!")
    print(f"   Intent correctly identified as: {expected_intent}")
    print(f"   Plan correctly set to: {expected_plan}")
else:
    print("\n❌ FIX FAILED")
    print(f"   Expected intent: {expected_intent}, got: {result['intent']}")
    print(f"   Expected plan: {expected_plan}, got: {result['plan']}")

