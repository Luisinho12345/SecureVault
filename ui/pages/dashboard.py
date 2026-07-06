import customtkinter as ctk

from ui import theme
from ui.widgets.page_layout import BasePage
from ui.widgets.header import Header
from ui.widgets.stat_card import StatCard
from ui.pages.vault import VaultPage
from database.models import Password


class DashboardPage(BasePage):

    def __init__(self, master):
        super().__init__(master, active_page="dashboard")

    def build_content(self, content):

        content.grid_rowconfigure(2, weight=1)
        content.grid_columnconfigure((0, 1, 2), weight=1)

        header = Header(content, username=self.app.current_username or "User")
        header.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 25))

        user_id = self.app.current_user_id

        passwords_list = Password.get_all(user_id)

        total_passwords = len(passwords_list)
        total_categories = len({p[6] for p in passwords_list}) if passwords_list else 0

        passwords_card = StatCard(content, "Passwords", total_passwords)
        passwords_card.grid(row=1, column=0, padx=10, sticky="ew")

        categories_card = StatCard(content, "Categories", total_categories)
        categories_card.grid(row=1, column=1, padx=10, sticky="ew")

        weak_card = StatCard(content, "Weak Passwords", 0, theme.ERROR)
        weak_card.grid(row=1, column=2, padx=10, sticky="ew")

        vault = VaultPage(content, user_id=user_id)
        vault.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=(30, 0))
