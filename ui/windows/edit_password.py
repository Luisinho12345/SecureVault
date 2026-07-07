import customtkinter as ctk

from ui import theme
from database.models import Password
from utils.validators import validate_password_entry
from utils.constants import DEFAULT_CATEGORIES
from utils.logger import get_logger
from ui.widgets.toast import show_toast

logger = get_logger()


class EditPasswordWindow(ctk.CTkToplevel):

    def __init__(self, master, password):
        super().__init__(master)

        self.master = master
        self.password_id = password[0]

        self.title("Edit Password")
        self.geometry("450x540")
        self.resizable(False, False)

        self.grab_set()

        ctk.CTkLabel(self, text="Edit Password", font=theme.TITLE_FONT).pack(pady=(20, 15))

        self.website = ctk.CTkEntry(self, width=350, height=40, placeholder_text="Website")
        self.website.insert(0, password[5])
        self.website.pack(pady=8)

        self.username = ctk.CTkEntry(self, width=350, height=40, placeholder_text="Username / Email")
        self.username.insert(0, password[3])
        self.username.pack(pady=8)

        self.password_entry = ctk.CTkEntry(self, width=350, height=40, placeholder_text="Password")
        self.password_entry.insert(0, password[4])
        self.password_entry.pack(pady=8)

        current_category = password[6]

        # Se a categoria guardada nao estiver na lista padrao, adiciona-a
        # temporariamente as opcoes para nao a perder ao editar.
        values = list(DEFAULT_CATEGORIES)
        if current_category not in values:
            values.append(current_category)

        self.category = ctk.CTkComboBox(
            self,
            width=350,
            height=40,
            values=values
        )
        self.category.set(current_category)
        self.category.pack(pady=8)

        self.message = ctk.CTkLabel(self, text="", font=theme.SMALL_FONT)
        self.message.pack(pady=(5, 5))

        ctk.CTkButton(
            self, text="Save Changes", width=350, height=40,
            fg_color=theme.PRIMARY, hover_color=theme.PRIMARY_HOVER, command=self.save
        ).pack(pady=15)

    def save(self):

        website = self.website.get()
        username = self.username.get()
        password = self.password_entry.get()
        category = self.category.get()

        valid, msg = validate_password_entry(website, username, password, category)

        if not valid:
            self.message.configure(text=msg, text_color="red")
            return

        Password.update(self.password_id, website, username, password, website, category)

        logger.info(f"Password updated: id={self.password_id}")

        self.destroy()
        self.master.load_passwords()

        show_toast(self.master.winfo_toplevel(), "Password updated!", kind="success")
