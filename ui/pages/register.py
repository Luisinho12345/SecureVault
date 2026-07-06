import customtkinter as ctk

from ui import theme
from database.models import User
from security.hashing import hash_password
from security.validators import validate_username, validate_master_password
from utils.logger import get_logger

logger = get_logger()


class RegisterPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=theme.BACKGROUND)

        ctk.CTkLabel(
            self,
            text="Create Account",
            font=theme.TITLE_FONT
        ).pack(pady=(60, 10))

        ctk.CTkLabel(
            self,
            text="Create your SecureVault account",
            font=theme.TEXT_FONT,
            text_color=theme.TEXT_SECONDARY
        ).pack(pady=(0, 30))

        self.username = ctk.CTkEntry(
            self, width=350, height=45, placeholder_text="Username"
        )
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(
            self, width=350, height=45, placeholder_text="Password", show="•"
        )
        self.password.pack(pady=10)

        self.confirm_password = ctk.CTkEntry(
            self, width=350, height=45, placeholder_text="Confirm Password", show="•"
        )
        self.confirm_password.pack(pady=10)

        self.message = ctk.CTkLabel(self, text="")
        self.message.pack(pady=15)

        ctk.CTkButton(
            self,
            text="Create Account",
            width=350,
            height=45,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_HOVER,
            command=self.register
        ).pack(pady=(10, 10))

        ctk.CTkButton(
            self,
            text="Back to Login",
            width=350,
            height=45,
            fg_color="transparent",
            border_width=1,
            border_color=theme.BORDER,
            hover_color="#263241",
            command=self.master.show_login
        ).pack()

    def register(self):

        username = self.username.get().strip()
        password = self.password.get()
        confirm = self.confirm_password.get()

        valid_username, msg = validate_username(username)
        if not valid_username:
            self.message.configure(text=msg, text_color="red")
            return

        valid_password, msg = validate_master_password(password)
        if not valid_password:
            self.message.configure(text=msg, text_color="red")
            return

        if password != confirm:
            self.message.configure(text="Passwords do not match.", text_color="red")
            return

        if User.exists(username):
            self.message.configure(text="Username already exists.", text_color="red")
            return

        User.create(username, hash_password(password))

        logger.info(f"New user registered: {username}")

        self.message.configure(text="Account created successfully!", text_color="green")

        self.after(1200, self.master.show_login)
