"""
Tela de Cálculo de Férias — SGR.IA
"""
import customtkinter as ctk
from tkinter import messagebox
from app.ui import theme as T
from app.services.ferias_service import calcular_ferias
from app.controllers.funcionario_controller import FuncionarioController
from app.services.validators import formatar_cpf


def _lbl(master, text, size=10, color=None, bold=False):
    return ctk.CTkLabel(master, text=text,
        font=ctk.CTkFont(T.FONT_FAMILY, size, "bold" if bold else "normal"),
        text_color=color or T.TEXT_MUTED, anchor="w")


def _entry(master, placeholder="") -> ctk.CTkEntry:
    return ctk.CTkEntry(master, height=32, fg_color=T.BG_INPUT, border_color=T.BORDER,
        text_color=T.TEXT, placeholder_text=placeholder, placeholder_text_color=T.TEXT_MUTED, corner_radius=6)


class FeriasPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=T.BG_MAIN)
        self._fc = FuncionarioController()
        self._funcs = []
        self._resultado = None
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=T.PAD, pady=(T.PAD, 6))
        ctk.CTkLabel(hdr, text="Cálculo de Férias", font=ctk.CTkFont(T.FONT_FAMILY, 22, "bold"), text_color=T.TEXT).pack(side="left")
        ctk.CTkLabel(hdr, text="CLT art. 129 a 145", font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.ACCENT_LIGHT).pack(side="left", padx=14, pady=4)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=T.PAD, pady=(0, T.PAD))
        body.grid_columnconfigure(0, weight=2, uniform="c")
        body.grid_columnconfigure(1, weight=3, uniform="c")
        body.grid_rowconfigure(0, weight=1)

        form = ctk.CTkScrollableFrame(body, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R)
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self._build_form(form)

        self._report = ctk.CTkFrame(body, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R)
        self._report.grid(row=0, column=1, sticky="nsew")
        self._report.grid_rowconfigure(0, weight=1)
        self._report.grid_columnconfigure(0, weight=1)
        self._placeholder()

    def _build_form(self, p):
        _lbl(p, "FUNCIONÁRIO", 10, T.ACCENT_LIGHT, True).pack(anchor="w", padx=14, pady=(14, 4))
        self._funcs = self._fc.listar()
        names = [f.nome for f in self._funcs] if self._funcs else ["(nenhum)"]
        self._func_var = ctk.StringVar(value=names[0])
        ctk.CTkOptionMenu(p, values=names, variable=self._func_var, fg_color=T.BG_INPUT,
            button_color=T.PRIMARY, button_hover_color=T.PRIMARY_HOVER, text_color=T.TEXT,
            command=self._on_func).pack(fill="x", padx=14, pady=(0, 4))
        self._info = ctk.CTkLabel(p, text="", font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.TEXT_SEC, anchor="w")
        self._info.pack(anchor="w", padx=14)

        ctk.CTkFrame(p, height=1, fg_color=T.SEPARATOR).pack(fill="x", padx=14, pady=10)
        _lbl(p, "DADOS DAS FÉRIAS", 10, T.ACCENT_LIGHT, True).pack(anchor="w", padx=14, pady=(0, 4))

        self._fields: dict = {}
        for key, label, ph in [
            ("salario", "Salário Base (R$)", ""),
            ("dias_ferias", "Dias de Férias (30 normal / 20 com abono)", "30"),
            ("media_extras", "Média HE (12 meses) R$", "0"),
            ("adicionais", "Adicionais (noturno, periculosidade) R$", "0"),
            ("dependentes", "Dependentes IRRF", "0"),
            ("periodo_aquisitivo", "Período Aquisitivo", "01/04/2024 a 31/03/2025"),
        ]:
            _lbl(p, label).pack(anchor="w", padx=14, pady=(6, 0))
            e = _entry(p, ph)
            e.pack(fill="x", padx=14, pady=(0, 2))
            self._fields[key] = e

        _lbl(p, "Abono Pecuniário (vender 10 dias)?").pack(anchor="w", padx=14, pady=(8, 0))
        self._abono_var = ctk.StringVar(value="Não")
        ctk.CTkSegmentedButton(p, values=["Não", "Sim"], variable=self._abono_var,
            fg_color=T.BG_INPUT, selected_color=T.PRIMARY, selected_hover_color=T.PRIMARY_HOVER,
            unselected_color=T.BG_INPUT, text_color=T.TEXT).pack(fill="x", padx=14, pady=(0, 4))

        ctk.CTkButton(p, text="  ▶  CALCULAR FÉRIAS", height=40, fg_color=T.PRIMARY, hover_color=T.PRIMARY_HOVER,
            font=ctk.CTkFont(T.FONT_FAMILY, 13, "bold"), corner_radius=T.CORNER_R, command=self._calcular).pack(fill="x", padx=14, pady=14)

        if self._funcs:
            self._on_func(self._funcs[0].nome)

    def _on_func(self, val):
        for f in self._funcs:
            if f.nome == val:
                self._info.configure(text=f"CPF: {formatar_cpf(f.cpf)}  |  R$ {f.salario:,.2f}")
                self._fields["salario"].delete(0, "end")
                self._fields["salario"].insert(0, str(f.salario))
                self._fields["dependentes"].delete(0, "end")
                self._fields["dependentes"].insert(0, str(f.dependentes))
                break

    def _placeholder(self):
        for w in self._report.winfo_children(): w.destroy()
        ctk.CTkLabel(self._report, text="▶  Preencha e calcule as férias",
            font=ctk.CTkFont(T.FONT_FAMILY, 13), text_color=T.TEXT_MUTED).place(relx=0.5, rely=0.5, anchor="center")

    def _calcular(self):
        try:
            dados = {
                "salario": float(self._fields["salario"].get().strip().replace(",", ".") or 0),
                "dias_ferias": int(self._fields["dias_ferias"].get().strip() or 30),
                "media_extras": float(self._fields["media_extras"].get().strip().replace(",", ".") or 0),
                "adicionais": float(self._fields["adicionais"].get().strip().replace(",", ".") or 0),
                "dependentes": int(self._fields["dependentes"].get().strip() or 0),
                "abono_pecuniario": self._abono_var.get() == "Sim",
                "periodo_aquisitivo": self._fields["periodo_aquisitivo"].get().strip(),
            }
        except ValueError as ex:
            messagebox.showerror("SGR.IA", f"Valor inválido: {ex}")
            return
        if dados["salario"] <= 0:
            messagebox.showerror("SGR.IA", "Informe o salário.")
            return
        self._resultado = calcular_ferias(dados)
        self._show_report()

    def _show_report(self):
        for w in self._report.winfo_children(): w.destroy()
        r = self._resultado
        scroll = ctk.CTkScrollableFrame(self._report, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=6, pady=6)

        tf = ctk.CTkFrame(scroll, fg_color=T.PRIMARY_DARK, corner_radius=T.CORNER_R)
        tf.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(tf, text="SGR.IA — RECIBO DE FÉRIAS", font=ctk.CTkFont(T.FONT_FAMILY, 14, "bold"), text_color=T.TEXT).pack(anchor="w", padx=16, pady=(12, 2))
        ctk.CTkLabel(tf, text=f"Funcionário: {self._func_var.get()}", font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.TEXT_SEC).pack(anchor="w", padx=16)
        ctk.CTkLabel(tf, text=f"Período: {r['detalhes'].get('periodo_aquisitivo', '—')}  |  Dias: {r['detalhes']['dias_ferias']}", font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.TEXT_MUTED).pack(anchor="w", padx=16, pady=(0, 12))

        self._sec(scroll, "PROVENTOS")
        for k, v in r["proventos"].items():
            self._row(scroll, k, v, T.SUCCESS)

        self._sec(scroll, "DESCONTOS")
        for k, v in r["descontos"].items():
            self._row(scroll, k, v, T.ERROR, True)

        tf2 = ctk.CTkFrame(scroll, fg_color=T.BG_CARD, corner_radius=T.CORNER_R)
        tf2.pack(fill="x", pady=8)
        ctk.CTkFrame(tf2, height=1, fg_color=T.BORDER).pack(fill="x", padx=14, pady=4)
        rw = ctk.CTkFrame(tf2, fg_color="transparent"); rw.pack(fill="x", padx=14, pady=(0, 12))
        ctk.CTkLabel(rw, text="VALOR LÍQUIDO FÉRIAS", font=ctk.CTkFont(T.FONT_FAMILY, 13, "bold"), text_color=T.TEXT).pack(side="left")
        ctk.CTkLabel(rw, text=f"R$ {r['totais']['liquido']:,.2f}", font=ctk.CTkFont(T.FONT_FAMILY, 16, "bold"), text_color=T.ACCENT).pack(side="right")

        if r.get("alertas"):
            self._sec(scroll, "ALERTAS")
            for a in r["alertas"]:
                af = ctk.CTkFrame(scroll, fg_color=T.INFO_BG, corner_radius=6); af.pack(fill="x", pady=2, padx=4)
                ctk.CTkLabel(af, text=f"ℹ️  {a}", font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.INFO, anchor="w", wraplength=380).pack(padx=10, pady=6)

    def _sec(self, p, t):
        f = ctk.CTkFrame(p, fg_color=T.BG_CARD, corner_radius=6); f.pack(fill="x", pady=(8, 2))
        ctk.CTkLabel(f, text=t, font=ctk.CTkFont(T.FONT_FAMILY, 10, "bold"), text_color=T.TEXT_MUTED).pack(anchor="w", padx=12, pady=6)

    def _row(self, p, label, valor, color, desc=False):
        rw = ctk.CTkFrame(p, fg_color="transparent"); rw.pack(fill="x", padx=4, pady=1)
        sign = "-" if desc else "+"
        ctk.CTkLabel(rw, text=label, font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.TEXT_SEC, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(rw, text=f"{sign} R$ {valor:,.2f}", font=ctk.CTkFont(T.FONT_FAMILY, 11, "bold"), text_color=color).pack(side="right", padx=10)
