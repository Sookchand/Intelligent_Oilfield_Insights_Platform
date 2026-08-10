"""
Unit Tests for Query Routing Fixes
Tests both the faulty equipment fix and forecast query fix
"""
import sys
import os
import unittest

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from agents.parser import QueryParser


class TestFaultyEquipmentQueryFix(unittest.TestCase):
    """Test suite for faulty equipment query routing fix"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = QueryParser()
    
    def test_faulty_equipment_intent_detection(self):
        """Test that faulty equipment queries are correctly identified"""
        query = "Show me all faulty equipment at Rig Alpha"
        result = self.parser.parse(query)
        
        self.assertEqual(result['intent'], 'equipment_fault_analysis',
                        "Should detect equipment_fault_analysis intent")
    
    def test_faulty_equipment_entity_extraction(self):
        """Test that rig entities are correctly extracted"""
        query = "Show me all faulty equipment at Rig Alpha"
        result = self.parser.parse(query)
        
        self.assertIn('rigs', result['entities'],
                     "Should extract rig entity")
        self.assertEqual(result['entities']['rigs'], ['Rig Alpha'],
                        "Should extract correct rig name")
    
    def test_faulty_equipment_plan_creation(self):
        """Test that correct execution plan is created"""
        query = "Show me all faulty equipment at Rig Alpha"
        result = self.parser.parse(query)
        
        expected_plan = ['sql_retriever', 'graph_retriever', 'reasoning']
        self.assertEqual(result['plan'], expected_plan,
                        "Should create correct multi-agent plan")
    
    def test_broken_equipment_synonym(self):
        """Test that 'broken' is recognized as fault keyword"""
        query = "Find broken equipment at Rig Alpha"
        result = self.parser.parse(query)
        
        self.assertEqual(result['intent'], 'equipment_fault_analysis',
                        "Should recognize 'broken' as fault keyword")
    
    def test_failed_equipment_synonym(self):
        """Test that 'failed' is recognized as fault keyword"""
        query = "Show failed sensors at Well W-12"
        result = self.parser.parse(query)
        
        self.assertEqual(result['intent'], 'equipment_fault_analysis',
                        "Should recognize 'failed' as fault keyword")
    
    def test_list_query_not_misclassified(self):
        """Test that normal list queries are not misclassified"""
        query = "List all wells"
        result = self.parser.parse(query)
        
        self.assertEqual(result['intent'], 'list_wells',
                        "Should not misclassify normal list queries")
    
    def test_priority_over_list_keywords(self):
        """Test that fault keywords have priority over list keywords"""
        query = "Show all faulty equipment"  # Has both 'show all' and 'faulty'
        result = self.parser.parse(query)
        
        self.assertEqual(result['intent'], 'equipment_fault_analysis',
                        "Fault keywords should have priority over list keywords")


class TestForecastQueryFix(unittest.TestCase):
    """Test suite for forecast query routing fix"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = QueryParser()
    
    def test_forecast_intent_detection(self):
        """Test that forecast queries are correctly identified"""
        query = "Predict production for next week"
        result = self.parser.parse(query)
        
        self.assertEqual(result['intent'], 'production_forecast',
                        "Should detect production_forecast intent")
    
    def test_forecast_plan_creation(self):
        """Test that correct execution plan is created for forecasts"""
        query = "Predict production for next week"
        result = self.parser.parse(query)
        
        self.assertIn('sql_retriever', result['plan'],
                     "Forecast should use SQL retriever")
    
    def test_forecast_keyword_variations(self):
        """Test different forecast keyword variations"""
        test_cases = [
            "Predict production for next week",
            "Forecast production trends",
            "What will production be next month",
            "Project future production"
        ]
        
        for query in test_cases:
            with self.subTest(query=query):
                result = self.parser.parse(query)
                self.assertEqual(result['intent'], 'production_forecast',
                               f"Should detect forecast intent for: {query}")
    
    def test_forecast_without_entities(self):
        """Test that forecast works without specific entities"""
        query = "Predict production for next week"
        result = self.parser.parse(query)
        
        # Forecast queries don't require specific entities
        self.assertEqual(result['intent'], 'production_forecast',
                        "Should work without specific rig/well entities")


