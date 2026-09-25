import ttkbootstrap as ttk

from gui.cards import StatCard

from datetime import datetime


class Dashboard:

    def __init__(self, parent):

        # ---------------- Main Frame ----------------

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        # ---------------- Title ----------------

        ttk.Label(
            self.frame,
            text="📊 Dashboard",
            font=("Segoe UI", 28, "bold"),
            bootstyle="primary"
        ).pack(pady=20)

        # ---------------- Statistics Cards ----------------

        cards_frame = ttk.Frame(self.frame)
        cards_frame.pack(pady=20)

        # Excel Files

        self.files = StatCard(
            cards_frame,
            "Excel Files",
            color="info"
        )

        self.files.grid(
            row=0,
            column=0,
            padx=10
        )

        # Total Rows

        self.rows = StatCard(
            cards_frame,
            "Total Rows",
            color="success"
        )

        self.rows.grid(
            row=0,
            column=1,
            padx=10
        )

        # Duplicates

        self.duplicates = StatCard(
            cards_frame,
            "Duplicates",
            color="danger"
        )

        self.duplicates.grid(
            row=0,
            column=2,
            padx=10
        )

        # Final Rows

        self.final = StatCard(
            cards_frame,
            "Final Rows",
            color="warning"
        )

        self.final.grid(
            row=0,
            column=3,
            padx=10
        )

        # ---------------- Separator ----------------

        ttk.Separator(
            self.frame,
            orient="horizontal"
        ).pack(
            fill="x",
            pady=20
        )

        # ---------------- Welcome Message ----------------

        ttk.Label(
            self.frame,
            text="Welcome to Excel Automation Toolkit PRO",
            font=("Segoe UI", 16)
        ).pack()

        # ---------------- Last Run ----------------

        self.last_run = ttk.Label(
            self.frame,
            text="Last Run : Never",
            font=("Segoe UI", 11)
        )

        self.last_run.pack(pady=10)

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

        # Excel files

        self.files.set_value(
            files
        )

        # Total rows

        self.rows.set_value(
            f"{total:,}"
        )

        # Duplicate rows

        self.duplicates.set_value(
            f"{duplicates:,}"
        )

        # Final rows

        self.final.set_value(
            f"{final:,}"
        )

        # Update last run time

        self.last_run.config(
            text=(
                "Last Run : "
                + datetime.now().strftime(
                    "%d-%m-%Y %I:%M %p"
                )
            )
        )