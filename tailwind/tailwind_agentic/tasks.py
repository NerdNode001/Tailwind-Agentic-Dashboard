from crewai import Task
from .agents import researcher, analyst, risk_officer, portfolio_constructor, validator

# Tasks run sequentially. Each agent receives the output of the previous task
# as context, so they build on each other naturally.

task1 = Task(
    description="""
    Universe scan for {topic} as of April 2026.
    List 8-10 emerging public stocks (market cap $10B–$200B).
    For each stock use the stock_data tool to include real YTD performance and growth estimates.
    Output EXACTLY as a markdown numbered list formatted strictly like: "1. [TICKER]: [Short summary of tailwinds]"
    """,
    agent=researcher,
    expected_output="A markdown numbered list of 8-10 [TICKER]s with a short thesis summary for each."
)

task2 = Task(
    description="""
    Take the list of stocks from the previous research.
    For each stock, evaluate structural tailwinds vs headwinds. 
    Rule: Tailwinds must systemically obliterate headwinds. If any single structural headwind threatens the company, remove it entirely.
    Output EXACTLY 5 passed stocks formatted as a markdown list: "- [TICKER]: BUY (Reason)"
    Any stock that fails must be omitted or marked as "- [TICKER]: WALK (Reason)".
    """,
    agent=analyst,
    expected_output="A strict markdown list evaluating the exact top 5 stocks, explicitly stating BUY or WALK with short rationale."
)

task3 = Task(
    description="""
    For the stocks that passed the Tailwind test (BUY), map their 12-24 month catalysts.
    Run a scenario analysis (Base Case vs Bear Case) relying strictly on the hard EV/Sales and PEG metrics pulled from Yahoo Finance.
    Do NOT invent or simulate numbers. Use real multiples.
    Output: qualitative risk-adjusted upside %, and a final conviction level (High/Medium/Low) per stock.
    """,
    agent=risk_officer,
    expected_output="Base vs Bear scenario mapping based on real PEG/EV multiples, with High/Medium/Low conviction ratings."
)

task4 = Task(
    description="""
    For the stocks with High or Medium conviction, build portfolio allocation logic.
    Target 5-10% allocation per position. Check pairwise correlation and liquidity.
    Apply the Mogul Rules: max 20% drawdown tolerance, minimum 3-year hold.
    Output: final watchlist with recommended position sizes.
    """,
    agent=portfolio_constructor,
    expected_output="Final watchlist with position sizes and Mogul Rules compliance check."
)

task5 = Task(
    description="""
    Review all previous findings from the research, scoring, stress test, and allocation steps.
    Validate the logic and flag any inconsistencies or risks that were underweighted.
    Write a final 'Mogul Approval Memo' — a concise, executive-level summary with:
    - Final approved stock list
    - Key tailwinds driving each pick
    - Position sizes
    - Risk watchpoints
    - Overall verdict: Approved / Conditional / Rejected
    """,
    agent=validator,
    expected_output="Mogul Approval Memo: final stock list, tailwinds, sizes, risk watchpoints, and overall verdict."
)