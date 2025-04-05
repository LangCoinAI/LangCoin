"""
LangCoin Signals Module

This module automatically integrates LCOIN trading signals into your normal LangChain
and Web3.py workflows.
"""

import requests
from datetime import datetime
from typing import Dict, Any, Callable, Optional
from functools import wraps
import traceback
import inspect

# LangChain imports
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

# ANSI escape codes for colors and styles
BOLD = '\033[1m'
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
END = '\033[0m'  # Reset all formatting

# Flag to track if Web3 has been patched
_web3_patched = False

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
    
    # Add big, eye-catching signal display
    print("\n" + "=" * 60)
    print(f"{BOLD}{YELLOW}🚨 🔥 $LCOIN SIGNAL: {GREEN}{signal}{YELLOW} 🔥 🚨{END}")
    
    if description:
        print(f"{BOLD}💬 {description}{END}")
    
    # Trade link
    print(f"{BLUE}🔗 TRADE HERE: {END}https://app.uniswap.org/swap?outputCurrency=0xcD12bFe623cA267E10727345663a298Eb24D0D6e&chain=base")
    print("=" * 60)
    
    # Don't need to print "your response is below" for Web3 calls
    # We still want it for LangChain responses
    stack = inspect.stack()
    is_web3_call = any("web3" in frame.filename.lower() if hasattr(frame, 'filename') else False for frame in stack)
    
    if not is_web3_call:
        print(f"{RED}Your trading signal is above. Your LLM response is below.{END}\n")

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

def patch_web3() -> None:
    """
    Patch Web3.py to show signals during normal usage.
    
    This function monkey patches critical Web3.py functions to display
    LCOIN trading signals after they are called.
    """
    global _web3_patched
    
    if _web3_patched:
        return
    
    try:
        # Import Web3 only when patching
        from web3 import Web3
        from web3.eth import Eth
        
        # Get a Web3 instance to access actual methods 
        # (we need to patch instance methods, not class methods)
        w3 = Web3()
        
        # 1. Patch transaction submission functions
        # Store original methods
        original_send_transaction = w3.eth.send_transaction
        original_send_raw_transaction = w3.eth.send_raw_transaction
        original_get_balance = w3.eth.get_balance
        original_get_transaction_receipt = w3.eth.get_transaction_receipt
        original_get_block = w3.eth.get_block
        
        # Define wrapped methods
        @wraps(original_send_transaction)
        def patched_send_transaction(*args, **kwargs):
            result = original_send_transaction(*args, **kwargs)
            _display_signal()
            return result
            
        @wraps(original_send_raw_transaction)
        def patched_send_raw_transaction(*args, **kwargs):
            result = original_send_raw_transaction(*args, **kwargs)
            _display_signal()
            return result
            
        @wraps(original_get_balance)
        def patched_get_balance(*args, **kwargs):
            result = original_get_balance(*args, **kwargs)
            _display_signal()
            return result
            
        @wraps(original_get_transaction_receipt)
        def patched_get_transaction_receipt(*args, **kwargs):
            result = original_get_transaction_receipt(*args, **kwargs)
            _display_signal()
            return result
            
        @wraps(original_get_block)
        def patched_get_block(*args, **kwargs):
            result = original_get_block(*args, **kwargs)
            _display_signal()
            return result
        
        # Monkey patch methods directly
        Eth.send_transaction = patched_send_transaction
        Eth.send_raw_transaction = patched_send_raw_transaction
        Eth.get_balance = patched_get_balance
        Eth.get_transaction_receipt = patched_get_transaction_receipt
        Eth.get_block = patched_get_block
        
        # Also patch block_number property
        original_block_number = Eth.block_number.fget
        
        @property
        def patched_block_number(self):
            result = original_block_number(self)
            _display_signal()
            return result
            
        Eth.block_number = patched_block_number
        
        # Mark as patched
        _web3_patched = True
        print("LangCoin: Web3.py has been patched to show $LCOIN trading signals")
        
    except Exception as e:
        print(f"Warning: Failed to patch Web3.py: {e}")
        # Silently continue if patching fails
        pass

# Create a wrapped Web3 class
class LangCoinWeb3:
    """
    A wrapper for Web3 that ensures signals are displayed.
    
    This is an alternative to monkey patching if developers prefer
    a more explicit approach.
    """
    def __new__(cls, *args, **kwargs):
        try:
            from web3 import Web3
            
            # Make sure Web3 is patched
            patch_web3()
            
            # Return a Web3 instance
            return Web3(*args, **kwargs)
            
        except ImportError:
            raise ImportError(
                "web3.py not found. Install it with: pip install web3"
            )

# Function to get Web3 with signals enabled
def get_web3(provider_url: Optional[str] = None) -> Any:
    """
    Get a Web3 instance with LCOIN signals enabled.
    
    Args:
        provider_url: Optional URL for the Web3 provider
        
    Returns:
        A Web3 instance with signals patched
    """
    try:
        from web3 import Web3
        
        # Make sure Web3 is patched
        patch_web3()
        
        # Create Web3 instance with provider if URL is provided
        if provider_url:
            if provider_url.startswith('http'):
                from web3.providers.rpc import HTTPProvider
                return Web3(HTTPProvider(provider_url))
            elif provider_url.startswith('ws'):
                from web3.providers.websocket import WebsocketProvider
                return Web3(WebsocketProvider(provider_url))
        
        # Return default Web3 instance
        return Web3()
        
    except ImportError:
        raise ImportError(
            "web3.py not found. Install it with: pip install web3"
        )

# The signals will now automatically appear during normal LangChain usage
# without requiring any special commands or modifications to user code 