from crewai import Task


def create_analysis_task(analyst_agent):

    return Task(

        description="""
        Analyze the stock {stock_symbol}.

        Use the Stock Research Tool to retrieve the latest
        available market information.

        Analyze:

        - Current price
        - Daily price movement
        - Trading volume
        - Market capitalization
        - 52-week high and low
        - Overall short-term market condition

        A company financial document is optional.

        If a Financial Document Research Tool is available,
        use it to retrieve relevant information from the
        provided company financial document.

        If the Financial Document Research Tool is not available,
        perform the analysis using market data only.

        Combine all available information into a concise
        financial analysis.

        Do not make the final BUY, SELL, or HOLD decision.
        """,

        expected_output="""
        A concise financial analysis containing:

        1. Current market data
        2. Key market observations
        3. Financial document insights, if available
        4. Short-term market outlook
        5. Important risks or concerns

        Clearly indicate when financial document information
        is unavailable.

        Do not provide a final BUY, SELL, or HOLD recommendation.
        """,

        agent=analyst_agent
    )