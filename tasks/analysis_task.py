from crewai import Task

from agents.analyst_agent import analyst_agent


analysis_task = Task(
    description="""
    Analyze the stock {stock_symbol}.

    Use the Stock Research Tool to retrieve the latest available
    market information.

    Analyze:
    - Current price
    - Daily price movement
    - Trading volume
    - Market capitalization
    - 52-week high and low
    - Overall short-term market condition

    Provide a concise analysis that can be passed to a Trader Agent.
    Do not make the final BUY, SELL, or HOLD decision.
    """,

    expected_output="""
    A concise financial analysis containing:
    1. Current market data
    2. Key observations
    3. Short-term market outlook
    4. Important risks or concerns

    Do not provide a final BUY, SELL, or HOLD recommendation.
    """,

    agent=analyst_agent
)