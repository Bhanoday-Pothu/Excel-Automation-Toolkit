from pathlib import Path
from zipfile import ZipFile

from utils.zip_report import create_zip


def test_create_zip(tmp_path):
    output_folder = tmp_path / "output"
    output_folder.mkdir()

    # Files that should be included.
    xlsx_file = output_folder / "merged_output.xlsx"
    csv_file = output_folder / "merged_output.csv"
    pdf_file = output_folder / "cleaning_report.pdf"

    xlsx_file.write_text("excel data")
    csv_file.write_text("csv data")
    pdf_file.write_text("pdf data")

    # Files that should NOT be included.
    txt_file = output_folder / "notes.txt"
    json_file = output_folder / "settings.json"

    txt_file.write_text("some notes")
    json_file.write_text('{"test": true}')

    result = create_zip(output_folder)

    zip_path = output_folder / "reports.zip"

    # Function should return the ZIP path.
    assert result == zip_path
    assert isinstance(result, Path)

    # ZIP should exist and contain data.
    assert zip_path.exists()
    assert zip_path.is_file()
    assert zip_path.stat().st_size > 0

    with ZipFile(zip_path, "r") as zipf:
        files_in_zip = zipf.namelist()

    # Supported report files should be included.
    assert "merged_output.xlsx" in files_in_zip
    assert "merged_output.csv" in files_in_zip
    assert "cleaning_report.pdf" in files_in_zip

    # Unsupported files should not be included.
    assert "notes.txt" not in files_in_zip
    assert "settings.json" not in files_in_zip

    # The ZIP should not include itself.
    assert "reports.zip" not in files_in_zip