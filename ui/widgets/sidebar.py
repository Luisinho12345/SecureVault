import customtkinter as ctk

from ui import theme


class Sidebar(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            width=240,
            fg_color=theme.SURFACE,
            corner_radius=0
        )

        self.grid_propagate(False)

        ctk.CTkLabel(
            self,
            text="🔐",
            font=("Segoe UI Emoji", 50)
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            self,
            text="SecureVault",
            font=("Segoe UI", 22, "bold"),
            text_color=theme.TEXT
        ).pack(pady=(0, 40))

        self.create_button("🏠 Dashboard")
        self.create_button("🔑 Vault")
        self.create_button("🎲 Generator")
        self.create_button("⚙ Settings")

        ctk.CTkLabel(self, text="").pack(expand=True)

        self.create_button("🚪 Logout")

    def create_button(self, text):
        button = ctk.CTkButton(
            self,
            text=text,
            width=200,
            height=45,
            fg_color="transparent",
            hover_color=theme.PRIMARY,
            text_color=theme.TEXT,
            anchor="w",
            corner_radius=10,
            font=("Segoe UI", 15)
        )

        button.pack(pady=6)

        return button