import customtkinter as ctk
from tkinter import messagebox

from ui import theme
from ui.widgets.icon_factory import make_icon
from ui.widgets.toast import show_toast
from ui.windows.add_password import AddPasswordWindow
from ui.windows.edit_password import EditPasswordWindow
from ui.windows.pin_dialog import CreatePinDialog, VerifyPinDialog
from database.models import Password, User
from utils.logger import get_logger

logger = get_logger()


class VaultPage(ctk.CTkFrame):

    def __init__(self, master, user_id):
        super().__init__(master, fg_color=theme.BACKGROUND)

        self.user_id = user_id
        self.rows = {}
        self.pin_unlocked = False

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=25, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            image=make_icon("vault", size=22, color=theme.TEXT),
            text="  Password Vault",
            compound="left",
            font=theme.TITLE_FONT
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            header, text="  Add Password",
            image=make_icon("plus", size=16, color="#FFFFFF"),
            width=180, height=40,
            fg_color=theme.PRIMARY, hover_color=theme.PRIMARY_HOVER, command=self.add_password
        ).grid(row=0, column=1, sticky="e")

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", padx=25, pady=(0, 15))
        search_frame.grid_columnconfigure(0, weight=1)

        self.search = ctk.CTkEntry(search_frame, height=40, placeholder_text="Search...")
        self.search.grid(row=0, column=0, sticky="ew")
        self.search.bind("<KeyRelease>", lambda e: self.load_passwords())

        self.table = ctk.CTkScrollableFrame(self, fg_color=theme.SURFACE)
        self.table.grid(row=2, column=0, sticky="nsew", padx=25, pady=(0, 25))

        self.table.grid_columnconfigure(0, weight=2)
        self.table.grid_columnconfigure(1, weight=2)
        self.table.grid_columnconfigure(2, weight=1)
        self.table.grid_columnconfigure(3, weight=2)
        self.table.grid_columnconfigure(4, weight=2)

        self.load_passwords()

    def load_passwords(self):

        for widget in self.table.winfo_children():
            widget.destroy()

        self.rows = {}

        headers = ["Website", "Username", "Category", "Password", "Actions"]

        for col, text in enumerate(headers):
            ctk.CTkLabel(
                self.table, text=text, font=("Segoe UI", 15, "bold"), text_color=theme.TEXT
            ).grid(row=0, column=col, padx=15, pady=15, sticky="w")

        passwords = Password.get_all(self.user_id)

        query = self.search.get().strip().lower()

        if query:
            passwords = [
                p for p in passwords
                if query in p[5].lower() or query in p[3].lower() or query in p[6].lower()
            ]

        if not passwords:
            ctk.CTkLabel(
                self.table, text="No passwords found.",
                font=theme.TEXT_FONT, text_color=theme.TEXT_SECONDARY
            ).grid(row=1, column=0, columnspan=5, pady=40)
            return

        for row, password in enumerate(passwords, start=1):

            password_id = password[0]
            username = password[3]
            real_password = password[4]
            website = password[5]
            category = password[6]

            ctk.CTkLabel(self.table, text=website, font=theme.TEXT_FONT, text_color=theme.TEXT).grid(
                row=row, column=0, padx=15, pady=10, sticky="w"
            )
            ctk.CTkLabel(self.table, text=username, font=theme.TEXT_FONT, text_color=theme.TEXT).grid(
                row=row, column=1, padx=15, pady=10, sticky="w"
            )
            ctk.CTkLabel(self.table, text=category, font=theme.TEXT_FONT, text_color=theme.TEXT).grid(
                row=row, column=2, padx=15, pady=10, sticky="w"
            )

            password_label = ctk.CTkLabel(self.table, text="•" * 10, font=theme.TEXT_FONT, text_color=theme.TEXT)
            password_label.grid(row=row, column=3, padx=15, pady=10, sticky="w")

            self.rows[password_id] = {"label": password_label, "real": real_password, "visible": False}

            actions = ctk.CTkFrame(self.table, fg_color="transparent")
            actions.grid(row=row, column=4, padx=10, pady=5, sticky="w")

            ctk.CTkButton(
                actions, image=make_icon("eye", size=16, color=theme.TEXT), text="",
                width=32, height=28, fg_color="transparent", hover_color=theme.BORDER,
                command=lambda pid=password_id: self.request_toggle_visibility(pid)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                actions, image=make_icon("copy", size=16, color=theme.TEXT), text="",
                width=32, height=28, fg_color="transparent", hover_color=theme.BORDER,
                command=lambda pw=real_password: self.request_copy_password(pw)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                actions, image=make_icon("edit", size=16, color=theme.TEXT), text="",
                width=32, height=28, fg_color="transparent", hover_color=theme.BORDER,
                command=lambda p=password: self.edit_password(p)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                actions, image=make_icon("trash", size=16, color=theme.ERROR), text="",
                width=32, height=28, fg_color="transparent", hover_color=theme.ERROR,
                command=lambda pid=password_id: self.delete_password(pid)
            ).pack(side="left", padx=2)

    # ==========================
    # Protecao por PIN
    # ==========================

    def ensure_unlocked(self, action):
        """
        Garante que o utilizador desbloqueou com PIN antes de executar 'action'.
        Se ainda nao tiver PIN definido, obriga a criar um primeiro.
        """

        if self.pin_unlocked:
            action()
            return

        if not User.has_pin(self.user_id):

            def after_create():
                self.pin_unlocked = True
                show_toast(self.winfo_toplevel(), "PIN created successfully!", kind="success")
                action()

            CreatePinDialog(self, self.user_id, on_success=after_create)
            return

        def after_verify():
            self.pin_unlocked = True
            action()

        VerifyPinDialog(self, self.user_id, on_success=after_verify)

    def request_toggle_visibility(self, password_id):
        self.ensure_unlocked(lambda: self.toggle_visibility(password_id))

    def request_copy_password(self, real_password):
        self.ensure_unlocked(lambda: self.copy_password(real_password))

    # ==========================
    # Acoes
    # ==========================

    def toggle_visibility(self, password_id):

        row = self.rows.get(password_id)
        if row is None:
            return

        row["visible"] = not row["visible"]
        row["label"].configure(text=row["real"] if row["visible"] else "•" * 10)

    def copy_password(self, real_password):

        self.clipboard_clear()
        self.clipboard_append(real_password)

        show_toast(self.winfo_toplevel(), "Password copied to clipboard!", kind="success")

    def delete_password(self, password_id):

        confirm = messagebox.askyesno("Delete Password", "Are you sure you want to delete this password?")

        if not confirm:
            return

        Password.delete(password_id)
        logger.info(f"Password deleted: id={password_id}")

        show_toast(self.winfo_toplevel(), "Password deleted.", kind="warning")

        self.load_passwords()

    def edit_password(self, password):
        EditPasswordWindow(self, password)

    def add_password(self):
        AddPasswordWindow(self, self.user_id)
