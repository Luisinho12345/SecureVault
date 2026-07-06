import customtkinter as ctk

from ui.theme import apply_theme, WINDOW_WIDTH, WINDOW_HEIGHT
from ui.pages.login import LoginPage
from ui.pages.register import RegisterPage
from ui.pages.dashboard import DashboardPage
from ui.pages.vault_full import VaultFullPage
from ui.pages.generator import GeneratorPage
from ui.pages.settings import SettingsPage


class SecureVaultApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        apply_theme()

        self.title("SecureVault")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(1100, 650)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.current_page = None
        self.current_user_id = None
        self.current_username = None

        self.show_login()

    def set_current_user(self, user_id, username):
        self.current_user_id = user_id
        self.current_username = username

    def clear_page(self):
        if self.current_page is not None:
            self.current_page.destroy()

    def _show(self, page_class):
        self.clear_page()
        self.current_page = page_class(self)
        self.current_page.grid(row=0, column=0, sticky="nsew")

    def show_login(self):
        self.current_user_id = None
        self.current_username = None
        self._show(LoginPage)

    def show_register(self):
        self._show(RegisterPage)

    def show_dashboard(self):
        self._show(DashboardPage)

    def show_vault(self):
        self._show(VaultFullPage)

    def show_generator(self):
        self._show(GeneratorPage)

    def show_settings(self):
        self._show(SettingsPage)
