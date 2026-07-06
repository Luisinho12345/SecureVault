import customtkinter as ctk

from ui import theme
from ui.widgets.icon_factory import make_icon


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, app=None, active_page=""):
        super().__init__(
            master,
            width=240,
            fg_color=theme.SURFACE,
            corner_radius=0
        )

        self.grid_propagate(False)

        self.app = app
        self.active_page = active_page

        ctk.CTkLabel(
            self,
            image=make_icon("vault", size=44, color=theme.PRIMARY),
            text=""
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            self,
            text="SecureVault",
            font=("Segoe UI", 22, "bold"),
            text_color=theme.TEXT
        ).pack(pady=(0, 40))

        self.create_button("Dashboard", "home", "dashboard", self._command("show_dashboard"))
        self.create_button("Vault", "vault", "vault", self._command("show_vault"))
        self.create_button("Generator", "dice", "generator", self._command("show_generator"))
        self.create_button("Settings", "gear", "settings", self._command("show_settings"))

        ctk.CTkLabel(self, text="").pack(expand=True)

        self.create_button("Logout", "logout", "logout", self._command("show_login"))

    def _command(self, method_name):
        if self.app is None:
            return None
        return getattr(self.app, method_name)

    def create_button(self, text, icon_name, page_key, command):

        is_active = page_key == self.active_page

        icon_color = "#FFFFFF" if is_active else theme.TEXT_SECONDARY

        button = ctk.CTkButton(
            self,
            text=f"  {text}",
            image=make_icon(icon_name, size=18, color=icon_color),
            width=200,
            height=45,
            fg_color=theme.PRIMARY if is_active else "transparent",
            hover_color=theme.PRIMARY_HOVER if is_active else "#263241",
            text_color=theme.TEXT,
            anchor="w",
            corner_radius=10,
            font=("Segoe UI", 15),
            command=command
        )

        button.pack(pady=4)

        return button
