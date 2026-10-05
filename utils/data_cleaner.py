import pandas as pd


def clean_data(
    df,
    remove_duplicates=True,
    remove_blank_rows=True
):
    total_rows = len(df)

    # --------------------------------------------
    # Remove duplicate rows
    # --------------------------------------------
    if remove_duplicates:
        duplicate_rows = df.duplicated().sum()
        df = df.drop_duplicates()
    else:
        duplicate_rows = 0

    # --------------------------------------------
    # Remove completely blank rows
    # --------------------------------------------
    if remove_blank_rows:
        blank_rows = df.isna().all(axis=1).sum()
        df = df.dropna(how="all")
    else:
        blank_rows = 0

    final_rows = len(df)

    stats = {
        "Total Rows": total_rows,
        "Duplicate Rows Removed": duplicate_rows,
        "Blank Rows Removed": blank_rows,
        "Final Rows": final_rows,
    }

    return df, stats