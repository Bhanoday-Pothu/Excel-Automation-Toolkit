import ttkbootstrap as ttk


class StatCard(ttk.Frame):

    def __init__(self, parent, title, value="0", color="primary"):

        super().__init__(
            parent,
            padding=15,
            bootstyle="light"
        )

        self.configure(width=200, height=130)

        self.pack_propagate(False)

        ttk.Label(
            self,
            text=title,
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(5, 10))

        self.value_label = ttk.Label(
            self,
            text=value,
            font=("Segoe UI", 28, "bold"),
            bootstyle=color
        )

        self.value_label.pack(expand=True)

    def set_value(self, value):
        self.value_label.config(text=str(value))