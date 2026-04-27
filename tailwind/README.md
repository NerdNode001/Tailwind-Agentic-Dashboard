# Tailwind Agentic 🚀

An autonomous AI agent swarming system designed to perform deep, data-driven equity research. By leveraging the CrewAI framework and Llama3-8B, this system scans the market, filters out structural headwinds, and strictly builds conviction around stocks with asymmetrical structural tailwinds.

It utilizes a team of 5 distinct AI personas working sequentially, relying entirely on hard logic and real-time financial API endpoints rather than LLM calculation hallucinations.

## Key Architecture

### 🧠 The Intelligence Engine
- **LLM Core:** Groq-hosted Llama3-8B (`groq/llama3-8b-8192`) 
- **Web Search Engine:** DuckDuckGo native community scraper (100% free, zero API restrictions)
- **Financial Data Layer:** Direct integration with Yahoo Finance (`yfinance`) for real-time multiples, EV/Sales, and PEG bounding.

### 🕵️ The 5-Agent Pipeline
1. **Scout (Market Researcher):** Scans the universe and identifies 8-10 momentum targets based on real-time internet narrative mapping.
2. **Tailwind Finder (Scoring Analyst):** A ruthless gatekeeper. It throws out any stock that faces a structural, thesis-breaking headwind. Only the top 5 survive.
3. **Risk Analyst (Stress Tester):** Translates narrative into valuation. Maps 12-24 month catalysts and builds Base vs. Bear scenarios grounded strictly in Yahoo Finance valuation floors.
4. **Evaluator (Portfolio Constructor):** Sizes positions ensuring no overarching allocation risk, with built-in maximum drawdown tolerance.
5. **Reporter (Independent Validator):** Runs the final executive review and prints the "Approval Memo".

## 🛠️ Stack & Technologies
- **Backend:** FastAPI, Python 3.10+
- **Frontend:** Vanilla JS, Tailwind CSS v4, dynamic markdown rendering
- **Agent Framework:** CrewAI 
- **Environment Management:** python-dotenv

## ⚙️ Quickstart Deployment

1. **Clone the repository && Initialize Environment:**
```bash
git clone https://github.com/YOUR_USERNAME/tailwind-agentic.git
cd tailwind-agentic
python -m venv .venv
.venv\Scripts\activate
```

2. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure the Brain:**
Create a `.env` file in the root directory and securely add your Groq API key:
```env
GROQ_API_KEY=gsk_your_api_key_here
```

4. **Launch the Engine:**
```bash
uvicorn main:app --reload
```
Navigate to `http://127.0.0.1:8000` to interact with the Swarm UI and deploy the crew.

## 🤝 Contributing
This is an open-research quantitative experiment. Fork the repository and run wild with the agent instructions. Pull requests are heavily welcomed for new Custom Tools (particularly for scraping SEC 10-K filings or tracking insider flows).

## 📄 License
MIT License
