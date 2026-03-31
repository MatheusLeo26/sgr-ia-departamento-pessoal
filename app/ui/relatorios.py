"""
Tela de Relatórios — SGR.IA
Gera relatórios em PDF e exibe resumos operacionais.
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import date, datetime
import os

from app.ui import theme as T
from app.controllers.empresa_controller import EmpresaController
from app.controllers.funcionario_controller import FuncionarioController
from app.controllers.rescisao_controller import RescisaoController
from app.services.validators import formatar_cpf, formatar_data_br


class RelatoriosPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=T.BG_MAIN)
        self._ec = EmpresaController()
        self._fc = FuncionarioController()
        self._rc = RescisaoController()
        self._build()

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=T.PAD, pady=(T.PAD, 6))
        ctk.CTkLabel(hdr, text="Relatórios", font=ctk.CTkFont(T.FONT_FAMILY, 22, "bold"), text_color=T.TEXT).pack(side="left")
        ctk.CTkLabel(hdr, text="Exportação e Resumos Operacionais", font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.ACCENT_LIGHT).pack(side="left", padx=14, pady=4)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=T.PAD, pady=(0, T.PAD))
        body.grid_columnconfigure(0, weight=1, uniform="r")
        body.grid_columnconfigure(1, weight=1, uniform="r")
        body.grid_rowconfigure((0, 1), weight=1)

        # Card: Funcionários Ativos
        self._card(body, 0, 0,
            "👤  Relatório de Funcionários Ativos",
            "Exporta lista completa de funcionários ativos com dados cadastrais, salário e empresa vinculada.",
            "Exportar TXT",
            self._relatorio_funcionarios,
        )

        # Card: Rescisões do Mês
        self._card(body, 0, 1,
            "📋  Relatório de Rescisões",
            "Exporta as últimas rescisões processadas com verbas, descontos e total líquido.",
            "Exportar TXT",
            self._relatorio_rescisoes,
        )

        # Card: Empresas
        self._card(body, 1, 0,
            "🏢  Relatório de Empresas",
            "Lista todas as empresas cadastradas com CNPJ, regime tributário e sindicato.",
            "Exportar TXT",
            self._relatorio_empresas,
        )

        # Card: Resumo Geral
        self._card(body, 1, 1,
            "📊  Resumo Geral do Sistema",
            "Visão consolidada: total de empresas, funcionários, rescisões e indicadores operacionais.",
            "Gerar Resumo",
            self._resumo_geral,
        )

    def _card(self, parent, row, col, title, desc, btn_text, command):
        frame = ctk.CTkFrame(parent, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R)
        frame.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
        frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(T.FONT_FAMILY, 13, "bold"), text_color=T.TEXT, wraplength=300).pack(anchor="w", padx=16, pady=(16, 4))
        ctk.CTkLabel(frame, text=desc, font=ctk.CTkFont(T.FONT_FAMILY, 10), text_color=T.TEXT_MUTED, wraplength=300).pack(anchor="w", padx=16, pady=(0, 12))

        ctk.CTkButton(
            frame, text=btn_text, height=36,
            fg_color=T.PRIMARY, hover_color=T.PRIMARY_HOVER,
            font=ctk.CTkFont(T.FONT_FAMILY, 11, "bold"),
            corner_radius=T.CORNER_R, command=command,
        ).pack(padx=16, pady=(0, 16), anchor="w")

    # ------------------------------------------------------------------
    def _save_report(self, filename: str, content: str):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de Texto", "*.txt"), ("Todos", "*.*")],
            initialfile=filename,
            title="Salvar Relatório — SGR.IA",
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("SGR.IA", f"✅ Relatório salvo em:\n{path}")

    # ------------------------------------------------------------------
    def _relatorio_funcionarios(self):
        funcs = self._fc.listar()
        if not funcs:
            messagebox.showinfo("SGR.IA", "Nenhum funcionário ativo.")
            return

        lines = []
        lines.append("=" * 80)
        lines.append("  SGR.IA — RELATÓRIO DE FUNCIONÁRIOS ATIVOS")
        lines.append(f"  Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        lines.append("=" * 80)
        lines.append("")

        for i, f in enumerate(funcs, 1):
            lines.append(f"  {i}. {f.nome}")
            lines.append(f"     CPF: {formatar_cpf(f.cpf)}   |   Cargo: {f.cargo or '—'}")
            lines.append(f"     Salário: R$ {f.salario:,.2f}   |   Admissão: {formatar_data_br(f.data_admissao)}")
            lines.append(f"     Empresa: {f.empresa_nome or '—'}")
            lines.append(f"     Jornada: {f.jornada}   |   Dependentes: {f.dependentes}")
            lines.append("-" * 60)

        lines.append(f"\n  Total: {len(funcs)} funcionário(s) ativo(s)")
        lines.append("=" * 80)

        self._save_report(f"funcionarios_ativos_{date.today().isoformat()}.txt", "\n".join(lines))

    # ------------------------------------------------------------------
    def _relatorio_rescisoes(self):
        recs = self._rc.listar_recentes(50)
        if not recs:
            messagebox.showinfo("SGR.IA", "Nenhuma rescisão registrada.")
            return

        tipo_map = {
            "sem_justa_causa": "Sem Justa Causa",
            "justa_causa": "Justa Causa",
            "pedido_demissao": "Pedido de Demissão",
            "acordo_consensual": "Acordo Consensual",
            "termino_contrato": "Término de Contrato",
        }

        lines = []
        lines.append("=" * 80)
        lines.append("  SGR.IA — RELATÓRIO DE RESCISÕES")
        lines.append(f"  Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        lines.append("=" * 80)
        lines.append("")

        for i, r in enumerate(recs, 1):
            lines.append(f"  {i}. {r.get('funcionario_nome', '—')}   |   {r.get('empresa_nome', '—')}")
            lines.append(f"     Tipo: {tipo_map.get(r.get('tipo_rescisao', ''), r.get('tipo_rescisao', ''))}")
            lines.append(f"     Último Dia: {formatar_data_br(r.get('ultimo_dia', ''))}")
            lines.append(f"     Bruto: R$ {r.get('valor_bruto', 0):,.2f}   |   Líquido: R$ {r.get('valor_liquido', 0):,.2f}")
            lines.append(f"     INSS: R$ {r.get('inss', 0):,.2f}   |   IRRF: R$ {r.get('irrf', 0):,.2f}")
            lines.append(f"     FGTS Rescisão: R$ {r.get('fgts_rescisao', 0):,.2f}   |   Multa FGTS: R$ {r.get('multa_fgts', 0):,.2f}")
            lines.append("-" * 60)

        total_liq = sum(r.get("valor_liquido", 0) for r in recs)
        lines.append(f"\n  Total: {len(recs)} rescisão(ões)   |   Valor Total Líquido: R$ {total_liq:,.2f}")
        lines.append("=" * 80)

        self._save_report(f"rescisoes_{date.today().isoformat()}.txt", "\n".join(lines))

    # ------------------------------------------------------------------
    def _relatorio_empresas(self):
        emps = self._ec.listar()
        if not emps:
            messagebox.showinfo("SGR.IA", "Nenhuma empresa cadastrada.")
            return

        lines = []
        lines.append("=" * 80)
        lines.append("  SGR.IA — RELATÓRIO DE EMPRESAS")
        lines.append(f"  Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        lines.append("=" * 80)
        lines.append("")

        for i, e in enumerate(emps, 1):
            from app.services.validators import formatar_cnpj
            lines.append(f"  {i}. {e.razao_social}")
            lines.append(f"     CNPJ: {formatar_cnpj(e.cnpj)}   |   Fantasia: {e.nome_fantasia or '—'}")
            lines.append(f"     Regime: {e.regime_tributario or '—'}   |   CNAE: {e.cnae or '—'}")
            lines.append(f"     Sindicato: {e.sindicato or '—'}")
            lines.append("-" * 60)

        lines.append(f"\n  Total: {len(emps)} empresa(s)")
        lines.append("=" * 80)

        self._save_report(f"empresas_{date.today().isoformat()}.txt", "\n".join(lines))

    # ------------------------------------------------------------------
    def _resumo_geral(self):
        n_emp  = self._ec.total_ativas()
        n_func = self._fc.total_ativos()
        n_resc = self._rc.total_mes_atual()
        recs   = self._rc.listar_recentes(100)
        total_liq = sum(r.get("valor_liquido", 0) for r in recs)

        lines = []
        lines.append("=" * 80)
        lines.append("  SGR.IA — RESUMO GERAL DO SISTEMA")
        lines.append(f"  Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"  🏢  Empresas ativas:         {n_emp}")
        lines.append(f"  👤  Funcionários ativos:      {n_func}")
        lines.append(f"  📋  Rescisões no mês:         {n_resc}")
        lines.append(f"  💰  Total líquido rescisões:   R$ {total_liq:,.2f}")
        lines.append("")
        lines.append("  Status: Sistema online e operacional")
        lines.append("=" * 80)

        self._save_report(f"resumo_geral_{date.today().isoformat()}.txt", "\n".join(lines))
