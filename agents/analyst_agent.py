import os
from dotenv import load_dotenv
from crewai import Agent, LLM

from tools.stock_tool import get_stock_data

load_dotenv()


gemini_llm = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)


analyst_agent = Agent(
    role="Financial Market Analyst",

    goal=(
        "Analyze stock market data and provide a clear, "
        "fact-based assessment of the stock's current market condition."
    ),

    backstory=(
        "You are an experienced financial market analyst. "
        "You analyze market data carefully, identify trends and "
        "important signals, and provide concise insights that can "
        "help another agent make a trading decision."
    ),

    tools=[get_stock_data],

    llm=gemini_llm,

    verbose=True
)