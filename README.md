# Multi-AI Agent Trader

An LLM-powered multi-agent system for stock market analysis and trading recommendations using **CrewAI, Google Gemini, and Yahoo Finance**.

The V1 system uses two specialized AI agents: a **Financial Analyst Agent** that retrieves and analyzes live market information, and a **Trader Agent** that evaluates the analysis and generates a **BUY, SELL, or HOLD** recommendation.

---

## Architecture

```text
                         User
                           │
                           │ Stock Symbol
                           ▼
                  ┌─────────────────┐
                  │  Analyst Agent  │
                  │                 │
                  │   Gemini LLM    │
                  └────────┬────────┘
                           │
                           │ Uses Tool
                           ▼
                  ┌─────────────────┐
                  │ Stock Research  │
                  │      Tool       │
                  └────────┬────────┘
                           │
                           ▼
                    Yahoo Finance
                           │
                           ▼
                     Market Data
                           │
                           ▼
                  Analyst's Report
                           │
                           ▼
                  ┌─────────────────┐
                  │   Trader Agent  │
                  │                 │
                  │   Gemini LLM    │
                  └────────┬────────┘
                           │
                           ▼
                    BUY / SELL / HOLD
```

---

## How It Works

The system follows a sequential multi-agent workflow:

### 1. User Input

The user provides a stock ticker such as:

```text
AAPL
```

or an Indian stock:

```text
RELIANCE.NS
```

### 2. Analyst Agent

The Financial Analyst Agent uses a custom Yahoo Finance tool to retrieve available market information, including:

* Current price
* Previous closing price
* Daily price change
* Trading volume
* Market capitalization
* 52-week high
* 52-week low

Gemini then analyzes the retrieved information and produces a concise market assessment.

### 3. Trader Agent

The Trader Agent receives the Analyst Agent's output and evaluates:

* Current market condition
* Price movement
* Market trend
* Positive signals
* Potential risks
* Potential opportunities

It then generates a final:

```text
BUY
SELL
or
HOLD
```

recommendation with supporting reasoning.

---

## Key Features

* **Multi-Agent Architecture** — Separates market analysis and trading decision-making into specialized agents.
* **Real-Time Market Data** — Retrieves stock information through Yahoo Finance.
* **LLM-Powered Analysis** — Uses Google Gemini for financial reasoning and interpretation.
* **Sequential Agent Workflow** — Analyst output is passed to the Trader Agent for final evaluation.
* **Multiple Market Support** — Supports ticker formats available through Yahoo Finance, including US and Indian stocks.
* **Tool-Enabled Agent** — The Analyst Agent can interact with an external data source through a custom CrewAI tool.

---

## Tech Stack

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| **Python 3.12**   | Core programming language       |
| **CrewAI**        | Multi-agent orchestration       |
| **Google Gemini** | Large Language Model            |
| **yfinance**      | Stock market data               |
| **python-dotenv** | Environment variable management |
| **Git & GitHub**  | Version control                 |

---

## Project Structure

```text
Multi-AI-Agent-Trader/
│
├── agents/
│   ├── analyst_agent.py
│   └── trader_agent.py
│
├── tasks/
│   ├── analysis_task.py
│   └── trading_task.py
│
├── tools/
│   └── stock_tool.py
│
├── crew.py
├── main.py
├── requirements.txt
├── .env
└── .gitignore
```

### `agents/`

Contains the specialized AI agents.

* `analyst_agent.py` — Defines the Financial Market Analyst.
* `trader_agent.py` — Defines the Strategic Stock Trader.

### `tasks/`

Defines the responsibilities assigned to each agent.

* `analysis_task.py` — Task for analyzing market information.
* `trading_task.py` — Task for generating the final trading recommendation.

### `tools/`

Contains external tools used by the agents.

* `stock_tool.py` — Retrieves stock market information using Yahoo Finance.

### `crew.py`

Initializes the CrewAI crew and defines the sequential execution of the agents and tasks.

