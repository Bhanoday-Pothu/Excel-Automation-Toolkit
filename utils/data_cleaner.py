import pandas as pd
def clean_data(df):
    """
    Clean the merged dataframe.
    Return:
    cleaned_df
    statistics(dict)

    """
    total_rows=len(df)
    #remove duplicate rows
    duplicate_rows = df.duplicated().sum()
    df = df.drop_duplicates()
    #remove completely blank rows
    blank_rows=df.isna().all(axis=1).sum()
    df=df.dropna(how="all")
    final_rows=len(df)
    stats={
        "Total Rows": total_rows,
        "Duplicate Rows Removed": duplicate_rows,
        "Blank Rows Removed": blank_rows,
        "Final Rows": final_rows,
    }
    return df,stats