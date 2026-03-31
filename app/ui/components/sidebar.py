import customtkinter as ctk
from app.ui import theme as T
from PIL import Image
import os
from app.services.config_service import ConfigService

MENU_ITEMS = [
    ("dashboard",       "📊  Dashboard"),
    ("rescisao",        "📋  Rescisão"),
    ("folha",           "💰  Folha de Pagamento"),
    ("ferias",          "🏖️  Férias"),
    ("decimo_terceiro", "🎄  13º Salário"),
    ("funcionarios",    "👤  Funcionários"),
    ("empresas",        "🏢  Empresas"),
    ("relatorios",      "📄  Relatórios"),
    ("tutoriais",       "📚  Tutoriais"),
    ("chat",            "🤖  Roberta Bot"),
]

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_navigate, **kwargs):
        super().__init__(
            master,
            width=T.SIDEBAR_W,
            fg_color=T.BG_SIDEBAR,
            corner_radius=0,
            **kwargs,
        )
        self.on_navigate = on_navigate
        self._active = "dashboard"
        self._buttons: dict[str, ctk.CTkButton] = {}
        self._config = ConfigService()
        self._build()

    # ------------------------------------------------------------------
    def _build(self):
        self.pack_propagate(False)

        # Logo / brand block (Aumentado para o novo Logo SGR)
        brand = ctk.CTkFrame(self, fg_color="transparent", height=T.SIDEBAR_LOGO_H)
        brand.pack(fill="x", pady=(20, 0))
        brand.pack_propagate(False)

        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "app", "assets", "logo_sgr.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(190, 190))
            ctk.CTkLabel(brand, image=logo_img, text="").pack(expand=True)
        else:
            ctk.CTkLabel(brand, text="SGR.IA", font=ctk.CTkFont(T.FONT_FAMILY, 24, "bold"), text_color=T.PRIMARY).pack(expand=True)

        # Separator
        ctk.CTkFrame(self, height=1, fg_color=T.SEPARATOR).pack(fill="x", pady=(10, 0))

        # Section label
        ctk.CTkLabel(
            self, text="MENU PRINCIPAL",
            font=ctk.CTkFont(T.FONT_FAMILY, 9, "bold"),
            text_color=T.TEXT_MUTED,
        ).pack(anchor="w", padx=20, pady=(16, 4))

        # Buttons frame
        btns_frame = ctk.CTkFrame(self, fg_color="transparent")
        btns_frame.pack(fill="both", expand=True)

        for key, label in MENU_ITEMS:
            btn = ctk.CTkButton(
                btns_frame,
                text=label,
                anchor="w",
                height=42,
                corner_radius=T.CORNER_R,
                fg_color="transparent",
                hover_color=T.BG_PANEL,
                text_color=T.TEXT_SEC,
                font=ctk.CTkFont(T.FONT_FAMILY, 12),
                command=lambda k=key: self._click(k)
            )
            btn.pack(fill="x", padx=10, pady=2)
            self._buttons[key] = btn

        self._highlight("dashboard")

        # Bottom section: Theme Toggle and Version
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", pady=12, padx=10)

        self.theme_btn = ctk.CTkButton(
            bottom_frame,
            text="🌓 Alternar Tema",
            height=32,
            fg_color=T.BG_PANEL,
            hover_color=T.PRIMARY_HOVER,
            text_color=T.TEXT_SEC,
            font=ctk.CTkFont(T.FONT_FAMILY, 10, "bold"),
            corner_radius=T.CORNER_R,
            command=self._toggle_theme
        )
        self.theme_btn.pack(fill="x", pady=5)

        ctk.CTkLabel(
            bottom_frame,
            text=f"v{T.VERSION} — SGR Contábil",
            font=ctk.CTkFont(T.FONT_FAMILY, 9),
            text_color=T.TEXT_MUTED,
        ).pack()

    # ------------------------------------------------------------------
    def _click(self, key: str):
        self._highlight(key)
        self.on_navigate(key)

    def _toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self._config.set_appearance_mode(new_mode)

    def _highlight(self, key: str):
        if self._active in self._buttons:
            self._buttons[self._active].configure(
                fg_color="transparent",
                text_color=T.TEXT_SEC,
            )
        self._active = key
        if key in self._buttons:
            self._buttons[key].configure(
                fg_color=T.PRIMARY_DARK,
                text_color=T.TEXT,
            )

    def set_active(self, key: str):
        self._highlight(key)
