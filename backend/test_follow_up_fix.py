"""
Test script to verify the follow-up question fix is working
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.flexible_executor import FlexibleExecutor
from agents.reasoning import ReasoningAgent
from datetime import datetime

def test_format_results():
    """Test that format_results works correctly"""
    print("=" * 80)
    print("Testing FlexibleExecutor.format_results()")
    print("=" * 80)
    
    executor = FlexibleExecutor()
    
    # Test 1: MIN timestamp (like "When did it start?")
    results = [{"min": "2024-01-15 14:30:00"}]
    question = "When did it start?"
    
    print(f"\nTest 1: MIN timestamp")
    print(f"Results: {results}")
    print(f"Question: {question}")
    
    answer = executor.format_results(results, question)
    print(f"Answer: {answer}")
    print(f"✅ PASS" if "January" in answer or "2024" in answer else "❌ FAIL")
    
    # Test 2: AVG value
    results = [{"avg": 1234.56}]
    question = "What is the average production?"
    
    print(f"\nTest 2: AVG value")
    print(f"Results: {results}")
    print(f"Question: {question}")
    
    answer = executor.format_results(results, question)
    print(f"Answer: {answer}")
    print(f"✅ PASS" if "1,234" in answer or "1234" in answer else "❌ FAIL")
    
    # Test 3: COUNT
    results = [{"count": 42}]
    question = "How many records?"
    
    print(f"\nTest 3: COUNT")
    print(f"Results: {results}")
    print(f"Question: {question}")
    
    answer = executor.format_results(results, question)
    print(f"Answer: {answer}")
    print(f"✅ PASS" if "42" in answer else "❌ FAIL")

def test_reasoning_agent():
    """Test that ReasoningAgent uses the new formatter"""
    print("\n" + "=" * 80)
    print("Testing ReasoningAgent._summarize_sql_results()")
    print("=" * 80)
    
    agent = ReasoningAgent()
    
    # Test with MIN timestamp
    results = [{"min": "2024-01-15 14:30:00"}]
    question = "When did it start?"
    
    print(f"\nResults: {results}")
    print(f"Question: {question}")
    
    summary = agent._summarize_sql_results(results, question)
    print(f"Summary: {summary}")
    print(f"✅ PASS" if "January" in summary or "2024" in summary else "❌ FAIL")

if __name__ == "__main__":
    print("\n🧪 Testing Follow-Up Question Fix\n")
    
    try:
        test_format_results()
        test_reasoning_agent()
        
        print("\n" + "=" * 80)
        print("✅ All tests completed!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

