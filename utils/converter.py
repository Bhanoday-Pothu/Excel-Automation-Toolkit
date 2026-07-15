import pandas as pd
from pathlib import Path

def excel_to_csv(excel_file,output_folder):
    """
    Converts one Excel file into CSV
    
    """
    excel_file=Path(excel_file)
    df=pd.read_excel(excel_file)
    csv_name=excel_file.stem+".csv"
    output_path=output_folder/csv_name
    df.to_csv(output_path,index=False)
    print(f"Converted -> {csv_name}")
    

def csv_to_excel(csv_file,output_folder):
    """
    Converts CSV into Excel

    """
    csv_file=Path(csv_file)
    df=pd.read_csv(csv_file)
    excel_name=csv_file.stem+".xlsx"
    output_path=output_folder/excel_name
    df.to_excel(output_path,index=False)
    print(f"Converted ->{excel_name}")
    