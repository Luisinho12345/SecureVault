import customtkinter as ctk

from ui import theme


class LoginPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=theme.BACKGROUND)

        # ----------------------------
        # Layout principal
        # ----------------------------

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ==========================================================
        # Painel Esquerdo
        # ==========================================================

        left = ctk.CTkFrame(
            self,
            fg_color=theme.SURFACE,
            corner_radius=0
        )
        left.grid(row=0, column=0, sticky="nsew")

        left.pack_propagate(False)

        logo = ctk.CTkLabel(
            left,
            text="🔐",
            font=("Segoe UI Emoji", 82)
        )
        logo.pack(pady=(110, 20))

        title = ctk.CTkLabel(
            left,
            text="SecureVault",
            font=theme.TITLE_FONT,
            text_color=theme.TEXT
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            left,
            text="Professional Password Manager",
            font=theme.SUBTITLE_FONT,
            text_color=theme.TEXT_SECONDARY
        )
        subtitle.pack(pady=(10, 40))

        description = ctk.CTkLabel(
            left,
            text=(
                "Store all your passwords securely.\n"
                "Encrypted. Simple. Fast."
            ),
            font=theme.TEXT_FONT,
            justify="center",
            text_color=theme.TEXT_SECONDARY
        )
        description.pack()

        # ==========================================================
        # Painel Direito
        # ==========================================================

        right = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        right.grid(row=0, column=1, sticky="nsew")

        login_title = ctk.CTkLabel(
            right,
            text="Welcome Back",
            font=theme.TITLE_FONT,
            text_color=theme.TEXT
        )
        login_title.pack(pady=(100, 10))

        login_subtitle = ctk.CTkLabel(
            right,
            text="Login to your SecureVault account",
            font=theme.TEXT_FONT,
            text_color=theme.TEXT_SECONDARY
        )
        login_subtitle.pack(pady=(0, 35))

        self.username = ctk.CTkEntry(
            right,
            width=340,
            height=45,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(
            right,
            width=340,
            height=45,
            placeholder_text="Password",
            show="•"
        )
        self.password.pack(pady=10)

        self.login_button = ctk.CTkButton(
            right,
            text="Login",
            width=340,
            height=45,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_HOVER,
            command=self.login
        )
        self.login_button.pack(pady=(30, 15))

        self.register_button = ctk.CTkButton(
            right,
            text="Create Account",
            width=340,
            height=45,
            fg_color="transparent",
            border_width=1,
            border_color=theme.BORDER,
            hover_color="#263241",
            command=self.register
        )
        self.register_button.pack()

        version = ctk.CTkLabel(
            right,
            text="SecureVault v1.0",
            font=("Segoe UI", 11),
            text_color="#6B7280"
        )
        version.pack(side="bottom", pady=20)

    # ==========================================================
    # Eventos
    # ==========================================================

    def login(self):
        print("Login clicked")

    def register(self):
        print("Register clicked")