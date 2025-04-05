"""
LangCoin: Automatic LCOIN trading signals in your LangChain and Web3 workflows

This package automatically shows LCOIN trading signals while you use LangChain and Web3.py.
No special commands or modifications needed - just use these libraries as usual.
"""

# Import all signal functions from our consolidated signals module
from .signals import (
    get_current_signal,
    patch_langchain,
    patch_web3,
    LangCoinWeb3,
    get_web3
)

# Automatically patch LangChain
patch_langchain()

# Try to patch Web3 if it's installed
try:
    patch_web3()
except Exception:
    # Silently continue if Web3 isn't available
    # It will be patched when the user imports web3 if they have it
    pass

__all__ = [
    'get_current_signal',
    'LangCoinWeb3',
    'get_web3',
] 