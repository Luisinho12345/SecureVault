import customtkinter as ctk

from ui import theme
from database.models import Password
from utils.validators import validate_password_entry
from utils.constants import DEFAULT_CATEGORIES
from utils.logger import get_logger
from ui.widgets.toast import show_toast

logger = get_logger()


class AddPasswordWindow(ctk.CTkToplevel):

    def __init__(self, master, user_id):
        super().__init__(master)

        self.master = master
        self.user_id = user_id

        self.title("Add Password")
        self.geometry("450x540")
        self.resizable(False, False)

        self.grab_set()

        ctk.CTkLabel(self, text="Add Password", font=theme.TITLE_FONT).pack(pady=(20, 15))

        self.website = ctk.CTkEntry(self, width=350, height=40, placeholder_text="Website")
        self.website.pack(pady=8)

        self.username = ctk.CTkEntry(self, width=350, height=40, placeholder_text="Username / Email")
        self.username.pack(pady=8)

        self.password = ctk.CTkEntry(self, width=350, height=40, placeholder_text="Password")
        self.password.pack(pady=8)

        self.category = ctk.CTkComboBox(
            self,
            width=350,
            height=40,
            values=DEFAULT_CATEGORIES
        )
        self.category.set(DEFAULT_CATEGORIES[0])
        self.category.pack(pady=8)

        self.message = ctk.CTkLabel(self, text="", font=theme.SMALL_FONT)
        self.message.pack(pady=(5, 5))

        ctk.CTkButton(
            self, text="Save", width=350, height=40,
            fg_color=theme.PRIMARY, hover_color=theme.PRIMARY_HOVER, command=self.save
        ).pack(pady=15)

    def save(self):

        website = self.website.get()
        username = self.username.get()
        password = self.password.get()
        category = self.category.get()

        valid, msg = validate_password_entry(website, username, password, category)

        if not valid:
            self.message.configure(text=msg, text_color="red")
            return

        Password.create(self.user_id, website, username, password, website, category)

        logger.info(f"Password created for user_id={self.user_id}, website={website}")

        self.destroy()

        if hasattr(self.master, "load_passwords"):
            self.master.load_passwords()

        show_toast(self.master.winfo_toplevel(), "Password saved!", kind="success")
