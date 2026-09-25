# import argparse
# from pathlib import Path

# from config import input_folder, output_folder
# from automation import run_automation

# parser = argparse.ArgumentParser(
#     description="Excel Automation Toolkit"
# )

# parser.add_argument(
#     "--input",
#     default=str(input_folder),
#     help="Input Folder"
# )

# parser.add_argument(
#     "--output",
#     default=str(output_folder),
#     help="Output Folder"
# )

# args = parser.parse_args()

# run_automation(
#     Path(args.input),
#     Path(args.output)
# )



from gui.main_window import MainWindow

if __name__ == "__main__":
    app = MainWindow()
    app.run()