from utils.console import success, error, info, warning, show_report


def test_success_prints_message(capsys):
    success("Automation completed successfully.")

    captured = capsys.readouterr()

    assert "Automation completed successfully." in captured.out


def test_error_prints_message(capsys):
    error("Automation failed.")

    captured = capsys.readouterr()

    assert "Automation failed." in captured.out


def test_info_prints_message(capsys):
    info("Processing files...")

    captured = capsys.readouterr()

    assert "Processing files..." in captured.out


def test_warning_prints_message(capsys):
    warning("Empty columns found.")

    captured = capsys.readouterr()

    assert "Empty columns found." in captured.out


def test_show_report_displays_stats(capsys):
    stats = {
        "Total Rows": 100,
        "Duplicate Rows Removed": 10,
        "Blank Rows Removed": 5,
        "Final Rows": 85,
    }

    show_report(stats)

    captured = capsys.readouterr()

    assert "Cleaning report" in captured.out
    assert "Total Rows" in captured.out
    assert "100" in captured.out
    assert "Duplicate Rows Removed" in captured.out
    assert "10" in captured.out
    assert "Final Rows" in captured.out
    assert "85" in captured.out