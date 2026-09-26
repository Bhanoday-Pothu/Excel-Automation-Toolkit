import ttkbootstrap as ttk


class StatCard(ttk.Frame):

    def __init__(self, parent, title, value="0", color="primary"):

        # Get the currently active ttkbootstrap theme
        self.style = ttk.Style()
        self.colors = self.style.colors

        # Theme-aware card colors
        self.card_bg = self.colors.inputbg
        self.card_fg = self.colors.inputfg

        super().__init__(
            parent,
            padding=18
        )

        self.configure(
            height=145
        )

        self.pack_propagate(False)

        # ==================================================
        # CARD CONTENT
        # ==================================================

        self.title_label = ttk.Label(
            self,
            text=title,
            font=("Segoe UI", 11, "bold"),
            background=self.card_bg,
            foreground=self.card_fg
        )

        self.title_label.pack(
            anchor="w",
            pady=(3, 5)
        )

        # ==================================================
        # VALUE
        # ==================================================

        self.value_label = ttk.Label(
            self,
            text=value,
            font=("Segoe UI", 30, "bold"),
            bootstyle=color,
            background=self.card_bg
        )

        self.value_label.pack(
            anchor="w",
            pady=(5, 0)
        )

        # ==================================================
        # STATUS
        # ==================================================

        self.status_label = ttk.Label(
            self,
            text="Updated after automation",
            font=("Segoe UI", 8),
            background=self.card_bg,
            foreground=self.card_fg
        )

        self.status_label.pack(
            anchor="w",
            side="bottom",
            pady=(0, 2)
        )

        # Apply theme-aware background
        self.configure(
            style="Card.TFrame"
        )

        self.update_theme()

    # ==================================================
    # THEME UPDATE
    # ==================================================

    def update_theme(self):

        self.style = ttk.Style()
        self.colors = self.style.colors

        self.card_bg = self.colors.inputbg
        self.card_fg = self.colors.inputfg

        # Configure card background
        self.style.configure(
            "Card.TFrame",
            background=self.card_bg
        )

        # Update labels
        self.title_label.configure(
            background=self.card_bg,
            foreground=self.card_fg
        )

        self.value_label.configure(
            background=self.card_bg
        )

        self.status_label.configure(
            background=self.card_bg,
            foreground=self.card_fg
        )

    # ==================================================
    # UPDATE VALUE
    # ==================================================

    def set_value(self, value):

        self.value_label.config(
            text=str(value)
        )