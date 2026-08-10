#!/usr/bin/env python
"""
Comprehensive End-to-End System Performance Test
Tests all components including ontology reasoning
"""
import requests
import json
import time
from typing import Dict, List, Any
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30

# Test queries covering different scenarios
TEST_QUERIES = [
    {
        "name": "Production Drop Analysis (Ontology Reasoning)",
        "query": "Why is production dropping at Rig Alpha?",
        "expected_agents": ["Parser", "SQL", "Graph", "Ontology", "Reasoning"],
        "expected_confidence_min": 0.7,
        "should_have_ontology": True,
        "should_have_sql": True,
        "should_have_graph": True,
    },
    {
        "name": "Safety Risk Assessment",
        "query": "What is the safety risk at Well W-12?",
        "expected_agents": ["Parser", "SQL", "Graph", "Reasoning"],
        "expected_confidence_min": 0.7,
        "should_have_sql": True,
        "should_have_graph": True,
    },
    {
        "name": "Equipment Status Query",
        "query": "Show me all faulty equipment at Rig Alpha",
        "expected_agents": ["Parser", "Graph", "Reasoning"],
        "expected_confidence_min": 0.7,
        "should_have_graph": True,
    },
    {
        "name": "Production Rate Query",
        "query": "What is the production rate for Well B-12?",
        "expected_agents": ["Parser", "SQL", "Reasoning"],
        "expected_confidence_min": 0.7,
        "should_have_sql": True,
    },
    {
        "name": "Forecasting Query",
        "query": "Predict production for next week",
        "expected_agents": ["Parser", "SQL", "Reasoning"],
        "expected_confidence_min": 0.6,
        "should_have_sql": True,
    },
]

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