### `main.py`

Application entry point that accepts a stock symbol and runs the complete workflow.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/multi-ai-agent-trader.git
cd multi-ai-agent-trader
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Setup

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The API key is loaded using `python-dotenv`.

**Never commit your `.env` file or expose your API key publicly.**

---

## Running the Project

Run the application from the project root:

```bash
python main.py
```

Enter a stock ticker when prompted:

```text
Enter stock symbol (e.g., AAPL or RELIANCE.NS): AAPL
```

The system will then execute:

```text
Stock Symbol
     ↓
Analyst Agent
     ↓
Yahoo Finance Tool
     ↓
Market Data
     ↓
Analyst Report
     ↓
Trader Agent
     ↓
BUY / SELL / HOLD
```

---

## Example Workflow

For:

```text
AAPL
```

the system retrieves market information and passes it to the Analyst Agent.

The Analyst produces observations such as:

```text
Current price and daily movement
Trading activity
52-week price range
Overall market condition
Potential risks
```

The Trader Agent then evaluates the analysis and produces a recommendation such as:

```text
Recommendation: BUY

Reason:
The available market indicators show positive short-term
momentum with favorable price movement, although market
volatility remains a risk.
```

*The actual output depends on the latest available market data and the Gemini model's analysis.*

---

## Agent Responsibilities

### Financial Market Analyst

**Role:** Market researcher and analyst

**Responsibilities:**

* Retrieve market data using the Yahoo Finance tool
* Analyze current market conditions
* Identify relevant market signals
* Highlight potential risks
* Provide an objective analysis to the Trader Agent

### Strategic Stock Trader

**Role:** Decision-making agent

**Responsibilities:**

* Evaluate the Analyst Agent's report
* Consider potential opportunities and risks
* Make a BUY, SELL, or HOLD recommendation
* Explain the reasoning behind the decision

---

## Why a Multi-Agent Architecture?

Instead of asking a single LLM to perform the entire workflow, the project separates responsibilities between specialized agents.

```text
Single Agent:

Market Data → Analysis → Decision
                  │
                 LLM
```

The V1 architecture separates these responsibilities:

```text
Market Data
     ↓
Analyst Agent
     ↓
Analysis
     ↓
Trader Agent
     ↓
Decision
```

This separation makes the system easier to understand, extend, and maintain.

---

## Current Limitations

V1 is intentionally designed as a lightweight proof of concept.

Current limitations include:

* Uses a limited set of market indicators.
* Does not perform advanced technical analysis.
* Does not retrieve financial news.
* Does not analyze company financial statements.
* Does not include a financial-document RAG pipeline.
* Does not execute real trades.
* Trading recommendations are generated by an LLM and should not be treated as financial advice.
* No historical backtesting or quantitative performance evaluation is included in V1.

---

## Future Improvements

Planned improvements for future versions include:

### V2 — Expanded Multi-Agent Analysis

Add specialized agents for:

* Technical analysis
* Fundamental analysis
* Financial news analysis
* Risk assessment

### V3 — Financial RAG

Integrate company documents such as:

* Annual reports
* Earnings reports
* Financial statements
* Investor presentations

This would allow the agents to combine real-time market data with company-specific financial information.

### V4 — Interactive Dashboard

Add a Streamlit interface with:

* Stock price charts
* Market indicators
* Agent analysis
* Trading recommendation
* Risk summary

### V5 — Backtesting & Evaluation

Evaluate recommendations against historical market data using:

* Historical backtesting
* Strategy returns
* Maximum drawdown
* Sharpe ratio
* Win rate

---

## Disclaimer

This project is intended for **educational and research purposes only**.

The BUY, SELL, or HOLD recommendations generated by the system are produced by an AI model and should not be considered professional financial advice. The project does not execute real trades or manage financial assets.

---

## Author

**Abhisek Gupta**

GitHub: [spycoder01](https://github.com/spycoder01)
