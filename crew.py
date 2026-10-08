from crewai import Crew, Process

from agents.analyst_agent import create_analyst_agent
from agents.trader_agent import trader_agent

from tasks.analysis_task import create_analysis_task
from tasks.trading_task import trading_task

from tools.create_rag_tool import create_financial_rag_tool


def create_crew(pdf_path=""):

    # Create optional RAG tool
    rag_tool = create_financial_rag_tool(pdf_path)

    # Create Analyst with or without RAG
    analyst_agent = create_analyst_agent(
        rag_tool=rag_tool
    )

    # Create analysis task for this Analyst
    analysis_task = create_analysis_task(
        analyst_agent
    )

    crew = Crew(
        agents=[
            analyst_agent,
            trader_agent
        ],

        tasks=[
            analysis_task,
            trading_task
        ],

        process=Process.sequential,

        verbose=True
    )

    return crew