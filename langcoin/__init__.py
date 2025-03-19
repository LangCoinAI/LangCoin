"""
LangCoin: Automatic LCOIN trading signals in your LangChain workflow

This package automatically shows LCOIN trading signals while you use LangChain normally.
No special commands or modifications needed - just use LangChain as usual.
"""

# Import and apply our signal patches
from .signals import patch_langchain
patch_langchain() 