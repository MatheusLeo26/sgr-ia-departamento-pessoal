"""
Motor de cálculo trabalhista — CLT 2026
Salário mínimo: R$ 1.621,00
INSS 2026 (tabela progressiva — verificar Portaria MPS vigente)
IRRF 2026 (tabela mensal — verificar Instrução Normativa RFB vigente)
"""
from datetime import date
from typing import Dict, Any, List

# ---------------------------------------------------------------------------
# Tabelas legais 2026
# ---------------------------------------------------------------------------

SALARIO_MINIMO = 1_621.00

# Tabela progressiva INSS 2026 (faixa_superior, alíquota)
FAIXAS_INSS: List[tuple] = [
    (1_518.00,  0.075),
    (2_793.88,  0.09),
    (4_190.83,  0.12),
    (8_157.41,  0.14),
]

# Tabela IRRF mensal 2026 (base_ate, aliquota, deducao)
FAIXAS_IRRF: List[tuple] = [
    (2_259.20, 0.000,  0.00),
    (2_826.65, 0.075,  169.44),
    (3_751.05, 0.150,  381.44),
    (4_664.68, 0.225,  662.77),
    (float("inf"), 0.275, 896.00),
]

DEDUCAO_DEPENDENTE = 189.59   # por dependente — IRRF 2026

# ---------------------------------------------------------------------------
# INSS progressivo
# ---------------------------------------------------------------------------

def calcular_inss(base: float) -> float:
    """Calcula INSS pela tabela progressiva 2026."""
    if base <= 0:
        return 0.0
    inss = 0.0
    limite_ant = 0.0
    for limite, aliq in FAIXAS_INSS:
        if base <= limite:
            inss += (base - limite_ant) * aliq
            break
        inss += (limite - limite_ant) * aliq
        limite_ant = limite
        if base > FAIXAS_INSS[-1][0]:
            break
    return round(inss, 2)


# ---------------------------------------------------------------------------
# IRRF mensal
# ---------------------------------------------------------------------------

def calcular_irrf(base: float, dependentes: int = 0) -> float:
    """Calcula IRRF sobre a base após dedução de INSS e dependentes."""
    base_calc = base - (dependentes * DEDUCAO_DEPENDENTE)
    if base_calc <= 0:
        return 0.0
    for limite, aliq, ded in FAIXAS_IRRF:
        if base_calc <= limite:
            irrf = base_calc * aliq - ded
            return max(0.0, round(irrf, 2))
    return 0.0


# ---------------------------------------------------------------------------
# Cálculo de meses
# ---------------------------------------------------------------------------

def meses_entre(inicio: date, fim: date) -> int:
    """
    Meses completos + regra CLT: se o dia final >= 15, conta mais 1 mês.
    """
    meses = (fim.year - inicio.year) * 12 + fim.month - inicio.month
    if fim.day >= 15:
        meses += 1
    return max(0, meses)


def anos_completos(inicio: date, fim: date) -> int:
    anos = fim.year - inicio.year
    if (fim.month, fim.day) < (inicio.month, inicio.day):
        anos -= 1
    return max(0, anos)


# ---------------------------------------------------------------------------
# Aviso prévio
# ---------------------------------------------------------------------------

def dias_aviso_previo(anos_servico: int) -> int:
    """30 dias + 3 dias por ano de serviço, máximo 90 dias (Lei 12.506/2011)."""
    return min(30 + anos_servico * 3, 90)


# ---------------------------------------------------------------------------
# Motor principal de rescisão
# ---------------------------------------------------------------------------

# Verbas devidas por tipo de rescisão
VERBAS_RESCISAO: Dict[str, Dict[str, bool]] = {
    "sem_justa_causa": {
        "saldo_salario": True,
        "ferias_vencidas": True,
        "ferias_proporcionais": True,
        "decimo_terceiro": True,
        "aviso_indenizado": True,
        "fgts": True,
        "multa_fgts": True,
        "multa_pct": 0.40,
    },
    "justa_causa": {
        "saldo_salario": True,
        "ferias_vencidas": True,
        "ferias_proporcionais": False,
        "decimo_terceiro": False,
        "aviso_indenizado": False,
        "fgts": True,
        "multa_fgts": False,
        "multa_pct": 0.0,
    },
    "pedido_demissao": {
        "saldo_salario": True,
        "ferias_vencidas": True,
        "ferias_proporcionais": True,
        "decimo_terceiro": True,
        "aviso_indenizado": False,
        "fgts": True,
        "multa_fgts": False,
        "multa_pct": 0.0,
    },
    "acordo_consensual": {
        "saldo_salario": True,
        "ferias_vencidas": True,
        "ferias_proporcionais": True,
        "decimo_terceiro": True,
        "aviso_indenizado": False,
        "fgts": True,
        "multa_fgts": True,
        "multa_pct": 0.20,
    },
    "termino_contrato": {
        "saldo_salario": True,
        "ferias_vencidas": True,
        "ferias_proporcionais": True,
        "decimo_terceiro": True,
        "aviso_indenizado": False,
        "fgts": True,
        "multa_fgts": True,
        "multa_pct": 0.40,
    },
}


