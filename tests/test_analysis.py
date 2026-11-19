import pytest
from crew.analysis import compute_summary, summary_markdown


@pytest.fixture
def mock_csv(tmp_path):
    p = tmp_path / "m.csv"
    p.write_text("company,revenue\nA,10\nB,20\nC,30\n")
    return str(p)


def test_summary_statistics(mock_csv):
    s = compute_summary(mock_csv)
    assert s.loc["mean", "revenue"] == 20
    assert s.loc["min", "revenue"] == 10
    assert s.loc["max", "revenue"] == 30
    assert s.loc["std", "revenue"] == pytest.approx(10)


def test_markdown_table(mock_csv):
    md = summary_markdown(mock_csv)
    assert "|" in md and "revenue" in md
