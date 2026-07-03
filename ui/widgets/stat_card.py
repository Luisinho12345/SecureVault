import customtkinter as ctk

from ui import theme


class StatCard(ctk.CTkFrame):

    def __init__(self, master, title, value, color=None):
        super().__init__(
            master,
            fg_color=theme.SURFACE,
            corner_radius=15,
            height=150
        )

        if color is None:
            color = theme.PRIMARY

        self.grid_propagate(False)

        value_label = ctk.CTkLabel(
            self,
            text=str(value),
            font=("Segoe UI", 36, "bold"),
            text_color=color
        )
        value_label.pack(pady=(22, 5))

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 15),
            text_color=theme.TEXT
        )
        title_label.pack()

        self.value_label = value_label

    def set_value(self, value):
        self.value_label.configure(text=str(value))