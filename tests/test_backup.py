from pathlib import Path

from utils.backup import backup_files


def test_backup_files_copies_excel_files(tmp_path):
    input_folder = tmp_path / "input"
    backup_folder = tmp_path / "backup"

    input_folder.mkdir()
    backup_folder.mkdir()

    # Excel files that should be backed up.
    sales_file = input_folder / "sales.xlsx"
    inventory_file = input_folder / "inventory.xlsx"

    sales_file.write_text("sales data")
    inventory_file.write_text("inventory data")

    # Non-Excel file that should NOT be backed up.
    notes_file = input_folder / "notes.txt"
    notes_file.write_text("notes")

    result = backup_files(
        input_folder,
        backup_folder
    )

    # Function should return the created backup folder.
    assert isinstance(result, Path)
    assert result.exists()
    assert result.is_dir()
    assert result.parent == backup_folder

    # Excel files should have been copied.
    backed_up_sales = result / "sales.xlsx"
    backed_up_inventory = result / "inventory.xlsx"

    assert backed_up_sales.exists()
    assert backed_up_inventory.exists()

    assert backed_up_sales.read_text() == "sales data"
    assert backed_up_inventory.read_text() == "inventory data"

    # Non-Excel files should not be copied.
    assert not (result / "notes.txt").exists()


def test_backup_files_creates_timestamped_folder(tmp_path):
    input_folder = tmp_path / "input"
    backup_folder = tmp_path / "backup"

    input_folder.mkdir()
    backup_folder.mkdir()

    result = backup_files(
        input_folder,
        backup_folder
    )

    # Folder name should follow YYYY-MM-DD_HH-MM-SS.
    folder_name = result.name

    assert len(folder_name) == 19
    assert folder_name[4] == "-"
    assert folder_name[7] == "-"
    assert folder_name[10] == "_"
    assert folder_name[13] == "-"
    assert folder_name[16] == "-"