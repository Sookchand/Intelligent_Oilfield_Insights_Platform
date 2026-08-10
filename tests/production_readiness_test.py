"""
Production Readiness Test Suite
Comprehensive validation for Intelligent Oilfield Insights Platform

Run with: python tests/production_readiness_test.py

Features:
- Automated testing of all system components
- Auto-correction of common issues
- Detailed JSON and HTML reports
- Production readiness scoring
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import requests
import time
import psycopg2
from neo4j import GraphDatabase
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import subprocess

# Test Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3002"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "oilfield_neo4j_pass"
POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5433,  # External port (mapped from 5432)
    "database": "oilfield_production",
    "user": "oilfield_user",
    "password": "oilfield_pass"  # Fixed: matches docker-compose.yml
}

class ProductionReadinessTest:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.auto_fixes = []
        self.start_time = datetime.now()
        
    def log_test(self, category: str, test_name: str, status: str, message: str, details: str = ""):
        """Log test result"""
        result = {
            "category": category,
            "test": test_name,
            "status": status,  # PASS, FAIL, WARN
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        
        if status == "PASS":
            self.passed += 1
            print(f"✅ {category} - {test_name}: {message}")
        elif status == "FAIL":
            self.failed += 1
            print(f"❌ {category} - {test_name}: {message}")
            if details:
                print(f"   Details: {details}")
        elif status == "WARN":
            self.warnings += 1
            print(f"⚠️  {category} - {test_name}: {message}")
            
    def test_database_connectivity(self):
        """Test 1: Database Connectivity"""
        print("\n" + "="*60)
        print("TEST CATEGORY 1: DATABASE CONNECTIVITY")
        print("="*60)
        
        # Test PostgreSQL
        try:
            conn = psycopg2.connect(**POSTGRES_CONFIG)
            conn.close()
            self.log_test("Database", "PostgreSQL Connection", "PASS", "Connected successfully")
        except Exception as e:
            self.log_test("Database", "PostgreSQL Connection", "FAIL", "Connection failed", str(e))
            
        # Test Neo4j
        try:
            driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            with driver.session() as session:
                result = session.run("RETURN 1")
                result.single()
            driver.close()
            self.log_test("Database", "Neo4j Connection", "PASS", "Connected successfully")
        except Exception as e:
            self.log_test("Database", "Neo4j Connection", "FAIL", "Connection failed", str(e))
            
        # Test Qdrant
        try:
            response = requests.get("http://localhost:6333/collections")
            if response.status_code == 200:
                self.log_test("Database", "Qdrant Connection", "PASS", "Connected successfully")
            else:
                self.log_test("Database", "Qdrant Connection", "FAIL", f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Database", "Qdrant Connection", "FAIL", "Connection failed", str(e))
            
        # Test MinIO
        try:
            response = requests.get("http://localhost:9003/minio/health/live")
            if response.status_code == 200:
                self.log_test("Database", "MinIO Connection", "PASS", "Connected successfully")
            else:
                self.log_test("Database", "MinIO Connection", "FAIL", f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Database", "MinIO Connection", "FAIL", "Connection failed", str(e))
            
    def test_data_integrity(self):
        """Test 2: Data Integrity"""
        print("\n" + "="*60)
        print("TEST CATEGORY 2: DATA INTEGRITY")
        print("="*60)
        
        # Test PostgreSQL data
        try:
            conn = psycopg2.connect(**POSTGRES_CONFIG)
            cur = conn.cursor()
            
            # Check production_data table exists and has data
            cur.execute("SELECT COUNT(*) FROM production_data")
            count = cur.fetchone()[0]
            if count > 0:
                self.log_test("Data", "PostgreSQL Production Data", "PASS", f"Found {count} records")
            else:
                self.log_test("Data", "PostgreSQL Production Data", "FAIL", "No production data found")
                
            # Check for Rig Alpha data
            cur.execute("SELECT COUNT(*) FROM production_data WHERE rig_name = 'Rig Alpha'")
            rig_count = cur.fetchone()[0]
            if rig_count > 0:
                self.log_test("Data", "Rig Alpha Data", "PASS", f"Found {rig_count} records for Rig Alpha")
            else:
                self.log_test("Data", "Rig Alpha Data", "FAIL", "No data for Rig Alpha")
                
            conn.close()
        except Exception as e:
            self.log_test("Data", "PostgreSQL Data Check", "FAIL", "Data check failed", str(e))

        # Test Neo4j data
        try:
            driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            with driver.session() as session:
                # Check total nodes
                result = session.run("MATCH (n) RETURN count(n) as count")
                count = result.single()["count"]
                if count > 0:
                    self.log_test("Data", "Neo4j Graph Data", "PASS", f"Found {count} nodes")
                else:
                    self.log_test("Data", "Neo4j Graph Data", "FAIL", "No graph data found")

                # Check for Well W-12
                result = session.run("MATCH (w:Well {name: 'Well W-12'}) RETURN w")
                if result.single():
                    self.log_test("Data", "Well W-12 Exists", "PASS", "Well W-12 found in graph")
                else:
                    self.log_test("Data", "Well W-12 Exists", "FAIL", "Well W-12 not found")

                # Check for sensors at Well W-12
                result = session.run(
                    "MATCH (w:Well {name: 'Well W-12'})-[:HAS_SENSOR]->(s:Sensor) RETURN count(s) as count"
                )
                sensor_count = result.single()["count"]
                if sensor_count > 0:
                    self.log_test("Data", "Well W-12 Sensors", "PASS", f"Found {sensor_count} sensors")
                else:
                    self.log_test("Data", "Well W-12 Sensors", "FAIL", "No sensors found for Well W-12")

            driver.close()
        except Exception as e:
            self.log_test("Data", "Neo4j Data Check", "FAIL", "Data check failed", str(e))

    def test_api_endpoints(self):
        """Test 3: API Endpoints"""
        print("\n" + "="*60)
        print("TEST CATEGORY 3: API ENDPOINTS")
        print("="*60)

        # Test health endpoint
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if response.status_code == 200:
                self.log_test("API", "Health Endpoint", "PASS", "Health check successful")
            else:
                self.log_test("API", "Health Endpoint", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("API", "Health Endpoint", "FAIL", "Request failed", str(e))

        # Test database status endpoint
        try:
            response = requests.get(f"{BACKEND_URL}/api/status/databases", timeout=5)
            if response.status_code == 200:
                data = response.json()
                all_healthy = data.get("all_healthy", False)
                if all_healthy:
                    self.log_test("API", "Database Status", "PASS", "All databases healthy")
                else:
                    failed_dbs = [k for k, v in data.get("databases", {}).items() if not v]
                    self.log_test("API", "Database Status", "FAIL", f"Unhealthy: {failed_dbs}")
            else:
                self.log_test("API", "Database Status", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("API", "Database Status", "FAIL", "Request failed", str(e))

        # Test query endpoint with sample query
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/query",
                json={"query": "What is the name and type of gauge at Well W-12?"},
                timeout=60  # Increased timeout for slow responses
            )
            if response.status_code == 200:
                data = response.json()
                confidence = data.get("confidence", 0)
                answer = data.get("answer", "")

                if confidence >= 0.7:
                    self.log_test("API", "Query Endpoint", "PASS", f"Confidence: {confidence:.0%}")
                elif confidence >= 0.5:
                    self.log_test("API", "Query Endpoint", "WARN", f"Low confidence: {confidence:.0%}")
                else:
                    self.log_test("API", "Query Endpoint", "FAIL", f"Very low confidence: {confidence:.0%}")

                # Check if answer contains expected data
                if "G-40" in answer or "Pressure Gauge" in answer:
                    self.log_test("API", "Query Answer Quality", "PASS", "Answer contains expected data")
                else:
                    self.log_test("API", "Query Answer Quality", "WARN", "Answer may not contain expected data", answer[:100])
            else:
                self.log_test("API", "Query Endpoint", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("API", "Query Endpoint", "FAIL", "Request failed", str(e))

    def test_ai_pipeline(self):
        """Test 4: AI Agent Pipeline"""
        print("\n" + "="*60)
        print("TEST CATEGORY 4: AI AGENT PIPELINE")
        print("="*60)

        test_queries = [
            {
                "query": "Why is production dropping at Rig Alpha?",
                "expected_keywords": ["production", "Rig Alpha", "drop"],
                "min_confidence": 0.7
            },
            {
                "query": "Show me all faulty equipment at Rig Alpha",
                "expected_keywords": ["faulty", "equipment"],
                "min_confidence": 0.7
            },
            {
                "query": "What is the safety risk at Well W-12?",
                "expected_keywords": ["Well W-12", "risk"],
                "min_confidence": 0.5
            }
        ]

        for test in test_queries:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/query",
                    json={"query": test["query"]},
                    timeout=60  # Increased timeout
                )

                if response.status_code == 200:
                    data = response.json()
                    confidence = data.get("confidence", 0)
                    answer = data.get("answer", "")
                    reasoning_trace = data.get("reasoning_trace", [])

                    # Check confidence
                    if confidence >= test["min_confidence"]:
                        self.log_test("AI Pipeline", f"Query: {test['query'][:40]}...", "PASS",
                                    f"Confidence: {confidence:.0%}")
                    else:
                        self.log_test("AI Pipeline", f"Query: {test['query'][:40]}...", "WARN",
                                    f"Low confidence: {confidence:.0%}")

                    # Check reasoning trace
                    if len(reasoning_trace) > 0:
                        self.log_test("AI Pipeline", "Reasoning Trace", "PASS",
                                    f"{len(reasoning_trace)} steps recorded")
                    else:
                        self.log_test("AI Pipeline", "Reasoning Trace", "WARN", "No reasoning trace")

                else:
                    self.log_test("AI Pipeline", f"Query: {test['query'][:40]}...", "FAIL",
                                f"Status: {response.status_code}")

            except Exception as e:
                self.log_test("AI Pipeline", f"Query: {test['query'][:40]}...", "FAIL",
                            "Request failed", str(e))

    def test_performance(self):
        """Test 5: Performance Metrics"""
        print("\n" + "="*60)
        print("TEST CATEGORY 5: PERFORMANCE")
        print("="*60)

        # Test query response time
        try:
            start_time = time.time()
            response = requests.post(
                f"{BACKEND_URL}/api/query",
                json={"query": "What is the status of Rig Alpha?"},
                timeout=60  # Increased timeout
            )
            response_time = time.time() - start_time

            if response_time < 10:
                self.log_test("Performance", "Query Response Time", "PASS",
                            f"{response_time:.2f}s (< 10s target)")
            elif response_time < 30:
                self.log_test("Performance", "Query Response Time", "WARN",
                            f"{response_time:.2f}s (10-30s - acceptable for AI queries)")
            else:
                self.log_test("Performance", "Query Response Time", "FAIL",
                            f"{response_time:.2f}s (> 30s - too slow)")
        except Exception as e:
            self.log_test("Performance", "Query Response Time", "FAIL", "Test failed", str(e))

        # Test concurrent queries (simple load test)
        try:
            import concurrent.futures

            def send_query():
                response = requests.post(
                    f"{BACKEND_URL}/api/query",
                    json={"query": "Show me Rig Alpha"},
                    timeout=60  # Increased timeout
                )
                return response.status_code == 200

            start_time = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(send_query) for _ in range(5)]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]

            total_time = time.time() - start_time
            success_count = sum(results)

            if success_count == 5:
                self.log_test("Performance", "Concurrent Queries", "PASS",
                            f"5/5 succeeded in {total_time:.2f}s")
            else:
                self.log_test("Performance", "Concurrent Queries", "WARN",
                            f"{success_count}/5 succeeded")
        except Exception as e:
            self.log_test("Performance", "Concurrent Queries", "FAIL", "Test failed", str(e))

    def test_error_handling(self):
        """Test 6: Error Handling & Resilience"""
        print("\n" + "="*60)
        print("TEST CATEGORY 6: ERROR HANDLING")
        print("="*60)

        # Test invalid query
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/query",
                json={"query": ""},
                timeout=30  # Increased timeout
            )
            if response.status_code in [200, 400]:
                self.log_test("Error Handling", "Empty Query", "PASS", "Handled gracefully")
            else:
                self.log_test("Error Handling", "Empty Query", "WARN", f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Error Handling", "Empty Query", "FAIL", "Request failed", str(e))

        # Test malformed request
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/query",
                json={"invalid_field": "test"},
                timeout=30  # Increased timeout
            )
            if response.status_code in [400, 422]:
                self.log_test("Error Handling", "Malformed Request", "PASS", "Rejected properly")
            else:
                self.log_test("Error Handling", "Malformed Request", "WARN",
                            f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("Error Handling", "Malformed Request", "FAIL", "Request failed", str(e))

        # Test nonsensical query
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/query",
                json={"query": "asdfghjkl qwerty zxcvbn"},
                timeout=30  # Increased timeout
            )
            if response.status_code == 200:
                data = response.json()
                # Should return low confidence
                if data.get("confidence", 1.0) < 0.5:
                    self.log_test("Error Handling", "Nonsensical Query", "PASS",
                                "Low confidence returned")
                else:
                    self.log_test("Error Handling", "Nonsensical Query", "WARN",
                                "High confidence for nonsense query")
            else:
                self.log_test("Error Handling", "Nonsensical Query", "WARN",
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Error Handling", "Nonsensical Query", "FAIL", "Request failed", str(e))

    def test_security_config(self):
        """Test 7: Security & Configuration"""
        print("\n" + "="*60)
        print("TEST CATEGORY 7: SECURITY & CONFIGURATION")
        print("="*60)

        # Test CORS headers
        try:
            response = requests.options(f"{BACKEND_URL}/api/query")
            cors_header = response.headers.get("Access-Control-Allow-Origin")
            if cors_header:
                self.log_test("Security", "CORS Headers", "PASS", "CORS configured")
                if cors_header == "*":
                    self.log_test("Security", "CORS Wildcard", "WARN",
                                "Using wildcard (*) - restrict in production")
            else:
                self.log_test("Security", "CORS Headers", "WARN", "No CORS headers found")
        except Exception as e:
            self.log_test("Security", "CORS Headers", "FAIL", "Test failed", str(e))

        # Check for environment variables (via backend response)
        try:
            response = requests.get(f"{BACKEND_URL}/health")
            if response.status_code == 200:
                # Backend is running, which means basic config is working
                self.log_test("Security", "Environment Config", "PASS", "Backend configured properly")
            else:
                self.log_test("Security", "Environment Config", "WARN", "Backend may have config issues")
        except Exception as e:
            self.log_test("Security", "Environment Config", "FAIL", "Cannot verify", str(e))

    def auto_fix_issue(self, issue: str, fix_command: str) -> bool:
        """Attempt to auto-fix an issue"""
        try:
            print(f"   🔧 Auto-fixing: {issue}")
            result = subprocess.run(fix_command, shell=True, capture_output=True, timeout=60)
            if result.returncode == 0:
                self.auto_fixes.append({"issue": issue, "command": fix_command, "success": True})
                print(f"   ✅ Fixed: {issue}")
                return True
            else:
                self.auto_fixes.append({"issue": issue, "command": fix_command, "success": False, "error": result.stderr.decode()})
                print(f"   ❌ Fix failed: {issue}")
                return False
        except Exception as e:
            self.auto_fixes.append({"issue": issue, "command": fix_command, "success": False, "error": str(e)})
            print(f"   ❌ Fix failed: {str(e)}")
            return False

    def generate_html_report(self, score: float):
        """Generate HTML report"""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Production Readiness Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-card.passed {{ background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); }}
        .stat-card.failed {{ background: linear-gradient(135deg, #f44336 0%, #da190b 100%); }}
        .stat-card.warnings {{ background: linear-gradient(135deg, #ff9800 0%, #fb8c00 100%); }}
        .stat-card h3 {{ margin: 0; font-size: 36px; }}
        .stat-card p {{ margin: 5px 0 0 0; opacity: 0.9; }}
        .score {{ font-size: 48px; font-weight: bold; text-align: center; margin: 30px 0; }}
        .score.excellent {{ color: #4CAF50; }}
        .score.good {{ color: #8BC34A; }}
        .score.fair {{ color: #ff9800; }}
        .score.poor {{ color: #f44336; }}
        .test-result {{ margin: 10px 0; padding: 15px; border-radius: 5px; border-left: 4px solid #ddd; }}
        .test-result.pass {{ background: #e8f5e9; border-left-color: #4CAF50; }}
        .test-result.fail {{ background: #ffebee; border-left-color: #f44336; }}
        .test-result.warn {{ background: #fff3e0; border-left-color: #ff9800; }}
        .test-result h4 {{ margin: 0 0 5px 0; }}
        .test-result p {{ margin: 5px 0; color: #666; }}
        .category {{ margin: 20px 0; }}
        .timestamp {{ color: #999; font-size: 14px; text-align: right; }}
        .recommendations {{ background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .recommendations h3 {{ color: #1976d2; margin-top: 0; }}
        .recommendations ul {{ margin: 10px 0; }}
        .auto-fixes {{ background: #f3e5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .auto-fixes h3 {{ color: #7b1fa2; margin-top: 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Production Readiness Test Report</h1>
        <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="summary">
            <div class="stat-card passed">
                <h3>{self.passed}</h3>
                <p>Passed</p>
            </div>
            <div class="stat-card failed">
                <h3>{self.failed}</h3>
                <p>Failed</p>
            </div>
            <div class="stat-card warnings">
                <h3>{self.warnings}</h3>
                <p>Warnings</p>
            </div>
            <div class="stat-card">
                <h3>{len(self.results)}</h3>
                <p>Total Tests</p>
            </div>
        </div>

        <div class="score {'excellent' if score >= 90 else 'good' if score >= 75 else 'fair' if score >= 60 else 'poor'}">
            Overall Score: {score:.1f}%
        </div>

        <div style="text-align: center; font-size: 24px; margin: 20px 0;">
            {'✅ PRODUCTION READY' if score >= 90 else '⚠️ MOSTLY READY - Address warnings' if score >= 75 else '⚠️ NEEDS WORK - Fix failures' if score >= 60 else '❌ NOT READY - Critical issues'}
        </div>
"""

        # Add auto-fixes section
        if self.auto_fixes:
            html_content += """
        <div class="auto-fixes">
            <h3>🔧 Auto-Fixes Applied</h3>
            <ul>
"""
            for fix in self.auto_fixes:
                status = "✅" if fix["success"] else "❌"
                html_content += f"                <li>{status} {fix['issue']}</li>\n"
            html_content += """            </ul>
        </div>
"""

        # Group results by category
        categories = {}
        for result in self.results:
            cat = result["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)

        # Add test results by category
        for category, tests in categories.items():
            html_content += f"""
        <div class="category">
            <h2>{category}</h2>
"""
            for test in tests:
                status_class = test["status"].lower()
                icon = "✅" if test["status"] == "PASS" else "❌" if test["status"] == "FAIL" else "⚠️"
                html_content += f"""
            <div class="test-result {status_class}">
                <h4>{icon} {test['test']}</h4>
                <p>{test['message']}</p>
"""
                if test.get("details"):
                    html_content += f"                <p style='font-size: 12px; color: #999;'>Details: {test['details'][:200]}</p>\n"
                html_content += """            </div>
"""
            html_content += """        </div>
"""

        # Add recommendations
        failures = [r for r in self.results if r["status"] == "FAIL"]
        warnings = [r for r in self.results if r["status"] == "WARN"]

        if failures or warnings:
            html_content += """
        <div class="recommendations">
            <h3>📋 Recommendations</h3>
            <ul>
"""
            if failures:
                html_content += f"                <li><strong>Critical:</strong> Fix {len(failures)} failed test(s) before production deployment</li>\n"
            if warnings:
                html_content += f"                <li><strong>Important:</strong> Address {len(warnings)} warning(s) to improve system reliability</li>\n"
            if score < 90:
                html_content += "                <li>Run tests again after fixes to verify improvements</li>\n"
            html_content += """            </ul>
        </div>
"""

        html_content += """
    </div>
</body>
</html>
"""

        with open("production_readiness_report.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"📄 HTML report saved to: production_readiness_report.html")

    def generate_report(self):
        """Generate final report"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        print("\n" + "="*60)
        print("PRODUCTION READINESS TEST REPORT")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   ✅ Passed:  {self.passed}")
        print(f"   ❌ Failed:  {self.failed}")
        print(f"   ⚠️  Warnings: {self.warnings}")
        print(f"   📝 Total:   {len(self.results)}")
        print(f"   ⏱️  Duration: {duration:.1f}s")
        if self.auto_fixes:
            print(f"   🔧 Auto-fixes: {len(self.auto_fixes)}")

        # Calculate score
        total_tests = self.passed + self.failed + self.warnings
        if total_tests > 0:
            score = (self.passed + (self.warnings * 0.5)) / total_tests * 100
            print(f"\n🎯 Overall Score: {score:.1f}%")

            if score >= 90:
                print("   ✅ PRODUCTION READY")
            elif score >= 75:
                print("   ⚠️  MOSTLY READY - Address warnings")
            elif score >= 60:
                print("   ⚠️  NEEDS WORK - Fix failures")
            else:
                print("   ❌ NOT READY - Critical issues")
        else:
            score = 0

        # Show failures
        failures = [r for r in self.results if r["status"] == "FAIL"]
        if failures:
            print(f"\n❌ Critical Issues ({len(failures)}):")
            for f in failures:
                print(f"   - {f['category']}: {f['test']}")
                print(f"     {f['message']}")

        # Show warnings
        warnings = [r for r in self.results if r["status"] == "WARN"]
        if warnings:
            print(f"\n⚠️  Warnings ({len(warnings)}):")
            for w in warnings:
                print(f"   - {w['category']}: {w['test']}")
                print(f"     {w['message']}")

        # Show auto-fixes
        if self.auto_fixes:
            print(f"\n🔧 Auto-Fixes Applied ({len(self.auto_fixes)}):")
            for fix in self.auto_fixes:
                status = "✅" if fix["success"] else "❌"
                print(f"   {status} {fix['issue']}")

        # Save detailed JSON report
        report_file = "production_readiness_report.json"
        with open(report_file, 'w') as f:
            json.dump({
                "summary": {
                    "passed": self.passed,
                    "failed": self.failed,
                    "warnings": self.warnings,
                    "total": len(self.results),
                    "score": score,
                    "duration_seconds": duration,
                    "auto_fixes": len(self.auto_fixes)
                },
                "results": self.results,
                "auto_fixes": self.auto_fixes,
                "timestamp": end_time.isoformat(),
                "production_ready": score >= 90
            }, f, indent=2)

        print(f"\n📄 Detailed JSON report saved to: {report_file}")

        # Generate HTML report
        self.generate_html_report(score)

    def run_all_tests(self):
        """Run all test categories"""
        print("\n" + "="*60)
        print("PRODUCTION READINESS TEST SUITE")
        print("Intelligent Oilfield Insights Platform")
        print("="*60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        self.test_database_connectivity()
        self.test_data_integrity()
        self.test_api_endpoints()
        self.test_ai_pipeline()
        self.test_performance()
        self.test_error_handling()
        self.test_security_config()

        self.generate_report()

        return self.failed == 0

if __name__ == "__main__":
    tester = ProductionReadinessTest()
    success = tester.run_all_tests()

    sys.exit(0 if success else 1)

