from crewai import Agent, Crew, Task, LLM
from crewai_tools import ScrapeWebsiteTool
from crewai.tools import tool
print("crewai imports: OK")
print("crewai_tools imports: OK")
import fastapi, uvicorn, jinja2, dotenv
print("web framework imports: OK")
import yfinance
print("yfinance import: OK")
import duckduckgo_search
print("duckduckgo_search import: OK")
import json
print("json import: OK")
print()
print("All checks passed!")
print("Run the server with:  .venv\\Scripts\\uvicorn main:app --reload")
