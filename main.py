# from config import INPUT_FOLDER

# print("=" *50)
# print("Excel Automation Toolkit")
# print("="*50)
# print(f"Input Folder :{INPUT_FOLDER}")


import pandas as pd
# from pathlib import Path
from config import INPUT_FOLDER,OUTPUT_FILE
print("="*50)
print("Excel Automation Toolkit")
print("="*50)
#find all excel files
excel_files=list(INPUT_FOLDER.glob("*.xlsx"))
print(f"\nFound {len(excel_files)} Excel files.\n")

dataframes=[]

for file in excel_files:
    print(f"Reading: {file.name}")
    df=pd.read_excel(file)
    dataframes.append(df)
#merge all dataframes
merged_df=pd.concat(dataframes,ignore_index=True)

#save output

merged_df.to_excel(OUTPUT_FILE,index=False)

print("\nMerger completed Successfully")

print(f"\nOutput saved to:\n{OUTPUT_FILE}")

