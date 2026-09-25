import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
import threading
import time
import os
import subprocess
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from automation import run_automation


# ============================================================
# Window
# ============================================================

root = ttk.Window(
    title="Excel Automation Toolkit PRO",
    themename="flatly"
)

root.geometry("1000x750")
root.minsize(900, 700)

start_time = 0
last_output_folder = None


# ============================================================
# Browse Input Folder
# ============================================================

def browse_input():

    folder = filedialog.askdirectory(
        title="Select Input Folder"
    )

    if folder:

        input_entry.delete(0, tk.END)
        input_entry.insert(0, folder)


# ============================================================
# Browse Output Folder
# ============================================================

def browse_output():

    folder = filedialog.askdirectory(
        title="Select Output Folder"
    )

    if folder:

        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder)


# ============================================================
# Live Log Window
# ============================================================

def write_log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")

    log_box.insert(
        tk.END,
        f"[{timestamp}] {message}\n"
    )



    log_box.see(tk.END)

    log_box.configure(state="disabled")

    root.update_idletasks()


# ============================================================
# Progress Bar
# ============================================================

def update_progress(value):
    

    progress["value"] = value

    progress_label.config(
        text=f"{value}%"
    )

    root.update_idletasks()

def run_on_ui(func):
    root.after(0,func)
# ============================================================
# Open Output Folder
# ============================================================

def open_output_folder():

    global last_output_folder

    if not last_output_folder:
        messagebox.showwarning(
            "Warning",
            "No Output Folder Available."
        )
        return

    try:

        os.startfile(last_output_folder)

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# ============================================================
# Open Generated File
# ============================================================

def open_file(filename):

    global last_output_folder

    if not last_output_folder:
        return

    file = Path(last_output_folder) / filename

    if file.exists():

        os.startfile(file)

    else:

        messagebox.showwarning(
            "Missing File",
            f"{filename} not found."
        )
        
        
# ============================================================
# Automation Worker (Background Thread)
# ============================================================

def automation_worker(input_path, output_path):

    global start_time
    global last_output_folder

    try:

        last_output_folder = output_path

        result = run_automation(
            Path(input_path),
            Path(output_path),
            log_callback=write_log,
            progress_callback=update_progress
        )

        elapsed = round(time.time() - start_time, 2)

        run_on_ui(lambda: status.config(
            text="Status : Completed Successfully",
            bootstyle="success"
        ))

        run_on_ui(lambda: run_btn.config(state="normal"))

        run_on_ui(lambda: messagebox.showinfo(
            "Completed",
            "Automation Completed Successfully!"
        ))
        write_log("")
        write_log("🎉 Automation Completed Successfully!")
        write_log(f"⏱ Processing Time : {elapsed} seconds")

        if result:

            if isinstance(result, dict):

                write_log("")
                write_log(f"📂 Files Processed : {result.get('files', 0)}")

        

    except Exception as e:

        run_on_ui(lambda: run_btn.config(state="normal"))

        run_on_ui(lambda: status.config(
            text="Status : Failed",
            bootstyle="danger"
        ))

        run_on_ui(lambda: messagebox.showerror(
            "Automation Error",
            str(e)
        ))

        write_log("")
        write_log(f"❌ ERROR : {e}")

    
# ============================================================
# Start Automation
# ============================================================

def start_automation():

    global start_time

    input_path = input_entry.get().strip()
    output_path = output_entry.get().strip()

    if not input_path:

        messagebox.showerror(
            "Error",
            "Please select the Input Folder."
        )
        return

    if not output_path:

        messagebox.showerror(
            "Error",
            "Please select the Output Folder."
        )
        return

    # Reset Log Window
    log_box.configure(state="normal")
    log_box.delete("1.0", tk.END)
    log_box.configure(state="disabled")

    progress["value"] = 0
    progress_label.config(text="0%")

    status.config(
        text="Status : Processing...",
        bootstyle="warning"
    )

    run_btn.config(state="disabled")

    start_time = time.time()

    write_log("=" * 60)
    write_log("📊 Excel Automation Toolkit PRO")
    write_log("=" * 60)
    write_log("")
    write_log(f"📂 Input Folder : {input_path}")
    write_log(f"📁 Output Folder : {output_path}")
    write_log("")
    write_log("🚀 Starting Automation...")
    write_log("")

    thread = threading.Thread(
        target=automation_worker,
        args=(input_path, output_path),
        daemon=True
    )

    thread.start()
    
