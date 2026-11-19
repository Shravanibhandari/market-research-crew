import os
from crewai import Agent, Task, Crew, Process, LLM
from crew.tools import web_search_scrape, save_metrics_csv, calculate_financial_metrics


def build_crew(query: str, bench) -> Crew:
    # Model comes from .env (LLM_MODEL). Works with Groq, OpenAI, etc.
    llm = LLM(
        model=os.getenv("LLM_MODEL", "groq/llama-3.3-70b-versatile"),
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2,
    )

    researcher = Agent(
        role="Market Research Specialist",
        goal="Search the web, locate financial data and scrape company metrics.",
        backstory="Experienced analyst who finds reliable, recent market data.",
        tools=[web_search_scrape, save_metrics_csv],
        llm=llm, allow_delegation=False, verbose=True)
    analyst = Agent(
        role="Financial Data Analyst",
        goal="Parse data with Pandas, compute averages and verify numeric consistency.",
        backstory="Quantitative analyst who double-checks every number.",
        tools=[calculate_financial_metrics],
        llm=llm, allow_delegation=False, verbose=True)
    writer = Agent(
        role="Technical Reports Writer",
        goal="Synthesize findings into a clear, structured report.",
        backstory="Writes concise business reports for executives.",
        llm=llm, allow_delegation=False, verbose=True)

    # No agent is fixed on tasks: the manager LLM delegates dynamically.
    t1 = Task(
        description=(f"Research: '{query}'. Search for revenue_billion, net_income_billion, "
                     "pe_ratio and growth_pct for 3 relevant companies. Save them as CSV "
                     "text (header: company,revenue_billion,net_income_billion,pe_ratio,"
                     "growth_pct) to output/metrics.csv using the Save Metrics CSV tool."),
        expected_output="Confirmation that output/metrics.csv was saved plus key sources.")
    t2 = Task(
        description=("Use the Calculate Financial Metrics tool on output/metrics.csv, then "
                     "check the numbers are consistent and explain what they mean."),
        expected_output="Markdown summary statistics table plus a short consistency check.")
    t3 = Task(
        description=(f"Write a report on '{query}' using the research and analysis. Use "
                     "Markdown with sections: # Title, ## Executive Summary, ## Key Findings, "
                     "## Analysis, ## Conclusion. Do not include tables."),
        expected_output="A complete Markdown report.")

    return Crew(
        agents=[researcher, analyst, writer],
        tasks=[t1, t2, t3],
        process=Process.hierarchical,
        manager_llm=llm,
        max_rpm=4, task_callback=bench.log_task,
        step_callback=bench.log_step,
        verbose=True)
