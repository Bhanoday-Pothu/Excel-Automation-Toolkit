import json
from pathlib import Path

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from gui.settings_page import SettingsPage
from gui.sidebar import Sidebar
from gui.dashboard import Dashboard
from gui.automation_page import AutomationPage
from gui.reports_page import ReportsPage
from gui.history_page import HistoryPage

class MainWindow:

    def __init__(self):

        self.settings = self.load_settings()

        self.root = ttk.Window(
            title="Excel Automation Toolkit PRO",
            themename=self.settings.get("theme", "flatly")
        )

        self.root.geometry("1400x850")
        self.root.minsize(1200, 700)

        self.last_result = None

        self.create_layout()

    # ======================================================
    # LOAD SETTINGS
    # ======================================================

    def load_settings(self):

        settings_file = Path("config") / "settings.json"

        default_settings = {
            "theme": "flatly",
            "input_folder": "",
            "output_folder": ""
        }

        if not settings_file.exists():
            return default_settings

        try:

            with open(
                settings_file,
                "r",
                encoding="utf-8"
            ) as file:

                saved_settings = json.load(file)

            default_settings.update(saved_settings)

            return default_settings

        except Exception as e:

            print(f"Unable to load settings: {e}")

            return default_settings

    def show_history(self):
        print("History Clicked")
        self.clear_content()
        self.history_page=HistoryPage(
            self.content_frame,
            self
        )

        # your existing create_layout code continues here

    # ======================================================
    # CREATE MAIN LAYOUT
    # ======================================================

    def create_layout(self):

        # ---------------- Sidebar ----------------

        self.sidebar_frame = ttk.Frame(
            self.root,
            width=250
        )

        self.sidebar_frame.pack(
            side=LEFT,
            fill=Y
        )

        self.sidebar_frame.pack_propagate(False)

        # ---------------- Content ----------------

        self.content_frame = ttk.Frame(
            self.root,
            padding=20
        )

        self.content_frame.pack(
            side=LEFT,
            fill=BOTH,
            expand=True
        )

        # ---------------- Sidebar ----------------

        self.sidebar = Sidebar(
            self.sidebar_frame,
            self
        )

        # ---------------- Default Page ----------------

        self.show_dashboard()

    # ======================================================
    # CLEAR CONTENT
    # ======================================================

    def clear_content(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ======================================================
    # DASHBOARD
    # ======================================================

    def show_dashboard(self):

        print("Dashboard Clicked")

        self.clear_content()

        self.dashboard = Dashboard(
            self.content_frame
        )

        # --------------------------------------------------
        # SHOW LAST AUTOMATION RESULT
        # --------------------------------------------------

        if self.last_result:

            self.dashboard.update_cards(
                files=self.last_result.get(
                    "files",
                    0
                ),

                total=self.last_result.get(
                    "total_rows",
                    0
                ),

                duplicates=self.last_result.get(
                    "duplicates",
                    0
                ),

                final=self.last_result.get(
                    "final_rows",
                    0
                )
            )

        else:

            self.dashboard.update_cards(
                files=0,
                total=0,
                duplicates=0,
                final=0
            )

    # ======================================================
    # AUTOMATION
    # ======================================================

    def show_automation(self):

        print("Automation Clicked")

        self.clear_content()

        self.automation_page = AutomationPage(
            self.content_frame,
            self
        )

    # ======================================================
    # REPORTS
    # ======================================================

    def show_reports(self):

        print("Reports Clicked")

        self.clear_content()

        self.reports_page = ReportsPage(
            self.content_frame,
            self
        )

    # ======================================================
    # SETTINGS
    # ======================================================

    def show_settings(self):

        print("Settings Clicked")

        self.clear_content()

        self.settings_page = SettingsPage(
            self.content_frame,
            self
        )

    # ======================================================
    # ABOUT
    # ======================================================

    def show_about(self):

        print("About Clicked")

        self.clear_content()

        # ---------------- Title ----------------

        label = ttk.Label(
            self.content_frame,
            text="ℹ About",
            font=("Segoe UI", 28, "bold"),
            bootstyle="primary"
        )

        label.pack(
            pady=50
        )

        # ---------------- Application Name ----------------

        info = ttk.Label(
            self.content_frame,
            text="Excel Automation Toolkit PRO",
            font=("Segoe UI", 16, "bold")
        )

        info.pack(
            pady=10
        )

        # ---------------- Version ----------------

        version = ttk.Label(
            self.content_frame,
            text="Version 1.0",
            font=("Segoe UI", 12)
        )

        version.pack()

        # ---------------- Description ----------------

        description = ttk.Label(
            self.content_frame,
            text=(
                "A professional Excel automation application "
                "for cleaning, processing and reporting data."
            ),
            font=("Segoe UI", 11),
            justify="center"
        )

        description.pack(
            pady=20
        )

    # ======================================================
    # RUN APPLICATION
    # ======================================================

    def run(self):

        self.root.mainloop()