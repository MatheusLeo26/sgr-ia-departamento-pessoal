import customtkinter as ctk
from app.ui import theme as T

MENU_ITEMS = [
    ("dashboard",       "📊  Dashboard"),
    ("rescisao",        "📋  Rescisão"),
    ("folha",           "💰  Folha de Pagamento"),
    ("ferias",          "🏖️  Férias"),
    ("decimo_terceiro", "🎄  13º Salário"),
    ("funcionarios",    "👤  Funcionários"),
    ("empresas",        "🏢  Empresas"),
    ("relatorios",      "📄  Relatórios"),
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
        self._build()

    # ------------------------------------------------------------------
    def _build(self):
        self.pack_propagate(False)

        # Logo / brand block
        brand = ctk.CTkFrame(self, fg_color="transparent", height=T.HEADER_H)
        brand.pack(fill="x")
        brand.pack_propagate(False)

        ctk.CTkLabel(
            brand, text="SGR.IA",
            font=ctk.CTkFont(T.FONT_FAMILY, 22, "bold"),
            text_color=T.ACCENT_LIGHT,
        ).pack(side="left", padx=20, pady=0)

        # Separator
        ctk.CTkFrame(self, height=1, fg_color=T.SEPARATOR).pack(fill="x")

        # Section label
        ctk.CTkLabel(
            self, text="MENU PRINCIPAL",
            font=ctk.CTkFont(T.FONT_FAMILY, 9, "bold"),
            text_color=T.TEXT_MUTED,
        ).pack(anchor="w", padx=20, pady=(16, 4))

        for key, label in MENU_ITEMS:
            btn = ctk.CTkButton(
                self,
                text=label,
                anchor="w",
                height=42,
                corner_radius=T.CORNER_R,
                fg_color="transparent",
                hover_color=T.BG_PANEL,
                text_color=T.TEXT_SEC,
                font=ctk.CTkFont(T.FONT_FAMILY, 12),
                command=lambda k=key: self._click(k),
            )
            btn.pack(fill="x", padx=10, pady=2)
            self._buttons[key] = btn

        self._highlight("dashboard")

        # Bottom version
        ctk.CTkLabel(
            self,
            text="v1.0 — SGR Contábil",
            font=ctk.CTkFont(T.FONT_FAMILY, 9),
            text_color=T.TEXT_MUTED,
        ).pack(side="bottom", pady=12)

    # ------------------------------------------------------------------
    def _click(self, key: str):
        self._highlight(key)
        self.on_navigate(key)

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
