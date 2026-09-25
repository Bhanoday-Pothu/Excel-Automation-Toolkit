import ttkbootstrap as ttk


class Header:

    def __init__(self, parent):

        frame = ttk.Frame(parent)

        frame.pack(fill="x", pady=10)

        ttk.Label(
            frame,
            text="📊 Excel Automation Toolkit PRO",
            font=("Segoe UI", 24, "bold"),
            bootstyle="primary"
        ).pack(side="left", padx=20)

        ttk.Label(
            frame,
            text="Version 2.0",
            bootstyle="secondary"
        ).pack(side="right", padx=20)