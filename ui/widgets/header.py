import customtkinter as ctk
from datetime import datetime

from ui import theme
from ui.widgets.icon_factory import make_icon


class Header(ctk.CTkFrame):

    def __init__(self, master, username="User"):
        super().__init__(
            master,
            fg_color="transparent",
            height=90
        )

        self.grid_columnconfigure(0, weight=1)

        left = ctk.CTkFrame(self, fg_color="transparent")
        left.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            left,
            text=f"Welcome back, {username}",
            font=("Segoe UI", 28, "bold"),
            text_color=theme.TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text=datetime.now().strftime("%A, %d %B %Y"),
            font=("Segoe UI", 14),
            text_color=theme.TEXT_SECONDARY
        ).pack(anchor="w")

        right = ctk.CTkFrame(self, fg_color="transparent")
        right.grid(row=0, column=1, sticky="e")

        self.search = ctk.CTkEntry(
            right,
            width=250,
            height=40,
            placeholder_text="Search...",
        )
        self.search.pack(side="left", padx=10)

        avatar = ctk.CTkLabel(
            right,
            image=make_icon("gear", size=28, color=theme.TEXT_SECONDARY),
            text=""
        )
        avatar.pack(side="left")
