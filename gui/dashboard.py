import ttkbootstrap as ttk
from gui.cards import StatCard
from datetime import datetime


class Dashboard:

    def __init__(self, parent):

        # ==================================================
        # MAIN FRAME
        # ==================================================

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        # ==================================================
        # HEADER
        # ==================================================

        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill="x", pady=(10, 5))

        ttk.Label(
            header_frame,
            text="📊 Dashboard",
            font=("Segoe UI", 28, "bold"),
            bootstyle="primary"
        ).pack(anchor="w")

        ttk.Label(
            header_frame,
            text="Monitor your Excel automation activity at a glance",
            font=("Segoe UI", 11),
            bootstyle="secondary"
        ).pack(anchor="w", pady=(5, 0))

        # ==================================================
        # AUTOMATION OVERVIEW
        # ==================================================

        ttk.Label(
            self.frame,
            text="Automation Overview",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", pady=(30, 10))

        # ==================================================
        # RESPONSIVE CARDS CONTAINER
        # ==================================================

        cards_frame = ttk.Frame(self.frame)

        cards_frame.pack(
            fill="x",
            expand=True,
            pady=(0, 20)
        )

        # Make all four columns share available width
        for column in range(4):
            cards_frame.columnconfigure(
                column,
                weight=1,
                uniform="cards"
            )

        # ==================================================
        # EXCEL FILES
        # ==================================================

        self.files = StatCard(
            cards_frame,
            "Excel Files",
            color="info"
        )

        self.files.grid(
            row=0,
            column=0,
            padx=(0, 10),
            pady=5,
            sticky="ew"
        )

        # ==================================================
        # TOTAL ROWS
        # ==================================================

        self.rows = StatCard(
            cards_frame,
            "Total Rows",
            color="success"
        )

        self.rows.grid(
            row=0,
            column=1,
            padx=10,
            pady=5,
            sticky="ew"
        )

        # ==================================================
        # DUPLICATES
        # ==================================================

        self.duplicates = StatCard(
            cards_frame,
            "Duplicates",
            color="danger"
        )

        self.duplicates.grid(
            row=0,
            column=2,
            padx=10,
            pady=5,
            sticky="ew"
        )

        # ==================================================
        # FINAL ROWS
        # ==================================================

        self.final = StatCard(
            cards_frame,
            "Final Rows",
            color="warning"
        )

        self.final.grid(
            row=0,
            column=3,
            padx=(10, 0),
            pady=5,
            sticky="ew"
        )

        # ==================================================
        # SEPARATOR
        # ==================================================

        ttk.Separator(
            self.frame,
            orient="horizontal"
        ).pack(
            fill="x",
            pady=25
        )

        # ==================================================
        # WELCOME / STATUS SECTION
        # ==================================================

        status_frame = ttk.Frame(
            self.frame,
            padding=20
        )

        status_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            status_frame,
            text="Welcome to Excel Automation Toolkit PRO",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        ttk.Label(
            status_frame,
            text=(
                "Use the Automation section to clean, validate, "
                "format, analyze and generate reports from your Excel files."
            ),
            font=("Segoe UI", 11),
            bootstyle="secondary",
            wraplength=900
        ).pack(
            anchor="w",
            pady=(8, 15)
        )

        self.last_run = ttk.Label(
            status_frame,
            text="Last Run : Never",
            font=("Segoe UI", 10),
            bootstyle="secondary"
        )

        self.last_run.pack(anchor="w")

    # ==================================================
    # UPDATE DASHBOARD
    # ==================================================

    def update_cards(
        self,
        files,
        total,
        duplicates,
        final
    ):

        self.files.set_value(files)

        self.rows.set_value(
            f"{total:,}"
        )

        self.duplicates.set_value(
            f"{duplicates:,}"
        )

        self.final.set_value(
            f"{final:,}"
        )

        self.last_run.config(
            text=(
                "Last Run : "
                + datetime.now().strftime(
                    "%d-%m-%Y %I:%M %p"
                )
            )
        )