# ============================================================
# Title
# ============================================================

title = ttk.Label(
    root,
    text="📊 Excel Automation Toolkit PRO v2.0",
    font=("Segoe UI", 24, "bold"),
    bootstyle="primary"
)


version = ttk.Label(
    root,
    text="Version 2.0",
    bootstyle="secondary",
    font=("Segoe UI", 10)
)

version.pack()

title.pack(pady=20)

# ============================================================
# Input Folder
# ============================================================

ttk.Label(
    root,
    text="Input Folder",
    font=("Segoe UI", 11, "bold")
).pack()

input_entry = ttk.Entry(
    root,
    width=80
)

input_entry.pack(pady=5)

ttk.Button(
    root,
    text="📂 Browse Input Folder",
    command=browse_input,
    bootstyle="info",
    width=30
).pack(pady=5)

# ============================================================
# Output Folder
# ============================================================

ttk.Label(
    root,
    text="Output Folder",
    font=("Segoe UI", 11, "bold")
).pack(pady=(15, 0))

output_entry = ttk.Entry(
    root,
    width=80
)

output_entry.pack(pady=5)

ttk.Button(
    root,
    text="📁 Browse Output Folder",
    command=browse_output,
    bootstyle="info",
    width=30
).pack(pady=5)

# ============================================================
# Run Button
# ============================================================

run_btn = ttk.Button(
    root,
    text="▶ Run Automation",
    command=start_automation,
    bootstyle="success",
    width=30
)

run_btn.pack(pady=20)


# ============================================================
# Progress
# ============================================================

progress = ttk.Progressbar(
    root,
    length=700,
    maximum=100,
    mode="determinate",
    bootstyle="success-striped"
)

progress.pack()

progress_label = ttk.Label(
    root,
    text="0%",
    bootstyle="info",
    font=("Segoe UI", 10, "bold")
)

progress_label.pack(pady=5)


# ============================================================
# Live Console
# ============================================================

ttk.Label(
    root,
    text="📝 Live Console",
    font=("Segoe UI", 12, "bold")
).pack(anchor="w", padx=25, pady=(15, 5))

log_box = ScrolledText(
    root,
    height=14,
    width=100,
    font=("Consolas", 10),
    state="disabled"
)

log_box.pack(padx=20)


# ============================================================
# Open Output Folder
# ============================================================

open_btn = ttk.Button(
    root,
    text="📂 Open Output Folder",
    command=open_output_folder,
    bootstyle="primary",
    width=30
)

open_btn.pack(pady=15)

# ============================================================
# Generated Files
# ============================================================

ttk.Label(
    root,
    text="Generated Files",
    font=("Segoe UI", 12, "bold")
).pack()

files_frame = ttk.Frame(root)

files_frame.pack(pady=10)

ttk.Button(
    files_frame,
    text="📗 Excel",
    bootstyle="success-outline",
    command=lambda: open_file("merged_output.xlsx")
).grid(row=0, column=0, padx=5)

ttk.Button(
    files_frame,
    text="📄 CSV",
    bootstyle="info-outline",
    command=lambda: open_file("merged_output.csv")
).grid(row=0, column=1, padx=5)

ttk.Button(
    files_frame,
    text="📕 PDF",
    bootstyle="danger-outline",
    command=lambda: open_file("cleaning_report.pdf")
).grid(row=0, column=2, padx=5)

ttk.Button(
    files_frame,
    text="📦 ZIP",
    bootstyle="warning-outline",
    command=lambda: open_file("reports.zip")
).grid(row=0, column=3, padx=5)

# ============================================================
# Status
# ============================================================

status = ttk.Label(
    root,
    text="Status : Ready",
    font=("Segoe UI", 11, "bold"),
    bootstyle="success"
)

status.pack(pady=15)


# ============================================================
# Footer
# ============================================================

footer = ttk.Label(
    root,
    text="Developed by Bhanoday Pothu",
    bootstyle="secondary"
)

footer.pack(side="bottom", pady=10)


# ============================================================
# Start App
# ============================================================

root.mainloop()






