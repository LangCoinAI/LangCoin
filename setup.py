#!/usr/bin/env python
"""Setup script for LangCoin."""

from setuptools import setup, find_packages

setup(
    name="langcoin",
    version="0.2.0",
    description="Automatic LCOIN trading signals in your LangChain and Web3 workflows",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=["langcoin"],  # Point to our langcoin package
    install_requires=[
        "langchain",  # Core dependency
        "langchain-community>=0.0.10",  # For LLMs and other components
        "langchain-openai>=0.0.1",  # For OpenAI integration
        "requests>=2.28.0",  # For API calls
        "openai>=1.0.0",  # Required for OpenAI integration
        "pydantic>=2.0.0",  # Required for data validation
        "aiohttp>=3.8.0",  # Required for async HTTP requests
        "numpy>=1.20.0",  # Common dependency for ML/AI tasks
        "web3>=6.0.0",  # For Web3 integration
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 