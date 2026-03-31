"""
Motor de Cálculo do 13º Salário — CLT 2026.
1ª parcela (até 30/11) e 2ª parcela (até 20/12).
"""
from datetime import date
from typing import Dict, Any

from app.services.calculators import calcular_inss, calcular_irrf


def calcular_decimo_terceiro(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parâmetros (dados):
        salario           float
        meses_trabalhados int     — meses trabalhados no ano (1-12)
        parcela           int     — 1 ou 2
        dependentes       int
        media_extras      float   — média mensal HE no ano
        adicionais        float   — noturno, periculosidade, etc.
        adiantamento      float   — valor já pago na 1ª parcela (para 2ª parcela)
    """
    salario     = float(dados.get("salario", 0))
    meses       = int(dados.get("meses_trabalhados", 12))
    parcela     = int(dados.get("parcela", 1))
    dependentes = int(dados.get("dependentes", 0))
    media_he    = float(dados.get("media_extras", 0))
    adicionais  = float(dados.get("adicionais", 0))
    adiantamento = float(dados.get("adiantamento", 0))

    resultado: Dict[str, Any] = {
        "proventos": {},
        "descontos": {},
        "totais": {},
        "detalhes": {},
    }

    # Base = (salário + médias) / 12 × meses
    base_mensal = salario + media_he + adicionais
    decimo_bruto = round((base_mensal / 12) * meses, 2)

    resultado["detalhes"] = {
        "salario_base": salario,
        "media_he": media_he,
        "adicionais": adicionais,
        "base_mensal": base_mensal,
        "meses_trabalhados": meses,
        "parcela": parcela,
    }

    if parcela == 1:
        # 1ª parcela: 50% do bruto, sem descontos
        valor_1a = round(decimo_bruto / 2, 2)
        resultado["proventos"]["13º Salário — 1ª Parcela (50%)"] = valor_1a
        resultado["totais"] = {
            "bruto": valor_1a,
            "descontos": 0.0,
            "inss": 0.0,
            "irrf": 0.0,
            "liquido": valor_1a,
        }
        resultado["alertas"] = [
            "1ª parcela deve ser paga até 30 de novembro.",
            "Pode ser paga junto com as férias, se solicitado pelo empregado.",
            "Não há desconto de INSS ou IRRF na 1ª parcela.",
        ]

    else:
        # 2ª parcela: bruto - adiantamento - INSS - IRRF
        resultado["proventos"]["13º Salário (bruto)"] = decimo_bruto

        # INSS sobre bruto total do 13º
        inss = calcular_inss(decimo_bruto)
        resultado["descontos"]["INSS"] = inss

        # IRRF sobre bruto - INSS
        base_irrf = decimo_bruto - inss
        irrf = calcular_irrf(base_irrf, dependentes)
        resultado["descontos"]["IRRF"] = irrf

        if adiantamento > 0:
            resultado["descontos"]["Adiantamento 1ª Parcela"] = adiantamento

        total_desc = round(inss + irrf + adiantamento, 2)
        liquido = round(decimo_bruto - total_desc, 2)

        resultado["totais"] = {
            "bruto": decimo_bruto,
            "descontos": total_desc,
            "inss": inss,
            "irrf": irrf,
            "adiantamento": adiantamento,
            "liquido": liquido,
        }

        resultado["alertas"] = [
            "2ª parcela deve ser paga até 20 de dezembro.",
            "INSS e IRRF incidem sobre o valor integral do 13º.",
            f"FGTS sobre 13º: R$ {round(decimo_bruto * 0.08, 2):,.2f} (recolhido pelo empregador).",
        ]

    return resultado
