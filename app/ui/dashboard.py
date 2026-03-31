import customtkinter as ctk
from app.ui import theme as T
from app.controllers.empresa_controller import EmpresaController
from app.controllers.funcionario_controller import FuncionarioController
from app.controllers.rescisao_controller import RescisaoController
from app.services.validators import formatar_data_br
import tkinter.filedialog as fd
from tkinter import messagebox
from app.services.config_service import ConfigService
import os


def _card(master, title: str, value: str, color: str, sub: str = "") -> ctk.CTkFrame:
    f = ctk.CTkFrame(master, fg_color=T.BG_CARD, corner_radius=T.CORNER_R)
    ctk.CTkLabel(f, text=title, font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.TEXT_MUTED).pack(anchor="w", padx=16, pady=(14, 0))
    ctk.CTkLabel(f, text=value, font=ctk.CTkFont(T.FONT_FAMILY, 28, "bold"), text_color=color).pack(anchor="w", padx=16, pady=(2, 0))
    if sub:
        ctk.CTkLabel(f, text=sub, font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.TEXT_MUTED).pack(anchor="w", padx=16, pady=(0, 12))
    else:
        ctk.CTkLabel(f, text="").pack(pady=4)
    return f


class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, navigate_cb):
        super().__init__(master, fg_color=T.BG_MAIN)
        self._nav = navigate_cb
        self._ec  = EmpresaController()
        self._fc  = FuncionarioController()
        self._rc  = RescisaoController()
        self._build()

    # ------------------------------------------------------------------
    def _build(self):
        # Page title
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=T.PAD, pady=(T.PAD, 8))
        ctk.CTkLabel(hdr, text="Dashboard", font=ctk.CTkFont(T.FONT_FAMILY, 22, "bold"), text_color=T.TEXT).pack(side="left")
        ctk.CTkLabel(hdr, text="Visão geral operacional", font=ctk.CTkFont(T.FONT_FAMILY, 12), text_color=T.TEXT_MUTED).pack(side="left", padx=12, pady=4)
        
        # Botão de Configuração de Rede
        ctk.CTkButton(
            hdr, text="🌐 CONFIGURAÇÃO DE REDE", width=190, height=32,
            fg_color=T.BG_PANEL, hover_color=T.PRIMARY_HOVER,
            font=ctk.CTkFont(T.FONT_FAMILY, 10, "bold"),
            text_color=T.TEXT_SEC,
            corner_radius=T.CORNER_R,
            command=self._configurar_rede
        ).pack(side="right", pady=4)

        # ---- KPI row -------------------------------------------------
        kpi_row = ctk.CTkFrame(self, fg_color="transparent")
        kpi_row.pack(fill="x", padx=T.PAD, pady=4)
        kpi_row.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="kpi")

        total_func   = self._fc.total_ativos()
        total_emp    = self._ec.total_ativas()
        total_resc   = self._rc.total_mes_atual()

        cards = [
            ("👤 Funcionários Ativos",  str(total_func),  T.ACCENT,   "Total cadastrado"),
            ("🏢 Empresas Ativas",       str(total_emp),   T.PRIMARY,  "Com cadastro ativo"),
            ("📋 Rescisões (mês)",       str(total_resc),  T.WARNING,  "Mês corrente"),
            ("✅ Status do Sistema",     "Online",          T.SUCCESS,  "Banco SQLite conectado"),
        ]
        for col, (title, val, color, sub) in enumerate(cards):
            c = _card(kpi_row, title, val, color, sub)
            c.grid(row=0, column=col, padx=6, pady=4, sticky="ew")

        # ---- Quick actions ------------------------------------------
        qa_frame = ctk.CTkFrame(self, fg_color="transparent")
        qa_frame.pack(fill="x", padx=T.PAD, pady=(12, 4))
        ctk.CTkLabel(qa_frame, text="Ações Rápidas", font=ctk.CTkFont(T.FONT_FAMILY, 13, "bold"), text_color=T.TEXT_SEC).pack(anchor="w")

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=T.PAD, pady=4)
        for label, page, color in [
            ("+ Nova Rescisão",     "rescisao",     T.PRIMARY),
            ("+ Novo Funcionário",  "funcionarios", T.ACCENT),
            ("+ Nova Empresa",      "empresas",     T.PRIMARY_DARK),
        ]:
            ctk.CTkButton(
                btn_row, text=label, width=180, height=38,
                fg_color=color, hover_color=T.PRIMARY_HOVER,
                font=ctk.CTkFont(T.FONT_FAMILY, 12, "bold"),
                corner_radius=T.CORNER_R,
                command=lambda p=page: self._nav(p),
            ).pack(side="left", padx=(0, 10))

        # ---- Recent rescisões table ---------------------------------
        ctk.CTkLabel(
            self, text="Rescisões Recentes",
            font=ctk.CTkFont(T.FONT_FAMILY, 13, "bold"),
            text_color=T.TEXT_SEC,
        ).pack(anchor="w", padx=T.PAD, pady=(16, 4))

        table_frame = ctk.CTkScrollableFrame(self, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R)
        table_frame.pack(fill="both", expand=True, padx=T.PAD, pady=(0, T.PAD))

        headers = ["Funcionário", "Empresa", "Tipo", "Último Dia", "Líquido"]
        widths  = [200, 200, 160, 110, 120]
        hdr_row = ctk.CTkFrame(table_frame, fg_color=T.BG_CARD, corner_radius=0)
        hdr_row.pack(fill="x")
        for h, w in zip(headers, widths):
            ctk.CTkLabel(
                hdr_row, text=h, width=w,
                font=ctk.CTkFont(T.FONT_FAMILY, 10, "bold"),
                text_color=T.TEXT_MUTED, anchor="w",
            ).pack(side="left", padx=10, pady=8)

        recentes = self._rc.listar_recentes(10)
        if not recentes:
            ctk.CTkLabel(
                table_frame,
                text="Nenhuma rescisão registrada ainda.",
                font=ctk.CTkFont(T.FONT_FAMILY, 11),
                text_color=T.TEXT_MUTED,
            ).pack(pady=20)
        else:
            for i, r in enumerate(recentes):
                bg = T.BG_PANEL if i % 2 == 0 else T.BG_CARD
                row = ctk.CTkFrame(table_frame, fg_color=bg, corner_radius=0)
                row.pack(fill="x")
                tipo_label = {
                    "sem_justa_causa": "Sem Justa Causa",
                    "justa_causa": "Justa Causa",
                    "pedido_demissao": "Pedido de Demissão",
                    "acordo_consensual": "Acordo Consensual",
                    "termino_contrato": "Término de Contrato",
                }.get(r.get("tipo_rescisao", ""), r.get("tipo_rescisao", ""))
                cells = [
                    (r.get("funcionario_nome", "—"), widths[0]),
                    (r.get("empresa_nome", "—"),     widths[1]),
                    (tipo_label,                     widths[2]),
                    (formatar_data_br(r.get("ultimo_dia", "")), widths[3]),
                    (f"R$ {r.get('valor_liquido', 0):,.2f}", widths[4]),
                ]
                for text, w in cells:
                    ctk.CTkLabel(
                        row, text=text, width=w,
                        font=ctk.CTkFont(T.FONT_FAMILY, 11),
                        text_color=T.TEXT, anchor="w",
                    ).pack(side="left", padx=10, pady=6)

    def _configurar_rede(self):
        config_service = ConfigService()
        current_path = config_service.get_db_path()
        
        new_path = fd.askopenfilename(
            title="Selecionar Banco de Dados SGR.IA",
            initialdir=os.path.dirname(current_path),
            filetypes=[("Banco de Dados SQLite", "*.db"), ("Todos os Arquivos", "*.*")]
        )
        
        if new_path:
            config_service.set_db_path(new_path)
            messagebox.showinfo("SGR.IA", f"Configuração atualizada!\nO banco agora está em:\n{new_path}\n\nPor favor, reinicie o aplicativo.")

