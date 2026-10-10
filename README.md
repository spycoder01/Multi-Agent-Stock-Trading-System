# Multi-Agent Stock Trading System

An AI-powered stock analysis system that combines market data from Yahoo Finance with financial document question answering using Retrieval-Augmented Generation (RAG). Built with CrewAI and Gemini, the system analyses a stock and generates a BUY, SELL, or HOLD recommendation.

**Current workflow:** Market Research → Financial Analysis → Trading Recommendation

**Planned enhancement:** Add a Risk/Validator Agent to independently review the recommendation before presenting the final result.

## Overview

This project uses a multi-agent architecture to support stock analysis by combining two information sources:

- **Market data:** Retrieves stock price information, daily price movements, trading volume, market capitalization, and the 52-week price range using Yahoo Finance.
- **Financial documents:** Optionally retrieves relevant information from company financial reports using a hybrid RAG pipeline.
- **AI-powered analysis:** Uses a Financial Market Analyst to interpret the available evidence and a Strategic Stock Trader to generate a trading recommendation.
- **Risk validation — planned:** A dedicated Risk/Validator Agent will review the recommendation, assess potential risks, and check whether the decision is supported by the available evidence.

The project currently generates research-based recommendations; it does not execute trades through a brokerage account.

## Key Features

- **Multi-agent orchestration:** Uses CrewAI to coordinate specialised agents and sequential tasks.
- **Market data integration:** Retrieves stock information through Yahoo Finance using `yfinance`.
- **Optional Financial RAG:** Supports querying financial information from a user-provided PDF.
- **Hybrid information retrieval:** Combines FAISS semantic search with BM25 keyword-based retrieval.
- **CrossEncoder reranking:** Reranks retrieved document chunks based on query relevance.
- **Context-grounded responses:** Uses Gemini to answer financial document questions using retrieved context.
- **Flexible workflow:** Runs with market data alone or with market data supplemented by a financial report.
- **Risk/Validator Agent — planned:** Will provide an additional review stage before the final recommendation.

## System Architecture

### Current Workflow

```text
User Input (Stock Ticker + Optional Financial PDF)
                         |
                         v
                  Create Crew (CrewAI)
                         |
             +-----------+-----------+
             |                       |
             v                       v
      Yahoo Finance Tool      Financial RAG (Optional)
             |                       |
             |                PDF Text Extraction
             |                       |
             |                 Text Chunking
             |                       |
             |              FAISS + BM25 Retrieval
             |                       |
             |                CrossEncoder Reranking
             |                       |
             |                  Gemini Answer
             |                       |
             +-----------+-----------+
                         |
                         v
              Financial Market Analyst
                         |
                         v
               Strategic Stock Trader
                         |
                         v
              BUY / SELL / HOLD
                         |
                         v
                 Final Output
```

### Planned Workflow — Risk/Validator Agent

```text
Strategic Stock Trader
          |
          v
   Risk/Validator Agent
          |
          v
 Review Recommendation
          |
     +----+----+
     |         |
     v         v
  Valid     Issues Found
     |         |
     v         v
Final Output  Flag for Review
```

**Note:** The current implementation includes the Analyst and Trader agents. The Risk/Validator Agent is planned and will be integrated after its implementation and testing.


## Detailed Workflow

### 1. User Input

The application starts from `main.py` and requests:

- A stock ticker, such as `AAPL` or `BMW.DE`.
- An optional path to a company financial report in PDF format.

If no PDF is provided, the application runs without Financial RAG. If a PDF is supplied, the application attempts to initialise the document retrieval pipeline.

### 2. Market Research

The custom Stock Research Tool uses `yfinance` to retrieve available information for the selected stock, including:

- Current price
- Previous closing price
- Daily price change and percentage change
- Trading volume
- Market capitalization
- 52-week high and low

The retrieved information is formatted for the Analyst Agent to interpret. Data availability depends on Yahoo Finance and the selected ticker.

### 3. Financial Document RAG — Optional

When a financial PDF is supplied, the application makes the Financial Document Research Tool available to the Analyst Agent.

The RAG pipeline follows these steps:

1. **Document loading:** `PyPDFLoader` extracts text and page metadata from the PDF.
2. **Text splitting:** `RecursiveCharacterTextSplitter` splits the document into chunks of 1,000 characters with 200 characters of overlap.
3. **Embedding generation:** `sentence-transformers/all-MiniLM-L6-v2` generates embeddings for semantic retrieval.
4. **Hybrid retrieval:** FAISS retrieves up to 15 semantic candidates, while BM25 retrieves up to 15 keyword-based candidates.
5. **Candidate merging:** The retrieved candidates are combined and duplicate text chunks are removed.
6. **Reranking:** `cross-encoder/ms-marco-MiniLM-L-6-v2` scores the query against the candidates and ranks them by relevance.
7. **Context selection:** The top three chunks are selected for answer generation.
8. **Answer generation:** Gemini receives the question and retrieved context and is instructed to answer from that context.

This pipeline allows the Analyst Agent to query relevant financial information from a supplied report without manually reading the entire document for every question.

### 4. Financial Market Analyst

The Analyst Agent uses Gemini and has access to the Stock Research Tool and, when enabled, the Financial Document Research Tool.

Its responsibilities include:

- Interpreting the available market data.
- Examining price movements and trading activity.
- Identifying relevant financial information from the supplied report.
- Summarising potential opportunities, risks, and uncertainties.
- Preparing an analysis for the Trader Agent.

