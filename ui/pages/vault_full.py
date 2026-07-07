from ui.widgets.page_layout import BasePage
from ui.pages.vault import VaultPage


class VaultFullPage(BasePage):

    def __init__(self, master):
        super().__init__(master, active_page="vault")

    def build_content(self, content):
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        self.vault = VaultPage(content, user_id=self.app.current_user_id)
        self.vault.grid(row=0, column=0, sticky="nsew")

    def refresh(self):
        self.vault.load_passwords()
