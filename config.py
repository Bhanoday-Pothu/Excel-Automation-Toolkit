from pathlib import Path

# Base project directory
BASE_DIR = Path(__file__).resolve().parent

# Folder paths
input_folder = BASE_DIR / "input"
output_folder = BASE_DIR / "output"
LOG_FOLDER = BASE_DIR / "logs"

# Output file
OUTPUT_FILE = output_folder / "merged_output.xlsx"
PDF_FILE=output_folder / "cleaning_report.pdf"

#backup files
BACKUP_FOLDER=BASE_DIR/"backup"
