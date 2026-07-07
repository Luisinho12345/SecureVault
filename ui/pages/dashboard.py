import customtkinter as ctk
from collections import Counter

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ui import theme
from ui.widgets.page_layout import BasePage
from ui.widgets.header import Header
from ui.widgets.stat_card import StatCard
from ui.pages.vault import VaultPage
from database.models import Password
from security.password_generator import check_strength


class DashboardPage(BasePage):

    def __init__(self, master):
        super().__init__(master, active_page="dashboard")

    def build_content(self, content):

        content.grid_rowconfigure(3, weight=1)
        content.grid_columnconfigure((0, 1, 2), weight=1)

        self.header = Header(content, username=self.app.current_username or "User")
        self.header.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 20))

        # ================= Linha 1 de cartões =================

        row1 = ctk.CTkFrame(content, fg_color="transparent")
        row1.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        row1.grid_columnconfigure((0, 1, 2), weight=1)

        self.passwords_card = StatCard(row1, "Total Passwords", 0)
        self.passwords_card.grid(row=0, column=0, padx=10, sticky="ew")

        self.strong_card = StatCard(row1, "Strong Passwords", 0, theme.SUCCESS)
        self.strong_card.grid(row=0, column=1, padx=10, sticky="ew")

        self.weak_card = StatCard(row1, "Weak Passwords", 0, theme.ERROR)
        self.weak_card.grid(row=0, column=2, padx=10, sticky="ew")

        # ================= Linha 2 de cartões =================

        row2 = ctk.CTkFrame(content, fg_color="transparent")
        row2.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        row2.grid_columnconfigure((0, 1, 2), weight=1)

        self.categories_card = StatCard(row2, "Categories", 0)
        self.categories_card.grid(row=0, column=0, padx=10, sticky="ew")

        self.last_added_card = StatCard(row2, "Last Added", "-")
        self.last_added_card.grid(row=0, column=1, padx=10, sticky="ew")

        self.last_login_card = StatCard(row2, "Last Login", "-")
        self.last_login_card.grid(row=0, column=2, padx=10, sticky="ew")

        # ================= Gráficos =================

        charts_frame = ctk.CTkFrame(content, fg_color="transparent")
        charts_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")
        charts_frame.grid_columnconfigure((0, 1), weight=1)
        charts_frame.grid_rowconfigure(0, weight=1)

        self.category_chart_frame = ctk.CTkFrame(charts_frame, fg_color=theme.SURFACE, corner_radius=15)
        self.category_chart_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.strength_chart_frame = ctk.CTkFrame(charts_frame, fg_color=theme.SURFACE, corner_radius=15)
        self.strength_chart_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.update_stats()
        self.build_charts()

    # ==========================
    # Estatísticas
    # ==========================

    def update_stats(self):

        user_id = self.app.current_user_id
        passwords_list = Password.get_all(user_id)

        total_passwords = len(passwords_list)
        total_categories = len({p[6] for p in passwords_list}) if passwords_list else 0

        strong_count = 0
        weak_count = 0

        for p in passwords_list:
            strength = check_strength(p[4])
            if strength == "Strong":
                strong_count += 1
            elif strength == "Weak":
                weak_count += 1

        self.passwords_card.set_value(total_passwords)
        self.strong_card.set_value(strong_count)
        self.weak_card.set_value(weak_count)
        self.categories_card.set_value(total_categories)

        if passwords_list:
            # get_all ordena por id DESC, logo o primeiro é o mais recente
            self.last_added_card.set_value(passwords_list[0][5])
        else:
            self.last_added_card.set_value("-")

        self.last_login_card.set_value(
            self.app.current_username or "-"
        )

    # ==========================
    # Gráficos
    # ==========================

    def build_charts(self):

        for widget in self.category_chart_frame.winfo_children():
            widget.destroy()
        for widget in self.strength_chart_frame.winfo_children():
            widget.destroy()

        user_id = self.app.current_user_id
        passwords_list = Password.get_all(user_id)

        ctk.CTkLabel(
            self.category_chart_frame, text="Passwords by Category",
            font=("Segoe UI", 15, "bold"), text_color=theme.TEXT
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            self.strength_chart_frame, text="Password Strength",
            font=("Segoe UI", 15, "bold"), text_color=theme.TEXT
        ).pack(anchor="w", padx=20, pady=(15, 5))

        if not passwords_list:
            ctk.CTkLabel(
                self.category_chart_frame, text="No data yet.",
                font=theme.TEXT_FONT, text_color=theme.TEXT_SECONDARY
            ).pack(pady=40)
            ctk.CTkLabel(
                self.strength_chart_frame, text="No data yet.",
                font=theme.TEXT_FONT, text_color=theme.TEXT_SECONDARY
            ).pack(pady=40)
            return

        # ---- Gráfico de categorias (barras) ----

        categories = [p[6] for p in passwords_list]
        counts = Counter(categories)

        fig1 = Figure(figsize=(4, 3), dpi=100, facecolor=theme.SURFACE)
        ax1 = fig1.add_subplot(111)
        ax1.set_facecolor(theme.SURFACE)

        bars = ax1.bar(list(counts.keys()), list(counts.values()), color=theme.PRIMARY)

        ax1.tick_params(colors=theme.TEXT, labelsize=8)
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.spines["left"].set_color(theme.BORDER)
        ax1.spines["bottom"].set_color(theme.BORDER)

        for label in ax1.get_xticklabels():
            label.set_rotation(20)

        fig1.tight_layout()

        canvas1 = FigureCanvasTkAgg(fig1, master=self.category_chart_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # ---- Gráfico de força (donut) ----

        strengths = [check_strength(p[4]) for p in passwords_list]
        strength_counts = Counter(strengths)

        labels = ["Strong", "Medium", "Weak"]
        values = [strength_counts.get(label, 0) for label in labels]
        colors = [theme.SUCCESS, theme.WARNING, theme.ERROR]

        # Remove fatias com valor 0 para não aparecerem no gráfico
        filtered = [(l, v, c) for l, v, c in zip(labels, values, colors) if v > 0]

        fig2 = Figure(figsize=(4, 3), dpi=100, facecolor=theme.SURFACE)
        ax2 = fig2.add_subplot(111)
        ax2.set_facecolor(theme.SURFACE)

        if filtered:
            flabels, fvalues, fcolors = zip(*filtered)

            wedges, _ = ax2.pie(
                fvalues,
                colors=fcolors,
                startangle=90,
                wedgeprops=dict(width=0.4, edgecolor=theme.SURFACE)
            )

            ax2.legend(
                wedges, flabels,
                loc="center left",
                bbox_to_anchor=(1, 0.5),
                fontsize=8,
                facecolor=theme.SURFACE,
                labelcolor=theme.TEXT,
                frameon=False
            )

        ax2.axis("equal")
        fig2.tight_layout()

        canvas2 = FigureCanvasTkAgg(fig2, master=self.strength_chart_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def refresh(self):
        self.vault_refresh_needed = True
        self.update_stats()
        self.build_charts()
