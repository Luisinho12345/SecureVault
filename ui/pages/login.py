import customtkinter as ctk

from ui import theme
from database.models import User
from security.hashing import verify_password
from ui.widgets.icon_factory import make_icon
from utils.logger import get_logger
from ui.widgets.toast import show_toast

logger = get_logger()


class LoginPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=theme.BACKGROUND)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left = ctk.CTkFrame(self, fg_color=theme.SURFACE, corner_radius=0)
        left.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(left, text="🔐", font=("Segoe UI Emoji", 82)).pack(pady=(110, 20))

        ctk.CTkLabel(
            left, text="SecureVault", font=theme.TITLE_FONT, text_color=theme.TEXT
        ).pack()

        ctk.CTkLabel(
            left, text="Professional Password Manager",
            font=theme.SUBTITLE_FONT, text_color=theme.TEXT_SECONDARY
        ).pack(pady=(10, 35))

        ctk.CTkLabel(
            left,
            text="Store all your passwords securely.\nEncrypted. Fast. Reliable.",
            justify="center", font=theme.TEXT_FONT, text_color=theme.TEXT_SECONDARY
        ).pack()

        right = ctk.CTkFrame(self, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(
            right, text="Welcome Back", font=theme.TITLE_FONT, text_color=theme.TEXT
        ).pack(pady=(90, 10))

        ctk.CTkLabel(
            right, text="Login to your SecureVault account",
            font=theme.TEXT_FONT, text_color=theme.TEXT_SECONDARY
        ).pack(pady=(0, 35))

        self.username = ctk.CTkEntry(right, width=340, height=45, placeholder_text="Username")
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(
            right, width=340, height=45, placeholder_text="Password", show="•"
        )
        self.password.pack(pady=10)

        self.password.bind("<Return>", lambda e: self.login())

        self.message = ctk.CTkLabel(right, text="", font=theme.TEXT_FONT)
        self.message.pack(pady=12)

        self.login_button = ctk.CTkButton(
            right, text="Login", width=340, height=45,
            fg_color=theme.PRIMARY, hover_color=theme.PRIMARY_HOVER, command=self.login
        )
        self.login_button.pack(pady=(10, 15))

        self.register_button = ctk.CTkButton(
            right, text="Create Account", width=340, height=45,
            fg_color="transparent", border_width=1, border_color=theme.BORDER,
            hover_color="#263241", command=self.register
        )
        self.register_button.pack()

        ctk.CTkLabel(
            right, text="SecureVault v1.0", text_color="#6B7280", font=("Segoe UI", 11)
        ).pack(side="bottom", pady=20)

    def login(self):

        username = self.username.get().strip()
        password = self.password.get()

        if username == "" or password == "":
            self.message.configure(text="Please fill all fields.", text_color="red")
            return

        user = User.get_by_username(username)

        if user is None or not verify_password(password, user[2]):
            logger.warning(f"Failed login attempt for username: {username}")
            self.message.configure(text="Invalid username or password.", text_color="red")
            return

        self.master.set_current_user(user[0], user[1])

        logger.info(f"User logged in: {username}")

        self.message.configure(text="Login successful!", text_color="green")

        self.after(500, self.master.show_dashboard)

    def register(self):
        self.master.show_register()


