"""
Test the AI-powered result formatter
"""
import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

load_dotenv()

# Mock results that would come from a database query
test_cases = [
    {
        "question": "When did production first drop below 850 barrels per day for Rig Alpha?",
        "results": [{"min": "2024-01-15 14:30:00"}]
    },
    {
        "question": "When did it start?",
        "results": [{"min": "2024-01-15 14:30:00"}]
    },
    {
        "question": "What is the average production rate?",
        "results": [{"avg": 1234.56}]
    },
    {
        "question": "Show me all faulty equipment",
        "results": [
            {"equipment_id": "PUMP-001", "status": "Faulty", "rig_name": "Rig Alpha"},
            {"equipment_id": "VALVE-042", "status": "Faulty", "rig_name": "Rig Alpha"},
            {"equipment_id": "SENSOR-123", "status": "Faulty", "rig_name": "Rig Beta"}
        ]
    }
]

# Test the formatter
from agents.flexible_executor import FlexibleExecutor

executor = FlexibleExecutor()

print("=" * 80)
print("AI-Powered Result Formatter Test")
print("=" * 80)

for i, test in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"Test {i}: {test['question']}")
    print(f"{'='*80}")
    print(f"Raw Results: {test['results']}")
    print(f"\nFormatted Answer:")
    print("-" * 80)
    
    answer = executor.format_results(test['results'], test['question'])
    print(answer)
    print("-" * 80)

print(f"\n{'='*80}")
print("✅ All tests complete!")
print("=" * 80)

