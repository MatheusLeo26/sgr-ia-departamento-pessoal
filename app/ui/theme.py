"""
Design tokens do SGR.IA — Suporte Multi-Tema (Light/Dark).
As cores agora usam ctk.CTkColor para alternância automática.
"""
import customtkinter as ctk

# -- Backgrounds ----------------------------------------------------------
# (Light Mode, Dark Mode)
BG_MAIN    = ("#F8FAFC", "#0B1422") # Cinza Suave / Azul Meia-noite
BG_SIDEBAR = ("#F1F5F9", "#080E1A") # Sidebar mais contrastada
BG_PANEL   = ("#FFFFFF", "#0F1A2A") # Branco / Azul Painel Profundo
BG_CARD    = ("#FFFFFF", "#16253B") # Branco / Azul Card Elevado
BG_INPUT   = ("#F1F5F9", "#060912")

# -- Brand (Inspirado no Azul da Logo #5376DC) -----------------------------
PRIMARY       = ("#5376DC", "#5376DC")
PRIMARY_HOVER = ("#4060C0", "#6A89E6")
PRIMARY_DARK  = ("#3452A3", "#1A2F5E")
ACCENT        = ("#6366F1", "#818CF8") # Indigo vibe para modernidade
ACCENT_HOVER  = ("#4F46E5", "#6366F1")
ACCENT_LIGHT  = ("#C7D2FE", "#312E81")

# -- Text -----------------------------------------------------------------
TEXT       = ("#0F172A", "#F8FAFC") # Slate 900 / Slate 50
TEXT_SEC   = ("#475569", "#94A3B8") # Slate 600 / Slate 400
TEXT_MUTED = ("#94A3B8", "#475569") # Slate 400 / Slate 600

# -- Status ---------------------------------------------------------------
SUCCESS    = ("#27AE60", "#27AE60")
SUCCESS_BG = ("#D5F5E3", "#0E2B1A")
WARNING    = ("#E67E22", "#E67E22")
WARNING_BG = ("#FBEEE6", "#2B1A07")
ERROR      = ("#E74C3C", "#E74C3C")
ERROR_BG   = ("#FADBD8", "#2B0E0E")
INFO       = ("#3498DB", "#3498DB")
INFO_BG    = ("#D6EAF8", "#0A1E30")

# -- Borders / separators -------------------------------------------------
BORDER     = ("#CBD5E0", "#1E3D5F")
SEPARATOR  = ("#E2E8F0", "#1A3250")

# -- Fonts ----------------------------------------------------------------
FONT_FAMILY  = "Segoe UI"
FONT_TITLE   = (FONT_FAMILY, 20, "bold")
FONT_H2      = (FONT_FAMILY, 14, "bold")
FONT_H3      = (FONT_FAMILY, 12, "bold")
FONT_BODY    = (FONT_FAMILY, 11)
FONT_SMALL   = (FONT_FAMILY, 10)
FONT_MONO    = ("Consolas", 10)
FONT_LABEL   = (FONT_FAMILY, 11, "bold")

# -- Dimensions -----------------------------------------------------------
SIDEBAR_W      = 230
SIDEBAR_LOGO_H = 220
TOP_HEADER_H   = 60
CORNER_R       = 8
PAD            = 16

VERSION        = "1.0.4"
