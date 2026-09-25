import json
import os
from pathlib import Path

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox


HISTORY_FILE = Path("config") / "history.json"


class HistoryPage:

    def __init__(self, parent, app):
        self.app = app

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=BOTH, expand=True)

        self.create_header()
        self.create_summary()
        self.create_table()
        self.create_buttons()

        self.load_history()

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------

    def create_header(self):

        header = ttk.Frame(self.frame)
        header.pack(fill=X, pady=(0, 20))

        ttk.Label(
            header,
            text="📜 Automation History",
            font=("Segoe UI", 28, "bold"),
            bootstyle="primary"
        ).pack(side=LEFT)

        ttk.Button(
            header,
            text="🔄 Refresh",
            bootstyle="info",
            command=self.load_history
        ).pack(side=RIGHT)

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    def create_summary(self):

        summary_frame = ttk.Frame(self.frame)
        summary_frame.pack(fill=X, pady=(0, 20))

        self.total_runs_label = self.create_summary_card(
            summary_frame,
            "Total Runs",
            "0",
            "primary"
        )

        self.success_label = self.create_summary_card(
            summary_frame,
            "Successful",
            "0",
            "success"
        )

        self.files_label = self.create_summary_card(
            summary_frame,
            "Excel Files",
            "0",
            "info"
        )

        self.rows_label = self.create_summary_card(
            summary_frame,
            "Rows Processed",
            "0",
            "warning"
        )

    def create_summary_card(self, parent, title, value, style):

        card = ttk.Frame(
            parent,
            padding=15,
            bootstyle=f"{style}-inverse"
        )

        card.pack(
            side=LEFT,
            fill=X,
            expand=True,
            padx=5
        )

        ttk.Label(
            card,
            text=title,
            font=("Segoe UI", 11)
        ).pack()

        label = ttk.Label(
            card,
            text=value,
            font=("Segoe UI", 22, "bold")
        )

        label.pack(pady=(5, 0))

        return label

    # --------------------------------------------------
    # TABLE
    # --------------------------------------------------

    def create_table(self):

        table_frame = ttk.Frame(self.frame)
        table_frame.pack(
            fill=BOTH,
            expand=True
        )

        columns = (
            "date",
            "input",
            "files",
            "rows",
            "duplicates",
            "blank",
            "final",
            "time",
            "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            bootstyle="primary"
        )

        headings = {
            "date": "Date & Time",
            "input": "Input Folder",
            "files": "Files",
            "rows": "Total Rows",
            "duplicates": "Duplicates",
            "blank": "Blank Rows",
            "final": "Final Rows",
            "time": "Processing Time",
            "status": "Status"
        }

        widths = {
            "date": 160,
            "input": 250,
            "files": 70,
            "rows": 100,
            "duplicates": 100,
            "blank": 100,
            "final": 100,
            "time": 120,
            "status": 100
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor=CENTER
            )

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient=VERTICAL,
            command=self.tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient=HORIZONTAL,
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tree.pack(
            side=LEFT,
            fill=BOTH,
            expand=True
        )

        scrollbar_y.pack(
            side=RIGHT,
            fill=Y
        )

        scrollbar_x.pack(
            side=BOTTOM,
            fill=X
        )

    # --------------------------------------------------
    # BUTTONS
    # --------------------------------------------------

    def create_buttons(self):

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=X, pady=15)

        ttk.Button(
            button_frame,
            text="📂 Open Output Folder",
            bootstyle="success",
            command=self.open_output_folder
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="🗑️ Clear History",
            bootstyle="danger",
            command=self.clear_history
        ).pack(side=LEFT, padx=5)

    # --------------------------------------------------
    # LOAD HISTORY
    # --------------------------------------------------

    def load_history(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        if not HISTORY_FILE.exists():
            self.update_summary([])
            return

        try:

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                history = json.load(file)

        except Exception as e:

            messagebox.showerror(
                "History Error",
                f"Unable to load history:\n\n{e}"
            )

            return

        for record in reversed(history):

            self.tree.insert(
                "",
                END,
                values=(
                    record.get("date_time", ""),
                    record.get("input_folder", ""),
                    record.get("excel_files", 0),
                    f"{record.get('total_rows', 0):,}",
                    f"{record.get('duplicates_removed', 0):,}",
                    f"{record.get('blank_rows_removed', 0):,}",
                    f"{record.get('final_rows', 0):,}",
                    f"{record.get('processing_time', 0):.2f}s",
                    record.get("status", "Unknown")
                )
            )

        self.update_summary(history)

    # --------------------------------------------------
    # SUMMARY UPDATE
    # --------------------------------------------------

    def update_summary(self, history):

        total_runs = len(history)

        successful_runs = sum(
            1
            for record in history
            if record.get("status") == "Success"
        )

        total_files = sum(
            int(record.get("excel_files", 0))
            for record in history
        )

        total_rows = sum(
            int(record.get("total_rows", 0))
            for record in history
        )

        self.total_runs_label.config(
            text=f"{total_runs:,}"
        )

        self.success_label.config(
            text=f"{successful_runs:,}"
        )

        self.files_label.config(
            text=f"{total_files:,}"
        )

        self.rows_label.config(
            text=f"{total_rows:,}"
        )

    # --------------------------------------------------
    # OPEN OUTPUT FOLDER
    # --------------------------------------------------

    def open_output_folder(self):

        output_folder = self.app.settings.get(
            "output_folder",
            ""
        )

        if not output_folder:

            messagebox.showwarning(
                "Output Folder",
                "No output folder has been configured."
            )

            return

        folder = Path(output_folder)

        if not folder.exists():

            messagebox.showwarning(
                "Output Folder",
                "The output folder does not exist."
            )

            return

        try:
            os.startfile(folder)

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to open folder:\n\n{e}"
            )

    # --------------------------------------------------
    # CLEAR HISTORY
    # --------------------------------------------------

    def clear_history(self):

        if not HISTORY_FILE.exists():
            messagebox.showinfo(
                "History",
                "There is no history to clear."
            )
            return

        confirm = messagebox.askyesno(
            "Clear History",
            "Are you sure you want to delete all automation history?"
        )

        if not confirm:
            return

        try:

            with open(
                HISTORY_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump([], file, indent=4)

            self.load_history()

            messagebox.showinfo(
                "History",
                "Automation history cleared successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "History Error",
                f"Unable to clear history:\n\n{e}"
            )