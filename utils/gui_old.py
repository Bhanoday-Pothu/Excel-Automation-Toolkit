import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pathlib import Path

from automation import run_automation


# ---------------- Window ----------------

root = tk.Tk()
root.title("Excel Automation Toolkit")
root.geometry("700x550")
root.resizable(False, False)


# ---------------- Browse Input ----------------

def browse_input():
    folder = filedialog.askdirectory()

    if folder:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, folder)


# ---------------- Browse Output ----------------

def browse_output():
    folder = filedialog.askdirectory()

    if folder:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder)
        


# ---------------- Run Automation ----------------

def start_automation():

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

    status.config(
        text="Status : Processing...",
        fg="orange"
    )

    progress.start(10)

    root.update()

    try:
        print("Input Folder:", input_path)
        print("Output Folder:", output_path)
        run_automation(
            Path(input_path),
            Path(output_path)
        )

        progress.stop()

        status.config(
            text="Status : Completed Successfully",
            fg="green"
        )

        messagebox.showinfo(
            "Success",
            "Automation Completed Successfully!"
        )

    except Exception as e:

        progress.stop()

        status.config(
            text="Status : Failed",
            fg="red"
        )

        messagebox.showerror(
            "Automation Error",
            str(e)
        )


# ---------------- Title ----------------

title = tk.Label(
    root,
    text="Excel Automation Toolkit",
    font=("Arial", 20, "bold")
)

title.pack(pady=20)


# ---------------- Input Folder ----------------

tk.Label(
    root,
    text="Input Folder"
).pack()

input_entry = tk.Entry(
    root,
    width=70
)

input_entry.pack(pady=5)

tk.Button(
    root,
    text="Browse",
    width=15,
    command=browse_input
).pack()


# ---------------- Output Folder ----------------

tk.Label(
    root,
    text="Output Folder"
).pack(pady=(20, 0))

output_entry = tk.Entry(
    root,
    width=70
)

output_entry.pack(pady=5)

tk.Button(
    root,
    text="Browse",
    width=15,
    command=browse_output
).pack()


# ---------------- Run Button ----------------

run_btn = tk.Button(
    root,
    text="Run Automation",
    bg="green",
    fg="white",
    font=("Arial", 12, "bold"),
    width=25,
    command=start_automation
)

run_btn.pack(pady=25)


# ---------------- Progress Bar ----------------

progress = Progressbar(
    root,
    orient="horizontal",
    length=500,
    mode="indeterminate"
)

progress.pack(pady=10)


# ---------------- Status ----------------

status = tk.Label(
    root,
    text="Status : Ready",
    fg="green",
    font=("Arial", 11, "bold")
)

status.pack(pady=20)


# ---------------- Footer ----------------

footer = tk.Label(
    root,
    text="Developed by Bhanoday Pothu",
    fg="gray"
)

footer.pack(side="bottom", pady=10)


root.mainloop()