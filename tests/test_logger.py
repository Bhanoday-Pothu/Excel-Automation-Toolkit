import utils.logger as logger_module
from utils.logger import log


def test_log_writes_message(tmp_path, monkeypatch):
    log_folder = tmp_path / "logs"
    log_file = log_folder / "automation_log.txt"

    log_folder.mkdir()

    monkeypatch.setattr(
        logger_module,
        "LOG_FOLDER",
        log_folder
    )

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE",
        log_file
    )

    result = log("Automation completed successfully.")

    assert result is None
    assert log_file.exists()

    content = log_file.read_text(
        encoding="utf-8"
    )

    assert "Automation completed successfully." in content


def test_log_appends_messages(tmp_path, monkeypatch):
    log_folder = tmp_path / "logs"
    log_file = log_folder / "automation_log.txt"

    log_folder.mkdir()

    monkeypatch.setattr(
        logger_module,
        "LOG_FOLDER",
        log_folder
    )

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE",
        log_file
    )

    log("First message")
    log("Second message")

    lines = log_file.read_text(
        encoding="utf-8"
    ).splitlines()

    assert len(lines) == 2
    assert "First message" in lines[0]
    assert "Second message" in lines[1]


def test_log_contains_timestamp_format(tmp_path, monkeypatch):
    log_folder = tmp_path / "logs"
    log_file = log_folder / "automation_log.txt"

    log_folder.mkdir()

    monkeypatch.setattr(
        logger_module,
        "LOG_FOLDER",
        log_folder
    )

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE",
        log_file
    )

    log("Test timestamp")

    content = log_file.read_text(
        encoding="utf-8"
    )

    assert content.startswith("[")
    assert "] Test timestamp" in content