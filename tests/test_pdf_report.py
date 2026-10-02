from pathlib import Path

from pypdf import PdfReader

from utils.pdf_report import create_pdf_report


def test_create_pdf_report(tmp_path):
    output_path = tmp_path / "cleaning_report.pdf"

    stats = {
        "Total Rows": 10,
        "Duplicate Rows Removed": 2,
        "Blank Rows Removed": 1,
        "Final Rows": 7,
    }

    result = create_pdf_report(output_path, stats)

    assert result is None
    assert output_path.exists()
    assert output_path.is_file()
    assert output_path.stat().st_size > 0

    reader = PdfReader(output_path)

    assert len(reader.pages) >= 1

    text = "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )

    assert "Excel Automaton Toolkit Report" in text
    assert "Metric" in text
    assert "Value" in text

    for key, value in stats.items():
        assert key in text
        assert str(value) in text