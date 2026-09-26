import json
from pathlib import Path
from datetime import datetime

import ttkbootstrap as ttk

from gui.cards import StatCard

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


HISTORY_FILE = Path("config") / "history.json"


class Dashboard:

    def __init__(self, parent):

        # ==================================================
        # OUTER DASHBOARD CONTAINER
        # ==================================================

        self.container = ttk.Frame(parent)
        self.container.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # SCROLLABLE CANVAS
        # ==================================================

        self.canvas = ttk.Canvas(
            self.container,
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            self.container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==================================================
        # INNER FRAME
        # ==================================================

        self.frame = ttk.Frame(
            self.canvas
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.frame,
            anchor="nw"
        )

        # Update scroll region
        self.frame.bind(
            "<Configure>",
            self._update_scroll_region
        )

        # Make inner frame follow canvas width
        self.canvas.bind(
            "<Configure>",
            self._resize_inner_frame
        )

        # Mouse wheel scrolling
        self.canvas.bind_all(
            "<MouseWheel>",
            self._on_mousewheel
        )

        # ==================================================
        # HEADER
        # ==================================================

        header_frame = ttk.Frame(
            self.frame
        )

        header_frame.pack(
            fill="x",
            pady=(10, 5)
        )

        ttk.Label(
            header_frame,
            text="📊 Dashboard",
            font=("Segoe UI", 28, "bold"),
            bootstyle="primary"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            header_frame,
            text="Monitor your Excel automation activity at a glance",
            font=("Segoe UI", 11),
            bootstyle="secondary"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # ==================================================
        # AUTOMATION OVERVIEW
        # ==================================================

        ttk.Label(
            self.frame,
            text="Automation Overview",
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            pady=(30, 10)
        )

        cards_frame = ttk.Frame(
            self.frame
        )

        cards_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        for column in range(4):

            cards_frame.columnconfigure(
                column,
                weight=1,
                uniform="cards"
            )

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
        # STATUS SECTION
        # ==================================================

        ttk.Separator(
            self.frame,
            orient="horizontal"
        ).pack(
            fill="x",
            pady=25
        )

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
        ).pack(
            anchor="w"
        )

        ttk.Label(
            status_frame,
            text=(
                "Use the Automation section to clean, validate, "
                "format, analyze and generate reports from your Excel files."
            ),
            font=("Segoe UI", 11),
            bootstyle="secondary",
            wraplength=1000
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

        self.last_run.pack(
            anchor="w"
        )

        # ==================================================
        # PERFORMANCE SUMMARY
        # ==================================================

        ttk.Separator(
            self.frame,
            orient="horizontal"
        ).pack(
            fill="x",
            pady=25
        )

        ttk.Label(
            self.frame,
            text="Performance Summary",
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        self.performance_frame = ttk.Frame(
            self.frame
        )

        self.performance_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        self.performance_labels = {}

        performance_items = [
            ("Total Runs", "total_runs"),
            ("Success Rate", "success_rate"),
            ("Average Time", "average_time"),
            ("Last Processing", "last_processing")
        ]

        for column in range(4):

            self.performance_frame.columnconfigure(
                column,
                weight=1,
                uniform="performance"
            )

        for column, (title, key) in enumerate(
            performance_items
        ):

            card = ttk.Frame(
                self.performance_frame,
                padding=15,
                relief="ridge"
            )

            card.grid(
                row=0,
                column=column,
                padx=5,
                pady=5,
                sticky="nsew"
            )

            ttk.Label(
                card,
                text=title,
                font=("Segoe UI", 10, "bold"),
                bootstyle="secondary"
            ).pack(
                anchor="w"
            )

            value_label = ttk.Label(
                card,
                text="0",
                font=("Segoe UI", 18, "bold")
            )

            value_label.pack(
                anchor="w",
                pady=(8, 0)
            )

            self.performance_labels[key] = value_label

        # ==================================================
        # AUTOMATION ACTIVITY
        # ==================================================

        ttk.Separator(
            self.frame,
            orient="horizontal"
        ).pack(
            fill="x",
            pady=25
        )

        ttk.Label(
            self.frame,
            text="Automation Activity",
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        self.chart_frame = ttk.Frame(
            self.frame,
            height=320
        )

        self.chart_frame.pack(
            fill="x",
            pady=(0, 30)
        )

        self.chart_frame.pack_propagate(
            False
        )

        self.create_activity_chart()

        # ==================================================
        # INITIAL DATA
        # ==================================================

        self.update_performance()

    # ======================================================
    # SCROLLING
    # ======================================================

    def _update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def _resize_inner_frame(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    def _on_mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ======================================================
    # LOAD HISTORY
    # ======================================================

    def load_history(self):

        if not HISTORY_FILE.exists():
            return []

        try:

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                history = json.load(file)

            if isinstance(history, list):
                return history

        except Exception:
            pass

        return []

    # ======================================================
    # UPDATE DASHBOARD CARDS
    # ======================================================

    def update_cards(
        self,
        files,
        total,
        duplicates,
        final
    ):

        self.files.set_value(
            files
        )

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

        self.update_performance()

        self.create_activity_chart()

        self.frame.update_idletasks()

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # ======================================================
    # PERFORMANCE SUMMARY
    # ======================================================

    def update_performance(self):

        history = self.load_history()

        if not history:

            self.performance_labels[
                "total_runs"
            ].config(
                text="0"
            )

            self.performance_labels[
                "success_rate"
            ].config(
                text="0%"
            )

            self.performance_labels[
                "average_time"
            ].config(
                text="0 sec"
            )

            self.performance_labels[
                "last_processing"
            ].config(
                text="0 sec"
            )

            return

        total_runs = len(
            history
        )

        successful_runs = sum(
            1
            for record in history
            if str(
                record.get(
                    "status",
                    ""
                )
            ).lower() == "success"
        )

        success_rate = (
            successful_runs
            / total_runs
        ) * 100

        processing_times = []

        for record in history:

            try:

                processing_time = float(
                    record.get(
                        "processing_time",
                        0
                    )
                )

                processing_times.append(
                    processing_time
                )

            except (
                TypeError,
                ValueError
            ):
                continue

        if processing_times:

            average_time = (
                sum(processing_times)
                / len(processing_times)
            )

            last_processing = (
                processing_times[-1]
            )

        else:

            average_time = 0
            last_processing = 0

        self.performance_labels[
            "total_runs"
        ].config(
            text=str(
                total_runs
            )
        )

        self.performance_labels[
            "success_rate"
        ].config(
            text=f"{success_rate:.1f}%"
        )

        self.performance_labels[
            "average_time"
        ].config(
            text=f"{average_time:.2f} sec"
        )

        self.performance_labels[
            "last_processing"
        ].config(
            text=f"{last_processing:.2f} sec"
        )

    # ======================================================
    # AUTOMATION ACTIVITY CHART
    # ======================================================

    def create_activity_chart(self):

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        history = self.load_history()

        if not history:

            ttk.Label(
                self.chart_frame,
                text="No automation history available.",
                bootstyle="secondary"
            ).pack(
                pady=20
            )

            return

        # ==================================================
        # PREPARE DATA
        # ==================================================

        run_counts = {}

        for record in history:

            date_text = record.get(
                "date_time",
                ""
            )

            try:

                date_value = datetime.strptime(
                    date_text,
                    "%d-%m-%Y %I:%M:%S %p"
                )

                date_key = date_value.strftime(
                    "%d-%m"
                )

            except ValueError:

                date_key = "Unknown"

            run_counts[date_key] = (
                run_counts.get(
                    date_key,
                    0
                ) + 1
            )

        x_labels = list(
            run_counts.keys()
        )

        values = list(
            run_counts.values()
        )

        # ==================================================
        # THEME
        # ==================================================

        style = ttk.Style()

        try:

            bg_color = style.colors.bg
            fg_color = style.colors.fg

        except Exception:

            bg_color = "#000000"
            fg_color = "#FFFFFF"

        # ==================================================
        # MATPLOTLIB
        # ==================================================

        figure, axis = plt.subplots(
            figsize=(10, 3.2),
            dpi=100
        )

        figure.patch.set_facecolor(
            bg_color
        )

        axis.set_facecolor(
            bg_color
        )

        axis.bar(
            x_labels,
            values
        )

        axis.set_title(
            "Automation Runs by Date",
            color=fg_color,
            fontsize=12,
            fontweight="bold"
        )

        axis.set_xlabel(
            "Date",
            color=fg_color
        )

        axis.set_ylabel(
            "Number of Runs",
            color=fg_color
        )

        axis.tick_params(
            axis="x",
            colors=fg_color
        )

        axis.tick_params(
            axis="y",
            colors=fg_color
        )

        for spine in axis.spines.values():

            spine.set_color(
                fg_color
            )

        axis.grid(
            axis="y",
            alpha=0.2
        )

        figure.tight_layout(
            pad=1.5
        )

        # ==================================================
        # TKINTER CANVAS
        # ==================================================

        canvas = FigureCanvasTkAgg(
            figure,
            master=self.chart_frame
        )

        canvas.draw()

        canvas_widget = (
            canvas.get_tk_widget()
        )

        canvas_widget.pack(
            fill="both",
            expand=True
        )

        self.activity_figure = figure
        self.activity_canvas = canvas