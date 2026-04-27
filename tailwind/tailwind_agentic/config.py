from pathlib import Path
from dotenv import load_dotenv
from crewai import LLM

# Explicit path ensures .env is found regardless of CWD (critical for cloud deploys)
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# Powers ALL 5 agents.
# groq/llama-3.1-8b-instant is the replacement for the deprecated llama3-8b-8192.
# Needs GROQ_API_KEY set in .env (get one free at https://console.groq.com)
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    temperature=0.3,   # Low = more consistent, factual answers
)