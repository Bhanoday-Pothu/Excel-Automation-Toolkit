import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
import threading
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from automation import run_automation
from automation import run_automation
from utils.history import save_history

class AutomationPage:

    def __init__(self, parent, app):

        self.app = app

        # --------------------------------------------------
        # Main Frame
        # --------------------------------------------------

        self.frame = ttk.Frame(
            parent,
            padding=20
        )

        self.frame.pack(
            fill=BOTH,
            expand=True
        )

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        title = ttk.Label(
            self.frame,
            text="⚙ Excel Automation",
            font=("Segoe UI", 28, "bold"),
            bootstyle="primary"
        )

        title.pack(
            pady=(10, 25)
        )

        subtitle = ttk.Label(
            self.frame,
            text="Select your input and output folders, then run the automation.",
            font=("Segoe UI", 12)
        )

        subtitle.pack(
            pady=(0, 20)
        )

        # --------------------------------------------------
        # Input Folder
        # --------------------------------------------------

        input_label = ttk.Label(
            self.frame,
            text="📂 Input Folder",
            font=("Segoe UI", 11, "bold")
        )

        input_label.pack(
            anchor=W,
            pady=(10, 5)
        )

        input_frame = ttk.Frame(
            self.frame
        )

        input_frame.pack(
            fill=X
        )

        self.input_entry = ttk.Entry(
            input_frame,
            font=("Segoe UI", 11)
        )

        self.input_entry.pack(
            side=LEFT,
            fill=X,
            expand=True,
            padx=(0, 10)
        )
