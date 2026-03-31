from dataclasses import dataclass
from typing import Optional


@dataclass
class Funcionario:
    nome: str
    cpf: str
    salario: float
    data_admissao: str          # "YYYY-MM-DD"
    id: Optional[int] = None
    rg: Optional[str] = None
    cargo: Optional[str] = None
    empresa_id: Optional[int] = None
    empresa_nome: Optional[str] = None   # joined field
    nome_mae: Optional[str] = None
    estado_civil: Optional[str] = None
    jornada: str = "44h semanais"
    dependentes: int = 0
    vale_transporte: float = 0.0
    ativo: int = 1

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "rg": self.rg,
            "cargo": self.cargo,
            "salario": self.salario,
            "data_admissao": self.data_admissao,
            "empresa_id": self.empresa_id,
            "nome_mae": self.nome_mae,
            "estado_civil": self.estado_civil,
            "jornada": self.jornada,
            "dependentes": self.dependentes,
            "vale_transporte": self.vale_transporte,
            "ativo": self.ativo,
        }

    @staticmethod
    def from_row(row) -> "Funcionario":
        return Funcionario(
            id=row["id"],
            nome=row["nome"],
            cpf=row["cpf"],
            rg=row["rg"] if "rg" in row.keys() else None,
            cargo=row["cargo"] if "cargo" in row.keys() else None,
            salario=row["salario"],
            data_admissao=row["data_admissao"],
            empresa_id=row["empresa_id"] if "empresa_id" in row.keys() else None,
            empresa_nome=row["empresa_nome"] if "empresa_nome" in row.keys() else None,
            nome_mae=row["nome_mae"] if "nome_mae" in row.keys() else None,
            estado_civil=row["estado_civil"] if "estado_civil" in row.keys() else None,
            jornada=row["jornada"] if "jornada" in row.keys() else "44h semanais",
            dependentes=row["dependentes"] if "dependentes" in row.keys() else 0,
            vale_transporte=row["vale_transporte"] if "vale_transporte" in row.keys() else 0.0,
            ativo=row["ativo"] if "ativo" in row.keys() else 1,
        )
