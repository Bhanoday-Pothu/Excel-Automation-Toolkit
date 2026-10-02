import json

import utils.history as history_module
from utils.history import save_history


def test_save_history_creates_history_file(tmp_path, monkeypatch):
    history_file = tmp_path / "config" / "history.json"

    monkeypatch.setattr(
        history_module,
        "HISTORY_FILE",
        history_file
    )

    result = {
        "files": 3,
        "total_rows": 100,
        "duplicates": 5,
        "blank_rows": 2,
        "final_rows": 93,
        "processing_time": 4.25,
    }

    input_folder = tmp_path / "input"
    output_folder = tmp_path / "output"

    input_folder.mkdir()
    output_folder.mkdir()

    response = save_history(
        result,
        input_folder,
        output_folder
    )

    assert response is None
    assert history_file.exists()

    with open(history_file, "r", encoding="utf-8") as file:
        history = json.load(file)

    assert len(history) == 1

    record = history[0]

    assert record["input_folder"] == str(input_folder)
    assert record["output_folder"] == str(output_folder)
    assert record["excel_files"] == 3
    assert record["total_rows"] == 100
    assert record["duplicates_removed"] == 5
    assert record["blank_rows_removed"] == 2
    assert record["final_rows"] == 93
    assert record["processing_time"] == 4.25
    assert record["status"] == "Success"
    assert record["date_time"]


def test_save_history_preserves_existing_records(tmp_path, monkeypatch):
    history_file = tmp_path / "config" / "history.json"

    monkeypatch.setattr(
        history_module,
        "HISTORY_FILE",
        history_file
    )

    history_file.parent.mkdir(parents=True)

    existing_record = {
        "date_time": "01-01-2026 10:00:00 AM",
        "input_folder": "old_input",
        "output_folder": "old_output",
        "excel_files": 1,
        "total_rows": 10,
        "duplicates_removed": 0,
        "blank_rows_removed": 0,
        "final_rows": 10,
        "processing_time": 1.5,
        "status": "Success",
    }

    with open(history_file, "w", encoding="utf-8") as file:
        json.dump([existing_record], file)

    result = {
        "files": 2,
        "total_rows": 20,
        "duplicates": 1,
        "blank_rows": 1,
        "final_rows": 18,
        "processing_time": 2.5,
    }

    save_history(
        result,
        tmp_path / "new_input",
        tmp_path / "new_output"
    )

    with open(history_file, "r", encoding="utf-8") as file:
        history = json.load(file)

    assert len(history) == 2

    assert history[0] == existing_record
    assert history[1]["excel_files"] == 2
    assert history[1]["total_rows"] == 20
    assert history[1]["status"] == "Success"


def test_save_history_handles_missing_result_values(tmp_path, monkeypatch):
    history_file = tmp_path / "config" / "history.json"

    monkeypatch.setattr(
        history_module,
        "HISTORY_FILE",
        history_file
    )

    result = {}

    save_history(
        result,
        tmp_path / "input",
        tmp_path / "output"
    )

    with open(history_file, "r", encoding="utf-8") as file:
        history = json.load(file)

    record = history[0]

    assert record["excel_files"] == 0
    assert record["total_rows"] == 0
    assert record["duplicates_removed"] == 0
    assert record["blank_rows_removed"] == 0
    assert record["final_rows"] == 0
    assert record["processing_time"] == 0.0


def test_save_history_handles_invalid_numeric_values(tmp_path, monkeypatch):
    history_file = tmp_path / "config" / "history.json"

    monkeypatch.setattr(
        history_module,
        "HISTORY_FILE",
        history_file
    )

    result = {
        "files": "invalid",
        "total_rows": None,
        "duplicates": "invalid",
        "blank_rows": "",
        "final_rows": "invalid",
        "processing_time": "invalid",
    }

    save_history(
        result,
        tmp_path / "input",
        tmp_path / "output"
    )

    with open(history_file, "r", encoding="utf-8") as file:
        history = json.load(file)

    record = history[0]

    assert record["excel_files"] == 0
    assert record["total_rows"] == 0
    assert record["duplicates_removed"] == 0
    assert record["blank_rows_removed"] == 0
    assert record["final_rows"] == 0
    assert record["processing_time"] == 0.0


def test_save_history_recovers_from_invalid_json(tmp_path, monkeypatch):
    history_file = tmp_path / "config" / "history.json"

    monkeypatch.setattr(
        history_module,
        "HISTORY_FILE",
        history_file
    )

    history_file.parent.mkdir(parents=True)

    history_file.write_text(
        "this is not valid json",
        encoding="utf-8"
    )

    result = {
        "files": 1,
        "total_rows": 10,
        "duplicates": 0,
        "blank_rows": 0,
        "final_rows": 10,
        "processing_time": 1.25,
    }

    save_history(
        result,
        tmp_path / "input",
        tmp_path / "output"
    )

    with open(history_file, "r", encoding="utf-8") as file:
        history = json.load(file)

    assert len(history) == 1
    assert history[0]["excel_files"] == 1
    assert history[0]["total_rows"] == 10
    assert history[0]["status"] == "Success"