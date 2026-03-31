import customtkinter as ctk
from app.ui import theme as T
from app.ui.components.sidebar import Sidebar

import os
try:
    from PIL import Image
    PIL_OK = True
except ImportError:
    PIL_OK = False


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SGR.IA — Departamento Pessoal | SGR Contábil")
        self.geometry("1280x780")
        self.minsize(1024, 680)
        self.configure(fg_color=T.BG_MAIN)

        ctk.set_appearance_mode("dark")

        # Window Icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "app", "assets", "robot_report_icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self._build_layout()
        self.navigate("dashboard")

    # ------------------------------------------------------------------
    def _build_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ---- Header --------------------------------------------------
        header = ctk.CTkFrame(self, height=T.HEADER_H, fg_color=T.BG_SIDEBAR, corner_radius=0)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        # Logo
        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "app", "assets", "logo_sgr.png"
        )
        if PIL_OK and os.path.exists(logo_path):
            img = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(120, 40),
            )
            ctk.CTkLabel(header, image=img, text="").grid(row=0, column=0, padx=20, pady=12)
        else:
            ctk.CTkLabel(
                header, text="[ SGR ]",
                font=ctk.CTkFont(T.FONT_FAMILY, 13, "bold"),
                text_color=T.ACCENT_LIGHT,
            ).grid(row=0, column=0, padx=20, pady=12)

        # System name
        ctk.CTkLabel(
            header, text="SGR.IA",
            font=ctk.CTkFont(T.FONT_FAMILY, 18, "bold"),
            text_color=T.TEXT,
        ).grid(row=0, column=1, padx=4, pady=0, sticky="w")

        ctk.CTkLabel(
            header, text="Departamento Pessoal Inteligente",
            font=ctk.CTkFont(T.FONT_FAMILY, 10),
            text_color=T.TEXT_MUTED,
        ).grid(row=0, column=2, padx=(0, 20), pady=0, sticky="e")

        # ---- Separator under header ----------------------------------
        ctk.CTkFrame(self, height=1, fg_color=T.SEPARATOR).grid(
            row=0, column=0, columnspan=2, sticky="sew"
        )

        # ---- Sidebar -------------------------------------------------
        self.sidebar = Sidebar(self, on_navigate=self.navigate)
        self.sidebar.grid(row=1, column=0, sticky="ns")

        # Right separator line
        ctk.CTkFrame(self, width=1, fg_color=T.SEPARATOR).grid(row=1, column=0, sticky="nse")

        # ---- Content area -------------------------------------------
        self.content = ctk.CTkFrame(self, fg_color=T.BG_MAIN, corner_radius=0)
        self.content.grid(row=1, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self._current_page = None

    # ------------------------------------------------------------------
    def navigate(self, key: str):
        # Clear content
        for w in self.content.winfo_children():
            w.destroy()
        self.sidebar.set_active(key)

        # Import and instantiate the target page
        if key == "dashboard":
            from app.ui.dashboard import DashboardPage
            page = DashboardPage(self.content, self.navigate)
        elif key == "rescisao":
            from app.ui.rescisao import RescisaoPage
            page = RescisaoPage(self.content)
        elif key == "folha":
            from app.ui.folha import FolhaPage
            page = FolhaPage(self.content)
        elif key == "ferias":
            from app.ui.ferias import FeriasPage
            page = FeriasPage(self.content)
        elif key == "decimo_terceiro":
            from app.ui.decimo_terceiro import DecimoTerceiroPage
            page = DecimoTerceiroPage(self.content)
        elif key == "funcionarios":
            from app.ui.funcionarios import FuncionariosPage
            page = FuncionariosPage(self.content)
        elif key == "empresas":
            from app.ui.empresas import EmpresasPage
            page = EmpresasPage(self.content)
        elif key == "relatorios":
            from app.ui.relatorios import RelatoriosPage
            page = RelatoriosPage(self.content)
        elif key == "tutoriais":
            from app.ui.tutoriais import TutoriaisPage
            page = TutoriaisPage(self.content)
        elif key == "chat":
            from app.ui.chat import ChatPage
            page = ChatPage(self.content)
        else:
            page = _PlaceholderPage(self.content, key)

        page.pack(fill="both", expand=True)
        self._current_page = page


# ----------------------------------------------------------------------
class _PlaceholderPage(ctk.CTkFrame):
    def __init__(self, master, name: str):
        super().__init__(master, fg_color=T.BG_MAIN)
        ctk.CTkLabel(
            self, text=f"🚧  {name.title()} — em breve",
            font=ctk.CTkFont(T.FONT_FAMILY, 18),
            text_color=T.TEXT_MUTED,
        ).place(relx=0.5, rely=0.5, anchor="center")
