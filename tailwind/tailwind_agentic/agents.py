from crewai import Agent
from .config import llm
from .tools import search_tool, scrape_tool, stock_data_tool

researcher = Agent(
    role="Senior Market Researcher",
    goal="Scan universe and map initial tailwinds/headwinds with April 2026 data",
    backstory="Victor Langford's 35-year veteran researcher. Ruthless on data.",
    llm=llm,
    tools=[search_tool, scrape_tool, stock_data_tool],
    verbose=True
)

analyst = Agent(
    role="Tailwind/Headwind Scoring Analyst",
    goal="Qualitatively evaluate tailwinds vs headwinds. Tailwinds must systemically dwarf headwinds. If ANY structural headwind exists that could ruin the thesis, reject it.",
    backstory="Cold-blooded analyst who looks for asymmetrical upside. Rejects stocks ruthlessly if the story breaks under pressure.",
    llm=llm,
    tools=[search_tool, stock_data_tool],
    verbose=True
)

risk_officer = Agent(
    role="Catalyst & Valuation Stress Tester",
    goal="Run Base vs Bear scenario analysis relying STRICTLY on hard EV/Sales and PEG metrics pulled from Yahoo Finance.",
    backstory="The guy who survived every crash since 1987. Doesn't guess — builds narrative models around real valuation floors.",
    llm=llm,
    tools=[stock_data_tool],
    verbose=True
)

portfolio_constructor = Agent(
    role="Portfolio Fit & Risk Overlay Specialist",
    goal="Build 5-10% allocation logic with drawdown rules",
    backstory="Managed $3B+ hedge fund. Sleep-at-night sizing only.",
    llm=llm,
    verbose=True
)

validator = Agent(
    role="Independent Mogul Validator",
    goal="Re-run entire framework from scratch and give final approval memo",
    backstory="Victor Langford himself doing the final gut check.",
    llm=llm,
    verbose=True
)