import customtkinter as ctk

from ui import theme
from ui.widgets.sidebar import Sidebar
from ui.widgets.header import Header
from ui.widgets.stat_card import StatCard


class DashboardPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=theme.BACKGROUND)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        sidebar = Sidebar(self)
        sidebar.grid(row=0, column=0, sticky="ns")

        # Conteúdo
        content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=30,
            pady=25
        )

        content.grid_columnconfigure((0, 1, 2), weight=1)

        # ================= HEADER =================

        header = Header(content)
        header.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(0, 25)
        )

        # ================= CARDS =================

        passwords = StatCard(content, "Passwords", 0)
        passwords.grid(row=1, column=0, padx=10, sticky="ew")

        categories = StatCard(content, "Categories", 0)
        categories.grid(row=1, column=1, padx=10, sticky="ew")

        weak = StatCard(content, "Weak Passwords", 0, theme.ERROR)
        weak.grid(row=1, column=2, padx=10, sticky="ew")

        # ================= PASSWORDS =================

        recent = ctk.CTkFrame(
            content,
            fg_color=theme.SURFACE,
            corner_radius=15
        )

        recent.grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="nsew",
            padx=10,
            pady=30
        )

        ctk.CTkLabel(
            recent,
            text="Recent Passwords",
            font=("Segoe UI", 20, "bold"),
            text_color=theme.TEXT
        ).pack(anchor="w", padx=20, pady=(20, 15))

        for site in [
            "Github",
            "Google",
            "Discord",
            "Steam",
            "Microsoft"
        ]:

            row = ctk.CTkFrame(
                recent,
                fg_color=theme.BACKGROUND,
                corner_radius=8,
                height=45
            )

            row.pack(fill="x", padx=20, pady=5)

            ctk.CTkLabel(
                row,
                text="🔑  " + site,
                font=("Segoe UI", 15),
                text_color=theme.TEXT
            ).pack(side="left", padx=15, pady=10)

            ctk.CTkButton(
                row,
                text="View",
                width=70,
                height=30
            ).pack(side="right", padx=10)