import pandas as pd
REQUIRED_COLUMNS = [
    "Name",
    "Product",
    "Amount",
    "City"
]

def validate_dataframe(df):
    # print("Validator is running...")
        #check if file is empty
    if df.empty:
        raise ValueError("Excel files is empty.")
    #check required column
    missing=[]
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            missing.append(column)
            
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )
        
#check duplicate column names
    if df.columns.duplicated().any():
        raise ValueError("Duplicate column names found.")
    
#check completly empty columns
    empty_columns=df.columns[df.isnull().all()].tolist()
    
    if empty_columns:
        print(f"Warning: Empty columns found: {empty_columns}")
        
    return True    