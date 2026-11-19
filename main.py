import argparse
import os
import time
from dotenv import load_dotenv

load_dotenv()

import pandas as pd
from crew.analysis import compute_summary
from crew.benchmark import Benchmark
from crew.build_crew import build_crew
from crew.pdf_report import build_pdf

OUT = "output"


def fallback_report(query: str, csv: str) -> str:
    """Used only if the LLM crew fails (e.g. rate limits). Built from the CSV data."""
    df = pd.read_csv(csv)
    s = compute_summary(csv)
    col = s.columns[0]
    top = df.loc[df[col].idxmax()].iloc[0]
    return (
        f"# {query}\n"
        "## Executive Summary\n"
        f"This report summarises {len(df)} companies using the metrics in the dataset. "
        "**Note:** it was generated in fallback mode because the LLM crew did not finish.\n"
        "## Key Findings\n"
        f"- Average {col}: {s.loc['mean', col]:.2f}\n"
        f"- Minimum {col}: {s.loc['min', col]:.2f}\n"
        f"- Maximum {col}: {s.loc['max', col]:.2f} ({top})\n"
        "## Analysis\n"
        f"The standard deviation of {col} is {s.loc['std', col]:.2f}, "
        "which shows how widely companies differ. See the statistics table below.\n"
        "## Conclusion\n"
        "Further qualitative research is recommended before drawing investment conclusions.\n"
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--query", default="Tech Sector Q3 Analysis")
    args = p.parse_args()
    os.makedirs(OUT, exist_ok=True)

    bench = Benchmark(args.query)
    print("Manager LLM initializing hierarchical workflow...")
    report_md = None
    for attempt in (1, 2):
        try:
            result = build_crew(args.query, bench).kickoff()
            report_md = str(getattr(result, "raw", result))
            break
        except Exception as e:
            print(f"Crew attempt {attempt} failed: {str(e)[:200]}")
            if attempt == 1:
                print("Waiting 40s for rate limit reset...")
                time.sleep(40)

    csv = f"{OUT}/metrics.csv"
    if not os.path.exists(csv):
        print("No researcher CSV; using data/sample_metrics.csv")
        csv = "data/sample_metrics.csv"
    if report_md is None:
        print("Using fallback report.")
        report_md = fallback_report(args.query, csv)

    with open(f"{OUT}/market_report.md", "w", encoding="utf-8") as f:
        f.write(report_md)
    build_pdf(report_md, compute_summary(csv), f"{OUT}/market_report.pdf",
              title=args.query, query=args.query)
    bench.save("benchmarks.json")
    print(f"Done: {OUT}/market_report.pdf and benchmarks.json")


if __name__ == "__main__":
    main()
