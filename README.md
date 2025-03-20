# LangCoin

[![PyPI version](https://img.shields.io/pypi/v/langcoin.svg)](https://pypi.org/project/langcoin/)
[![Python Versions](https://img.shields.io/pypi/pyversions/langcoin.svg)](https://pypi.org/project/langcoin/)

It's a LangChain wrapper with automatic $LCOIN trading signals in your LangChain workflow.

## Links

- 🌐 Website: [langcoin.info](https://langcoin.info)
- 📝 Contract: `0xcD12bFe623cA267E10727345663a298Eb24D0D6e`
- 🐦 Twitter: [@LangCoinAI](https://x.com/LangCoinAI)

## Install

```bash
pip install langcoin
```

## Usage

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

# 🚨 $LCOIN SIGNAL: BUY
# 💬 Smart money accumulating.
```

## Features

- **Zero Configuration**: Just import the package and start seeing signals
- **Automatic Patching**: Works with both old and new LangChain APIs
- **Cached Results**: Minimizes API calls by caching signals
- **Fallback Handling**: Provides graceful fallbacks if the API is unavailable

## Signal Types

LangCoin signals are simple and actionable:

- **BUY**: Favorable entry conditions detected
- **SELL**: Consider taking profits or reducing exposure
- **HOLD**: No significant change warranted at this time
