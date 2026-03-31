from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Empresa:
    razao_social: str
    cnpj: str
    id: Optional[int] = None
    nome_fantasia: Optional[str] = None
    cnae: Optional[str] = None
    fpas: Optional[str] = None
    sindicato: Optional[str] = None
    regime_tributario: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    ativo: int = 1

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cnpj": self.cnpj,
            "razao_social": self.razao_social,
            "nome_fantasia": self.nome_fantasia,
            "cnae": self.cnae,
            "fpas": self.fpas,
            "sindicato": self.sindicato,
            "regime_tributario": self.regime_tributario,
            "email": self.email,
            "telefone": self.telefone,
            "ativo": self.ativo,
        }

    @staticmethod
    def from_row(row) -> "Empresa":
        return Empresa(
            id=row["id"],
            cnpj=row["cnpj"],
            razao_social=row["razao_social"],
            nome_fantasia=row["nome_fantasia"],
            cnae=row["cnae"],
            fpas=row["fpas"],
            sindicato=row["sindicato"],
            regime_tributario=row["regime_tributario"],
            email=row["email"],
            telefone=row["telefone"],
            ativo=row["ativo"],
        )
