import customtkinter as ctk

from ui import theme


class Toast(ctk.CTkFrame):
    """
    Notificação temporária que aparece no canto inferior direito
    da janela principal e desaparece sozinha.
    """

    _active_toasts = []

    def __init__(self, parent_window, message, kind="success", duration=2500):

        color = theme.SUCCESS
        if kind == "error":
            color = theme.ERROR
        elif kind == "warning":
            color = theme.WARNING
        elif kind == "info":
            color = theme.PRIMARY

        super().__init__(
            parent_window,
            fg_color=theme.SURFACE,
            border_width=2,
            border_color=color,
            corner_radius=10
        )

        self.parent_window = parent_window

        bar = ctk.CTkFrame(self, fg_color=color, width=6, corner_radius=0)
        bar.pack(side="left", fill="y")

        ctk.CTkLabel(
            self,
            text=message,
            font=("Segoe UI", 13),
            text_color=theme.TEXT,
            wraplength=260,
            justify="left"
        ).pack(side="left", padx=15, pady=12)

        # Posiciona no canto inferior direito, empilhando se já houver outros toasts
        Toast._active_toasts.append(self)
        self._reposition_all()

        self.after(duration, self.close)

    def _reposition_all(self):

        self.parent_window.update_idletasks()

        win_w = self.parent_window.winfo_width()
        win_h = self.parent_window.winfo_height()

        bottom_margin = 20
        spacing = 10

        y = win_h - bottom_margin

        for toast in reversed(Toast._active_toasts):
            toast.update_idletasks()
            h = toast.winfo_reqheight() or 50
            y -= h
            x = win_w - toast.winfo_reqwidth() - 20 if toast.winfo_reqwidth() > 1 else win_w - 300
            toast.place(x=x, y=y)
            y -= spacing

    def close(self):

        if self in Toast._active_toasts:
            Toast._active_toasts.remove(self)

        self.destroy()

        self._reposition_all_static(self.parent_window)

    @staticmethod
    def _reposition_all_static(parent_window):

        if not Toast._active_toasts:
            return

        parent_window.update_idletasks()

        win_w = parent_window.winfo_width()
        win_h = parent_window.winfo_height()

        bottom_margin = 20
        spacing = 10

        y = win_h - bottom_margin

        for toast in reversed(Toast._active_toasts):
            h = toast.winfo_reqheight() or 50
            y -= h
            x = win_w - toast.winfo_reqwidth() - 20 if toast.winfo_reqwidth() > 1 else win_w - 300
            toast.place(x=x, y=y)
            y -= spacing


def show_toast(window, message, kind="success", duration=2500):
    """
    window: a janela de topo (ctk.CTk ou CTkToplevel) onde o toast deve aparecer.
    kind: "success", "error", "warning", "info"
    """
    return Toast(window, message, kind=kind, duration=duration)
