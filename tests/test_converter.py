import pandas as pd

from utils.converter import excel_to_csv, csv_to_excel


def test_excel_to_csv(tmp_path):
    excel_file = tmp_path / "sales.xlsx"
    output_folder = tmp_path / "output"

    output_folder.mkdir()

    df = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "Product": ["Laptop", "Mouse"],
        "Amount": [50000, 1000],
        "City": ["Hyderabad", "Bangalore"],
    })

    df.to_excel(excel_file, index=False)

    result = excel_to_csv(
        excel_file,
        output_folder
    )

    csv_file = output_folder / "sales.csv"

    assert result is None
    assert csv_file.exists()

    converted_df = pd.read_csv(csv_file)

    pd.testing.assert_frame_equal(
        df,
        converted_df
    )


def test_csv_to_excel(tmp_path):
    csv_file = tmp_path / "sales.csv"
    output_folder = tmp_path / "output"

    output_folder.mkdir()

    df = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "Product": ["Laptop", "Mouse"],
        "Amount": [50000, 1000],
        "City": ["Hyderabad", "Bangalore"],
    })

    df.to_csv(csv_file, index=False)

    result = csv_to_excel(
        csv_file,
        output_folder
    )

    excel_file = output_folder / "sales.xlsx"

    assert result is None
    assert excel_file.exists()

    converted_df = pd.read_excel(excel_file)

    pd.testing.assert_frame_equal(
        df,
        converted_df
    )