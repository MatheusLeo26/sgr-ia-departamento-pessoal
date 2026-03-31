"""
Motor de Cálculo de Férias — CLT 2026.
Individuais, coletivas, abono pecuniário.
"""
from datetime import date
from typing import Dict, Any

from app.services.calculators import calcular_inss, calcular_irrf


def calcular_ferias(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parâmetros (dados):
        salario          float
        dias_ferias      int     — 30 (normal), 20 (vendeu 10)
        abono_pecuniario bool    — se vendeu 1/3 das férias
        dependentes      int
        media_extras     float   — média mensal de HE nos últimos 12 meses
        adicionais       float   — noturno, periculosidade etc. médias
        data_inicio      str     — início do gozo
        data_fim         str     — fim do gozo
        periodo_aquisitivo str   — ex: "01/04/2024 a 31/03/2025"
    """
    salario     = float(dados.get("salario", 0))
    dias_ferias = int(dados.get("dias_ferias", 30))
    abono       = bool(dados.get("abono_pecuniario", False))
    dependentes = int(dados.get("dependentes", 0))
    media_he    = float(dados.get("media_extras", 0))
    adicionais  = float(dados.get("adicionais", 0))

    resultado: Dict[str, Any] = {
        "proventos": {},
        "descontos": {},
        "totais": {},
        "detalhes": {},
    }

    # Base de férias = salário + adicionais + média HE
    base = salario + media_he + adicionais

    # Férias proporcionais (dias_ferias / 30)
    ferias_val = round(base * (dias_ferias / 30), 2)
    resultado["proventos"]["Férias"] = ferias_val

    # 1/3 constitucional
    terco = round(ferias_val / 3, 2)
    resultado["proventos"]["1/3 Constitucional"] = terco

    # Abono pecuniário (10 dias)
    abono_val = 0.0
    terco_abono = 0.0
    if abono:
        dias_abono = 10
        abono_val = round(base * (dias_abono / 30), 2)
        terco_abono = round(abono_val / 3, 2)
        resultado["proventos"]["Abono Pecuniário (10 dias)"] = abono_val
        resultado["proventos"]["1/3 s/ Abono"] = terco_abono

    # Média HE integrada
    if media_he > 0:
        resultado["detalhes"]["Média HE (12 meses)"] = media_he

    total_proventos = round(sum(resultado["proventos"].values()), 2)

    # ---- Descontos --------------------------------------------------
    # INSS incide sobre férias + 1/3 (exceto abono)
    base_inss = ferias_val + terco
    inss = calcular_inss(base_inss)
    resultado["descontos"]["INSS"] = inss

    # IRRF incide sobre férias + 1/3 - INSS (abono é tributado em separado)
    base_irrf = base_inss - inss
    irrf = calcular_irrf(base_irrf, dependentes)
    resultado["descontos"]["IRRF"] = irrf

    total_descontos = round(sum(resultado["descontos"].values()), 2)
    liquido = round(total_proventos - total_descontos, 2)

    resultado["totais"] = {
        "bruto": total_proventos,
        "descontos": total_descontos,
        "inss": inss,
        "irrf": irrf,
        "liquido": liquido,
    }

    resultado["detalhes"].update({
        "dias_ferias": dias_ferias,
        "abono_pecuniario": abono,
        "base_calculo": base,
        "periodo_aquisitivo": dados.get("periodo_aquisitivo", "—"),
    })

    # Alertas
    alertas = []
    if dias_ferias < 20:
        alertas.append("Férias com menos de 20 dias — possível irregularidade.")
    alertas.append("Pagamento das férias deve ser feito até 2 dias antes do início do gozo (CLT art. 145).")
    if abono:
        alertas.append("Abono pecuniário solicitado: funcionário goza 20 dias e recebe 10 dias em dinheiro.")
    resultado["alertas"] = alertas

    return resultado