def test_health_check() -> bool:
    """Test if backend is healthy"""
    print_header("HEALTH CHECK")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend is healthy: {data.get('status')}")
            print_info(f"Service: {data.get('service')}")
            print_info(f"Version: {data.get('version')}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False

def validate_response(response_data: Dict[str, Any], test_config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate response against test configuration"""
    results = {
        "passed": True,
        "checks": [],
        "warnings": []
    }
    
    # Check required fields
    required_fields = ["answer", "confidence", "reasoning_trace"]
    for field in required_fields:
        if field in response_data:
            results["checks"].append(f"Has '{field}' field")
        else:
            results["passed"] = False
            results["checks"].append(f"MISSING '{field}' field")
    
    # Check confidence score
    confidence = response_data.get("confidence", 0)
    min_confidence = test_config.get("expected_confidence_min", 0.5)
    if confidence >= min_confidence:
        results["checks"].append(f"Confidence {confidence:.2f} >= {min_confidence}")
    else:
        results["warnings"].append(f"Low confidence: {confidence:.2f} < {min_confidence}")
    
    # Check agents executed
    reasoning_trace = response_data.get("reasoning_trace", [])
    agents_executed = [step.get("agent") for step in reasoning_trace]
    expected_agents = test_config.get("expected_agents", [])

    for agent in expected_agents:
        if agent in agents_executed:
            results["checks"].append(f"Agent '{agent}' executed")
        else:
            results["warnings"].append(f"Expected agent '{agent}' not executed")

    # Check for ontology reasoning
    if test_config.get("should_have_ontology", False):
        ontology_steps = [s for s in reasoning_trace if s.get("agent") == "Ontology"]
        if ontology_steps:
            results["checks"].append("Ontology reasoning present")
            # Check for causal explanation
            for step in ontology_steps:
                if step.get("causal_explanation"):
                    results["checks"].append("Has causal explanation")
                if step.get("domain_knowledge"):
                    results["checks"].append("Has domain knowledge")
                if step.get("details", {}).get("confidence"):
                    results["checks"].append("Has ontology confidence score")
        else:
            results["warnings"].append("Expected ontology reasoning not found")

    # Check for SQL queries
    if test_config.get("should_have_sql", False):
        sql_steps = [s for s in reasoning_trace if s.get("sql_query")]
        if sql_steps:
            results["checks"].append(f"SQL queries executed ({len(sql_steps)})")
        else:
            results["warnings"].append("Expected SQL queries not found")

    # Check for Graph queries
    if test_config.get("should_have_graph", False):
        graph_steps = [s for s in reasoning_trace if s.get("cypher_query")]
        if graph_steps:
            results["checks"].append(f"Graph queries executed ({len(graph_steps)})")
        else:
            results["warnings"].append("Expected graph queries not found")

    return results

def run_query_test(test_config: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single query test"""
    test_name = test_config["name"]
    query = test_config["query"]

    print(f"\n{Colors.BOLD}Test: {test_name}{Colors.END}")
    print(f"Query: {Colors.CYAN}{query}{Colors.END}")

    start_time = time.time()

    try:
        response = requests.post(
            f"{BASE_URL}/api/query",
            json={"query": query},
            timeout=TIMEOUT
        )

        elapsed_time = time.time() - start_time

        if response.status_code != 200:
            print_error(f"Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return {
                "test_name": test_name,
                "passed": False,
                "error": f"HTTP {response.status_code}",
                "elapsed_time": elapsed_time
            }

        response_data = response.json()

        # Validate response
        validation = validate_response(response_data, test_config)

        # Print results
        print(f"\n{Colors.BOLD}Response Time:{Colors.END} {elapsed_time:.2f}s")
        print(f"{Colors.BOLD}Answer:{Colors.END} {response_data.get('answer', 'N/A')[:100]}...")
        print(f"{Colors.BOLD}Confidence:{Colors.END} {response_data.get('confidence', 0):.2%}")

        print(f"\n{Colors.BOLD}Reasoning Trace:{Colors.END}")
        for step in response_data.get("reasoning_trace", []):
            agent = step.get("agent", "Unknown")
            action = step.get("action", "N/A")
            duration = step.get("duration_ms", 0)
            print(f"  {step.get('step', '?')}. {agent}: {action} ({duration:.1f}ms)")

        print(f"\n{Colors.BOLD}Validation Checks:{Colors.END}")
        for check in validation["checks"]:
            print_success(check)

        if validation["warnings"]:
            print(f"\n{Colors.BOLD}Warnings:{Colors.END}")
            for warning in validation["warnings"]:
                print_warning(warning)

        if validation["passed"] and not validation["warnings"]:
            print_success(f"\n{test_name} PASSED")
        elif validation["passed"]:
            print_warning(f"\n{test_name} PASSED WITH WARNINGS")
        else:
            print_error(f"\n{test_name} FAILED")

        return {
            "test_name": test_name,
            "passed": validation["passed"],
            "warnings": len(validation["warnings"]),
            "elapsed_time": elapsed_time,
            "confidence": response_data.get("confidence", 0),
            "agents_count": len(response_data.get("reasoning_trace", [])),
            "response_data": response_data
        }

    except Exception as e:
        elapsed_time = time.time() - start_time
        print_error(f"Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "test_name": test_name,
            "passed": False,
            "error": str(e),
            "elapsed_time": elapsed_time
        }

def print_summary(results: List[Dict[str, Any]]):
    """Print test summary"""
    print_header("TEST SUMMARY")

    total_tests = len(results)
    passed_tests = sum(1 for r in results if r.get("passed", False))
    failed_tests = total_tests - passed_tests
    total_warnings = sum(r.get("warnings", 0) for r in results)

    avg_time = sum(r.get("elapsed_time", 0) for r in results) / total_tests if total_tests > 0 else 0
    avg_confidence = sum(r.get("confidence", 0) for r in results) / total_tests if total_tests > 0 else 0

    print(f"{Colors.BOLD}Total Tests:{Colors.END} {total_tests}")
    print_success(f"Passed: {passed_tests}")
    if failed_tests > 0:
        print_error(f"Failed: {failed_tests}")
    if total_warnings > 0:
        print_warning(f"Total Warnings: {total_warnings}")

    print(f"\n{Colors.BOLD}Performance Metrics:{Colors.END}")
    print(f"Average Response Time: {avg_time:.2f}s")
    print(f"Average Confidence: {avg_confidence:.2%}")

    print(f"\n{Colors.BOLD}Individual Test Results:{Colors.END}")
    for result in results:
        status = "✅ PASS" if result.get("passed") else "❌ FAIL"
        warnings = f" ({result.get('warnings', 0)} warnings)" if result.get("warnings", 0) > 0 else ""
        print(f"  {status} {result['test_name']}: {result.get('elapsed_time', 0):.2f}s{warnings}")

    # Overall result
    print()
    if failed_tests == 0 and total_warnings == 0:
        print_success(f"ALL TESTS PASSED! 🎉")
    elif failed_tests == 0:
        print_warning(f"ALL TESTS PASSED WITH {total_warnings} WARNINGS")
    else:
        print_error(f"{failed_tests} TEST(S) FAILED")

    return passed_tests == total_tests

def main():
    """Main test execution"""
    print_header("END-TO-END SYSTEM PERFORMANCE TEST")
    print(f"Testing backend at: {BASE_URL}")
    print(f"Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Health check
    if not test_health_check():
        print_error("Backend is not healthy. Aborting tests.")
        return False

    # Run all tests
    results = []
    for i, test_config in enumerate(TEST_QUERIES, 1):
        print(f"\n{Colors.BOLD}[{i}/{len(TEST_QUERIES)}]{Colors.END}")
        result = run_query_test(test_config)
        results.append(result)
        time.sleep(1)  # Brief pause between tests

    # Print summary
    success = print_summary(results)

    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)


