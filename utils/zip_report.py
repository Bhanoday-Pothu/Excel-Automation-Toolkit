from zipfile import ZipFile
from pathlib import Path

def create_zip(output_folder):
    zip_path= output_folder/"reports.zip"
    with ZipFile(zip_path, "w") as zipf:
        for file in output_folder.iterdir():
            if file.suffix in [".xlsx",".csv",".pdf"]:
                zipf.write(file,arcname=file.name)
    return zip_path