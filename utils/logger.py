from datetime import datetime
from pathlib import Path

#create logs folder if it does'nt exist

LOG_FOLDER=Path("logs")
LOG_FOLDER.mkdir(exist_ok=True)

LOG_FILE=LOG_FOLDER/"automation_log.txt"

def log(message):
    """
    Writes a message to the log file with date and time

    """
    current_time=datetime.now().strftime("%d-%m-%y %I:%M:%S %p")
    with open(LOG_FILE,"a",encoding="utf-8") as file:
        file.write(f"[{current_time}] {message}\n")