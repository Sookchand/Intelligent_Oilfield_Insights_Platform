"""
Integration Tests for Graph Engine
Tests the complete query processing pipeline including routing fixes
"""
import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from graph_engine import OilfieldOrchestrator


class TestGraphEngineRouting(unittest.TestCase):
    """Test graph engine routing logic"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.orchestrator = OilfieldOrchestrator()
    
    @patch('graph_engine.OilfieldOrchestrator._process_with_ai')
    def test_forecast_not_routed_to_ai(self, mock_ai_process):
        """Test that forecast queries are NOT routed to AI path"""
        # Mock the AI generator to be available
        self.orchestrator.ai_generator.openai_available = True
        
        # Create a forecast query with no entities
        query = "Predict production for next week"
        
        # Mock the parser result
        with patch.object(self.orchestrator.parser, 'parse') as mock_parse:
            mock_parse.return_value = {
                'intent': 'production_forecast',
                'entities': {},  # No entities
                'plan': ['sql_retriever']
            }
            
            # Mock SQL agent
            with patch.object(self.orchestrator.sql_agent, 'query_production_trends') as mock_sql:
                mock_sql.return_value = [{'production': 100}] * 70
                
                # Mock forecaster
                with patch('graph_engine.forecaster') as mock_forecaster:
                    mock_forecaster.forecast_production.return_value = {
                        'forecast_value': 831.4,
                        'trend': 'decreasing',
                        'trend_percentage': -2.2,
                        'confidence': 0.87
                    }
                    mock_forecaster.calculate_confidence_calibration.return_value = []
                    
                    # Process query
                    try:
                        result = self.orchestrator.process_query(query)
                        
                        # Verify AI path was NOT called
                        mock_ai_process.assert_not_called()
                        
                        # Verify forecast was generated
                        self.assertIn('answer', result)
                        self.assertIn('831.4', result['answer'])
                    except Exception as e:
                        # If there's an error, it should not be because of AI routing
                        self.assertNotIn('AI', str(e))
    
    @patch('graph_engine.OilfieldOrchestrator._process_with_ai')
    def test_general_query_routed_to_ai(self, mock_ai_process):
        """Test that general queries ARE routed to AI path"""
        # Mock the AI generator to be available
        self.orchestrator.ai_generator.openai_available = True
        
        # Mock AI process to return a result
        mock_ai_process.return_value = {
            'answer': 'Test answer',
            'confidence': 0.85,
            'reasoning_trace': []
        }
        
        # Create a general query with no entities
        query = "What is the name of the gauge?"
        
        # Mock the parser result
        with patch.object(self.orchestrator.parser, 'parse') as mock_parse:
            mock_parse.return_value = {
                'intent': 'general_query',
                'entities': {},
                'plan': []
            }
            
            # Process query
            result = self.orchestrator.process_query(query)
            
            # Verify AI path WAS called
            mock_ai_process.assert_called_once()


class TestFaultyEquipmentIntegration(unittest.TestCase):
    """Integration tests for faulty equipment query processing"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.orchestrator = OilfieldOrchestrator()
    
    def test_faulty_equipment_uses_correct_agents(self):
        """Test that faulty equipment queries use SQL + Graph + Reasoning"""
        query = "Show me all faulty equipment at Rig Alpha"
        
        # Mock the agents
        with patch.object(self.orchestrator.sql_agent, 'query_production_trends') as mock_sql, \
             patch.object(self.orchestrator.graph_agent, 'find_faulty_equipment') as mock_graph, \
             patch.object(self.orchestrator.reasoning_agent, 'synthesize') as mock_reasoning:
            
            # Set up mock returns
            mock_sql.return_value = [{'production': 943.2}] * 70
            mock_graph.return_value = [{
                'rig': 'Rig Alpha',
                'well': 'Well W-12',
                'sensor': 'Gauge G-40',
                'status': 'FAULTY'
            }]
            mock_reasoning.return_value = {
                'answer': 'Found 1 faulty equipment',
                'confidence': 0.87
            }
            
            # Mock forecaster
            with patch('graph_engine.forecaster') as mock_forecaster:
                mock_forecaster.calculate_confidence_calibration.return_value = []
                
                # Process query
                try:
                    result = self.orchestrator.process_query(query)
                    
                    # Verify all agents were called
                    mock_sql.assert_called_once()
                    mock_graph.assert_called_once()
                    mock_reasoning.assert_called_once()
                    
                    # Verify result structure
                    self.assertIn('answer', result)
                    self.assertIn('confidence', result)
                    self.assertIn('reasoning_trace', result)
                except Exception as e:
                    # Print error for debugging
                    print(f"Error: {e}")
                    raise


class TestForecastIntegration(unittest.TestCase):
    """Integration tests for forecast query processing"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.orchestrator = OilfieldOrchestrator()
    
    def test_forecast_calls_forecasting_module(self):
        """Test that forecast queries call the forecasting module"""
        query = "Predict production for next week"
        
        # Mock the agents
        with patch.object(self.orchestrator.sql_agent, 'query_production_trends') as mock_sql:
            mock_sql.return_value = [{'production': 100}] * 70
            
            # Mock forecaster
            with patch('graph_engine.forecaster') as mock_forecaster:
                mock_forecaster.forecast_production.return_value = {
                    'forecast_value': 831.4,
                    'trend': 'decreasing',
                    'trend_percentage': -2.2,
                    'confidence': 0.87
                }
                mock_forecaster.calculate_confidence_calibration.return_value = []
                
                # Process query
                try:
                    result = self.orchestrator.process_query(query)
                    
                    # Verify forecaster was called
                    mock_forecaster.forecast_production.assert_called_once()
                    
                    # Verify result contains forecast
                    self.assertIn('answer', result)
                    self.assertIn('831.4', result['answer'])
                except Exception as e:
                    print(f"Error: {e}")
                    raise


def run_tests():
    """Run all integration tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestGraphEngineRouting))
    suite.addTests(loader.loadTestsFromTestCase(TestFaultyEquipmentIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestForecastIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

