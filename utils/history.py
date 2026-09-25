import json
from pathlib import Path
from datetime import datetime


HISTORY_FILE = Path("config") / "history.json"


def save_history(result, input_folder, output_folder):
    """
    Save one successful automation run to history.
    """

    HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------
    # Load existing history
    # --------------------------------------------------

    if HISTORY_FILE.exists():

        try:

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                history = json.load(file)

        except Exception:

            history = []

    else:

        history = []

    # --------------------------------------------------
    # Convert values to normal Python types
    # --------------------------------------------------

    def safe_int(value):

        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def safe_float(value):

        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    # --------------------------------------------------
    # Create history record
    # --------------------------------------------------

    record = {
        "date_time": datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        ),

        "input_folder": str(
            input_folder
        ),

        "output_folder": str(
            output_folder
        ),

        "excel_files": safe_int(
            result.get("files", 0)
        ),

        "total_rows": safe_int(
            result.get("total_rows", 0)
        ),

        "duplicates_removed": safe_int(
            result.get("duplicates", 0)
        ),

        "blank_rows_removed": safe_int(
            result.get("blank_rows", 0)
        ),

        "final_rows": safe_int(
            result.get("final_rows", 0)
        ),

        "processing_time": safe_float(
            result.get("processing_time", 0)
        ),

        "status": "Success"
    }

    # --------------------------------------------------
    # Add newest run
    # --------------------------------------------------

    history.append(record)

    # --------------------------------------------------
    # Save history
    # --------------------------------------------------

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )