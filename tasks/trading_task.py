from crewai import Task

from agents.trader_agent import trader_agent


trading_task = Task(
    description="""
    Review the stock analysis provided by the Financial Market Analyst.

    Based only on the analyst's findings, evaluate:

    - Current market condition
    - Price movement
    - Trading activity
    - Overall market trend
    - Potential risks
    - Potential opportunities

    Then make one final recommendation:

    BUY
    SELL
    or
    HOLD

    Clearly explain the reasoning behind your decision.
    """,

    expected_output="""
    A concise trading recommendation containing:

    1. Summary of the analyst's findings
    2. Key positive signals
    3. Key risks
    4. Final recommendation: BUY, SELL, or HOLD
    5. Short explanation supporting the recommendation
    """,

    agent=trader_agent
)