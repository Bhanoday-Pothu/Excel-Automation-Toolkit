from pathlib import Path

# Base project directory
BASE_DIR = Path(__file__).resolve().parent

# Folder paths
INPUT_FOLDER = BASE_DIR / "input"
OUTPUT_FOLDER = BASE_DIR / "output"
LOG_FOLDER = BASE_DIR / "logs"

# Output file
OUTPUT_FILE = OUTPUT_FOLDER / "merged_output.xlsx"