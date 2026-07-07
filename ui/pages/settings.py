import customtkinter as ctk
from tkinter import messagebox

from ui import theme
from ui.widgets.page_layout import BasePage
from ui.windows.pin_dialog import CreatePinDialog
from utils.helpers import create_backup, list_backups, restore_backup
from database.models import User
from utils.logger import get_logger

logger = get_logger()


class SettingsPage(BasePage):

    def __init__(self, master):
        super().__init__(master, active_page="settings")

    def refresh(self):
        self.refresh_backups()

    def build_content(self, content):

        content.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            content, text="Settings", font=theme.TITLE_FONT, text_color=theme.TEXT
        ).grid(row=0, column=0, sticky="w", pady=(10, 25))

        # ==========================
        # Card: Access PIN
        # ==========================

        pin_card = ctk.CTkFrame(content, fg_color=theme.SURFACE, corner_radius=15)
        pin_card.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        pin_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            pin_card, text="Access PIN", font=("Segoe UI", 18, "bold"), text_color=theme.TEXT
        ).grid(row=0, column=0, sticky="w", padx=25, pady=(20, 5))

        ctk.CTkLabel(
            pin_card,
            text="Your PIN is required to view or copy any password, even after logging in.\n"
                 "Keep it different from your login password.",
            font=theme.SMALL_FONT,
            text_color=theme.TEXT_SECONDARY,
            justify="left"
        ).grid(row=1, column=0, sticky="w", padx=25, pady=(0, 15))

        has_pin = User.has_pin(self.app.current_user_id)

        button_text = "Change PIN" if has_pin else "Create PIN"

        ctk.CTkButton(
            pin_card, text=button_text, height=40, width=180,
            fg_color=theme.PRIMARY, hover_color=theme.PRIMARY_HOVER,
            command=self.open_pin_dialog
        ).grid(row=2, column=0, sticky="w", padx=25, pady=(0, 20))

        # ==========================
        # Card: Backups
        # ==========================

        card = ctk.CTkFrame(content, fg_color=theme.SURFACE, corner_radius=15)
        card.grid(row=2, column=0, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text="Database Backups", font=("Segoe UI", 18, "bold"), text_color=theme.TEXT
        ).grid(row=0, column=0, sticky="w", padx=25, pady=(20, 5))

        ctk.CTkLabel(
            card,
            text="Save a copy of your encrypted database, or restore a previous one.",
            font=theme.SMALL_FONT,
            text_color=theme.TEXT_SECONDARY
        ).grid(row=1, column=0, sticky="w", padx=25, pady=(0, 15))

        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.grid(row=2, column=0, sticky="ew", padx=25, pady=(0, 10))
        top_row.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            top_row, text="+ Create Backup Now", height=40,
            fg_color=theme.PRIMARY, hover_color=theme.PRIMARY_HOVER,
            command=self.do_backup
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            card, text="Available backups:", font=theme.TEXT_FONT, text_color=theme.TEXT
        ).grid(row=3, column=0, sticky="w", padx=25, pady=(15, 5))

        self.backups_frame = ctk.CTkScrollableFrame(card, fg_color=theme.BACKGROUND, height=200)
        self.backups_frame.grid(row=4, column=0, sticky="ew", padx=25, pady=(0, 25))
        self.backups_frame.grid_columnconfigure(0, weight=1)

        self.refresh_backups()

    def open_pin_dialog(self):

        def on_success():
            show_toast_safe(self, "PIN saved successfully!")
            self.app.show_settings()

        CreatePinDialog(self, self.app.current_user_id, on_success=on_success)

    def do_backup(self):

        path = create_backup()

        if path is None:
            messagebox.showerror("Error", "No database found.")
            return

        logger.info(f"Backup created: {path}")

        self.refresh_backups()

    def refresh_backups(self):

        for widget in self.backups_frame.winfo_children():
            widget.destroy()

        backups = list_backups()

        if not backups:
            ctk.CTkLabel(
                self.backups_frame, text="No backups yet.",
                font=theme.SMALL_FONT, text_color=theme.TEXT_SECONDARY
            ).grid(row=0, column=0, pady=20)
            return

        for row, filename in enumerate(backups):

            row_frame = ctk.CTkFrame(self.backups_frame, fg_color="transparent")
            row_frame.grid(row=row, column=0, sticky="ew", pady=4)
            row_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                row_frame, text=filename, font=theme.SMALL_FONT, text_color=theme.TEXT
            ).grid(row=0, column=0, sticky="w")

            ctk.CTkButton(
                row_frame, text="Restore", width=90, height=28,
                fg_color="transparent", border_width=1, border_color=theme.BORDER,
                hover_color=theme.WARNING,
                command=lambda f=filename: self.do_restore(f)
            ).grid(row=0, column=1, sticky="e")

    def do_restore(self, filename):

        confirm = messagebox.askyesno(
            "Restore Backup",
            f"This will replace your current database with '{filename}'.\n"
            "Any passwords added after this backup will be lost.\n\n"
            "Are you sure you want to continue?"
        )

        if not confirm:
            return

        success = restore_backup(filename)

        if success:
            logger.info(f"Database restored from backup: {filename}")
            messagebox.showinfo("Restore Complete", "Database restored successfully. Please log in again.")
            self.app.show_login()
        else:
            messagebox.showerror("Error", "Could not restore the selected backup.")


def show_toast_safe(page, message):
    from ui.widgets.toast import show_toast
    show_toast(page.winfo_toplevel(), message, kind="success")
