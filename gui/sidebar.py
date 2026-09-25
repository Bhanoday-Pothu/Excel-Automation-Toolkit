import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class Sidebar:

    def __init__(self, parent, app):

        self.app = app

        self.frame = ttk.Frame(
            parent,
            padding=15
        )

        self.frame.pack(
            fill=BOTH,
            expand=True
        )

        ttk.Label(
            self.frame,
            text="MENU",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        self.make_button(
            "🏠 Dashboard",
            app.show_dashboard
        )

        self.make_button(
            "⚙ Automation",
            app.show_automation
        )

        self.make_button(
            "📊 Reports",
            app.show_reports
        )

        self.make_button(
            "🌙 Settings",
            app.show_settings
        )

        self.make_button(
            "ℹ About",
            app.show_about
        )
        ttk.Button(
            self.frame,
            text="📜 History",
            bootstyle="secondary",
            command=self.app.show_history
        ).pack(fill="x",padx=15,pady=5)
        

    # ----------------------------------

    def make_button(self, text, command):

        ttk.Button(
            self.frame,
            text=text,
            command=command,
            bootstyle="primary",
            width=22
        ).pack(
            pady=8
        )