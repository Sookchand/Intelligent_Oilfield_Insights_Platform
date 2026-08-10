"""
End-to-End System Tests
Tests the complete system including database connections
"""
import sys
import os
import unittest
import requests
import time

# Configuration
BACKEND_URL = "http://localhost:8000"
TIMEOUT = 30  # seconds


class TestSystemHealth(unittest.TestCase):
    """Test system health and connectivity"""
    
    def test_backend_is_running(self):
        """Test that backend server is accessible"""
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            self.assertEqual(response.status_code, 200,
                           "Backend should be accessible")
        except requests.exceptions.ConnectionError:
            self.fail("Backend is not running. Start with: cd backend && python main.py")
    
    def test_database_connections(self):
        """Test that all databases are connected"""
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            data = response.json()
            
            self.assertEqual(data.get('postgres'), 'connected',
                           "PostgreSQL should be connected")
            self.assertEqual(data.get('neo4j'), 'connected',
                           "Neo4j should be connected")
            self.assertEqual(data.get('qdrant'), 'connected',
                           "Qdrant should be connected")
            self.assertEqual(data.get('minio'), 'connected',
                           "MinIO should be connected")
        except Exception as e:
            self.fail(f"Database health check failed: {e}")


class TestFaultyEquipmentEndToEnd(unittest.TestCase):
    """End-to-end tests for faulty equipment query"""
    
    def test_faulty_equipment_query_confidence(self):
        """Test that faulty equipment query returns high confidence"""
        query = "Show me all faulty equipment at Rig Alpha"
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/query",
                json={"query": query},
                timeout=TIMEOUT
            )
            
            self.assertEqual(response.status_code, 200,
                           "Query should return 200 OK")
            
            data = response.json()
            
            # Check confidence is high (>= 80%)
            confidence = data.get('confidence', 0)
            self.assertGreaterEqual(confidence, 0.80,
                                  f"Confidence should be >= 80%, got {confidence*100:.1f}%")
            
            # Check answer exists
            self.assertIn('answer', data,
                         "Response should contain answer")
            self.assertTrue(len(data['answer']) > 0,
                          "Answer should not be empty")
            
        except requests.exceptions.Timeout:
            self.fail("Query timed out after 30 seconds")
        except Exception as e:
            self.fail(f"Query failed: {e}")
    
    def test_faulty_equipment_uses_correct_agents(self):
        """Test that faulty equipment query uses correct agent workflow"""
        query = "Show me all faulty equipment at Rig Alpha"
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/query",
                json={"query": query},
                timeout=TIMEOUT
            )
            
            data = response.json()
            reasoning_trace = data.get('reasoning_trace', [])
            
            # Check that Parser, SQL, Graph, and Reasoning agents were used
            agent_names = [step.get('agent') for step in reasoning_trace]
            
            self.assertIn('Parser', agent_names,
                         "Should use Parser agent")
            self.assertIn('SQL', agent_names,
                         "Should use SQL agent")
            self.assertIn('Graph', agent_names,
                         "Should use Graph agent")
            self.assertIn('Reasoning', agent_names,
                         "Should use Reasoning agent")
            
        except Exception as e:
            self.fail(f"Query failed: {e}")
    
    def test_faulty_equipment_finds_data(self):
        """Test that faulty equipment query finds actual faulty equipment"""
        query = "Show me all faulty equipment at Rig Alpha"
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/query",
                json={"query": query},
                timeout=TIMEOUT
            )
            
            data = response.json()
            answer = data.get('answer', '').lower()
            
            # Should mention faulty equipment
            self.assertTrue(
                'faulty' in answer or 'fault' in answer or 'gauge' in answer,
                "Answer should mention faulty equipment"
            )
            
        except Exception as e:
            self.fail(f"Query failed: {e}")


class TestForecastEndToEnd(unittest.TestCase):
    """End-to-end tests for forecast query"""
    
    def test_forecast_query_confidence(self):
        """Test that forecast query returns high confidence"""
        query = "Predict production for next week"
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/query",
                json={"query": query},
                timeout=TIMEOUT
            )
            
            self.assertEqual(response.status_code, 200,
                           "Query should return 200 OK")
            
            data = response.json()
            
            # Check confidence is high (>= 80%)
            confidence = data.get('confidence', 0)
            self.assertGreaterEqual(confidence, 0.80,
                                  f"Confidence should be >= 80%, got {confidence*100:.1f}%")
            
        except requests.exceptions.Timeout:
            self.fail("Query timed out after 30 seconds")
        except Exception as e:
            self.fail(f"Query failed: {e}")
    
    def test_forecast_uses_forecasting_agent(self):
        """Test that forecast query uses Forecasting agent"""
        query = "Predict production for next week"
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/query",
                json={"query": query},
                timeout=TIMEOUT
            )
            
            data = response.json()
            reasoning_trace = data.get('reasoning_trace', [])
            agent_names = [step.get('agent') for step in reasoning_trace]
            
            self.assertIn('Forecasting', agent_names,
                         "Should use Forecasting agent")
            
        except Exception as e:
            self.fail(f"Query failed: {e}")
    
    def test_forecast_returns_numeric_value(self):
        """Test that forecast returns a numeric forecast value"""
        query = "Predict production for next week"
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/query",
                json={"query": query},
                timeout=TIMEOUT
            )
            
            data = response.json()
            answer = data.get('answer', '')
            
            # Should contain a number (forecast value)
            import re
            numbers = re.findall(r'\d+\.?\d*', answer)
            self.assertTrue(len(numbers) > 0,
                          "Answer should contain numeric forecast value")
            
        except Exception as e:
            self.fail(f"Query failed: {e}")


def run_tests():
    """Run all end-to-end tests"""
    print("\n" + "="*80)
    print("END-TO-END SYSTEM TESTS")
    print("="*80)
    print("\nPrerequisites:")
    print("1. Backend must be running: cd backend && python main.py")
    print("2. All databases must be running: docker-compose up -d")
    print("\nStarting tests...\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestSystemHealth))
    suite.addTests(loader.loadTestsFromTestCase(TestFaultyEquipmentEndToEnd))
    suite.addTests(loader.loadTestsFromTestCase(TestForecastEndToEnd))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

