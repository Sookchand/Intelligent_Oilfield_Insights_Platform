# Query Validation & Verification System

## 🎯 Purpose

This system validates AI-generated queries **before** and **after** execution to prevent common mistakes and ensure data integrity.

---

## 🔍 Common AI Query Mistakes (Detected & Prevented)

### 1. **Literal Strings in SELECT Clause**
❌ **WRONG:**
```sql
SELECT 'min_time' AS min_time FROM production_data
```
Returns: `{'min_time': 'min_time'}` (literal string, not data!)

✅ **CORRECT:**
```sql
SELECT MIN(timestamp) AS min_time FROM production_data
```
Returns: `{'min_time': '2024-12-29 09:00:00'}` (actual data!)

**How we detect:** Check if column value equals column name (string comparison)

---

### 2. **NULL from Aggregate Functions**
❌ **WRONG:**
```sql
SELECT MIN(timestamp) WHERE production_rate < 850.5
```
Returns: `{'min_time': None}` (no records match!)

✅ **CORRECT:**
```sql
SELECT MIN(timestamp) WHERE production_rate < 943.2
```
Returns: `{'min_time': '2024-12-29 09:00:00'}` (actual data!)

**How we detect:** Check if aggregate function returns NULL, suggest broader WHERE clause

---

### 3. **Parameter Count Mismatch**
❌ **WRONG:**
```sql
SQL: "SELECT * FROM production_data WHERE rig_name = $1 AND rate < $2"
Parameters: ['Rig Alpha']  # Missing $2!
```

✅ **CORRECT:**
```sql
SQL: "SELECT * FROM production_data WHERE rig_name = $1 AND rate < $2"
Parameters: ['Rig Alpha', 943.2]  # All parameters provided
```

**How we detect:** Count placeholders ($1, $2, %s) and compare to parameter list length

---

### 4. **Wrong Threshold Values**
❌ **WRONG (for "when did drop start"):**
```sql
-- Using current low value (850.5) instead of average (943.2)
SELECT MIN(timestamp) WHERE production_rate < 850.5
```

✅ **CORRECT:**
```sql
-- Using average to find when drop STARTED
SELECT MIN(timestamp) WHERE production_rate < 943.2
```

**How we detect:** AI prompt engineering + result validation

---

## 🛠️ Validation Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. AI Generates Query                                       │
│    - SQL: SELECT MIN(timestamp) WHERE rate < $1             │
│    - Parameters: [943.2, 'Rig Alpha']                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. PRE-EXECUTION VALIDATION (QueryValidator)                │
│    ✓ Check for literal strings in SELECT                    │
│    ✓ Validate parameter count matches placeholders          │
│    ✓ Ensure parameters are not None/empty                   │
│    ✓ Verify table names exist in schema                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. EXECUTE QUERY (FlexibleExecutor)                         │
│    - Convert $1, $2 to %s for psycopg2                      │
│    - Execute against PostgreSQL                             │
│    - Fetch results                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. POST-EXECUTION VALIDATION (QueryValidator)               │
│    ✓ Check if column value == column name (literal string)  │
│    ✓ Check if aggregate returned NULL (no matches)          │
│    ✓ Validate data types are correct                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. RETURN VALIDATED RESULTS                                 │
│    - If valid: return cleaned results                       │
│    - If invalid: return [] and log error + suggestion       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Testing the Validator

Run the test suite:
```bash
cd backend
python test_validator.py
```

Expected output:
```
================================================================================
QUERY VALIDATOR TEST SUITE
================================================================================

📋 Test 1: Detect literal string in SELECT
   SQL: SELECT 'min_time' AS min_time FROM production_data WHERE rig_name = $1
   Valid: False
   Error: Query contains literal strings in SELECT clause
   ✅ PASS

📋 Test 2: Validate correct aggregate function
   SQL: SELECT MIN(timestamp) AS min_time FROM production_data WHERE rig_name = $1
   Valid: True
   Error: None
   ✅ PASS

... (more tests)
```

---

## 🚀 Usage in Code

```python
from agents.flexible_executor import FlexibleExecutor

executor = FlexibleExecutor()  # Validator is auto-initialized

# Execute query - validation happens automatically
results = executor.execute_sql(
    sql="SELECT MIN(timestamp) AS min_time FROM production_data WHERE production_rate < $1 AND rig_name = $2",
    parameters=[943.2, 'Rig Alpha']
)

# Results are guaranteed to be valid or empty list
if results:
    print(f"Valid data: {results[0]}")
else:
    print("No valid results (check logs for validation errors)")
```

---

## 📝 Best Practices

1. **Always use the FlexibleExecutor** - it has built-in validation
2. **Check logs for validation errors** - they include suggestions for fixes
3. **Test queries with test_validator.py** before deploying
4. **Update AI prompts** based on validation failures
5. **Monitor validation failure rate** in production

---

## 🔧 Extending the Validator

To add new validation rules:

1. Edit `backend/agents/query_validator.py`
2. Add validation logic to `validate_sql_query()` or `validate_sql_results()`
3. Add suggestion logic to `suggest_query_fix()`
4. Add test case to `backend/test_validator.py`
5. Run tests to verify

---

## 📈 Metrics to Monitor

- **Validation failure rate**: % of queries that fail validation
- **Most common errors**: Which validation rules trigger most often
- **Suggestion effectiveness**: Do AI prompts improve after suggestions?
- **False positive rate**: Valid queries incorrectly rejected

---

## ✅ Summary

This validation system ensures:
- ✅ No literal strings in results
- ✅ Correct parameter counts
- ✅ Valid SQL syntax
- ✅ Meaningful results (not NULL/empty)
- ✅ Helpful error messages and suggestions

**Result: Reliable, auditable, production-ready AI query system!**

