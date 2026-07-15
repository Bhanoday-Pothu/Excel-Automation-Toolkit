# from config import INPUT_FOLDER

# print("=" *50)
# print("Excel Automation Toolkit")
# print("="*50)
# print(f"Input Folder :{INPUT_FOLDER}")


# import pandas as pd
# # from pathlib import Path
# from config import INPUT_FOLDER,OUTPUT_FILE
# print("="*50)
# print("Excel Automation Toolkit")
# print("="*50)
# #find all excel files
# excel_files=list(INPUT_FOLDER.glob("*.xlsx"))
# print(f"\nFound {len(excel_files)} Excel files.\n")

# dataframes=[]

# for file in excel_files:
#     print(f"Reading: {file.name}")
#     df=pd.read_excel(file)
#     dataframes.append(df)
# #merge all dataframes
# merged_df=pd.concat(dataframes,ignore_index=True)

# #save output

# merged_df.to_excel(OUTPUT_FILE,index=False)

# print("\nMerger completed Successfully")

# print(f"\nOutput saved to:\n{OUTPUT_FILE}")
from tqdm import tqdm
from utils.validator import validate_dataframe
from utils.summary import create_summary
from utils.formatter import format_excel
import pandas as pd
from config import INPUT_FOLDER, OUTPUT_FILE,OUTPUT_FOLDER
from utils.data_cleaner import clean_data
from utils.converter import excel_to_csv
from utils.charts import create_chart
from utils.logger import log
print("="*50)
print("Excel Automation Toolkit")
print("="*50)
log("="*60)
log("Excel Automation Toolkit Started")
try:
#read excel files

    excel_files=list(INPUT_FOLDER.glob("*.xlsx"))
    if not excel_files:
        raise FileNotFoundError("NO Excel files found in the input folder.")
    print(f"\nFound {len(excel_files)} Excel files.\n")
    log(f"Found {len(excel_files)} Excel files")
    dataframes=[]
    # for file in excel_files:
    for file in tqdm(excel_files,desc="Processing Excel Files"): 
         tqdm.write(f"Reading:{file.name}")      
        # print(f"Reading: {file.name}")
         log(f"Reading file: {file.name}")
    
         df=pd.read_excel(file)
         print(df.columns.tolist())
         print(df.head())
         validate_dataframe(df)
        
         log(f"{file.name} validate successfully")
         dataframes.append(df)
    
#merge
    merged_df = pd.concat(dataframes,ignore_index=True)

#clean
    cleaned_df,stats = clean_data(merged_df)

#save
    cleaned_df.to_excel(OUTPUT_FILE,index=False)


    
    format_excel(OUTPUT_FILE)
    create_summary(OUTPUT_FILE,stats)
    log("Summary sheet created")
    create_chart(OUTPUT_FILE)
    log("Chart created successfully.")
    excel_to_csv(OUTPUT_FILE,OUTPUT_FOLDER)
    log("CSV file created successfully.")
    log(f"Total Rows: {stats['Total Rows']}")
    log(f"Duplicate Rows Removed: {stats['Duplicate Rows Removed']}")
    log(f"Blank Rows Removed: {stats['Blank Rows Removed']}")
    log(f"Final Rows: {stats['Final Rows']}")
    print("\nCleaning Report")
    print("_"*30)
    for key,value in stats.items():
        print(f"{key}:{value}")
    print("\n Output Saved Successfully!")
    print(OUTPUT_FILE)
    log("Excel Automation Toolkit Completed Successfully")
    log("="*60)
except Exception as e:
    print(f"\nError:{e}")
    log(f"Error: {e}")    