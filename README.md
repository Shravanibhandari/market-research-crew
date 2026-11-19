# Multi-Agent Market Research with CrewAI
- **Repository**: [Insert URL]

## Setup
1. `python -m venv .venv` then activate it (Windows: `.venv\Scripts\activate`, Mac/Linux: `source .venv/bin/activate`)
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in OPENAI_API_KEY and TAVILY_API_KEY
4. Run: `python main.py --query "Tech Sector Q3 Analysis"`
5. Test: `pytest`

Outputs: `output/market_report.pdf`, `output/market_report.md`, `benchmarks.json`.

## Layout
- `crew/` agents/tasks (`build_crew.py`), tools, pandas logic, PDF builder, benchmarks
- `tests/` pytest tests
- `data/` sample CSV (fallback)
