"""Custom CrewAI tools built with the @tool decorator."""
import os
import requests
from crewai.tools import tool
from crew.analysis import summary_markdown

OUTPUT_DIR = "output"
METRICS_CSV = os.path.join(OUTPUT_DIR, "metrics.csv")


@tool("Web Search and Scrape")
def web_search_scrape(query: str) -> str:
    """Searches the web with Tavily for the query and returns short text from the top results."""
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        return "ERROR: TAVILY_API_KEY is not set."
    resp = requests.post(
        "https://api.tavily.com/search",
        json={"api_key": key, "query": query, "max_results": 2,
              "include_raw_content": False},
        timeout=60,
    )
    resp.raise_for_status()
    parts = []
    for r in resp.json().get("results", []):
        text = (r.get("content") or "")[:600]
        parts.append(f"SOURCE: {r['url']}\n{text}")
    return "\n\n---\n\n".join(parts) or "No results found."


@tool("Save Metrics CSV")
def save_metrics_csv(csv_text: str) -> str:
    """Saves CSV text (header row + data rows, numeric columns) to output/metrics.csv."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(METRICS_CSV, "w", encoding="utf-8") as f:
        f.write(csv_text.strip() + "\n")
    return f"Saved to {METRICS_CSV}"


@tool("Calculate Financial Metrics")
def calculate_financial_metrics(csv_path: str) -> str:
    """Loads a CSV of company metrics and returns summary statistics as a Markdown table."""
    try:
        return summary_markdown(csv_path)
    except Exception as e:  # return error text so the agent can recover
        return f"ERROR: {e}"

