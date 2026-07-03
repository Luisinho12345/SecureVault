import customtkinter as ctk

from ui.theme import apply_theme, WINDOW_WIDTH, WINDOW_HEIGHT
from ui.pages.login import LoginPage
from ui.pages.register import RegisterPage
from ui.pages.dashboard import DashboardPage


class SecureVaultApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        apply_theme()

        self.title("🔐 SecureVault")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(1100, 650)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.current_page = None

        # Página inicial
        self.show_login()

    def clear_page(self):
        if self.current_page is not None:
            self.current_page.destroy()

    def show_login(self):
        self.clear_page()

        self.current_page = LoginPage(self)
        self.current_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    def show_register(self):
        self.clear_page()

        self.current_page = RegisterPage(self)
        self.current_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    def show_dashboard(self):
        self.clear_page()

        self.current_page = DashboardPage(self)
        self.current_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )