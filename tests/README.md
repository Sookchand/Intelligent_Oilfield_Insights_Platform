# 🧪 Test Suite - Query Routing Fixes

## 📋 **Overview**

This directory contains comprehensive tests for the query routing fixes that improved confidence from 30% to 85-90% for two critical queries.

**Total Tests:** 24
- **Unit Tests:** 12
- **Integration Tests:** 4
- **End-to-End Tests:** 8

---

## 🚀 **Quick Start**

### **Run All Tests:**
```powershell
# From project root:
RUN_ALL_TESTS.bat

# Or manually:
cd tests
python run_all_tests.py
```

### **Run Individual Test Suites:**
```powershell
# Unit tests only (fastest)
python test_query_routing_fixes.py

# Integration tests only
python test_graph_engine_integration.py

# End-to-end tests only (requires backend + databases)
python test_system_end_to_end.py
```

---

## 📁 **Test Files**

### **1. test_query_routing_fixes.py** (12 tests)

**Purpose:** Unit tests for parser and routing logic

**Test Classes:**
- `TestFaultyEquipmentQueryFix` (7 tests)
  - Intent detection
  - Entity extraction
  - Execution plan creation
  - Synonym recognition
  - Priority-based routing

- `TestForecastQueryFix` (4 tests)
  - Intent detection
  - Plan creation
  - Keyword variations
  - Entity-optional queries

- `TestQueryRoutingIntegration` (1 test)
  - Multi-query type routing

**Run Time:** < 1 second

---

### **2. test_graph_engine_integration.py** (4 tests)

**Purpose:** Integration tests for graph engine and agent orchestration

**Test Classes:**
- `TestGraphEngineRouting` (2 tests)
  - Forecast queries excluded from AI routing
  - General queries routed to AI when appropriate

- `TestFaultyEquipmentIntegration` (1 test)
  - Faulty equipment uses correct agents

- `TestForecastIntegration` (1 test)
  - Forecast calls forecasting module

**Run Time:** < 2 seconds

---

### **3. test_system_end_to_end.py** (8 tests)

**Purpose:** End-to-end tests for complete system

**Prerequisites:**
- Backend running: `cd backend && python main.py`
- Databases running: `docker-compose up -d`

**Test Classes:**
- `TestSystemHealth` (2 tests)
  - Backend accessibility
  - Database connections

- `TestFaultyEquipmentEndToEnd` (3 tests)
  - Query confidence (85-90%)
  - Correct agent workflow
  - Actual data retrieval

- `TestForecastEndToEnd` (3 tests)
  - Query confidence (85-90%)
  - Forecasting agent usage
  - Numeric forecast value

**Run Time:** < 30 seconds

---

### **4. run_all_tests.py**

**Purpose:** Test runner that executes all test suites

**Features:**
- Discovers all test files
- Runs all tests
- Provides summary report

---

## ✅ **What's Tested**

### **Fix #1: Faulty Equipment Query**

**Query:** "Show me all faulty equipment at Rig Alpha"

**Tests Verify:**
- ✅ Parser identifies `equipment_fault_analysis` intent
- ✅ Rig entity "Rig Alpha" is extracted
- ✅ Execution plan: `['sql_retriever', 'graph_retriever', 'reasoning']`
- ✅ Fault keywords have priority over list keywords
- ✅ Graph engine routes to correct agents
- ✅ End-to-end query returns 85-90% confidence
- ✅ Result contains actual faulty equipment data

---

### **Fix #2: Forecast Query**

**Query:** "Predict production for next week"

**Tests Verify:**
- ✅ Parser identifies `production_forecast` intent
- ✅ Forecast queries excluded from AI routing
- ✅ Forecasting module is called
- ✅ Execution plan includes forecasting
- ✅ End-to-end query returns 85-90% confidence
- ✅ Result contains numeric forecast value
- ✅ Reasoning trace shows "Forecasting" agent

---

## 📊 **Expected Results**

```
================================================================================
TEST SUMMARY
================================================================================
Tests run: 24
Successes: 24
Failures: 0
Errors: 0
================================================================================

✅ ALL TESTS PASSED!

Your query routing fixes are working correctly!
  ✅ Faulty equipment queries: 30% → 85-90% confidence
  ✅ Forecast queries: 30% → 85-90% confidence
  ✅ All agents working correctly
  ✅ System integration verified
```

---

## 🎯 **Test Coverage**

| Component | Unit | Integration | E2E | Total |
|-----------|------|-------------|-----|-------|
| Parser | ✅ 7 | - | - | 7 |
| Routing Logic | ✅ 5 | ✅ 2 | - | 7 |
| Graph Engine | - | ✅ 2 | - | 2 |
| Multi-Agent | - | - | ✅ 6 | 6 |
| System Health | - | - | ✅ 2 | 2 |
| **Total** | **12** | **4** | **8** | **24** |

---

## 🔧 **Troubleshooting**

### **Tests Fail:**
1. Make sure virtual environment is activated
2. Check that backend code changes are saved
3. For E2E tests, ensure backend and databases are running

### **Import Errors:**
1. Make sure you're in the `tests` directory
2. Check that `__init__.py` exists in `tests` directory
3. Verify Python path includes backend directory

### **Timeout Errors (E2E tests):**
1. Ensure backend is running: `cd backend && python main.py`
2. Ensure databases are running: `docker-compose up -d`
3. Check backend is accessible: http://localhost:8000/health

---

## 📚 **Documentation**

For more information, see:
- `../TESTING_COMPREHENSIVE.md` - Detailed testing guide
- `../COMPLETE_TESTING_GUIDE.md` - Quick start guide
- `../TESTING_AND_VALIDATION_SUMMARY.md` - V&V summary

---

**All tests are ready! Run `RUN_ALL_TESTS.bat` from project root!** 🚀

