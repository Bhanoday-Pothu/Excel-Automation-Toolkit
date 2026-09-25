import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as ttk


class LogPanel:

    def __init__(self, parent):

        ttk.Label(
            parent,
            text="📝 Live Console",
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w", pady=(20, 5))

        self.log = ScrolledText(
            parent,
            height=15,
            font=("Consolas", 10)
        )

        self.log.pack(fill="both", expand=True)

    def write(self, message):

        self.log.insert(tk.END, message + "\n")
        self.log.see(tk.END)