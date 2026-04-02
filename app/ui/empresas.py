import customtkinter as ctk
from tkinter import messagebox
from app.ui import theme as T
from app.controllers.empresa_controller import EmpresaController
from app.models.empresa import Empresa
from app.services.validators import formatar_cnpj
from app.services.import_service import ImportService
from tkinter import filedialog


class EmpresasPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=T.BG_MAIN)
        self._ctrl = EmpresaController()
        self._import_service = ImportService()
        self._editing_id = None
        self._build()

    # ------------------------------------------------------------------
    def _build(self):
        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=T.PAD, pady=(T.PAD, 8))
        ctk.CTkLabel(hdr, text="Empresas", font=ctk.CTkFont(T.FONT_FAMILY, 22, "bold"), text_color=T.TEXT).pack(side="left")
        ctk.CTkButton(
            hdr, text="+ Nova Empresa", width=150, height=34,
            fg_color=T.PRIMARY, hover_color=T.PRIMARY_HOVER,
            font=ctk.CTkFont(T.FONT_FAMILY, 12, "bold"),
            corner_radius=T.CORNER_R,
            command=self._abrir_form,
        ).pack(side="right", padx=(8, 0))
        
        ctk.CTkButton(
            hdr, text="Importar Planilha", width=150, height=34,
            fg_color=T.BG_INPUT, border_color=T.BORDER, border_width=1,
            text_color=T.TEXT_SEC, hover_color=T.BORDER,
            font=ctk.CTkFont(T.FONT_FAMILY, 12, "bold"),
            corner_radius=T.CORNER_R,
            command=self._importar,
        ).pack(side="right")

        # Split: list | form
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=T.PAD, pady=4)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        # List panel
        list_panel = ctk.CTkFrame(body, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R)
        list_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        list_panel.grid_rowconfigure(1, weight=1)
        list_panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(list_panel, text="Cadastradas", font=ctk.CTkFont(T.FONT_FAMILY, 12, "bold"), text_color=T.TEXT_SEC).grid(row=0, column=0, sticky="w", padx=14, pady=10)

        self._list_frame = ctk.CTkScrollableFrame(list_panel, fg_color="transparent")
        self._list_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 6))

        # Form panel
        self._form_panel = ctk.CTkFrame(body, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R)
        self._form_panel.grid(row=0, column=1, sticky="nsew")
        self._form_widgets: dict = {}
        self._build_form()
        self._refresh_list()

    # ------------------------------------------------------------------
    def _build_form(self):
        f = self._form_panel
        ctk.CTkLabel(f, text="Dados da Empresa", font=ctk.CTkFont(T.FONT_FAMILY, 13, "bold"), text_color=T.TEXT_SEC).pack(anchor="w", padx=14, pady=(14, 6))

        fields = [
            ("razao_social",      "Razão Social *"),
            ("cnpj",              "CNPJ *"),
            ("nome_fantasia",     "Nome Fantasia"),
            ("cnae",              "CNAE"),
            ("fpas",              "FPAS"),
            ("sindicato",         "Sindicato"),
            ("regime_tributario", "Regime Tributário"),
            ("email",             "E-mail"),
            ("telefone",          "Telefone"),
        ]
        for key, label in fields:
            ctk.CTkLabel(f, text=label, font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.TEXT_MUTED).pack(anchor="w", padx=14, pady=(6, 0))
            entry = ctk.CTkEntry(f, height=32, fg_color=T.BG_INPUT, border_color=T.BORDER, text_color=T.TEXT, corner_radius=6)
            entry.pack(fill="x", padx=14, pady=(0, 2))
            self._form_widgets[key] = entry

        btn_row = ctk.CTkFrame(f, fg_color="transparent")
        btn_row.pack(fill="x", padx=14, pady=14)
        ctk.CTkButton(btn_row, text="Salvar", width=100, fg_color=T.PRIMARY, hover_color=T.PRIMARY_HOVER, corner_radius=T.CORNER_R, command=self._salvar).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_row, text="Limpar", width=80, fg_color=T.BG_CARD, hover_color=T.BORDER, text_color=T.TEXT_SEC, corner_radius=T.CORNER_R, command=self._limpar).pack(side="left")

    # ------------------------------------------------------------------
    def _refresh_list(self):
        for w in self._list_frame.winfo_children():
            w.destroy()

        empresas = self._ctrl.listar()
        if not empresas:
            ctk.CTkLabel(self._list_frame, text="Nenhuma empresa cadastrada.", font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.TEXT_MUTED).pack(pady=20)
            return

        for emp in empresas:
            row = ctk.CTkFrame(self._list_frame, fg_color=T.BG_CARD, corner_radius=6)
            row.pack(fill="x", pady=3)
            row.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(row, text=emp.razao_social, font=ctk.CTkFont(T.FONT_FAMILY, 11, "bold"), text_color=T.TEXT, anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=(8, 0))
            ctk.CTkLabel(row, text=formatar_cnpj(emp.cnpj), font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.TEXT_MUTED, anchor="w").grid(row=1, column=0, sticky="w", padx=10, pady=(0, 8))

            btns = ctk.CTkFrame(row, fg_color="transparent")
            btns.grid(row=0, column=1, rowspan=2, padx=8, pady=4)
            ctk.CTkButton(btns, text="✏", width=30, height=28, fg_color=T.ACCENT, hover_color=T.ACCENT_HOVER, corner_radius=6, command=lambda e=emp: self._editar(e)).pack(side="left", padx=2)
            ctk.CTkButton(btns, text="🗑", width=30, height=28, fg_color=T.ERROR_BG, hover_color=T.ERROR, corner_radius=6, command=lambda e=emp: self._excluir(e)).pack(side="left", padx=2)

    # ------------------------------------------------------------------
    def _abrir_form(self):
        self._limpar()

    def _limpar(self):
        self._editing_id = None
        for entry in self._form_widgets.values():
            entry.delete(0, "end")

    def _editar(self, emp: Empresa):
        self._editing_id = emp.id
        mapping = {
            "razao_social": emp.razao_social or "",
            "cnpj": emp.cnpj or "",
            "nome_fantasia": emp.nome_fantasia or "",
            "cnae": emp.cnae or "",
            "fpas": emp.fpas or "",
            "sindicato": emp.sindicato or "",
            "regime_tributario": emp.regime_tributario or "",
            "email": emp.email or "",
            "telefone": emp.telefone or "",
        }
        for key, val in mapping.items():
            e = self._form_widgets[key]
            e.delete(0, "end")
            e.insert(0, val)

    def _salvar(self):
        vals = {k: w.get().strip() for k, w in self._form_widgets.items()}
        if not vals["razao_social"] or not vals["cnpj"]:
            messagebox.showerror("SGR.IA", "Razão Social e CNPJ são obrigatórios.")
            return
        emp = Empresa(
            id=self._editing_id,
            razao_social=vals["razao_social"],
            cnpj=vals["cnpj"],
            nome_fantasia=vals["nome_fantasia"] or None,
            cnae=vals["cnae"] or None,
            fpas=vals["fpas"] or None,
            sindicato=vals["sindicato"] or None,
            regime_tributario=vals["regime_tributario"] or None,
            email=vals["email"] or None,
            telefone=vals["telefone"] or None,
        )
        ok, msg = self._ctrl.salvar(emp)
        if ok:
            messagebox.showinfo("SGR.IA", msg)
            self._limpar()
            self._refresh_list()
        else:
            messagebox.showerror("SGR.IA", msg)

    def _excluir(self, emp: Empresa):
        if messagebox.askyesno("SGR.IA", f"Desativar empresa '{emp.razao_social}'?"):
            self._ctrl.excluir(emp.id)
            self._refresh_list()

    def _importar(self):
        """Abre seletor de arquivo para importar empresas do Excel."""
        fpath = filedialog.askopenfilename(
            title="Importar Empresas",
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )
        if not fpath:
            return
        
        count, msg = self._import_service.importar_empresas(fpath)
        if count > 0:
            messagebox.showinfo("SGR.IA", msg)
            self._refresh_list()
        else:
            messagebox.showerror("SGR.IA", msg)
