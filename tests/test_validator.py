import pandas as pd
import pytest

from utils.validator import validate_dataframe


def test_valid_dataframe():
    df = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "Product": ["Laptop", "Mouse"],
        "Amount": [50000, 1000],
        "City": ["Hyderabad", "Bangalore"],
    })

    assert validate_dataframe(df) is True


def test_empty_dataframe():
    df = pd.DataFrame()

    with pytest.raises(
        ValueError,
        match="Excel files is empty."
    ):
        validate_dataframe(df)


def test_missing_required_columns():
    df = pd.DataFrame({
        "Name": ["Alice"],
        "Product": ["Laptop"],
    })

    with pytest.raises(
        ValueError,
        match="Missing required columns"
    ):
        validate_dataframe(df)


def test_duplicate_column_names():
    df = pd.DataFrame(
        [
            ["Alice", "Laptop", 50000, "Hyderabad", "Extra"]
        ],
        columns=[
            "Name",
            "Product",
            "Amount",
            "City",
            "Name"
        ]
    )

    with pytest.raises(
        ValueError,
        match="Duplicate column names found."
    ):
        validate_dataframe(df)


def test_completely_empty_column_warning(capsys):
    df = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "Product": ["Laptop", "Mouse"],
        "Amount": [50000, 1000],
        "City": ["Hyderabad", "Bangalore"],
        "Unused": [None, None],
    })

    result = validate_dataframe(df)

    captured = capsys.readouterr()

    assert result is True
    assert "Empty columns found" in captured.out