import customtkinter as ctk

from ui import theme
from database.models import User
from security.hashing import hash_password


class RegisterPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=theme.BACKGROUND)

        ctk.CTkLabel(
            self,
            text="Create Account",
            font=theme.TITLE_FONT
        ).pack(pady=(80, 40))

        self.username = ctk.CTkEntry(
            self,
            width=350,
            height=45,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(
            self,
            width=350,
            height=45,
            placeholder_text="Password",
            show="•"
        )
        self.password.pack(pady=10)

        self.message = ctk.CTkLabel(
            self,
            text=""
        )
        self.message.pack(pady=15)

        ctk.CTkButton(
            self,
            text="Create Account",
            width=350,
            height=45,
            command=self.register
        ).pack(pady=10)

    def register(self):

        username = self.username.get().strip()
        password = self.password.get()

        if username == "" or password == "":
            self.message.configure(
                text="Fill all fields.",
                text_color="red"
            )
            return

        if User.exists(username):
            self.message.configure(
                text="Username already exists.",
                text_color="red"
            )
            return

        User.create(
            username,
            hash_password(password)
        )

        self.message.configure(
            text="Account created successfully!",
            text_color="green"
        )