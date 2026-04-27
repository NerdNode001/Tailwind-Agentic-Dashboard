from crewai_tools import ScrapeWebsiteTool
from crewai.tools import tool
import yfinance as yf
from duckduckgo_search import DDGS
import json

# ── Web scrape (free, no key needed) ──────────────────────────────────────────
scrape_tool = ScrapeWebsiteTool()

# ── DuckDuckGo Search (100% FREE alternative to Serper) ────────────────────────
@tool("Web Search")
def search_tool(query: str) -> str:
    """Searches the web for a given query (e.g. recent stock news).
    Returns a list of matching results with URL, title, and snippet text."""
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No recent news found."
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Search error: {str(e)}"


# ── Yahoo Finance live data (FREE, no API key) ────────────────────────────────

@tool("Stock Data Lookup")
def stock_data_tool(ticker: str) -> str:
    """Fetch real-time stock data from Yahoo Finance for a given ticker symbol
    (e.g. NVDA, MSFT, TSLA, PLTR). Returns: current price, market cap, P/E,
    forward P/E, PEG ratio, EV/Sales, revenue growth, profit margins, beta,
    52-week range, analyst target price, recommendation, and recent news."""
    try:
        stock = yf.Ticker(ticker.upper().strip())
        info = stock.info

        # ── Core metrics ──
        data = {
            "ticker":           ticker.upper(),
            "name":             info.get("longName", "N/A"),
            "sector":           info.get("sector", "N/A"),
            "industry":         info.get("industry", "N/A"),
            "current_price":    info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
            "market_cap":       info.get("marketCap", "N/A"),
            "pe_ratio":         info.get("trailingPE", "N/A"),
            "forward_pe":       info.get("forwardPE", "N/A"),
            "peg_ratio":        info.get("pegRatio", "N/A"),
            "ev_to_revenue":    info.get("enterpriseToRevenue", "N/A"),
            "revenue_growth":   info.get("revenueGrowth", "N/A"),
            "earnings_growth":  info.get("earningsGrowth", "N/A"),
            "profit_margin":    info.get("profitMargins", "N/A"),
            "52w_high":         info.get("fiftyTwoWeekHigh", "N/A"),
            "52w_low":          info.get("fiftyTwoWeekLow", "N/A"),
            "50d_avg":          info.get("fiftyDayAverage", "N/A"),
            "200d_avg":         info.get("twoHundredDayAverage", "N/A"),
            "beta":             info.get("beta", "N/A"),
            "dividend_yield":   info.get("dividendYield", "N/A"),
            "target_mean_price": info.get("targetMeanPrice", "N/A"),
            "recommendation":   info.get("recommendationKey", "N/A"),
        }

        # ── Friendly market cap ──
        mc = data["market_cap"]
        if isinstance(mc, (int, float)):
            if mc >= 1e12:
                data["market_cap_fmt"] = f"${mc / 1e12:.2f}T"
            elif mc >= 1e9:
                data["market_cap_fmt"] = f"${mc / 1e9:.2f}B"
            else:
                data["market_cap_fmt"] = f"${mc / 1e6:.0f}M"

        # ── Recent news headlines ──
        try:
            news_items = stock.news[:5] if stock.news else []
            data["recent_news"] = [
                {"title": n.get("title", ""), "publisher": n.get("publisher", "")}
                for n in news_items
            ]
        except Exception:
            data["recent_news"] = []

        # ── Analyst recommendations ──
        try:
            recs = stock.recommendations
            if recs is not None and not recs.empty:
                latest = recs.tail(3).to_dict("records")
                data["analyst_recommendations"] = latest
            else:
                data["analyst_recommendations"] = []
        except Exception:
            data["analyst_recommendations"] = []

        return json.dumps(data, indent=2, default=str)

    except Exception as e:
        return f"Error fetching data for {ticker}: {str(e)}"