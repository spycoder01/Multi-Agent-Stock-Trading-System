from crewai import Crew, Process

from agents.analyst_agent import analyst_agent
from agents.trader_agent import trader_agent

from tasks.analysis_task import analysis_task
from tasks.trading_task import trading_task


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