"""
Design tokens do SGR.IA — Suporte Multi-Tema (Light/Dark).
As cores agora usam ctk.CTkColor para alternância automática.
"""
import customtkinter as ctk

# -- Backgrounds ----------------------------------------------------------
# (Light Mode, Dark Mode)
BG_MAIN    = ctk.CTkColor(("#F5F7FA", "#0D1926")) # Branco Gelo / Azul Profundo
BG_SIDEBAR = ctk.CTkColor(("#EAECEF", "#091520")) # Cinza Claro / Azul Sidebar
BG_PANEL   = ctk.CTkColor(("#FFFFFF", "#132338")) # Branco / Azul Painel
BG_CARD    = ctk.CTkColor(("#FAFAFA", "#1A2E47")) # Branco Puro / Azul Card
BG_INPUT   = ctk.CTkColor(("#FFFFFF", "#0F1E30"))

# -- Brand (Inspirado no Azul da Logo #5376DC) -----------------------------
PRIMARY       = ctk.CTkColor(("#5376DC", "#5376DC"))
PRIMARY_HOVER = ctk.CTkColor(("#4366CC", "#6386EC"))
PRIMARY_DARK  = ctk.CTkColor(("#3A56A8", "#163D70"))
ACCENT        = ctk.CTkColor(("#7C6FCD", "#7C6FCD"))
ACCENT_HOVER  = ctk.CTkColor(("#8C7FDD", "#8C7FDD"))
ACCENT_LIGHT  = ctk.CTkColor(("#5376DC", "#A89EE0"))

# -- Text -----------------------------------------------------------------
TEXT       = ctk.CTkColor(("#1A1A1A", "#E8EFF8")) # Preto / Branco
TEXT_SEC   = ctk.CTkColor(("#4A5568", "#96ACCA")) # Cinza / Azul Sec
TEXT_MUTED = ctk.CTkColor(("#718096", "#5A7090")) # Cinza Muted

# -- Status ---------------------------------------------------------------
SUCCESS    = ctk.CTkColor(("#27AE60", "#27AE60"))
SUCCESS_BG = ctk.CTkColor(("#D5F5E3", "#0E2B1A"))
WARNING    = ctk.CTkColor(("#E67E22", "#E67E22"))
WARNING_BG = ctk.CTkColor(("#FBEEE6", "#2B1A07"))
ERROR      = ctk.CTkColor(("#E74C3C", "#E74C3C"))
ERROR_BG   = ctk.CTkColor(("#FADBD8", "#2B0E0E"))
INFO       = ctk.CTkColor(("#3498DB", "#3498DB"))
INFO_BG    = ctk.CTkColor(("#D6EAF8", "#0A1E30"))

# -- Borders / separators -------------------------------------------------
BORDER     = ctk.CTkColor(("#CBD5E0", "#1E3D5F"))
SEPARATOR  = ctk.CTkColor(("#E2E8F0", "#1A3250"))

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

VERSION        = "1.0.2"
