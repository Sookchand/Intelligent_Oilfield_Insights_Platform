"""
Test Query Validator
Run this to verify the validator catches common AI mistakes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from agents.query_validator import QueryValidator
from agents.flexible_executor import FlexibleExecutor

def test_validator():
    """Test the query validator with common AI mistakes"""
    
    print("=" * 80)
    print("QUERY VALIDATOR TEST SUITE")
    print("=" * 80)
    
    validator = QueryValidator()
    executor = FlexibleExecutor()
    
    # Test 1: Literal string in SELECT (WRONG)
    print("\n📋 Test 1: Detect literal string in SELECT")
    sql = "SELECT 'min_time' AS min_time FROM production_data WHERE rig_name = $1"
    params = ['Rig Alpha']
    is_valid, error = validator.validate_sql_query(sql, params)
    print(f"   SQL: {sql}")
    print(f"   Valid: {is_valid}")
    print(f"   Error: {error}")
    assert not is_valid, "Should detect literal string"
    print("   ✅ PASS")
    
    # Test 2: Correct aggregate function (CORRECT)
    print("\n📋 Test 2: Validate correct aggregate function")
    sql = "SELECT MIN(timestamp) AS min_time FROM production_data WHERE rig_name = $1"
    params = ['Rig Alpha']
    is_valid, error = validator.validate_sql_query(sql, params)
    print(f"   SQL: {sql}")
    print(f"   Valid: {is_valid}")
    print(f"   Error: {error}")
    assert is_valid, "Should accept valid query"
    print("   ✅ PASS")
    
    # Test 3: Parameter count mismatch
    print("\n📋 Test 3: Detect parameter count mismatch")
    sql = "SELECT * FROM production_data WHERE rig_name = $1 AND production_rate < $2"
    params = ['Rig Alpha']  # Missing second parameter
    is_valid, error = validator.validate_sql_query(sql, params)
    print(f"   SQL: {sql}")
    print(f"   Params: {params}")
    print(f"   Valid: {is_valid}")
    print(f"   Error: {error}")
    assert not is_valid, "Should detect parameter mismatch"
    print("   ✅ PASS")
    
    # Test 4: Execute real query and validate results
    print("\n📋 Test 4: Execute query and validate results")
    sql = "SELECT MIN(timestamp) AS min_time FROM production_data WHERE production_rate < $1 AND rig_name = $2"
    params = [943.2, 'Rig Alpha']
    print(f"   SQL: {sql}")
    print(f"   Params: {params}")
    
    results = executor.execute_sql(sql, params)
    print(f"   Results: {results}")
    
    if results:
        print("   ✅ PASS - Query returned valid results")
    else:
        print("   ⚠️  Query returned no results (may be expected if no data matches)")
    
    # Test 5: Test query with sample data
    print("\n📋 Test 5: Test query with sample data")
    test_result = validator.test_query_with_sample_data(sql, params)
    print(f"   Success: {test_result['success']}")
    print(f"   Record count: {test_result['record_count']}")
    print(f"   Sample record: {test_result['sample_record']}")
    print(f"   Issues: {test_result['issues']}")
    
    if test_result['success']:
        print("   ✅ PASS")
    else:
        print(f"   ❌ FAIL: {test_result['issues']}")
    
    print("\n" + "=" * 80)
    print("TEST SUITE COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_validator()

