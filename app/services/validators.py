"""
Validadores para CPF, CNPJ, datas e regras trabalhistas.
"""
import re
from datetime import date, datetime
from typing import Tuple


# ---------------------------------------------------------------------------
# CPF
# ---------------------------------------------------------------------------

def formatar_cpf(cpf: str) -> str:
    digits = re.sub(r"\D", "", cpf)
    if len(digits) == 11:
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
    return cpf


def validar_cpf(cpf: str) -> bool:
    digits = re.sub(r"\D", "", cpf)
    if len(digits) != 11 or digits == digits[0] * 11:
        return False
    for pos in range(9, 11):
        s = sum(int(digits[i]) * (pos + 1 - i) for i in range(pos))
        d = (s * 10 % 11) % 10
        if d != int(digits[pos]):
            return False
    return True


# ---------------------------------------------------------------------------
# CNPJ
# ---------------------------------------------------------------------------

def formatar_cnpj(cnpj: str) -> str:
    digits = re.sub(r"\D", "", cnpj)
    if len(digits) == 14:
        return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"
    return cnpj


def validar_cnpj(cnpj: str) -> bool:
    digits = re.sub(r"\D", "", cnpj)
    if len(digits) != 14 or digits == digits[0] * 14:
        return False
    for pos, weights in enumerate([[5,4,3,2,9,8,7,6,5,4,3,2], [6,5,4,3,2,9,8,7,6,5,4,3,2]]):
        idx = 12 + pos
        s = sum(int(digits[i]) * weights[i] for i in range(idx))
        d = 0 if s % 11 < 2 else 11 - s % 11
        if d != int(digits[idx]):
            return False
    return True


# ---------------------------------------------------------------------------
# Datas
# ---------------------------------------------------------------------------

def parse_date(date_str: str) -> date:
    """Aceita DD/MM/AAAA ou YYYY-MM-DD."""
    date_str = date_str.strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Data inválida: {date_str}")


def formatar_data_br(date_obj) -> str:
    """date → DD/MM/AAAA"""
    if isinstance(date_obj, str):
        try:
            date_obj = parse_date(date_obj)
        except ValueError:
            return date_obj
    return date_obj.strftime("%d/%m/%Y")


def validar_datas_rescisao(data_admissao: date, data_desligamento: date) -> Tuple[bool, str]:
    if data_desligamento < data_admissao:
        return False, "Data de desligamento anterior à data de admissão."
    if data_desligamento > date.today():
        return False, "Data de desligamento não pode ser futura."
    return True, ""


# ---------------------------------------------------------------------------
# Salário mínimo 2026
# ---------------------------------------------------------------------------

SALARIO_MINIMO_2026 = 1_621.00


def validar_salario(salario: float) -> Tuple[bool, str]:
    if salario < SALARIO_MINIMO_2026:
        return False, f"Salário abaixo do mínimo de R$ {SALARIO_MINIMO_2026:,.2f}."
    return True, ""
