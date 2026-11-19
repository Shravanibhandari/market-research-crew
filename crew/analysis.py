"""Pure pandas logic (no CrewAI import) so it is easy to test."""
import pandas as pd


def compute_summary(csv_path: str) -> pd.DataFrame:
    """Return count/mean/min/max/std for every numeric column."""
    df = pd.read_csv(csv_path)
    numeric = df.select_dtypes("number")
    if numeric.empty:
        raise ValueError("CSV has no numeric columns")
    return numeric.describe().loc[["count", "mean", "min", "max", "std"]]


def summary_markdown(csv_path: str) -> str:
    return compute_summary(csv_path).round(2).to_markdown()