def calcular_rescisao(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parâmetros (dados):
        salario           float   — salário base
        data_admissao     date
        data_desligamento date
        tipo_rescisao     str     — chave de VERBAS_RESCISAO
        dias_trabalhados  int     — dias no último mês (0-31)
        periodos_ferias   int     — períodos aquisitivos de férias vencidas completos
        meses_ferias_prop int     — meses no período aquisitivo em curso
        aviso_trabalhado  bool    — aviso trabalhado (True) ou indenizado (False)
        saldo_fgts        float   — saldo FGTS acumulado (banco informa)
        dependentes       int     — dependentes para IRRF
        outras_verbas     float   — outros valores a somar (horas extras, etc.)
    """
    salario        = float(dados.get("salario", 0))
    admissao       = dados["data_admissao"]
    desligamento   = dados["data_desligamento"]
    tipo           = dados.get("tipo_rescisao", "sem_justa_causa")
    dias_trab      = int(dados.get("dias_trabalhados", 30))
    periodos_fer   = int(dados.get("periodos_ferias", 0))
    meses_fer_prop = int(dados.get("meses_ferias_prop", 0))
    aviso_trab     = bool(dados.get("aviso_trabalhado", False))
    saldo_fgts_acc = float(dados.get("saldo_fgts", 0))
    dependentes    = int(dados.get("dependentes", 0))
    outras_verbas  = float(dados.get("outras_verbas", 0))

    verbas_cfg = VERBAS_RESCISAO.get(tipo, VERBAS_RESCISAO["sem_justa_causa"])
    anos_serv  = anos_completos(admissao, desligamento)
    dias_aviso = dias_aviso_previo(anos_serv)

    res: Dict[str, Any] = {
        "verbas":    {},
        "descontos": {},
        "totais":    {},
        "alertas":   [],
        "checklist": [],
        "detalhes":  {},
    }

    # 1. Saldo de salário (tributado: INSS + IRRF)
    saldo_sal = round((salario / 30) * dias_trab, 2) if verbas_cfg["saldo_salario"] else 0.0
    if verbas_cfg["saldo_salario"]:
        res["verbas"]["Saldo de Salário"] = saldo_sal

    # 2. Férias vencidas + 1/3 (INSS isento; tributado IRRF)
    fer_vencidas = 0.0
    if verbas_cfg["ferias_vencidas"] and periodos_fer > 0:
        fer_vencidas = round(salario * (4 / 3) * periodos_fer, 2)
        res["verbas"]["Férias Vencidas + 1/3"] = fer_vencidas

    # 3. Férias proporcionais + 1/3 (isento INSS e IRRF na rescisão sem justa causa)
    fer_prop = 0.0
    if verbas_cfg["ferias_proporcionais"] and meses_fer_prop > 0:
        fer_prop = round((salario / 12) * meses_fer_prop * (4 / 3), 2)
        res["verbas"]["Férias Proporcionais + 1/3"] = fer_prop

    # 4. 13º proporcional (INSS + IRRF)
    meses_ano = meses_entre(date(desligamento.year, 1, 1), desligamento)
    meses_ano = min(meses_ano, 12)
    decimo = 0.0
    if verbas_cfg["decimo_terceiro"] and meses_ano > 0:
        decimo = round((salario / 12) * meses_ano, 2)
        res["verbas"]["13º Salário Proporcional"] = decimo

    # 5. Aviso prévio indenizado (isento INSS e IRRF; integra FGTS)
    aviso_ind = 0.0
    if verbas_cfg.get("aviso_indenizado") and not aviso_trab:
        aviso_ind = round((salario / 30) * dias_aviso, 2)
        res["verbas"]["Aviso Prévio Indenizado"] = aviso_ind

    # 6. Outras verbas
    if outras_verbas > 0:
        res["verbas"]["Outras Verbas"] = round(outras_verbas, 2)

    # ---- Bases fiscais ----
    # Base INSS: saldo salário + 13° proporcional
    base_inss = saldo_sal + decimo + outras_verbas
    inss = calcular_inss(base_inss) if verbas_cfg["saldo_salario"] else 0.0

    # Base IRRF: saldo salário + férias vencidas + 13° − INSS − dependentes
    base_irrf = saldo_sal + fer_vencidas + decimo + outras_verbas - inss
    irrf = calcular_irrf(base_irrf, dependentes)

    # 7. FGTS sobre verbas rescisórias (depósito pelo empregador)
    base_fgts = saldo_sal + fer_prop + decimo + aviso_ind
    fgts_resc = round(base_fgts * 0.08, 2) if verbas_cfg["fgts"] else 0.0
    if fgts_resc:
        res["verbas"]["FGTS s/ Verbas Rescisórias (8%)"] = fgts_resc

    # 8. Multa FGTS sobre saldo acumulado
    multa_pct = verbas_cfg.get("multa_pct", 0.0)
    multa = round(saldo_fgts_acc * multa_pct, 2) if verbas_cfg["multa_fgts"] else 0.0
    if multa:
        res["verbas"][f"Multa FGTS ({int(multa_pct*100)}%)"] = multa

    # ---- Totais ----
    total_bruto     = round(sum(res["verbas"].values()), 2)
    total_descontos = round(inss + irrf, 2)
    total_liquido   = round(total_bruto - total_descontos, 2)

    res["descontos"]["INSS"] = inss
    res["descontos"]["IRRF"] = irrf

    res["totais"] = {
        "bruto":     total_bruto,
        "inss":      inss,
        "irrf":      irrf,
        "descontos": total_descontos,
        "liquido":   total_liquido,
    }

    res["detalhes"] = {
        "anos_servico":    anos_serv,
        "dias_aviso":      dias_aviso,
        "base_inss":       round(base_inss, 2),
        "base_irrf":       round(base_irrf, 2),
        "meses_ano":       meses_ano,
        "aviso_trabalhado": aviso_trab,
    }

    # ---- Checklist documental ----
    res["checklist"] = _gerar_checklist(tipo, aviso_trab)

    # ---- Alertas jurídicos ----
    res["alertas"] = _gerar_alertas(dados, res, tipo, anos_serv)

    return res


def _gerar_checklist(tipo: str, aviso_trabalhado: bool) -> List[str]:
    base = [
        "Termo de Rescisão de Contrato de Trabalho (TRCT)",
        "Homologação (sindicato ou via digital, conforme convenção coletiva)",
        "Extrato FGTS atualizado (Caixa Econômica Federal)",
        "Guia de Recolhimento Rescisório do FGTS (GRRF)",
        "Comunicação de Dispensa (CD) no e-Social",
        "Documentos pessoais do funcionário (CPF, RG, CTPS)",
        "Comprovante de pagamento das verbas rescisórias",
    ]
    if tipo == "sem_justa_causa":
        base += [
            "Seguro-desemprego: preencher formulário SD/CD e entregar ao funcionário",
            "Carta de demissão assinada pelo empregador",
        ]
    if tipo == "justa_causa":
        base += [
            "Relatório circunstanciado da justa causa (fato, data, testemunhas)",
            "Advertências anteriores (se aplicável)",
        ]
    if tipo == "pedido_demissao":
        base += [
            "Carta de pedido de demissão assinada pelo funcionário",
        ]
    if tipo == "acordo_consensual":
        base += [
            "Acordo por escrito assinado por ambas as partes",
            "Homologação: 10 dias corridos após o acordo",
        ]
    if not aviso_trabalhado:
        base.append("Recibo de pagamento do aviso prévio indenizado")
    return base


def _gerar_alertas(dados, resultado, tipo, anos_serv) -> List[Dict[str, str]]:
    alertas = []
    liq = resultado["totais"]["liquido"]

    if liq <= 0:
        alertas.append({"nivel": "erro", "msg": "Total líquido negativo — revisar os dados informados."})

    if tipo == "sem_justa_causa" and anos_serv >= 10:
        alertas.append({"nivel": "atencao", "msg": f"Funcionário com {anos_serv} anos de serviço. Verificar estabilidade provisória ou convenção coletiva."})

    if dados.get("saldo_fgts", 0) == 0 and tipo in ("sem_justa_causa", "acordo_consensual"):
        alertas.append({"nivel": "atencao", "msg": "Saldo FGTS informado como R$ 0,00. Confirme o saldo no extrato da CEF."})

    if tipo == "sem_justa_causa":
        alertas.append({"nivel": "info", "msg": "Prazo de pagamento: 10 dias corridos após o último dia trabalhado (ou do aviso)."})

    if tipo == "pedido_demissao":
        alertas.append({"nivel": "info", "msg": "Funcionário que pede demissão não tem direito ao seguro-desemprego."})

    return alertas
