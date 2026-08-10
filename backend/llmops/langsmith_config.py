"""
LangSmith Configuration for LLM Observability
Automatically traces all LangChain/LangGraph operations
"""
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def setup_langsmith() -> bool:
    """
    Configure LangSmith tracing for LLM observability
    
    Returns:
        bool: True if LangSmith is configured, False otherwise
    """
    
    # Check if LangSmith is enabled
    tracing_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    
    if not tracing_enabled:
        logger.info("LangSmith tracing is disabled. Set LANGCHAIN_TRACING_V2=true to enable.")
        return False
    
    # Check for API key
    api_key = os.getenv("LANGCHAIN_API_KEY")
    if not api_key or api_key == "your-langsmith-api-key-here":
        logger.warning("""
        ⚠️  LangSmith API key not configured!
        
        To enable LLM observability:
        1. Sign up at https://smith.langchain.com (free tier available)
        2. Get your API key from Settings → API Keys
        3. Add to .env: LANGCHAIN_API_KEY=your-key-here
        4. Restart the backend
        
        Benefits:
        - 🔍 Trace every LLM call and agent decision
        - 💰 Track costs per query
        - 🐛 Debug hallucinations and errors
        - 📊 Monitor performance over time
        """)
        return False
    
    # LangSmith is configured
    project = os.getenv("LANGCHAIN_PROJECT", "oilfield-intelligence")
    endpoint = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    
    logger.info(f"""
    ✅ LangSmith LLMOps Enabled!
    
    Project: {project}
    Endpoint: {endpoint}
    
    View traces at: https://smith.langchain.com/o/default/projects/p/{project}
    
    All LLM calls, agent decisions, and reasoning steps will be automatically traced.
    """)
    
    return True


def get_langsmith_url(run_id: Optional[str] = None) -> Optional[str]:
    """
    Get LangSmith URL for a specific run
    
    Args:
        run_id: Optional run ID to link to specific trace
        
    Returns:
        URL to LangSmith dashboard or None if not configured
    """
    if not os.getenv("LANGCHAIN_TRACING_V2") == "true":
        return None
    
    project = os.getenv("LANGCHAIN_PROJECT", "oilfield-intelligence")
    base_url = f"https://smith.langchain.com/o/default/projects/p/{project}"
    
    if run_id:
        return f"{base_url}/r/{run_id}"
    
    return base_url