#load saved input folder
        saved_input=self.app.settings.get(
            "input_folder",
            ""
        )
        if saved_input:
            self.input_entry.insert(
                0,
                saved_input
            )
        input_button = ttk.Button(
            input_frame,
            text="📂 Browse",
            command=self.browse_input,
            bootstyle="info",
            width=15
        )

        input_button.pack(
            side=RIGHT
        )

        # --------------------------------------------------
        # Output Folder
        # --------------------------------------------------

        output_label = ttk.Label(
            self.frame,
            text="📁 Output Folder",
            font=("Segoe UI", 11, "bold")
        )

        output_label.pack(
            anchor=W,
            pady=(20, 5)
        )

        output_frame = ttk.Frame(
            self.frame
        )

        output_frame.pack(
            fill=X
        )

        self.output_entry = ttk.Entry(
            output_frame,
            font=("Segoe UI", 11)
        )

        self.output_entry.pack(
            side=LEFT,
            fill=X,
            expand=True,
            padx=(0, 10)
        )
        #Load saved output folder
        saved_output=self.app.settings.get(
            "output_folder",
            ""
        )
        if saved_output:
            self.output_entry.insert(
                0,
                saved_output
            )

        output_button = ttk.Button(
            output_frame,
            text="📂 Browse",
            command=self.browse_output,
            bootstyle="info",
            width=15
        )

        output_button.pack(
            side=RIGHT
        )

        # --------------------------------------------------
        # Run Button
        # --------------------------------------------------

        self.run_button = ttk.Button(
            self.frame,
            text="▶ Run Automation",
            command=self.start_automation,
            bootstyle="success",
            width=25
        )

        self.run_button.pack(
            pady=25
        )

        # --------------------------------------------------
        # Progress Section
        # --------------------------------------------------

        progress_frame = ttk.Frame(
            self.frame
        )

        progress_frame.pack(
            fill=X,
            pady=(0, 10)
        )

        self.progress = ttk.Progressbar(
            progress_frame,
            maximum=100,
            mode="determinate",
            bootstyle="success-striped"
        )

        self.progress.pack(
            side=LEFT,
            fill=X,
            expand=True,
            padx=(0, 15)
        )

        self.progress_label = ttk.Label(
            progress_frame,
            text="0%",
            font=("Segoe UI", 10, "bold"),
            bootstyle="info"
        )

        self.progress_label.pack(
            side=RIGHT
        )

        # --------------------------------------------------
        # Status
        # --------------------------------------------------

        self.status = ttk.Label(
            self.frame,
            text="Status : Ready",
            font=("Segoe UI", 11, "bold"),
            bootstyle="success"
        )

        self.status.pack(
            pady=5
        )

        # --------------------------------------------------
        # Log Window
        # --------------------------------------------------

        log_label = ttk.Label(
            self.frame,
            text="📋 Automation Log",
            font=("Segoe UI", 11, "bold")
        )

        log_label.pack(
            anchor=W,
            pady=(15, 5)
        )

        self.log_box = ScrolledText(
            self.frame,
            height=12,
            font=("Consolas", 10),
            state="disabled"
        )

        self.log_box.pack(
            fill=BOTH,
            expand=True
        )

        # --------------------------------------------------
        # Open Output Folder Button
        # --------------------------------------------------

        self.open_button = ttk.Button(
            self.frame,
            text="📂 Open Output Folder",
            command=self.open_output_folder,
            bootstyle="primary",
            width=25,
            state="disabled"
        )

        self.open_button.pack(
            pady=15
        )

    # ======================================================
    # BROWSE INPUT
    # ======================================================

    def browse_input(self):

        folder = filedialog.askdirectory(
            title="Select Input Folder"
        )

        if folder:

            self.input_entry.delete(
                0,
                tk.END
            )

            self.input_entry.insert(
                0,
                folder
            )

            self.write_log(
                f"📂 Input Folder Selected: {folder}"
            )

    # ======================================================
    # BROWSE OUTPUT
    # ======================================================

    def browse_output(self):

        folder = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if folder:

            self.output_entry.delete(
                0,
                tk.END
            )

            self.output_entry.insert(
                0,
                folder
            )

            self.write_log(
                f"📁 Output Folder Selected: {folder}"
            )

    # ======================================================
    # WRITE LOG
    # ======================================================

    def write_log(self, message):

        # GUI updates must happen on the main Tkinter thread

        self.frame.after(
            0,
            self._write_log,
            str(message)
        )

    def _write_log(self, message):

        self.log_box.config(
            state="normal"
        )

        self.log_box.insert(
            tk.END,
            message + "\n"
        )

        self.log_box.see(
            tk.END
        )

        self.log_box.config(
            state="disabled"
        )

    # ======================================================
    # UPDATE PROGRESS
    # ======================================================

    def update_progress(self, value):

        self.frame.after(
            0,
            self._update_progress,
            value
        )

    def _update_progress(self, value):

        self.progress["value"] = value

        self.progress_label.config(
            text=f"{value}%"
        )

    # ======================================================
    # START AUTOMATION
    # ======================================================

    def start_automation(self):

        input_path = self.input_entry.get().strip()
        output_path = self.output_entry.get().strip()

        # --------------------------------------------------
        # Validate Input Folder
        # --------------------------------------------------

        if not input_path:

            messagebox.showerror(
                "Input Folder Missing",
                "Please select an Input Folder."
            )

            return

        if not Path(input_path).exists():

            messagebox.showerror(
                "Invalid Input Folder",
                "The selected Input Folder does not exist."
            )

            return

        # --------------------------------------------------
        # Validate Output Folder
        # --------------------------------------------------

        if not output_path:

            messagebox.showerror(
                "Output Folder Missing",
                "Please select an Output Folder."
            )

            return
