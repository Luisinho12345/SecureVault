import customtkinter as ctk

# ==========================
# Tema
# ==========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==========================
# Cores
# ==========================

BACKGROUND = "#0F172A"
SURFACE = "#1E293B"

PRIMARY = "#2563EB"
PRIMARY_HOVER = "#1D4ED8"

SUCCESS = "#22C55E"
WARNING = "#F59E0B"
ERROR = "#EF4444"

TEXT = "#F8FAFC"
TEXT_SECONDARY = "#94A3B8"

BORDER = "#475569"

# ==========================
# Fontes
# ==========================

FONT = "Segoe UI"

TITLE_FONT = (FONT, 32, "bold")
SUBTITLE_FONT = (FONT, 18)
TEXT_FONT = (FONT, 15)
SMALL_FONT = (FONT, 13)

# ==========================
# Janela
# ==========================

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

# ==========================
# Aplicar Tema
# ==========================

def apply_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")