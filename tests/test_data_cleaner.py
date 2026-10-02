import pandas as pd

from utils.data_cleaner import clean_data


def test_clean_data_removes_duplicate_rows():
    df = pd.DataFrame({
        "Name": ["Alice", "Bob", "Alice"],
        "Product": ["Laptop", "Mouse", "Laptop"],
        "Amount": [50000, 1000, 50000],
        "City": ["Hyderabad", "Bangalore", "Hyderabad"],
    })

    cleaned_df, stats = clean_data(df)

    assert len(cleaned_df) == 2
    assert stats["Total Rows"] == 3
    assert stats["Duplicate Rows Removed"] == 1
    assert stats["Blank Rows Removed"] == 0
    assert stats["Final Rows"] == 2


def test_clean_data_removes_completely_blank_rows():
    df = pd.DataFrame({
        "Name": ["Alice", None, "Bob"],
        "Product": ["Laptop", None, "Mouse"],
        "Amount": [50000, None, 1000],
        "City": ["Hyderabad", None, "Bangalore"],
    })

    cleaned_df, stats = clean_data(df)

    assert len(cleaned_df) == 2
    assert stats["Total Rows"] == 3
    assert stats["Duplicate Rows Removed"] == 0
    assert stats["Blank Rows Removed"] == 1
    assert stats["Final Rows"] == 2


def test_clean_data_removes_duplicates_and_blank_rows():
    df = pd.DataFrame({
        "Name": ["Alice", "Alice", None, "Bob"],
        "Product": ["Laptop", "Laptop", None, "Mouse"],
        "Amount": [50000, 50000, None, 1000],
        "City": ["Hyderabad", "Hyderabad", None, "Bangalore"],
    })

    cleaned_df, stats = clean_data(df)

    assert len(cleaned_df) == 2
    assert stats["Total Rows"] == 4
    assert stats["Duplicate Rows Removed"] == 1
    assert stats["Blank Rows Removed"] == 1
    assert stats["Final Rows"] == 2


def test_clean_data_preserves_valid_rows():
    df = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "Product": ["Laptop", "Mouse"],
        "Amount": [50000, 1000],
        "City": ["Hyderabad", "Bangalore"],
    })

    cleaned_df, stats = clean_data(df)

    assert len(cleaned_df) == 2
    assert stats["Total Rows"] == 2
    assert stats["Duplicate Rows Removed"] == 0
    assert stats["Blank Rows Removed"] == 0
    assert stats["Final Rows"] == 2