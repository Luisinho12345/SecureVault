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

        self.current_user_id = None
        self.current_username = None

        # Cache de instâncias de página (não recriamos do zero)
        self._pages = {}
        self._current_page_key = None

        self.show_login()

    def get_current_page(self):
        return self._pages.get(self._current_page_key)



    def set_current_user(self, user_id, username):
        self.current_user_id = user_id
        self.current_username = username

    def _clear_authenticated_pages(self):
        """Destroi apenas as páginas que dependem de um utilizador (para forçar recriação no próximo login/logout)."""
        for key in ["dashboard", "vault", "generator", "settings"]:
            page = self._pages.pop(key, None)
            if page is not None:
                page.destroy()

    def _show(self, key, page_class, *args):

        page = self._pages.get(key)

        if page is None:
            page = page_class(self, *args)
            page.grid(row=0, column=0, sticky="nsew")
            self._pages[key] = page

        # Se a página souber atualizar-se sozinha, chama refresh()
        if hasattr(page, "refresh"):
            page.refresh()

        page.tkraise()
        self._current_page_key = key

    def show_login(self):
        self.current_user_id = None
        self.current_username = None
        self._clear_authenticated_pages()
        self._show("login", LoginPage)

    def show_register(self):
        self._show("register", RegisterPage)

    def show_dashboard(self):
        self._show("dashboard", DashboardPage)

    def show_vault(self):
        self._show("vault", VaultFullPage)

    def show_generator(self):
        self._show("generator", GeneratorPage)

    def show_settings(self):
        self._show("settings", SettingsPage)