class TestQueryRoutingIntegration(unittest.TestCase):
    """Integration tests for query routing"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = QueryParser()
    
    def test_multiple_query_types(self):
        """Test that different query types are routed correctly"""
        test_cases = [
            {
                'query': 'Show me all faulty equipment at Rig Alpha',
                'expected_intent': 'equipment_fault_analysis',
                'description': 'Fault analysis query'
            },
            {
                'query': 'Predict production for next week',
                'expected_intent': 'production_forecast',
                'description': 'Forecast query'
            },
            {
                'query': 'List all wells',
                'expected_intent': 'list_wells',
                'description': 'List query'
            },
            {
                'query': 'Why is production dropping at Rig Alpha?',
                'expected_intent': 'production_analysis',
                'description': 'Production analysis query'
            }
        ]
        
        for test_case in test_cases:
            with self.subTest(description=test_case['description']):
                result = self.parser.parse(test_case['query'])
                self.assertEqual(result['intent'], test_case['expected_intent'],
                               f"{test_case['description']} should be routed correctly")


class TestFollowUpQueryExtraction(unittest.TestCase):
    """Test suite for follow-up query extraction"""

    def setUp(self):
        """Set up test fixtures"""
        # Import here to avoid circular imports
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
        from graph_engine import OilfieldOrchestrator
        self.orchestrator = OilfieldOrchestrator()

    def test_follow_up_query_extraction(self):
        """Test that follow-up queries are extracted correctly"""
        # Simulate frontend follow-up format
        contextual_query = """Previous context: Found 1 faulty equipment at Rig Alpha

Follow-up question: When did it start?"""

        # The orchestrator should extract just "When did it start?"
        # We can't easily test the internal extraction, but we can verify
        # that the query is processed differently than the full context

        # This is more of an integration test - just verify it doesn't crash
        try:
            # Mock the parser to verify it receives the extracted query
            original_parse = self.orchestrator.parser.parse
            extracted_query = None

            def mock_parse(query):
                nonlocal extracted_query
                extracted_query = query
                return original_parse(query)

            self.orchestrator.parser.parse = mock_parse

            # Process the contextual query
            # Note: This will fail if databases aren't available, but that's ok
            # We just want to verify the extraction happens
            try:
                self.orchestrator.process_query(contextual_query)
            except:
                pass  # Ignore database errors

            # Verify the parser received the extracted query, not the full context
            self.assertIsNotNone(extracted_query)
            self.assertEqual(extracted_query.lower(), "when did it start?")
            self.assertNotIn("Previous context:", extracted_query)
            self.assertNotIn("Follow-up question:", extracted_query)

        finally:
            # Restore original parse method
            self.orchestrator.parser.parse = original_parse

    def test_regular_query_not_affected(self):
        """Test that regular queries are not affected by extraction logic"""
        regular_query = "Show me all faulty equipment at Rig Alpha"

        # Mock the parser to capture what it receives
        original_parse = self.orchestrator.parser.parse
        extracted_query = None

        def mock_parse(query):
            nonlocal extracted_query
            extracted_query = query
            return original_parse(query)

        self.orchestrator.parser.parse = mock_parse

        try:
            # Process regular query
            try:
                self.orchestrator.process_query(regular_query)
            except:
                pass  # Ignore database errors

            # Verify the parser received the original query unchanged
            self.assertEqual(extracted_query, regular_query)

        finally:
            # Restore original parse method
            self.orchestrator.parser.parse = original_parse


def run_tests():
    """Run all tests and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestFaultyEquipmentQueryFix))
    suite.addTests(loader.loadTestsFromTestCase(TestForecastQueryFix))
    suite.addTests(loader.loadTestsFromTestCase(TestQueryRoutingIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestFollowUpQueryExtraction))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

