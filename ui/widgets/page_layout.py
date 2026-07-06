import customtkinter as ctk

from ui import theme
from ui.widgets.sidebar import Sidebar


class BasePage(ctk.CTkFrame):
    """
    Página base com Sidebar já incluída.
    Cada página (Dashboard, Vault, Generator, Settings) herda desta classe
    e só precisa de implementar build_content().
    """

    def __init__(self, master, active_page=""):
        super().__init__(master, fg_color=theme.BACKGROUND)

        self.app = master  # master é sempre a SecureVaultApp

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        sidebar = Sidebar(self, app=self.app, active_page=active_page)
        sidebar.grid(row=0, column=0, sticky="ns")

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=30, pady=25)

        self.build_content(self.content)

    def build_content(self, content):
        raise NotImplementedError