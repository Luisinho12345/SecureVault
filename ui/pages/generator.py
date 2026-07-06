import customtkinter as ctk

from ui import theme
from ui.widgets.page_layout import BasePage
from ui.windows.add_password import AddPasswordWindow
from security.password_generator import generate_password, check_strength


class GeneratorPage(BasePage):

    def __init__(self, master):
        super().__init__(master, active_page="generator")

    def build_content(self, content):

        content.grid_rowconfigure(0, weight=0)
        content.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            content,
            text="Password Generator",
            font=theme.TITLE_FONT,
            text_color=theme.TEXT
        ).grid(row=0, column=0, sticky="w", pady=(10, 25))

        card = ctk.CTkFrame(content, fg_color=theme.SURFACE, corner_radius=15)
        card.grid(row=1, column=0, sticky="ew", padx=(0, 0))
        card.grid_columnconfigure(0, weight=1)

        self.result_var = ctk.StringVar(value="Click Generate to create a password")

        result_frame = ctk.CTkFrame(card, fg_color="transparent")
        result_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        result_frame.grid_columnconfigure(0, weight=1)

        self.result_entry = ctk.CTkEntry(
            result_frame,
            textvariable=self.result_var,
            height=50,
            font=("Consolas", 18),
            justify="center"
        )
        self.result_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        ctk.CTkButton(
            result_frame,
            text="Copy",
            width=60,
            height=50,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_HOVER,
            command=self.copy_password
        ).grid(row=0, column=1)

        self.strength_label = ctk.CTkLabel(
            card,
            text="",
            font=theme.SMALL_FONT
        )
        self.strength_label.grid(row=1, column=0, sticky="w", padx=30)

        length_frame = ctk.CTkFrame(card, fg_color="transparent")
        length_frame.grid(row=2, column=0, sticky="ew", padx=30, pady=(25, 10))
        length_frame.grid_columnconfigure(0, weight=1)

        self.length_value_label = ctk.CTkLabel(
            length_frame,
            text="Length: 16",
            font=theme.TEXT_FONT,
            text_color=theme.TEXT
        )
        self.length_value_label.grid(row=0, column=0, sticky="w")

        self.length_slider = ctk.CTkSlider(
            card,
            from_=6,
            to=32,
            number_of_steps=26,
            command=self.on_length_change
        )
        self.length_slider.set(16)
        self.length_slider.grid(row=3, column=0, sticky="ew", padx=30, pady=(0, 20))

        options_frame = ctk.CTkFrame(card, fg_color="transparent")
        options_frame.grid(row=4, column=0, sticky="ew", padx=30, pady=(0, 20))
        options_frame.grid_columnconfigure((0, 1), weight=1)

        self.var_uppercase = ctk.BooleanVar(value=True)
        self.var_lowercase = ctk.BooleanVar(value=True)
        self.var_numbers = ctk.BooleanVar(value=True)
        self.var_symbols = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(
            options_frame, text="Uppercase (A-Z)", variable=self.var_uppercase,
            font=theme.TEXT_FONT
        ).grid(row=0, column=0, sticky="w", pady=8)

        ctk.CTkCheckBox(
            options_frame, text="Lowercase (a-z)", variable=self.var_lowercase,
            font=theme.TEXT_FONT
        ).grid(row=0, column=1, sticky="w", pady=8)

        ctk.CTkCheckBox(
            options_frame, text="Numbers (0-9)", variable=self.var_numbers,
            font=theme.TEXT_FONT
        ).grid(row=1, column=0, sticky="w", pady=8)

        ctk.CTkCheckBox(
            options_frame, text="Symbols (!@#$...)", variable=self.var_symbols,
            font=theme.TEXT_FONT
        ).grid(row=1, column=1, sticky="w", pady=8)

        buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
        buttons_frame.grid(row=5, column=0, sticky="ew", padx=30, pady=(0, 30))
        buttons_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            buttons_frame,
            text="Generate",
            height=45,
            fg_color=theme.PRIMARY,
            hover_color=theme.PRIMARY_HOVER,
            command=self.generate
        ).grid(row=0, column=0, sticky="ew", padx=(0, 10))

        ctk.CTkButton(
            buttons_frame,
            text="+ Use in New Password",
            height=45,
            fg_color="transparent",
            border_width=1,
            border_color=theme.BORDER,
            hover_color="#263241",
            command=self.use_password
        ).grid(row=0, column=1, sticky="ew", padx=(10, 0))

        self.status_label = ctk.CTkLabel(
            card, text="", font=theme.SMALL_FONT, text_color=theme.SUCCESS
        )
        self.status_label.grid(row=6, column=0, pady=(0, 20))

        self.generate()

    def on_length_change(self, value):
        self.length_value_label.configure(text=f"Length: {int(value)}")

    def generate(self):

        length = int(self.length_slider.get())

        password = generate_password(
            length=length,
            use_uppercase=self.var_uppercase.get(),
            use_lowercase=self.var_lowercase.get(),
            use_numbers=self.var_numbers.get(),
            use_symbols=self.var_symbols.get()
        )

        if not password:
            self.result_var.set("Select at least one option")
            self.strength_label.configure(text="")
            return

        self.result_var.set(password)

        strength = check_strength(password)

        color = theme.ERROR
        if strength == "Medium":
            color = theme.WARNING
        elif strength == "Strong":
            color = theme.SUCCESS

        self.strength_label.configure(text=f"Strength: {strength}", text_color=color)

    def copy_password(self):

        password = self.result_var.get()

        self.clipboard_clear()
        self.clipboard_append(password)

        self.status_label.configure(text="Password copied!")
        self.after(2000, lambda: self.status_label.configure(text=""))

    def use_password(self):

        password = self.result_var.get()

        window = AddPasswordWindow(self.app.current_page, self.app.current_user_id)
        window.password.insert(0, password)