#save selected folders for the rest of application
        self.app.settings["input folder"]=input_path
        self.app.settings["output_folder"]=output_path

        # --------------------------------------------------
        # Clear Previous Log
        # --------------------------------------------------

        self.log_box.config(
            state="normal"
        )

        self.log_box.delete(
            "1.0",
            tk.END
        )

        self.log_box.config(
            state="disabled"
        )

        # --------------------------------------------------
        # Reset Progress
        # --------------------------------------------------

        self.progress["value"] = 0

        self.progress_label.config(
            text="0%"
        )

        self.status.config(
            text="Status : Processing...",
            bootstyle="warning"
        )

        # --------------------------------------------------
        # Disable Run Button
        # --------------------------------------------------

        self.run_button.config(
            state="disabled"
        )

        self.open_button.config(
            state="disabled"
        )

        self.write_log("=" * 60)
        self.write_log("📊 Excel Automation Toolkit PRO")
        self.write_log("=" * 60)
        self.write_log("")
        self.write_log(f"📂 Input Folder : {input_path}")
        self.write_log(f"📁 Output Folder : {output_path}")
        self.write_log("")
        self.write_log("🚀 Starting automation...")
        self.write_log("")

        # --------------------------------------------------
        # Run Automation in Background Thread
        # --------------------------------------------------

        thread = threading.Thread(
            target=self.run_process,
            args=(
                input_path,
                output_path
            ),
            daemon=True
        )

        thread.start()

    # ======================================================
    # RUN PROCESS
    # ======================================================

    def run_process(
        self,
        input_path,
        output_path
    ):

        try:

            result = run_automation(
                Path(input_path),
                Path(output_path),
                log_callback=self.write_log,
                progress_callback=self.update_progress
            )

            self.frame.after(
                0,
                self.automation_completed,
                result,
                output_path
            )

        except Exception as e:

            self.frame.after(
                0,
                self.automation_failed,
                str(e)
            )

    # ======================================================
    # AUTOMATION COMPLETED
    # ======================================================

    def automation_completed(
        self,
        result,
        output_path
    ):

        self.progress["value"] = 100

        self.progress_label.config(
            text="100%"
        )

        self.status.config(
            text="Status : Completed Successfully",
            bootstyle="success"
        )

        self.run_button.config(
            state="normal"
        )

        self.open_button.config(
            state="normal"
        )

        self.last_output_folder = output_path

        self.write_log("")
        self.write_log("=" * 60)
        self.write_log("🎉 AUTOMATION COMPLETED SUCCESSFULLY")
        self.write_log("=" * 60)

        # --------------------------------------------------
        # Show Result Statistics
        # --------------------------------------------------

        if isinstance(result, dict):

            self.write_log(
                f"📊 Excel Files : {result.get('files', 'N/A')}"
            )

            self.write_log(
                f"📋 Total Rows : {result.get('total_rows', 'N/A')}"
            )

            self.write_log(
                f"🗑 Duplicate Rows Removed : {result.get('duplicates', 'N/A')}"
            )

            self.write_log(
                f"⬜ Blank Rows Removed : {result.get('blank_rows', 'N/A')}"
            )

            self.write_log(
                f"✅ Final Rows : {result.get('final_rows', 'N/A')}"
            )

            # --------------------------------------------------
            # Update Dashboard
            # --------------------------------------------------
        # --------------------------------------------------
# SAVE RESULT FOR DASHBOARD
# --------------------------------------------------

       
        self.app.last_result = result
        self.app.settings["output_folder"]=str(output_path) 
        #save autimation history
        save_history(
            result,
            self.input_entry.get().strip(),
            output_path
        )           
        self.write_log("")
        self.write_log(
            f"📁 Output Folder: {output_path}"
        )

        messagebox.showinfo(
            "Success",
            "Automation Completed Successfully!"
        )

    # ======================================================
    # AUTOMATION FAILED
    # ======================================================

    def automation_failed(
        self,
        error_message
    ):

        self.progress["value"] = 0

        self.progress_label.config(
            text="0%"
        )

        self.status.config(
            text="Status : Failed",
            bootstyle="danger"
        )

        self.run_button.config(
            state="normal"
        )

        self.open_button.config(
            state="disabled"
        )

        self.write_log("")
        self.write_log("=" * 60)
        self.write_log("❌ AUTOMATION FAILED")
        self.write_log("=" * 60)
        self.write_log(
            f"Error: {error_message}"
        )

        messagebox.showerror(
            "Automation Error",
            error_message
        )

    # ======================================================
    # OPEN OUTPUT FOLDER
    # ======================================================

    def open_output_folder(self):

        output_path = self.output_entry.get().strip()

        if not output_path:

            messagebox.showerror(
                "Error",
                "Output folder is not selected."
            )

            return

        output_path = Path(output_path)

        if not output_path.exists():

            messagebox.showerror(
                "Error",
                "Output folder does not exist."
            )

            return

        try:

            os.startfile(
                output_path
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to open folder:\n{e}"
            )