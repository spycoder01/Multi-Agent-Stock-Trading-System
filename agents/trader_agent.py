import os
from dotenv import load_dotenv
from crewai import Agent, LLM

load_dotenv()


gemini_llm = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)


trader_agent = Agent(
    role="Strategic Stock Trader",

    goal=(
        "Evaluate the financial analysis provided by the Analyst Agent "
        "and make a reasoned BUY, SELL, or HOLD recommendation."
    ),

    backstory=(
        "You are an experienced stock trader who specializes in "
        "evaluating market analysis and making disciplined trading "
        "decisions. You consider both opportunities and risks before "
        "making a recommendation."
    ),

    llm=gemini_llm,

    verbose=True
)