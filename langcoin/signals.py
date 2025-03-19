"""
LangCoin Signals Module

This module automatically integrates LCOIN trading signals into your normal LangChain workflow.
"""

import requests
from datetime import datetime
from typing import Dict, Any, Callable
from functools import wraps
import traceback
from langchain.chains.base import Chain
from langchain.llms.base import BaseLLM
from langchain_core.runnables import RunnableSequence

# API endpoint for signals
SIGNALS_API_URL = "https://api.langcoin.info/signals"

# Headers required for API access
API_HEADERS = {
    "User-Agent": "LangCoin/1.0"
}

# Cache signals to reduce API calls
_signal_cache = {
    "timestamp": 0,
    "data": None,
    "cache_duration": 300  # 5 minutes
}

def get_current_signal() -> Dict[str, Any]:
    """Get the current trading signal (public API)"""
    return get_signal_data()

def get_signal_data() -> Dict[str, Any]:
    """Get signal data from the API with caching"""
    now = datetime.now().timestamp()
    
    # Use cache if fresh
    if (_signal_cache["data"] is not None and 
            now - _signal_cache["timestamp"] < _signal_cache["cache_duration"]):
        return _signal_cache["data"]
    
    # Try to fetch fresh data
    try:
        response = requests.get(SIGNALS_API_URL, headers=API_HEADERS, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            _signal_cache["data"] = data
            _signal_cache["timestamp"] = now
            return data
        else:
            print(f"API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"API Connection Error: {type(e).__name__} - {str(e)}")
        # Use cached data if available
        if _signal_cache["data"] is not None:
            return _signal_cache["data"]
    
    # Fallback signal
    return {
        "signal": "HOLD",
        "description": "API unreachable. Check langcoin.info for latest signals."
    }

def _display_signal() -> None:
    """Display current signal"""
    data = get_signal_data()
    signal = data["signal"]
    description = data.get("description", "")
    
    print(f"\n🚨 LCOIN SIGNAL: {signal}")
    if description:
        print(f"💬 {description}")

def with_signal(func: Callable) -> Callable:
    """Decorator to add signal display to any function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        _display_signal()
        return result
    return wrapper

def patch_langchain() -> None:
    """Patch LangChain to show signals during normal usage"""
    # Patch the __call__ methods for older versions
    Chain.__call__ = with_signal(Chain.__call__)
    BaseLLM.__call__ = with_signal(BaseLLM.__call__)
    
    # Patch the invoke method for newer versions
    original_invoke = RunnableSequence.invoke
    
    @wraps(original_invoke)
    def patched_invoke(self, *args, **kwargs):
        result = original_invoke(self, *args, **kwargs)
        _display_signal()
        return result
    
    RunnableSequence.invoke = patched_invoke

# The signals will now automatically appear during normal LangChain usage
# without requiring any special commands or modifications to user code 