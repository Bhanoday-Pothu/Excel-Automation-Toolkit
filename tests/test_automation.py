import pandas as pd
import pytest

from automation import run_automation


def test_automation_with_no_excel_files(tmp_path):
    input_folder = tmp_path / "input"
    output_folder = tmp_path / "output"

    input_folder.mkdir()

    with pytest.raises(FileNotFoundError):
        run_automation(
            input_folder,
            output_folder
        )


def test_automation_with_valid_excel_file(tmp_path, monkeypatch):
    input_folder = tmp_path / "input"
    output_folder = tmp_path / "output"

    input_folder.mkdir()

    input_file = input_folder / "sales.xlsx"

    df = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Product": ["Laptop", "Mouse", "Keyboard"],
        "Amount": [50000, 1000, 2000],
        "City": ["Hyderabad", "Bangalore", "Chennai"],
    })

    df.to_excel(input_file, index=False)

    monkeypatch.setattr(
        "automation.BACKUP_FOLDER",
        tmp_path / "backup"
    )

    result = run_automation(
        input_folder,
        output_folder
    )

    assert isinstance(result, dict)

    assert result["files"] == 1
    assert result["total_rows"] == 3
    assert result["final_rows"] >= 0
    assert result["processing_time"] >= 0

    assert (output_folder / "merged_output.xlsx").exists()
    assert (output_folder / "merged_output.csv").exists()
    assert (output_folder / "cleaning_report.pdf").exists()
    assert (output_folder / "reports.zip").exists()