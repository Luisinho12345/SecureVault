import customtkinter as ctk

from ui import theme
from ui.widgets.icon_factory import make_icon


class SplashScreen(ctk.CTk):

    def __init__(self, on_finish):
        super().__init__()

        self.on_finish = on_finish

        self.overrideredirect(True)
        self.configure(fg_color=theme.BACKGROUND)

        width, height = 420, 300
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.configure(fg_color=theme.BACKGROUND)

        container = ctk.CTkFrame(self, fg_color=theme.BACKGROUND)
        container.pack(expand=True, fill="both")

        ctk.CTkLabel(
            container,
            image=make_icon("vault", size=64, color=theme.PRIMARY),
            text=""
        ).pack(pady=(50, 15))

        ctk.CTkLabel(
            container,
            text="SecureVault",
            font=("Segoe UI", 26, "bold"),
            text_color=theme.TEXT
        ).pack()

        ctk.CTkLabel(
            container,
            text="Professional Password Manager",
            font=("Segoe UI", 13),
            text_color=theme.TEXT_SECONDARY
        ).pack(pady=(2, 25))

        self.progress = ctk.CTkProgressBar(
            container,
            width=280,
            height=8,
            progress_color=theme.PRIMARY
        )
        self.progress.pack(pady=(0, 10))
        self.progress.set(0)

        ctk.CTkLabel(
            container,
            text="v1.0.0",
            font=("Segoe UI", 11),
            text_color="#6B7280"
        ).pack(side="bottom", pady=15)

        self.duration_ms = 2000
        self.steps = 40
        self.step_delay = self.duration_ms // self.steps
        self.current_step = 0

        self.after(100, self.animate_progress)

    def animate_progress(self):

        self.current_step += 1
        value = self.current_step / self.steps
        self.progress.set(min(value, 1.0))

        if self.current_step < self.steps:
            self.after(self.step_delay, self.animate_progress)
        else:
            self.after(150, self.finish)

    def finish(self):
        self.destroy()
        self.on_finish()
