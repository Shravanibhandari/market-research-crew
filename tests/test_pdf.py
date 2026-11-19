from crew.analysis import compute_summary
from crew.pdf_report import build_pdf


def test_pdf_is_valid(tmp_path):
    out = tmp_path / "r.pdf"
    md = "# T\n## Summary\nHello **world**.\n- point one\n" * 40  # forces multi-page
    build_pdf(md, compute_summary("data/sample_metrics.csv"), str(out), "Test", "q")
    data = out.read_bytes()
    assert data.startswith(b"%PDF") and len(data) > 1000
