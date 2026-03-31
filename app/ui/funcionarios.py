import customtkinter as ctk
from tkinter import messagebox
from app.ui import theme as T
from app.controllers.funcionario_controller import FuncionarioController
from app.controllers.empresa_controller import EmpresaController
from app.models.funcionario import Funcionario
from app.services.validators import formatar_cpf, formatar_data_br


class FuncionariosPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=T.BG_MAIN)
        self._ctrl  = FuncionarioController()
        self._ectr  = EmpresaController()
        self._editing_id = None
        self._empresas   = []
        self._build()

    # ------------------------------------------------------------------
    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=T.PAD, pady=(T.PAD, 8))
        ctk.CTkLabel(hdr, text="Funcionários", font=ctk.CTkFont(T.FONT_FAMILY, 22, "bold"), text_color=T.TEXT).pack(side="left")
        ctk.CTkButton(hdr, text="+ Novo Funcionário", width=160, height=34, fg_color=T.PRIMARY, hover_color=T.PRIMARY_HOVER, font=ctk.CTkFont(T.FONT_FAMILY, 12, "bold"), corner_radius=T.CORNER_R, command=self._limpar).pack(side="right")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=T.PAD, pady=4)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        # List
        list_panel = ctk.CTkFrame(body, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R)
        list_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        list_panel.grid_rowconfigure(1, weight=1)
        list_panel.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(list_panel, text="Ativos", font=ctk.CTkFont(T.FONT_FAMILY, 12, "bold"), text_color=T.TEXT_SEC).grid(row=0, column=0, sticky="w", padx=14, pady=10)
        self._list_frame = ctk.CTkScrollableFrame(list_panel, fg_color="transparent")
        self._list_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 6))

        # Form
        form_panel = ctk.CTkScrollableFrame(body, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R)
        form_panel.grid(row=0, column=1, sticky="nsew")
        self._form_panel = form_panel
        self._form_widgets: dict = {}
        self._build_form(form_panel)
        self._refresh_list()

    # ------------------------------------------------------------------
    def _build_form(self, parent):
        ctk.CTkLabel(parent, text="Dados do Funcionário", font=ctk.CTkFont(T.FONT_FAMILY, 13, "bold"), text_color=T.TEXT_SEC).pack(anchor="w", padx=14, pady=(14, 6))

        fields = [
            ("nome",           "Nome Completo *"),
            ("cpf",            "CPF *  (000.000.000-00)"),
            ("rg",             "RG"),
            ("cargo",          "Cargo"),
            ("salario",        "Salário (R$) *"),
            ("data_admissao",  "Data de Admissão *  (DD/MM/AAAA)"),
            ("jornada",        "Jornada"),
            ("dependentes",    "Dependentes IRRF"),
            ("vale_transporte","Vale Transporte (R$)"),
            ("nome_mae",       "Nome da Mãe"),
            ("estado_civil",   "Estado Civil"),
        ]
        for key, label in fields:
            ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.TEXT_MUTED).pack(anchor="w", padx=14, pady=(6, 0))
            entry = ctk.CTkEntry(parent, height=32, fg_color=T.BG_INPUT, border_color=T.BORDER, text_color=T.TEXT, corner_radius=6)
            entry.pack(fill="x", padx=14, pady=(0, 2))
            self._form_widgets[key] = entry

        # Default jornada
        self._form_widgets["jornada"].insert(0, "44h semanais")

        # Empresa dropdown
        ctk.CTkLabel(parent, text="Empresa *", font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.TEXT_MUTED).pack(anchor="w", padx=14, pady=(6, 0))
        self._empresas = self._ectr.listar()
        emp_names = [f"{e.razao_social}" for e in self._empresas] if self._empresas else ["(nenhuma empresa)"]
        self._emp_var = ctk.StringVar(value=emp_names[0])
        ctk.CTkOptionMenu(parent, values=emp_names, variable=self._emp_var, fg_color=T.BG_INPUT, button_color=T.PRIMARY, button_hover_color=T.PRIMARY_HOVER, text_color=T.TEXT).pack(fill="x", padx=14, pady=(0, 2))

        btn_row = ctk.CTkFrame(parent, fg_color="transparent")
        btn_row.pack(fill="x", padx=14, pady=14)
        ctk.CTkButton(btn_row, text="Salvar", width=100, fg_color=T.PRIMARY, hover_color=T.PRIMARY_HOVER, corner_radius=T.CORNER_R, command=self._salvar).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_row, text="Limpar", width=80, fg_color=T.BG_CARD, hover_color=T.BORDER, text_color=T.TEXT_SEC, corner_radius=T.CORNER_R, command=self._limpar).pack(side="left")

    # ------------------------------------------------------------------
    def _refresh_list(self):
        for w in self._list_frame.winfo_children():
            w.destroy()
        funcs = self._ctrl.listar()
        if not funcs:
            ctk.CTkLabel(self._list_frame, text="Nenhum funcionário ativo.", font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.TEXT_MUTED).pack(pady=20)
            return
        for func in funcs:
            row = ctk.CTkFrame(self._list_frame, fg_color=T.BG_CARD, corner_radius=6)
            row.pack(fill="x", pady=3)
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(row, text=func.nome, font=ctk.CTkFont(T.FONT_FAMILY, 11, "bold"), text_color=T.TEXT, anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=(6, 0))
            sub = f"{formatar_cpf(func.cpf)}  |  {func.cargo or '—'}  |  R$ {func.salario:,.2f}"
            ctk.CTkLabel(row, text=sub, font=ctk.CTkFont(T.FONT_FAMILY, 9), text_color=T.TEXT_MUTED, anchor="w").grid(row=1, column=0, sticky="w", padx=10, pady=(0, 6))
            emp_sub = func.empresa_nome or "—"
            ctk.CTkLabel(row, text=emp_sub, font=ctk.CTkFont(T.FONT_FAMILY, 9), text_color=T.ACCENT_LIGHT, anchor="w").grid(row=2, column=0, sticky="w", padx=10, pady=(0, 6))

            btns = ctk.CTkFrame(row, fg_color="transparent")
            btns.grid(row=0, column=1, rowspan=3, padx=8, pady=4)
            ctk.CTkButton(btns, text="✏", width=30, height=28, fg_color=T.ACCENT, hover_color=T.ACCENT_HOVER, corner_radius=6, command=lambda f=func: self._editar(f)).pack(side="left", padx=2)
            ctk.CTkButton(btns, text="🗑", width=30, height=28, fg_color=T.ERROR_BG, hover_color=T.ERROR, corner_radius=6, command=lambda f=func: self._excluir(f)).pack(side="left", padx=2)

    # ------------------------------------------------------------------
    def _limpar(self):
        self._editing_id = None
        for key, entry in self._form_widgets.items():
            entry.delete(0, "end")
        self._form_widgets["jornada"].insert(0, "44h semanais")

    def _editar(self, func: Funcionario):
        self._editing_id = func.id
        mapping = {
            "nome": func.nome, "cpf": func.cpf, "rg": func.rg or "",
            "cargo": func.cargo or "", "salario": str(func.salario),
            "data_admissao": formatar_data_br(func.data_admissao),
            "jornada": func.jornada, "dependentes": str(func.dependentes),
            "vale_transporte": str(func.vale_transporte),
            "nome_mae": func.nome_mae or "", "estado_civil": func.estado_civil or "",
        }
        for k, v in mapping.items():
            e = self._form_widgets[k]
            e.delete(0, "end")
            e.insert(0, v)
        if func.empresa_id and self._empresas:
            for emp in self._empresas:
                if emp.id == func.empresa_id:
                    self._emp_var.set(emp.razao_social)
                    break

    def _get_empresa_id(self) -> int | None:
        sel = self._emp_var.get()
        for emp in self._empresas:
            if emp.razao_social == sel:
                return emp.id
        return None

    def _salvar(self):
        v = {k: w.get().strip() for k, w in self._form_widgets.items()}
        if not v["nome"] or not v["cpf"] or not v["salario"] or not v["data_admissao"]:
            messagebox.showerror("SGR.IA", "Nome, CPF, Salário e Data de Admissão são obrigatórios.")
            return
        from app.services.validators import parse_date
        try:
            sal = float(v["salario"].replace(",", "."))
            adm = parse_date(v["data_admissao"]).isoformat()
        except Exception as ex:
            messagebox.showerror("SGR.IA", f"Valor inválido: {ex}")
            return
        func = Funcionario(
            id=self._editing_id,
            nome=v["nome"], cpf=v["cpf"], rg=v["rg"] or None,
            cargo=v["cargo"] or None, salario=sal, data_admissao=adm,
            empresa_id=self._get_empresa_id(),
            jornada=v["jornada"] or "44h semanais",
            dependentes=int(v["dependentes"] or 0),
            vale_transporte=float((v["vale_transporte"] or "0").replace(",", ".")),
            nome_mae=v["nome_mae"] or None, estado_civil=v["estado_civil"] or None,
        )
        ok, msg = self._ctrl.salvar(func)
        if ok:
            messagebox.showinfo("SGR.IA", msg)
            self._limpar()
            self._refresh_list()
        else:
            messagebox.showerror("SGR.IA", msg)

    def _excluir(self, func: Funcionario):
        if messagebox.askyesno("SGR.IA", f"Desativar funcionário '{func.nome}'?"):
            self._ctrl.excluir(func.id)
            self._refresh_list()
