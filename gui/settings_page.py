import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

import json
from pathlib import Path


class SettingsPage:

    SETTINGS_FILE = Path("config") / "settings.json"

    def __init__(self, parent, app):

        self.app = app

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        ttk.Label(
            self.frame,
            text="⚙ Settings",
            font=("Segoe UI", 28, "bold"),
            bootstyle="primary"
        ).pack(pady=(30, 10))

        ttk.Label(
            self.frame,
            text="Configure your Excel Automation Toolkit.",
            font=("Segoe UI", 13)
        ).pack(pady=(0, 30))

        # --------------------------------------------------
        # SETTINGS FRAME
        # --------------------------------------------------

        settings_frame = ttk.Frame(self.frame)
        settings_frame.pack(fill="x", padx=50)

        # --------------------------------------------------
        # THEME
        # --------------------------------------------------

        ttk.Label(
            settings_frame,
            text="Application Theme",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(10, 5))

        self.theme_var = ttk.StringVar(
            value=self.app.settings.get("theme", "flatly")
        )

        self.theme_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.theme_var,
            values=[
                "flatly",
                "darkly",
                "superhero",
                "cyborg",
                "solar",
                "minty",
                "litera",
                "journal",
                "pulse",
                "sandstone"
            ],
            state="readonly",
            width=40
        )

        self.theme_combo.pack(
            anchor="w",
            pady=5
        )

        # --------------------------------------------------
        # INPUT FOLDER
        # --------------------------------------------------

        ttk.Label(
            settings_frame,
            text="Default Input Folder",
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        input_frame = ttk.Frame(settings_frame)
        input_frame.pack(fill="x")

        self.input_entry = ttk.Entry(
            input_frame,
            width=60
        )

        self.input_entry.pack(
            side=LEFT,
            fill="x",
            expand=True
        )

        ttk.Button(
            input_frame,
            text="📂 Browse",
            command=self.browse_input,
            bootstyle="info"
        ).pack(
            side=LEFT,
            padx=10
        )

        # Load saved input folder
        saved_input = self.app.settings.get(
            "input_folder",
            ""
        )

        if saved_input:
            self.input_entry.insert(
                0,
                saved_input
            )

        # --------------------------------------------------
        # OUTPUT FOLDER
        # --------------------------------------------------

        ttk.Label(
            settings_frame,
            text="Default Output Folder",
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        output_frame = ttk.Frame(settings_frame)
        output_frame.pack(fill="x")

        self.output_entry = ttk.Entry(
            output_frame,
            width=60
        )

        self.output_entry.pack(
            side=LEFT,
            fill="x",
            expand=True
        )

        ttk.Button(
            output_frame,
            text="📂 Browse",
            command=self.browse_output,
            bootstyle="info"
        ).pack(
            side=LEFT,
            padx=10
        )

        # Load saved output folder
        saved_output = self.app.settings.get(
            "output_folder",
            ""
        )

        if saved_output:
            self.output_entry.insert(
                0,
                saved_output
            )

        # --------------------------------------------------
        # SEPARATOR
        # --------------------------------------------------

        ttk.Separator(
            self.frame,
            orient="horizontal"
        ).pack(
            fill="x",
            padx=50,
            pady=35
        )

        # --------------------------------------------------
        # BUTTONS
        # --------------------------------------------------

        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.pack()

        ttk.Button(
            buttons_frame,
            text="💾 Save Settings",
            command=self.save_settings,
            bootstyle="success",
            width=20
        ).grid(
            row=0,
            column=0,
            padx=10
        )
        ttk.Button(
            buttons_frame,
            text= "🎨 Apply Theme",
            command=self.apply_theme,
            bootstyle="info",
            width=20
        ).grid(
            row=0,
            column=1,
            padx=10
        )

        ttk.Button(
            buttons_frame,
            text="🔄 Reset",
            command=self.reset_settings,
            bootstyle="warning",
            width=20
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        # --------------------------------------------------
        # STATUS
        # --------------------------------------------------

        self.status = ttk.Label(
            self.frame,
            text="Settings ready.",
            font=("Segoe UI", 11),
            bootstyle="secondary"
        )

        self.status.pack(pady=25)

    # ======================================================
    # BROWSE INPUT
    # ======================================================

    def browse_input(self):

        folder = filedialog.askdirectory()

        if folder:

            self.input_entry.delete(
                0,
                END
            )

            self.input_entry.insert(
                0,
                folder
            )

    # ======================================================
    # BROWSE OUTPUT
    # ======================================================

    def browse_output(self):

        folder = filedialog.askdirectory()

        if folder:

            self.output_entry.delete(
                0,
                END
            )

            self.output_entry.insert(
                0,
                folder
            )

    # ======================================================
    # SAVE SETTINGS
    # ======================================================

    def save_settings(self):

        self.app.settings = {
            "theme": self.theme_var.get(),
            "input_folder": self.input_entry.get().strip(),
            "output_folder": self.output_entry.get().strip()
        }

        # Create config directory
        self.SETTINGS_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        try:

            with open(
                self.SETTINGS_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.app.settings,
                    file,
                    indent=4
                )

            self.status.config(
                text="Settings saved successfully.",
                bootstyle="success"
            )

            messagebox.showinfo(
                "Settings",
                "Settings saved successfully!"
            )

        except Exception as e:

            messagebox.showerror(
                "Settings Error",
                f"Unable to save settings:\n\n{e}"
            )
# ======================================================
# APPLY THEME
# ======================================================

    def apply_theme(self):

        selected_theme = self.theme_var.get()

        try:

            self.app.root.style.theme_use(
                selected_theme
            )

            self.app.settings["theme"] = selected_theme

            self.status.config(
                text=f"Theme '{selected_theme}' applied.",
                bootstyle="success"
            )

        except Exception as e:

            messagebox.showerror(
                "Theme Error",
                f"Unable to apply theme:\n\n{e}"
            )

    # ======================================================
    # RESET
    # ======================================================

    def reset_settings(self):

        self.theme_var.set("flatly")

        self.input_entry.delete(
            0,
            END
        )

        self.output_entry.delete(
            0,
            END
        )

        # Reset application settings
        self.app.settings = {
            "theme": "flatly",
            "input_folder": "",
            "output_folder": ""
        }

        # Remove saved settings file
        try:

            if self.SETTINGS_FILE.exists():
                self.SETTINGS_FILE.unlink()

        except Exception as e:

            messagebox.showwarning(
                "Reset Warning",
                f"Settings reset in the application, "
                f"but the saved file could not be removed.\n\n{e}"
            )

        self.status.config(
            text="Settings reset.",
            bootstyle="warning"
        )