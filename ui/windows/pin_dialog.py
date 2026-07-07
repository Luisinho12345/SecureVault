import customtkinter as ctk

from ui import theme
from database.models import User
from security.hashing import hash_password, verify_password


def _is_valid_pin(pin):
    return pin.isdigit() and 4 <= len(pin) <= 6


class CreatePinDialog(ctk.CTkToplevel):
    """
    Pedida quando o utilizador ainda nao tem PIN definido,
    ou quando escolhe mudar o PIN nas Settings.
    """

    def __init__(self, master, user_id, on_success):
        super().__init__(master)

        self.user_id = user_id
        self.on_success = on_success

        self.title("Create Access PIN")
        self.geometry("380x330")
        self.resizable(False, False)
        self.grab_set()

        ctk.CTkLabel(
            self, text="Create Access PIN", font=theme.TITLE_FONT
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="This PIN protects your passwords from being viewed\nwithout your permission. Use 4 to 6 digits.\nIt must be different from your login password.",
            font=theme.SMALL_FONT,
            text_color=theme.TEXT_SECONDARY,
            justify="center"
        ).pack(pady=(0, 20))

        self.pin_entry = ctk.CTkEntry(
            self, width=250, height=40, placeholder_text="New PIN (4-6 digits)", show="•"
        )
        self.pin_entry.pack(pady=8)

        self.confirm_entry = ctk.CTkEntry(
            self, width=250, height=40, placeholder_text="Confirm PIN", show="•"
        )
        self.confirm_entry.pack(pady=8)

        self.message = ctk.CTkLabel(self, text="", font=theme.SMALL_FONT)
        self.message.pack(pady=(5, 5))

        ctk.CTkButton(
            self, text="Save PIN", width=250, height=40,
            fg_color=theme.PRIMARY, hover_color=theme.PRIMARY_HOVER,
            command=self.save
        ).pack(pady=10)

        self.confirm_entry.bind("<Return>", lambda e: self.save())

    def save(self):

        pin = self.pin_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        if not _is_valid_pin(pin):
            self.message.configure(text="PIN must be 4 to 6 digits.", text_color="red")
            return

        if pin != confirm:
            self.message.configure(text="PINs do not match.", text_color="red")
            return

        pin_hash = hash_password(pin)
        User.set_pin(self.user_id, pin_hash)

        self.destroy()
        self.on_success()


class VerifyPinDialog(ctk.CTkToplevel):
    """
    Pedida sempre que o utilizador quer ver/copiar uma password
    e ainda nao desbloqueou nesta sessao.
    """

    def __init__(self, master, user_id, on_success):
        super().__init__(master)

        self.user_id = user_id
        self.on_success = on_success

        self.title("Enter Access PIN")
        self.geometry("380x260")
        self.resizable(False, False)
        self.grab_set()

        ctk.CTkLabel(
            self, text="Enter Access PIN", font=theme.TITLE_FONT
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="Enter your PIN to view or copy passwords.",
            font=theme.SMALL_FONT,
            text_color=theme.TEXT_SECONDARY
        ).pack(pady=(0, 20))

        self.pin_entry = ctk.CTkEntry(
            self, width=200, height=45, placeholder_text="PIN", show="•", justify="center",
            font=("Segoe UI", 18)
        )
        self.pin_entry.pack(pady=8)
        self.pin_entry.focus()

        self.message = ctk.CTkLabel(self, text="", font=theme.SMALL_FONT)
        self.message.pack(pady=(5, 5))

        ctk.CTkButton(
            self, text="Unlock", width=200, height=40,
            fg_color=theme.PRIMARY, hover_color=theme.PRIMARY_HOVER,
            command=self.verify
        ).pack(pady=10)

        self.pin_entry.bind("<Return>", lambda e: self.verify())

    def verify(self):

        pin = self.pin_entry.get().strip()

        pin_hash = User.get_pin_hash(self.user_id)

        if pin_hash and verify_password(pin, pin_hash):
            self.destroy()
            self.on_success()
        else:
            self.message.configure(text="Incorrect PIN.", text_color="red")
            self.pin_entry.delete(0, "end")
