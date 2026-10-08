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


def create_analyst_agent(rag_tool=None):

    tools = [get_stock_data]

    if rag_tool:
        tools.append(rag_tool)

    analyst_agent = Agent(
        role="Financial Market Analyst",

        goal=(
            "Analyze the stock using available market data and, "
            "when available, company financial information."
        ),

        backstory=(
            "You are an experienced financial market analyst. "
            "You analyze market data carefully and identify important "
            "signals, trends, risks, and opportunities. "
            "When a company financial document is available, "
            "use it to supplement the market analysis. "
            "If no financial document is available, rely only on "
            "the available market data."
        ),

        tools=tools,

        llm=gemini_llm,

        verbose=True
    )

    return analyst_agent