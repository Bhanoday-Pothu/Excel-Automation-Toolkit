from pathlib import Path
import pandas as pd
from tqdm import tqdm
import time

from utils.validator import validate_dataframe
from utils.summary import create_summary
from utils.formatter import format_excel
from utils.data_cleaner import clean_data
from utils.converter import excel_to_csv
from utils.charts import create_chart
from utils.logger import log
from utils.pdf_report import create_pdf_report
from utils.backup import backup_files
from utils.console import success, error
from utils.zip_report import create_zip

from config import BACKUP_FOLDER


def run_automation(
    input_folder,
    output_folder,
    log_callback=None,
    progress_callback=None
):
    start_time=time.time()
    """
    Main Excel Automation Function
    """

    # -----------------------------------------
    # START TIMER
    # -----------------------------------------

    start_time = time.time()

    # -----------------------------------------
    # Logger
    # -----------------------------------------

    def log_message(message):
        print(message)

        if log_callback:
            log_callback(str(message))

    # -----------------------------------------
    # Progress
    # -----------------------------------------

    def update_progress(value):
        if progress_callback:
            progress_callback(value)

    # -----------------------------------------
    # Paths
    # -----------------------------------------

    input_folder = Path(input_folder)
    output_folder = Path(output_folder)

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------------------
    # START LOG
    # -----------------------------------------

    log("=" * 60)
    log("Excel Automation Toolkit Started")

    log_message("=" * 60)
    log_message("📊 Excel Automation Toolkit")
    log_message("=" * 60)

    log_message(f"📂 Input Folder : {input_folder}")
    log_message(f"📁 Output Folder : {output_folder}")
    log_message("")

    try:

        # =========================================
        # STEP 1 - BACKUP
        # =========================================

        log_message("💾 Creating Backup...")

        backup_path = backup_files(
            input_folder,
            BACKUP_FOLDER
        )

        # backup_files may return None
        if backup_path is not None:

            log_message(
                f"✅ Backup Created : {Path(backup_path).name}"
            )

            log(
                f"Backup Created : {backup_path}"
            )

        else:

            log_message(
                "⚠ Backup completed."
            )

            log(
                "Backup completed, but no backup path was returned."
            )

        update_progress(5)

        # =========================================
        # STEP 2 - FIND EXCEL FILES
        # =========================================

        log_message("")
        log_message("🔍 Searching Excel Files...")

        excel_files = list(
            input_folder.glob("*.xlsx")
        )

        # Do not process our own generated output
        excel_files = [
            file for file in excel_files
            if file.name != "merged_output.xlsx"
        ]

        if not excel_files:

            raise FileNotFoundError(
                "No Excel files found in selected Input Folder."
            )

        log_message(
            f"📂 Found {len(excel_files)} Excel files"
        )

        success(
            f"Found {len(excel_files)} Excel files."
        )

        # =========================================
        # STEP 3 - READ & VALIDATE
        # =========================================

        dataframes = []

        progress = tqdm(
            excel_files,
            desc="Processing Excel Files",
            unit="file"
        )

        for index, file in enumerate(progress, start=1):

            progress.set_postfix(
                File=file.name
            )

            log_message(
                f"📄 Reading {file.name}"
            )

            df = pd.read_excel(file)

            validate_dataframe(df)

            log_message(
                "   ✔ Validation Completed"
            )

            dataframes.append(df)

            log(
                f"{file.name} validated successfully"
            )

            # Progress between 5 and 20
            current_progress = 5 + int(
                (index / len(excel_files)) * 15
            )

            update_progress(current_progress)

        # =========================================
        # STEP 4 - MERGE
        # =========================================

        log_message("")
        log_message("🔄 Merging Excel Files...")

        merged_df = pd.concat(
            dataframes,
            ignore_index=True
        )

        log_message(
            "✔ Merge Completed"
        )

        update_progress(40)

        # =========================================
        # STEP 5 - CLEAN DATA
        # =========================================

        log_message("")
        log_message("🧹 Cleaning Data...")

        cleaned_df, stats = clean_data(
            merged_df
        )

        log_message(
            "✔ Data Cleaned"
        )

        update_progress(55)

        # =========================================
        # STEP 6 - SAVE EXCEL
        # =========================================

        output_file = (
            output_folder /
            "merged_output.xlsx"
        )

        log_message("")
        log_message(
            "💾 Saving Excel File..."
        )

        cleaned_df.to_excel(
            output_file,
            index=False
        )

        log_message(
            f"✔ Excel Saved : {output_file.name}"
        )

        # =========================================
        # STEP 7 - FORMAT EXCEL
        # =========================================

        log_message("")
        log_message(
            "🎨 Formatting Excel..."
        )

        format_excel(
            output_file
        )

        log_message(
            "✔ Formatting Completed"
        )

        update_progress(65)

        # =========================================
        # STEP 8 - SUMMARY
        # =========================================

        log_message("")
        log_message(
            "📊 Creating Summary Sheet..."
        )

        create_summary(
            output_file,
            stats
        )

        log_message(
            "✔ Summary Created"
        )

        update_progress(75)

        # =========================================
        # STEP 9 - CHARTS
        # =========================================

        log_message("")
        log_message(
            "📈 Creating Charts..."
        )

        create_chart(
            output_file
        )

        log_message(
            "✔ Charts Created"
        )

        update_progress(85)

        # =========================================
        # STEP 10 - CSV
        # =========================================

        log_message("")
        log_message(
            "📄 Creating CSV File..."
        )

        csv_result = excel_to_csv(
            output_file,
            output_folder
        )

        csv_file = (
            output_folder /
            "merged_output.csv"
        )

        if csv_file.exists():

            log_message(
                f"✔ CSV Created : {csv_file.name}"
            )

        else:

            log_message(
                "⚠ CSV function completed, "
                "but CSV file was not found."
            )

        update_progress(92)

        # =========================================
        # STEP 11 - PDF
        # =========================================

        pdf_file = (
            output_folder /
            "cleaning_report.pdf"
        )

        log_message("")
        log_message(
            "📕 Creating PDF Report..."
        )

        create_pdf_report(
            pdf_file,
            stats
        )

        if pdf_file.exists():

            log_message(
                f"✔ PDF Created : {pdf_file.name}"
            )

        update_progress(97)

        # =========================================
        # STEP 12 - ZIP
        # =========================================

        log_message("")
        log_message(
            "📦 Creating ZIP Archive..."
        )

        zip_result = create_zip(
            output_folder
        )

        # IMPORTANT:
        # create_zip() may return None.
        # Therefore we safely determine the ZIP path.

        if zip_result is not None:

            zip_file = Path(zip_result)

        else:

            # Your project appears to create reports.zip
            zip_file = (
                output_folder /
                "reports.zip"
            )

        if zip_file.exists():

            log_message(
                f"✔ ZIP Created : {zip_file.name}"
            )

        else:

            log_message(
                "⚠ ZIP function completed, "
                "but ZIP file was not found."
            )

        update_progress(100)

        # =========================================
        # PROCESSING TIME
        # =========================================

        processing_time = round(
            time.time() - start_time,
            2
        )

        # =========================================
        # CLEANING REPORT
        # =========================================

        log_message("")
        log_message(
            "📋 Cleaning Report"
        )

        log_message(
            "-" * 40
        )

        for key, value in stats.items():

            log_message(
                f"{key}: {value}"
            )

        log_message(
            f"Processing Time: {processing_time} seconds"
        )

        # =========================================
        # GENERATED FILES
        # =========================================

        log_message("")
        log_message(
            "📂 Generated Files"
        )

        log_message(
            f"📗 Excel : {output_file.name}"
        )

        log_message(
            f"📄 CSV   : {csv_file.name}"
        )

        log_message(
            f"📕 PDF   : {pdf_file.name}"
        )

        if zip_file.exists():

            log_message(
                f"📦 ZIP   : {zip_file.name}"
            )

        # =========================================
        # LOG FILE
        # =========================================

        log(
            "Summary Sheet Created"
        )

        log(
            "Charts Created"
        )

        log(
            "CSV Created"
        )

        log(
            "PDF Created"
        )

        log(
            "ZIP Created"
        )

        log(
            f"Total Rows : "
            f"{stats['Total Rows']}"
        )

        log(
            f"Duplicate Rows Removed : "
            f"{stats['Duplicate Rows Removed']}"
        )

        log(
            f"Blank Rows Removed : "
            f"{stats['Blank Rows Removed']}"
        )

        log(
            f"Final Rows : "
            f"{stats['Final Rows']}"
        )

        log(
            f"Processing Time : "
            f"{processing_time} seconds"
        )

        log("=" * 60)

        log(
            "Excel Automation Toolkit "
            "Completed Successfully"
        )

        success(
            "Output Saved Successfully!"
        )

        # =========================================
        # FINAL GUI MESSAGE
        # =========================================

        log_message("")
        log_message(
            "🎉 Automation Completed Successfully!"
        )

        # =========================================
        # RETURN RESULT TO DASHBOARD
        # =========================================
        processing_time=round(time.time()-start_time,2)
        return {
            "files": len(excel_files),

            "total_rows": stats[
                "Total Rows"
            ],

            "duplicates": stats[
                "Duplicate Rows Removed"
            ],

            "final_rows": stats[
                "Final Rows"
            ],

            "blank_rows": stats[
                "Blank Rows Removed"
            ],

            "output_folder": str(
                output_folder
            ),

            "processing_time": processing_time
        }

    # =============================================
    # ERROR HANDLING
    # =============================================

    except Exception as e:

        log_message("")
        log_message(
            f"❌ ERROR : {e}"
        )

        error(
            f"Error : {e}"
        )

        log(
            f"Error : {e}"
        )

        raise