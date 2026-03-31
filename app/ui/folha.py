"""
Tela de Folha de Pagamento — SGR.IA
"""
import customtkinter as ctk
from tkinter import messagebox
from app.ui import theme as T
from app.services.folha_service import calcular_folha
from app.controllers.funcionario_controller import FuncionarioController
from app.services.validators import formatar_cpf


def _lbl(master, text, size=10, color=None, bold=False):
    return ctk.CTkLabel(master, text=text,
        font=ctk.CTkFont(T.FONT_FAMILY, size, "bold" if bold else "normal"),
        text_color=color or T.TEXT_MUTED, anchor="w")


def _entry(master, placeholder="") -> ctk.CTkEntry:
    return ctk.CTkEntry(master, height=32, fg_color=T.BG_INPUT, border_color=T.BORDER,
        text_color=T.TEXT, placeholder_text=placeholder, placeholder_text_color=T.TEXT_MUTED, corner_radius=6)


class FolhaPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=T.BG_MAIN)
        self._fc = FuncionarioController()
        self._funcs = []
        self._resultado = None
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=T.PAD, pady=(T.PAD, 6))
        ctk.CTkLabel(hdr, text="Folha de Pagamento", font=ctk.CTkFont(T.FONT_FAMILY, 22, "bold"), text_color=T.TEXT).pack(side="left")
        ctk.CTkLabel(hdr, text="Cálculo Mensal — CLT 2026", font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.ACCENT_LIGHT).pack(side="left", padx=14, pady=4)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=T.PAD, pady=(0, T.PAD))
        body.grid_columnconfigure(0, weight=2, uniform="c")
        body.grid_columnconfigure(1, weight=3, uniform="c")
        body.grid_rowconfigure(0, weight=1)

        form_scroll = ctk.CTkScrollableFrame(body, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R)
        form_scroll.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self._build_form(form_scroll)

        self._report_panel = ctk.CTkFrame(body, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R)
        self._report_panel.grid(row=0, column=1, sticky="nsew")
        self._report_panel.grid_rowconfigure(0, weight=1)
        self._report_panel.grid_columnconfigure(0, weight=1)
        self._show_placeholder()

    def _build_form(self, parent):
        _lbl(parent, "FUNCIONÁRIO", 10, T.ACCENT_LIGHT, True).pack(anchor="w", padx=14, pady=(14, 4))

        self._funcs = self._fc.listar()
        names = [f.nome for f in self._funcs] if self._funcs else ["(nenhum)"]
        self._func_var = ctk.StringVar(value=names[0])
        ctk.CTkOptionMenu(parent, values=names, variable=self._func_var, fg_color=T.BG_INPUT,
            button_color=T.PRIMARY, button_hover_color=T.PRIMARY_HOVER, text_color=T.TEXT,
            command=self._on_func_change).pack(fill="x", padx=14, pady=(0, 4))

        self._info = ctk.CTkLabel(parent, text="", font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.TEXT_SEC, anchor="w")
        self._info.pack(anchor="w", padx=14)

        ctk.CTkFrame(parent, height=1, fg_color=T.SEPARATOR).pack(fill="x", padx=14, pady=10)
        _lbl(parent, "PROVENTOS", 10, T.ACCENT_LIGHT, True).pack(anchor="w", padx=14, pady=(0, 4))

        fields = [
            ("salario_base",    "Salário Base (R$)"),
            ("horas_extras_50", "Horas Extras 50% (qtd horas)"),
            ("horas_extras_100","Horas Extras 100% (qtd horas)"),
            ("adicional_noturno","Adicional Noturno (R$)"),
            ("comissoes",       "Comissões (R$)"),
            ("outros_proventos","Outros Proventos (R$)"),
        ]
        self._fields: dict = {}
        for key, label in fields:
            _lbl(parent, label).pack(anchor="w", padx=14, pady=(6, 0))
            e = _entry(parent, "0")
            e.pack(fill="x", padx=14, pady=(0, 2))
            self._fields[key] = e

        ctk.CTkFrame(parent, height=1, fg_color=T.SEPARATOR).pack(fill="x", padx=14, pady=10)
        _lbl(parent, "DESCONTOS", 10, T.ACCENT_LIGHT, True).pack(anchor="w", padx=14, pady=(0, 4))

        for key, label in [("vale_transporte", "Vale Transporte (R$)"), ("outros_descontos", "Outros Descontos (R$)"), ("faltas_dias", "Faltas (dias)")]:
            _lbl(parent, label).pack(anchor="w", padx=14, pady=(6, 0))
            e = _entry(parent, "0")
            e.pack(fill="x", padx=14, pady=(0, 2))
            self._fields[key] = e

        _lbl(parent, "Dependentes IRRF").pack(anchor="w", padx=14, pady=(6, 0))
        self._e_dep = _entry(parent, "0")
        self._e_dep.pack(fill="x", padx=14, pady=(0, 4))

        btn = ctk.CTkFrame(parent, fg_color="transparent")
        btn.pack(fill="x", padx=14, pady=14)
        ctk.CTkButton(btn, text="  ▶  CALCULAR FOLHA", height=40, fg_color=T.PRIMARY, hover_color=T.PRIMARY_HOVER,
            font=ctk.CTkFont(T.FONT_FAMILY, 13, "bold"), corner_radius=T.CORNER_R, command=self._calcular).pack(fill="x")

        if self._funcs:
            self._on_func_change(self._funcs[0].nome)

    def _on_func_change(self, val):
        for f in self._funcs:
            if f.nome == val:
                self._info.configure(text=f"CPF: {formatar_cpf(f.cpf)}  |  R$ {f.salario:,.2f}")
                self._fields["salario_base"].delete(0, "end")
                self._fields["salario_base"].insert(0, str(f.salario))
                self._e_dep.delete(0, "end")
                self._e_dep.insert(0, str(f.dependentes))
                break

    def _show_placeholder(self):
        for w in self._report_panel.winfo_children(): w.destroy()
        ctk.CTkLabel(self._report_panel, text="▶  Preencha e clique em Calcular",
            font=ctk.CTkFont(T.FONT_FAMILY, 13), text_color=T.TEXT_MUTED).place(relx=0.5, rely=0.5, anchor="center")

    def _val(self, key):
        v = self._fields[key].get().strip().replace(",", ".")
        return float(v) if v else 0.0

    def _calcular(self):
        try:
            dados = {
                "salario_base":     self._val("salario_base"),
                "horas_extras_50":  self._val("horas_extras_50"),
                "horas_extras_100": self._val("horas_extras_100"),
                "adicional_noturno":self._val("adicional_noturno"),
                "comissoes":        self._val("comissoes"),
                "outros_proventos": self._val("outros_proventos"),
                "vale_transporte":  self._val("vale_transporte"),
                "outros_descontos": self._val("outros_descontos"),
                "faltas_dias":      int(self._val("faltas_dias")),
                "dependentes":      int(self._e_dep.get().strip() or 0),
            }
        except ValueError as ex:
            messagebox.showerror("SGR.IA", f"Valor inválido: {ex}")
            return

        if dados["salario_base"] <= 0:
            messagebox.showerror("SGR.IA", "Informe o salário base.")
            return

        self._resultado = calcular_folha(dados)
        self._show_report()

    def _show_report(self):
        for w in self._report_panel.winfo_children(): w.destroy()
        r = self._resultado
        scroll = ctk.CTkScrollableFrame(self._report_panel, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=6, pady=6)

        # Title
        tf = ctk.CTkFrame(scroll, fg_color=T.PRIMARY_DARK, corner_radius=T.CORNER_R)
        tf.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(tf, text="SGR.IA — HOLERITE MENSAL", font=ctk.CTkFont(T.FONT_FAMILY, 14, "bold"), text_color=T.TEXT).pack(anchor="w", padx=16, pady=(12, 2))
        ctk.CTkLabel(tf, text=f"Funcionário: {self._func_var.get()}", font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.TEXT_SEC).pack(anchor="w", padx=16, pady=(0, 12))

        # Proventos
        self._section(scroll, "PROVENTOS")
        for k, v in r["proventos"].items():
            self._row(scroll, k, v, T.SUCCESS)

        # Descontos
        self._section(scroll, "DESCONTOS")
        for k, v in r["descontos"].items():
            self._row(scroll, k, v, T.ERROR, True)

        # Encargos empresa
        self._section(scroll, "ENCARGOS EMPRESA (informativo)")
        for k, v in r["encargos_empresa"].items():
            color = T.WARNING if "Total" in k else T.TEXT_SEC
            self._row(scroll, k, v, color)

        # Total
        tf2 = ctk.CTkFrame(scroll, fg_color=T.BG_CARD, corner_radius=T.CORNER_R)
        tf2.pack(fill="x", pady=8)
        for lbl, key, col in [("Total Bruto", "bruto", T.TEXT), ("(-) Descontos", "descontos", T.ERROR)]:
            rw = ctk.CTkFrame(tf2, fg_color="transparent"); rw.pack(fill="x", padx=14, pady=2)
            ctk.CTkLabel(rw, text=lbl, font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.TEXT_SEC).pack(side="left")
            ctk.CTkLabel(rw, text=f"R$ {r['totais'][key]:,.2f}", font=ctk.CTkFont(T.FONT_FAMILY, 11, "bold"), text_color=col).pack(side="right")
        ctk.CTkFrame(tf2, height=1, fg_color=T.BORDER).pack(fill="x", padx=14, pady=4)
        rw = ctk.CTkFrame(tf2, fg_color="transparent"); rw.pack(fill="x", padx=14, pady=(0, 6))
        ctk.CTkLabel(rw, text="SALÁRIO LÍQUIDO", font=ctk.CTkFont(T.FONT_FAMILY, 13, "bold"), text_color=T.TEXT).pack(side="left")
        ctk.CTkLabel(rw, text=f"R$ {r['totais']['liquido']:,.2f}", font=ctk.CTkFont(T.FONT_FAMILY, 16, "bold"), text_color=T.ACCENT).pack(side="right")

        rw2 = ctk.CTkFrame(tf2, fg_color="transparent"); rw2.pack(fill="x", padx=14, pady=(0, 12))
        ctk.CTkLabel(rw2, text="Custo Total Empresa", font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.TEXT_MUTED).pack(side="left")
        ctk.CTkLabel(rw2, text=f"R$ {r['totais']['custo_total_empresa']:,.2f}", font=ctk.CTkFont(T.FONT_FAMILY, 11, "bold"), text_color=T.WARNING).pack(side="right")

    def _section(self, parent, title):
        f = ctk.CTkFrame(parent, fg_color=T.BG_CARD, corner_radius=6); f.pack(fill="x", pady=(8, 2))
        ctk.CTkLabel(f, text=title, font=ctk.CTkFont(T.FONT_FAMILY, 10, "bold"), text_color=T.TEXT_MUTED).pack(anchor="w", padx=12, pady=6)

    def _row(self, parent, label, valor, color, desc=False):
        rw = ctk.CTkFrame(parent, fg_color="transparent"); rw.pack(fill="x", padx=4, pady=1)
        sign = "-" if desc else "+"
        ctk.CTkLabel(rw, text=label, font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.TEXT_SEC, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(rw, text=f"{sign} R$ {valor:,.2f}", font=ctk.CTkFont(T.FONT_FAMILY, 11, "bold"), text_color=color).pack(side="right", padx=10)
