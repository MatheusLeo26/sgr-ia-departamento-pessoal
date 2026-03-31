"""
Motor de cálculo de Folha de Pagamento — CLT 2026.
Processa salário bruto, horas extras, adicionais, encargos e descontos.
"""
from datetime import date
from typing import Dict, Any

from app.services.calculators import calcular_inss, calcular_irrf, SALARIO_MINIMO


def calcular_folha(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parâmetros (dados):
        salario_base       float
        horas_extras_50    float   — qtd horas extras a 50%
        horas_extras_100   float   — qtd horas extras a 100%
        adicional_noturno  float   — valor ou 0
        comissoes          float
        outros_proventos   float
        vale_transporte    float   — desconto VT (6% do salário base, máx)
        outros_descontos   float
        dependentes        int     — para IRRF
        jornada_mensal     float   — horas/mês (default 220)
        faltas_dias        int     — dias de falta sem justificativa
    """
    sal_base       = float(dados.get("salario_base", 0))
    he50           = float(dados.get("horas_extras_50", 0))
    he100          = float(dados.get("horas_extras_100", 0))
    adic_noturno   = float(dados.get("adicional_noturno", 0))
    comissoes      = float(dados.get("comissoes", 0))
    outros_prov    = float(dados.get("outros_proventos", 0))
    vt             = float(dados.get("vale_transporte", 0))
    outros_desc    = float(dados.get("outros_descontos", 0))
    dependentes    = int(dados.get("dependentes", 0))
    jornada        = float(dados.get("jornada_mensal", 220))
    faltas         = int(dados.get("faltas_dias", 0))

    resultado: Dict[str, Any] = {
        "proventos": {},
        "descontos": {},
        "encargos_empresa": {},
        "totais": {},
    }

    # ---- Proventos --------------------------------------------------

    # Salário base (- faltas)
    valor_dia = sal_base / 30
    desc_faltas = round(valor_dia * faltas, 2)
    sal_efetivo = round(sal_base - desc_faltas, 2)
    resultado["proventos"]["Salário Base"] = sal_base
    if faltas > 0:
        resultado["descontos"][f"Faltas ({faltas} dias)"] = desc_faltas

    # Hora extra
    valor_hora = sal_base / jornada
    he50_val = round(he50 * valor_hora * 1.5, 2)
    he100_val = round(he100 * valor_hora * 2.0, 2)
    if he50_val > 0:
        resultado["proventos"]["Horas Extras 50%"] = he50_val
    if he100_val > 0:
        resultado["proventos"]["Horas Extras 100%"] = he100_val

    # DSR sobre horas extras
    # Fórmula: (total HE / dias úteis do mês) × domingos/feriados
    # Simplificação: estima 26 úteis e 4 domingos
    total_he = he50_val + he100_val
    dsr = round((total_he / 26) * 4, 2) if total_he > 0 else 0.0
    if dsr > 0:
        resultado["proventos"]["DSR s/ Horas Extras"] = dsr

    # Adicional noturno
    if adic_noturno > 0:
        resultado["proventos"]["Adicional Noturno"] = adic_noturno

    # Comissões
    if comissoes > 0:
        resultado["proventos"]["Comissões"] = comissoes

    # Outros proventos
    if outros_prov > 0:
        resultado["proventos"]["Outros Proventos"] = outros_prov

    # ---- Base de cálculo -------------------------------------------
    total_proventos = round(sum(resultado["proventos"].values()), 2)
    base_calc = total_proventos - desc_faltas

    # ---- Descontos -------------------------------------------------

    # INSS (empregado)
    inss = calcular_inss(base_calc)
    resultado["descontos"]["INSS (Empregado)"] = inss

    # IRRF
    base_irrf = base_calc - inss
    irrf = calcular_irrf(base_irrf, dependentes)
    resultado["descontos"]["IRRF"] = irrf

    # Vale transporte (6% do salário base, se houver)
    if vt > 0:
        vt_desc = min(round(sal_base * 0.06, 2), vt)
        resultado["descontos"]["Vale Transporte (6%)"] = vt_desc
    else:
        vt_desc = 0.0

    # Outros descontos
    if outros_desc > 0:
        resultado["descontos"]["Outros Descontos"] = outros_desc

    total_descontos = round(sum(resultado["descontos"].values()), 2)

    # ---- Encargos empresa ------------------------------------------
    fgts = round(base_calc * 0.08, 2)
    inss_patronal = round(base_calc * 0.20, 2)
    rat = round(base_calc * 0.02, 2)   # RAT médio 2%
    terceiros = round(base_calc * 0.058, 2)  # Sistema S + INCRA etc ~5,8%

    resultado["encargos_empresa"] = {
        "FGTS (8%)": fgts,
        "INSS Patronal (20%)": inss_patronal,
        "RAT (2%)": rat,
        "Terceiros (~5,8%)": terceiros,
        "Total Encargos Empresa": round(fgts + inss_patronal + rat + terceiros, 2),
    }

    # ---- Totais ----------------------------------------------------
    salario_liquido = round(total_proventos - total_descontos, 2)
    resultado["totais"] = {
        "bruto": total_proventos,
        "descontos": total_descontos,
        "inss": inss,
        "irrf": irrf,
        "fgts": fgts,
        "liquido": salario_liquido,
        "custo_total_empresa": round(total_proventos + resultado["encargos_empresa"]["Total Encargos Empresa"], 2),
    }

    return resultado
