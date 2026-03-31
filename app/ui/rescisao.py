"""
Tela de Cálculo de Rescisão — SGR.IA
Motor CLT 2026 integrado com relatório completo.
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import date

from app.ui import theme as T
from app.services.calculators import calcular_rescisao, VERBAS_RESCISAO
from app.services.validators import parse_date, formatar_data_br, formatar_cpf
from app.controllers.funcionario_controller import FuncionarioController
from app.controllers.rescisao_controller import RescisaoController

TIPOS_LABEL = {
    "sem_justa_causa":  "Sem Justa Causa",
    "justa_causa":      "Com Justa Causa",
    "pedido_demissao":  "Pedido de Demissão",
    "acordo_consensual":"Acordo Consensual (art. 484-A)",
    "termino_contrato": "Término de Contrato",
}
TIPOS_KEYS = list(TIPOS_LABEL.values())


def _lbl(master, text, size=10, color=None, bold=False):
    return ctk.CTkLabel(
        master, text=text,
        font=ctk.CTkFont(T.FONT_FAMILY, size, "bold" if bold else "normal"),
        text_color=color or T.TEXT_MUTED,
        anchor="w",
    )


def _entry(master, placeholder="") -> ctk.CTkEntry:
    return ctk.CTkEntry(
        master, height=32,
        fg_color=T.BG_INPUT, border_color=T.BORDER,
        text_color=T.TEXT, placeholder_text=placeholder,
        placeholder_text_color=T.TEXT_MUTED,
        corner_radius=6,
    )


class RescisaoPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=T.BG_MAIN)
        self._fc      = FuncionarioController()
        self._rc      = RescisaoController()
        self._funcs   = []
        self._resultado = None
        self._func_selecionado = None
        self._build()

    # ==================================================================
    def _build(self):
        # Page header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=T.PAD, pady=(T.PAD, 6))
        ctk.CTkLabel(hdr, text="Cálculo de Rescisão",
                     font=ctk.CTkFont(T.FONT_FAMILY, 22, "bold"), text_color=T.TEXT).pack(side="left")
        ctk.CTkLabel(hdr, text="SGR.IA — Especialista CLT 2026",
                     font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.ACCENT_LIGHT).pack(side="left", padx=14, pady=4)

        # Main body: form (left) + report (right)
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=T.PAD, pady=(0, T.PAD))
        body.grid_columnconfigure(0, weight=2, uniform="cols")
        body.grid_columnconfigure(1, weight=3, uniform="cols")
        body.grid_rowconfigure(0, weight=1)

        # --- Form panel -----------------------------------------------
        form_scroll = ctk.CTkScrollableFrame(body, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R)
        form_scroll.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self._build_form(form_scroll)

        # --- Report panel ---------------------------------------------
        self._report_panel = ctk.CTkFrame(body, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R)
        self._report_panel.grid(row=0, column=1, sticky="nsew")
        self._report_panel.grid_rowconfigure(0, weight=1)
        self._report_panel.grid_columnconfigure(0, weight=1)
        self._show_report_placeholder()

    # ------------------------------------------------------------------
    def _build_form(self, parent):
        _lbl(parent, "DADOS DO FUNCIONÁRIO", 10, T.ACCENT_LIGHT, True).pack(anchor="w", padx=14, pady=(14, 4))

        # Funcionário (dropdown)
        _lbl(parent, "Selecionar Funcionário").pack(anchor="w", padx=14, pady=(6, 0))
        self._funcs = self._fc.listar()
        func_names  = [f.nome for f in self._funcs] if self._funcs else ["(nenhum cadastrado)"]
        self._func_var = ctk.StringVar(value=func_names[0])
        ctk.CTkOptionMenu(
            parent, values=func_names, variable=self._func_var,
            fg_color=T.BG_INPUT, button_color=T.PRIMARY,
            button_hover_color=T.PRIMARY_HOVER, text_color=T.TEXT,
            command=self._on_func_change,
        ).pack(fill="x", padx=14, pady=(0, 4))

        # Info bar (auto-fill)
        self._info_bar = ctk.CTkLabel(
            parent, text="", font=ctk.CTkFont(T.FONT_FAMILY, 10),
            text_color=T.TEXT_SEC, anchor="w",
        )
        self._info_bar.pack(anchor="w", padx=14)

        # Salário override
        _lbl(parent, "Salário Base (R$) — ou deixe vazio para usar do cadastro").pack(anchor="w", padx=14, pady=(8, 0))
        self._e_salario = _entry(parent, "Ex: 2500,00")
        self._e_salario.pack(fill="x", padx=14, pady=(0, 4))

        # Separator
        ctk.CTkFrame(parent, height=1, fg_color=T.SEPARATOR).pack(fill="x", padx=14, pady=10)
        _lbl(parent, "DADOS DA RESCISÃO", 10, T.ACCENT_LIGHT, True).pack(anchor="w", padx=14, pady=(0, 4))

        # Tipo
        _lbl(parent, "Tipo de Rescisão *").pack(anchor="w", padx=14, pady=(6, 0))
        self._tipo_var = ctk.StringVar(value=TIPOS_KEYS[0])
        ctk.CTkOptionMenu(
            parent, values=TIPOS_KEYS, variable=self._tipo_var,
            fg_color=T.BG_INPUT, button_color=T.PRIMARY,
            button_hover_color=T.PRIMARY_HOVER, text_color=T.TEXT,
        ).pack(fill="x", padx=14, pady=(0, 4))

        # Dates
        _lbl(parent, "Último Dia Trabalhado *  (DD/MM/AAAA)").pack(anchor="w", padx=14, pady=(6, 0))
        self._e_ultimo_dia = _entry(parent, "31/03/2026")
        self._e_ultimo_dia.pack(fill="x", padx=14, pady=(0, 4))

        _lbl(parent, "Data do Aviso Prévio  (DD/MM/AAAA) — opcional").pack(anchor="w", padx=14, pady=(6, 0))
        self._e_aviso = _entry(parent, "DD/MM/AAAA")
        self._e_aviso.pack(fill="x", padx=14, pady=(0, 4))

        # Aviso prévio
        _lbl(parent, "Situação do Aviso Prévio").pack(anchor="w", padx=14, pady=(6, 0))
        self._aviso_var = ctk.StringVar(value="Trabalhado")
        ctk.CTkSegmentedButton(
            parent,
            values=["Trabalhado", "Indenizado", "Dispensado"],
            variable=self._aviso_var,
            fg_color=T.BG_INPUT,
            selected_color=T.PRIMARY,
            selected_hover_color=T.PRIMARY_HOVER,
            unselected_color=T.BG_INPUT,
            text_color=T.TEXT,
        ).pack(fill="x", padx=14, pady=(0, 4))

        # Dias trabalhados no mês
        _lbl(parent, "Dias Trabalhados no Último Mês *").pack(anchor="w", padx=14, pady=(6, 0))
        self._e_dias = _entry(parent, "Ex: 15")
        self._e_dias.pack(fill="x", padx=14, pady=(0, 4))

        # Separator
        ctk.CTkFrame(parent, height=1, fg_color=T.SEPARATOR).pack(fill="x", padx=14, pady=10)
        _lbl(parent, "FÉRIAS E 13º", 10, T.ACCENT_LIGHT, True).pack(anchor="w", padx=14, pady=(0, 4))

        _lbl(parent, "Períodos de Férias Vencidas (anos)").pack(anchor="w", padx=14, pady=(6, 0))
        self._e_fer_venc = _entry(parent, "Ex: 1")
        self._e_fer_venc.pack(fill="x", padx=14, pady=(0, 4))

        _lbl(parent, "Meses no Período Aquisitivo Atual (férias prop.)").pack(anchor="w", padx=14, pady=(6, 0))
        self._e_fer_prop = _entry(parent, "Ex: 7")
        self._e_fer_prop.pack(fill="x", padx=14, pady=(0, 4))

        # Separator
        ctk.CTkFrame(parent, height=1, fg_color=T.SEPARATOR).pack(fill="x", padx=14, pady=10)
        _lbl(parent, "FGTS E DESCONTOS", 10, T.ACCENT_LIGHT, True).pack(anchor="w", padx=14, pady=(0, 4))

        _lbl(parent, "Saldo FGTS Acumulado (R$) — extrato CEF").pack(anchor="w", padx=14, pady=(6, 0))
        self._e_fgts = _entry(parent, "Ex: 4200,00")
        self._e_fgts.pack(fill="x", padx=14, pady=(0, 4))

        _lbl(parent, "Dependentes para IRRF").pack(anchor="w", padx=14, pady=(6, 0))
        self._e_dep = _entry(parent, "Ex: 2")
        self._e_dep.pack(fill="x", padx=14, pady=(0, 4))

        _lbl(parent, "Outras Verbas / Adicionais (R$)").pack(anchor="w", padx=14, pady=(6, 0))
        self._e_outras = _entry(parent, "Ex: 500,00")
        self._e_outras.pack(fill="x", padx=14, pady=(0, 4))

        # Observações
        _lbl(parent, "Observações").pack(anchor="w", padx=14, pady=(8, 0))
        self._e_obs = ctk.CTkTextbox(
            parent, height=60, fg_color=T.BG_INPUT,
            border_color=T.BORDER, text_color=T.TEXT, corner_radius=6,
        )
        self._e_obs.pack(fill="x", padx=14, pady=(0, 4))

        # Buttons
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x", padx=14, pady=14)

        ctk.CTkButton(
            btn_frame, text="  ▶  CALCULAR RESCISÃO",
            height=40,
            fg_color=T.PRIMARY, hover_color=T.PRIMARY_HOVER,
            font=ctk.CTkFont(T.FONT_FAMILY, 13, "bold"),
            corner_radius=T.CORNER_R,
            command=self._calcular,
        ).pack(fill="x", pady=(0, 6))

        ctk.CTkButton(
            btn_frame, text="Limpar",
            height=32,
            fg_color=T.BG_CARD, hover_color=T.BORDER,
            text_color=T.TEXT_SEC,
            corner_radius=T.CORNER_R,
            command=self._limpar,
        ).pack(fill="x")

        # Auto-fill first func
        if self._funcs:
            self._on_func_change(self._funcs[0].nome)

    # ------------------------------------------------------------------
    def _on_func_change(self, value):
        self._func_selecionado = None
        for f in self._funcs:
            if f.nome == value:
                self._func_selecionado = f
                break
        if self._func_selecionado:
            f = self._func_selecionado
            info = f"CPF: {formatar_cpf(f.cpf)}  |  Admissão: {formatar_data_br(f.data_admissao)}  |  R$ {f.salario:,.2f}"
            self._info_bar.configure(text=info)
            # Auto-fill dependentes
            self._e_dep.delete(0, "end")
            self._e_dep.insert(0, str(f.dependentes))

    # ------------------------------------------------------------------
    def _limpar(self):
        for w in [self._e_salario, self._e_ultimo_dia, self._e_aviso, self._e_dias,
                  self._e_fer_venc, self._e_fer_prop, self._e_fgts, self._e_dep, self._e_outras]:
            w.delete(0, "end")
        self._e_obs.delete("1.0", "end")
        self._show_report_placeholder()

    # ------------------------------------------------------------------
    def _calcular(self):
        erros = []

        # Funcionário / salário
        func = self._func_selecionado
        sal_str = self._e_salario.get().strip().replace(",", ".")
        if sal_str:
            try:
                salario = float(sal_str)
            except ValueError:
                erros.append("Salário inválido.")
                salario = 0.0
        elif func:
            salario = func.salario
        else:
            erros.append("Selecione um funcionário ou informe o salário.")
            salario = 0.0

        # Último dia
        ultimo_str = self._e_ultimo_dia.get().strip()
        if not ultimo_str:
            erros.append("Informe o último dia trabalhado.")
            ultimo_dia = date.today()
        else:
            try:
                ultimo_dia = parse_date(ultimo_str)
            except ValueError:
                erros.append("Data do último dia inválida.")
                ultimo_dia = date.today()

        # Admissão
        if func:
            try:
                admissao = parse_date(func.data_admissao)
            except ValueError:
                erros.append("Data de admissão inválida no cadastro.")
                admissao = date.today()
        else:
            erros.append("Selecione um funcionário com data de admissão.")
            admissao = date.today()

        # Dias trabalhados
        dias_str = self._e_dias.get().strip()
        try:
            dias = int(dias_str) if dias_str else 30
        except ValueError:
            erros.append("Dias trabalhados inválido.")
            dias = 30

        # Tipo
        tipo_label = self._tipo_var.get()
        tipo_key = next((k for k, v in TIPOS_LABEL.items() if v == tipo_label), "sem_justa_causa")

        # Aviso prévio
        aviso_trab = self._aviso_var.get() == "Trabalhado"

        # Ferías
        try:
            periodos_fer = int(self._e_fer_venc.get().strip() or 0)
        except ValueError:
            periodos_fer = 0
        try:
            meses_fer_prop = int(self._e_fer_prop.get().strip() or 0)
        except ValueError:
            meses_fer_prop = 0

        # FGTS
        fgts_str = self._e_fgts.get().strip().replace(",", ".")
        try:
            saldo_fgts = float(fgts_str) if fgts_str else 0.0
        except ValueError:
            saldo_fgts = 0.0

        # Dependentes
        try:
            dependentes = int(self._e_dep.get().strip() or 0)
        except ValueError:
            dependentes = 0

        # Outras verbas
        outras_str = self._e_outras.get().strip().replace(",", ".")
        try:
            outras = float(outras_str) if outras_str else 0.0
        except ValueError:
            outras = 0.0

        if erros:
            messagebox.showerror("SGR.IA — Dados Incompletos", "\n".join(erros))
            return

        if ultimo_dia < admissao:
            messagebox.showerror("SGR.IA", "Data de desligamento anterior à admissão.")
            return

        dados = {
            "salario":           salario,
            "data_admissao":     admissao,
            "data_desligamento": ultimo_dia,
            "tipo_rescisao":     tipo_key,
            "dias_trabalhados":  dias,
            "periodos_ferias":   periodos_fer,
            "meses_ferias_prop": meses_fer_prop,
            "aviso_trabalhado":  aviso_trab,
            "saldo_fgts":        saldo_fgts,
            "dependentes":       dependentes,
            "outras_verbas":     outras,
        }

        self._resultado = calcular_rescisao(dados)
        self._resultado["_meta"] = {
            "funcionario": func.nome if func else "Avulso",
            "func_id":     func.id if func else None,
            "admissao":    admissao,
            "desligamento": ultimo_dia,
            "tipo_key":    tipo_key,
            "tipo_label":  tipo_label,
            "observacoes": self._e_obs.get("1.0", "end").strip(),
            "saldo_fgts":  saldo_fgts,
        }
        self._show_report()

    # ==================================================================
    # RELATÓRIO
    # ==================================================================

    def _show_report_placeholder(self):
        for w in self._report_panel.winfo_children():
            w.destroy()
        ctk.CTkLabel(
            self._report_panel,
            text="▶  Preencha o formulário e clique em Calcular",
            font=ctk.CTkFont(T.FONT_FAMILY, 13),
            text_color=T.TEXT_MUTED,
        ).place(relx=0.5, rely=0.5, anchor="center")

    # ------------------------------------------------------------------
    def _show_report(self):
        for w in self._report_panel.winfo_children():
            w.destroy()

        r   = self._resultado
        meta = r["_meta"]

        scroll = ctk.CTkScrollableFrame(self._report_panel, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=6, pady=6)

        # ---- Title block -------------------------------------------
        title_frame = ctk.CTkFrame(scroll, fg_color=T.PRIMARY_DARK, corner_radius=T.CORNER_R)
        title_frame.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(title_frame, text="SGR.IA — RELATÓRIO DE RESCISÃO",
                     font=ctk.CTkFont(T.FONT_FAMILY, 14, "bold"), text_color=T.TEXT).pack(anchor="w", padx=16, pady=(12, 2))
        ctk.CTkLabel(title_frame, text=f"Funcionário: {meta['funcionario']}",
                     font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.TEXT_SEC).pack(anchor="w", padx=16, pady=0)
        ctk.CTkLabel(title_frame, text=f"Tipo: {meta['tipo_label']}   |   Admissão: {formatar_data_br(meta['admissao'])}   |   Desligamento: {formatar_data_br(meta['desligamento'])}",
                     font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.TEXT_MUTED).pack(anchor="w", padx=16, pady=(0, 12))

        det = r["detalhes"]
        ctk.CTkLabel(title_frame,
                     text=f"Anos de serviço: {det['anos_servico']}   |   Aviso Prévio: {det['dias_aviso']} dias   |   Meses no ano: {det['meses_ano']}",
                     font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.ACCENT_LIGHT).pack(anchor="w", padx=16, pady=(0, 12))

        # ---- Verbas ------------------------------------------------
        self._section(scroll, "VERBAS RESCISÓRIAS")
        for nome, valor in r["verbas"].items():
            self._row(scroll, nome, valor, T.SUCCESS)

        # ---- Descontos --------------------------------------------
        self._section(scroll, "DESCONTOS")
        for nome, valor in r["descontos"].items():
            self._row(scroll, nome, valor, T.ERROR, desconto=True)

        # ---- Totais -----------------------------------------------
        totais_frame = ctk.CTkFrame(scroll, fg_color=T.BG_CARD, corner_radius=T.CORNER_R)
        totais_frame.pack(fill="x", pady=8)
        for label, key, color in [
            ("Total Bruto",     "bruto",     T.TEXT),
            ("(-) INSS",        "inss",      T.ERROR),
            ("(-) IRRF",        "irrf",      T.ERROR),
        ]:
            row = ctk.CTkFrame(totais_frame, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=2)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.TEXT_SEC, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=f"R$ {r['totais'][key]:,.2f}", font=ctk.CTkFont(T.FONT_FAMILY, 11, "bold"), text_color=color).pack(side="right")

        # Divider
        ctk.CTkFrame(totais_frame, height=1, fg_color=T.BORDER).pack(fill="x", padx=14, pady=4)

        liq_row = ctk.CTkFrame(totais_frame, fg_color="transparent")
        liq_row.pack(fill="x", padx=14, pady=(0, 12))
        ctk.CTkLabel(liq_row, text="TOTAL LÍQUIDO A RECEBER", font=ctk.CTkFont(T.FONT_FAMILY, 13, "bold"), text_color=T.TEXT).pack(side="left")
        ctk.CTkLabel(liq_row, text=f"R$ {r['totais']['liquido']:,.2f}", font=ctk.CTkFont(T.FONT_FAMILY, 16, "bold"), text_color=T.ACCENT).pack(side="right")

        # ---- Checklist -------------------------------------------
        self._section(scroll, "CHECKLIST DOCUMENTAL")
        for item in r["checklist"]:
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", padx=4, pady=1)
            ctk.CTkLabel(row, text="☐", font=ctk.CTkFont(T.FONT_FAMILY, 12), text_color=T.ACCENT).pack(side="left", padx=(6, 4))
            ctk.CTkLabel(row, text=item, font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.TEXT_SEC, anchor="w", wraplength=380).pack(side="left", fill="x", expand=True)

        # ---- Alertas ----------------------------------------------
        if r["alertas"]:
            self._section(scroll, "ALERTAS JURÍDICOS")
            nivel_cfg = {
                "erro":    (T.ERROR,   T.ERROR_BG,   "⛔"),
                "atencao": (T.WARNING, T.WARNING_BG, "⚠️"),
                "info":    (T.INFO,    T.INFO_BG,    "ℹ️"),
            }
            for alerta in r["alertas"]:
                nivel = alerta.get("nivel", "info")
                color, bg, icon = nivel_cfg.get(nivel, (T.INFO, T.INFO_BG, "ℹ️"))
                af = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=6)
                af.pack(fill="x", pady=3, padx=4)
                ctk.CTkLabel(af, text=icon, font=ctk.CTkFont(T.FONT_FAMILY, 12)).pack(side="left", padx=8, pady=8)
                ctk.CTkLabel(af, text=alerta["msg"], font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=color, anchor="w", wraplength=360).pack(side="left", fill="x", expand=True, padx=(0, 8), pady=8)

        # ---- Save button -----------------------------------------
        ctk.CTkButton(
            scroll, text="💾  Salvar Rescisão no Banco",
            height=38, fg_color=T.ACCENT, hover_color=T.ACCENT_HOVER,
            font=ctk.CTkFont(T.FONT_FAMILY, 12, "bold"),
            corner_radius=T.CORNER_R,
            command=self._salvar_resultado,
        ).pack(fill="x", pady=(12, 4))

    # ------------------------------------------------------------------
    def _section(self, parent, title: str):
        f = ctk.CTkFrame(parent, fg_color=T.BG_CARD, corner_radius=6)
        f.pack(fill="x", pady=(8, 2))
        ctk.CTkLabel(f, text=title, font=ctk.CTkFont(T.FONT_FAMILY, 10, "bold"), text_color=T.TEXT_MUTED).pack(anchor="w", padx=12, pady=6)

    def _row(self, parent, label: str, valor: float, color: str, desconto=False):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=4, pady=1)
        sign = "-" if desconto else "+"
        ctk.CTkLabel(row, text=label, font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.TEXT_SEC, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(row, text=f"{sign} R$ {valor:,.2f}", font=ctk.CTkFont(T.FONT_FAMILY, 11, "bold"), text_color=color).pack(side="right", padx=10)

    # ------------------------------------------------------------------
    def _salvar_resultado(self):
        if not self._resultado:
            return
        r    = self._resultado
        meta = r["_meta"]
        verbas = r["verbas"]
        dados_db = {
            "funcionario_id":    meta["func_id"],
            "tipo_rescisao":     meta["tipo_key"],
            "ultimo_dia":        meta["desligamento"].isoformat(),
            "aviso_previo_tipo": self._aviso_var.get(),
            "saldo_salario":     verbas.get("Saldo de Salário", 0),
            "ferias_vencidas":   verbas.get("Férias Vencidas + 1/3", 0),
            "ferias_proporcionais": verbas.get("Férias Proporcionais + 1/3", 0),
            "decimo_terceiro":   verbas.get("13º Salário Proporcional", 0),
            "aviso_indenizado":  verbas.get("Aviso Prévio Indenizado", 0),
            "fgts_rescisao":     verbas.get("FGTS s/ Verbas Rescisórias (8%)", 0),
            "multa_fgts":        verbas.get(next((k for k in verbas if "Multa" in k), ""), 0),
            "inss":              r["totais"]["inss"],
            "irrf":              r["totais"]["irrf"],
            "valor_bruto":       r["totais"]["bruto"],
            "valor_liquido":     r["totais"]["liquido"],
            "saldo_fgts_total":  meta["saldo_fgts"],
            "observacoes":       meta["observacoes"],
        }
        ok, msg = self._rc.salvar(dados_db)
        if ok:
            messagebox.showinfo("SGR.IA", "✅  Rescisão salva com sucesso!")
        else:
            messagebox.showerror("SGR.IA", f"Erro ao salvar: {msg}")
