"""
Test PostgreSQL parameter conversion
Verifies that $1, $2 style parameters are correctly converted to %s for psycopg2
"""
import re

def convert_postgres_params(sql: str) -> str:
    """Convert PostgreSQL-style parameters ($1, $2) to psycopg2-style (%s)"""
    def replace_param(match):
        return '%s'
    return re.sub(r'\$\d+', replace_param, sql)

# Test cases
test_cases = [
    {
        "name": "Simple SELECT with 2 parameters",
        "input": "SELECT MIN(timestamp) FROM production_data WHERE production_rate < $1 AND rig_name = $2",
        "expected": "SELECT MIN(timestamp) FROM production_data WHERE production_rate < %s AND rig_name = %s",
        "parameters": [850.5, 'Rig Alpha']
    },
    {
        "name": "SELECT with 3 parameters",
        "input": "SELECT * FROM production_data WHERE rig_name = $1 AND timestamp > $2 AND production_rate < $3",
        "expected": "SELECT * FROM production_data WHERE rig_name = %s AND timestamp > %s AND production_rate < %s",
        "parameters": ['Rig Alpha', '2024-01-01', 900.0]
    },
    {
        "name": "No parameters",
        "input": "SELECT * FROM production_data",
        "expected": "SELECT * FROM production_data",
        "parameters": []
    },
    {
        "name": "Single parameter",
        "input": "SELECT AVG(production_rate) FROM production_data WHERE rig_name = $1",
        "expected": "SELECT AVG(production_rate) FROM production_data WHERE rig_name = %s",
        "parameters": ['Rig Alpha']
    },
    {
        "name": "Parameters in different order",
        "input": "SELECT * FROM production_data WHERE $1 < production_rate AND rig_name = $2",
        "expected": "SELECT * FROM production_data WHERE %s < production_rate AND rig_name = %s",
        "parameters": [800.0, 'Rig Alpha']
    }
]

print("=" * 80)
print("PostgreSQL Parameter Conversion Test")
print("=" * 80)

all_passed = True
for i, test in enumerate(test_cases, 1):
    print(f"\nTest {i}: {test['name']}")
    print(f"Input:    {test['input']}")
    
    result = convert_postgres_params(test['input'])
    print(f"Output:   {result}")
    print(f"Expected: {test['expected']}")
    
    if result == test['expected']:
        print("✅ PASS")
    else:
        print("❌ FAIL")
        all_passed = False
    
    # Show how it would be used with parameters
    if test['parameters']:
        print(f"Parameters: {test['parameters']}")
        print(f"Would execute: cursor.execute('{result}', {test['parameters']})")

print("\n" + "=" * 80)
if all_passed:
    print("✅ ALL TESTS PASSED")
else:
    print("❌ SOME TESTS FAILED")
print("=" * 80)