The Analyst produces the analysis but does not make the final BUY, SELL, or HOLD recommendation.

### 5. Strategic Stock Trader

The Trader Agent receives the Analyst's output through the sequential CrewAI workflow.

It evaluates the available findings and generates a BUY, SELL, or HOLD recommendation with supporting reasoning.

The Trader Agent is responsible for the final recommendation in the current implementation. It does not independently call the market-data or Financial RAG tools.

### 6. Risk/Validator Agent — Planned

A dedicated Risk/Validator Agent will be added as a separate stage after the Trader Agent.

Its intended responsibilities are to:

- Review the proposed recommendation and its supporting evidence.
- Identify conflicting signals or material risks.
- Flag missing, unreliable, or insufficient evidence.
- Check that the reasoning supports the proposed recommendation.
- Return a validation result or flag the recommendation for further review.

This agent is planned and is **not yet part of the current executable workflow**. Its implementation, validation rules, and final output format remain future work.

### 7. Final Output

In the current version, the application prints the Trader Agent's recommendation and reasoning in the terminal.

After the Risk/Validator Agent is implemented, the intended output will include the validation result before the recommendation is presented as reviewed.

## Financial RAG Retrieval Strategy

The project uses hybrid retrieval to improve the relevance of financial information retrieved from a report.

| Component | Role |
|---|---|
| FAISS | Semantic similarity search over document embeddings |
| BM25 | Keyword-based document retrieval |
| Candidate merging | Combines results and removes duplicate text chunks |
| CrossEncoder | Reranks candidates according to query-document relevance |
| Gemini | Generates an answer using the retrieved context |

FAISS and BM25 retrieve candidate chunks using different methods. The CrossEncoder then reranks those candidates before the most relevant chunks are passed to Gemini.

## Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Multi-agent framework | CrewAI |
| LLM | Google Gemini |
| Market data | Yahoo Finance, `yfinance` |
| RAG framework and document processing | LangChain, PyPDF |
| Vector retrieval | FAISS |
| Keyword retrieval | BM25, `rank-bm25` |
| Embeddings | Sentence Transformers, `all-MiniLM-L6-v2` |
| Reranking | CrossEncoder, `ms-marco-MiniLM-L-6-v2` |
| Configuration | `python-dotenv` |

## Project Structure

```text
Multi-Agent-Stock-Trading-System/
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
│   ├── stock_tool.py
│   └── create_rag_tool.py
│
├── rag/
│   ├── document_loader.py
│   ├── hybrid_retriever.py
│   └── rag_pipeline.py
│
├── documents/
│   └── (local financial PDFs)
│
├── crew.py
├── main.py
├── test_rag.py
├── requirements.txt
├── .gitignore
└── README.md
```

The `documents/` directory is intended for local financial PDFs and should not contain committed reports unless you have the right to redistribute them. The directory and its PDFs may not appear in a fresh clone.

## Installation and Setup

### Prerequisites

- Python 3.12
- A Google Gemini API key
- Internet access for market-data retrieval, Gemini API calls, and downloading model files when needed

### 1. Clone the repository

```bash
git clone https://github.com/spycoder01/Multi-Agent-Stock-Trading-System.git
cd Multi-Agent-Stock-Trading-System
```

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own API key. Keep `.env` private and never commit it to GitHub.

### 5. Run the application

```bash
python main.py
```

Enter a stock ticker when prompted. To use Financial RAG, provide the path to an existing financial PDF when asked. Otherwise, leave the PDF path blank to run the market-data-only workflow.

**Note:** The first RAG run may take additional time because embedding and reranking models may need to be downloaded and loaded.

## Testing

The repository includes `test_rag.py` for testing the Financial RAG pipeline separately from the full CrewAI workflow.

Recommended checks:

- Test a financial question whose answer is present in the PDF.
- Test a question whose answer is not present in the PDF.
- Test a valid ticker with no PDF.
- Test a valid ticker with a financial PDF.
- Test an invalid PDF path.
- Test the system's behaviour when market data or Gemini is unavailable.

A successful standalone RAG test does not guarantee that the complete multi-agent workflow will finish successfully. The full workflow should also be tested with and without a PDF.

## Current Limitations

- The Risk/Validator Agent is planned but not implemented.
- The system produces recommendations; it does not execute trades or connect to a brokerage account.
- Recommendation quality and profitability have not been established through a formal backtest.
- Market-data availability depends on Yahoo Finance and the selected ticker.
- Financial RAG answers depend on PDF text extraction, retrieval quality, and the supplied document's coverage.
- Gemini API quotas, rate limits, or service errors may interrupt analysis.
- Retrieved financial document context is sent to Gemini for answer generation; the current version is not a fully local LLM pipeline.
- The current recommendation should not be treated as guaranteed or personalised financial advice.

## Future Improvements

- Implement the Risk/Validator Agent as a separate stage in the CrewAI workflow.
- Define validation criteria for evidence quality, conflicting signals, and recommendation consistency.
- Improve handling of failed RAG calls so error messages cannot be mistaken for financial evidence.
- Add structured outputs for the recommendation and validation result.
- Evaluate retrieval quality and recommendation performance using documented test cases and historical data.
- Add a dashboard for viewing market data, retrieved evidence, agent analysis, and final recommendations.

## Disclaimer

This project is intended for educational and research purposes. Its outputs are AI-generated analyses and recommendations, not guarantees of future stock performance. Always independently verify financial information and consider the risks before making investment decisions.
