from pathlib import Path
import shutil
from datetime import datetime

def backup_files(input_folder,backup_folder):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    current_backup = backup_folder / timestamp
    current_backup.mkdir(parents=True,exist_ok=True)
    excel_files=input_folder.glob("*.xlsx")
    for file in excel_files:
        shutil.copy(file,current_backup / file.name)
    return current_backup