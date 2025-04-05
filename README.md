# LangCoin

[![PyPI version](https://img.shields.io/pypi/v/langcoin.svg)](https://pypi.org/project/langcoin/)
[![Python Versions](https://img.shields.io/pypi/pyversions/langcoin.svg)](https://pypi.org/project/langcoin/)

It's a LangChain and Web3.py wrapper. Automatic $LCOIN trading signals in both your LangChain and Web3.py workflows.

## Links

- 🌐 Website: [langcoin.info](https://langcoin.info)
- 📝 Contract: `0xcD12bFe623cA267E10727345663a298Eb24D0D6e`
- 🐦 Twitter: [@LangCoinAI](https://x.com/LangCoinAI)

## Install

```bash
pip install langcoin
```## Usage with LangChain

Just use LangChain normally - you'll automatically see $LCOIN trading signals:

```python
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import langcoin  # This automatically patches LangChain

# Initialize the LLM and prompt
llm = OpenAI()
prompt = PromptTemplate.from_template("What is the current state of {topic}?")

# Use LangChain as usual - signals appear automatically 
result = (prompt | llm).invoke({"topic": "AI in finance"})

# 🚨 🔥 $LCOIN SIGNAL: BUY 🚨
# 💬 Smart money accumulating.
```

## Usage with Web3.py

We also integrate with Web3.py - just import and see $LCOIN signals during blockchain operations:

```python
# Option 1: Import both separately (automatic integration)
import langcoin  # This patches Web3.py when it's imported
from web3 import Web3

# Connect to a network
w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))

# Do normal Web3 operations - signals appear automatically
balance = w3.eth.get_balance("0xcD12bFe623cA267E10727345663a298Eb24D0D6e")
latest_block = w3.eth.get_block('latest')

# 🚨 🔥 $LCOIN SIGNAL: BUY 🚨
# 💬 Bullish pattern forming on higher timeframes.
```

```python
# Option 2: Use our helper functions
from langcoin import get_web3

# Get Web3 instance with signals enabled
w3 = get_web3("https://mainnet.base.org")

# Now use Web3 normally with signals
# ... 
```

## Features

- **Zero Configuration**: Just import the package and start seeing signals
- **Automatic Patching**: Works with both LangChain and Web3.py
- **Cached Results**: Minimizes API calls by caching signals
- **Fallback Handling**: Provides graceful fallbacks if the API is unavailable

## Signal Types

LangCoin signals are simple and actionable:

- **BUY**: Favorable entry conditions detected
- **SELL**: Consider taking profits or reducing exposure
- **HOLD**: No significant change warranted at this time


