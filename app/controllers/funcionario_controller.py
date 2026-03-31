from app.database.db_manager import DatabaseManager
from app.models.funcionario import Funcionario
from app.services.validators import validar_cpf
from typing import List, Optional


class FuncionarioController:
    def __init__(self):
        self.db = DatabaseManager()

    # ------------------------------------------------------------------
    def listar(self, empresa_id: int = None, apenas_ativos: bool = True) -> List[Funcionario]:
        conn = self.db.get_connection()
        try:
            q = """
                SELECT f.*, e.razao_social AS empresa_nome
                FROM funcionarios f
                LEFT JOIN empresas e ON e.id = f.empresa_id
                WHERE 1=1
            """
            params = []
            if apenas_ativos:
                q += " AND f.ativo = 1"
            if empresa_id:
                q += " AND f.empresa_id = ?"
                params.append(empresa_id)
            q += " ORDER BY f.nome"
            rows = conn.execute(q, params).fetchall()
            return [Funcionario.from_row(r) for r in rows]
        finally:
            conn.close()

    # ------------------------------------------------------------------
    def obter(self, id: int) -> Optional[Funcionario]:
        conn = self.db.get_connection()
        try:
            row = conn.execute("""
                SELECT f.*, e.razao_social AS empresa_nome
                FROM funcionarios f
                LEFT JOIN empresas e ON e.id = f.empresa_id
                WHERE f.id = ?
            """, (id,)).fetchone()
            return Funcionario.from_row(row) if row else None
        finally:
            conn.close()

    # ------------------------------------------------------------------
    def salvar(self, f: Funcionario) -> tuple[bool, str]:
        if not validar_cpf(f.cpf):
            return False, "CPF inválido."
        conn = self.db.get_connection()
        try:
            if f.id:
                conn.execute("""
                    UPDATE funcionarios
                    SET nome=?,cpf=?,rg=?,cargo=?,salario=?,data_admissao=?,empresa_id=?,
                        nome_mae=?,estado_civil=?,jornada=?,dependentes=?,vale_transporte=?,ativo=?
                    WHERE id=?
                """, (f.nome, f.cpf, f.rg, f.cargo, f.salario, f.data_admissao,
                      f.empresa_id, f.nome_mae, f.estado_civil, f.jornada,
                      f.dependentes, f.vale_transporte, f.ativo, f.id))
            else:
                # Verifica duplicado (mesmo CPF + empresa)
                dup = conn.execute(
                    "SELECT id FROM funcionarios WHERE cpf=? AND empresa_id=? AND ativo=1",
                    (f.cpf, f.empresa_id)
                ).fetchone()
                if dup:
                    return False, "Funcionário com mesmo CPF já ativo nesta empresa."
                conn.execute("""
                    INSERT INTO funcionarios
                    (nome,cpf,rg,cargo,salario,data_admissao,empresa_id,nome_mae,
                     estado_civil,jornada,dependentes,vale_transporte,ativo)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (f.nome, f.cpf, f.rg, f.cargo, f.salario, f.data_admissao,
                      f.empresa_id, f.nome_mae, f.estado_civil, f.jornada,
                      f.dependentes, f.vale_transporte, f.ativo))
            conn.commit()
            return True, "Funcionário salvo com sucesso."
        except Exception as ex:
            return False, str(ex)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    def excluir(self, id: int) -> tuple[bool, str]:
        conn = self.db.get_connection()
        try:
            conn.execute("UPDATE funcionarios SET ativo=0 WHERE id=?", (id,))
            conn.commit()
            return True, "Funcionário desativado."
        finally:
            conn.close()

    # ------------------------------------------------------------------
    def total_ativos(self) -> int:
        conn = self.db.get_connection()
        try:
            return conn.execute("SELECT COUNT(*) FROM funcionarios WHERE ativo=1").fetchone()[0]
        finally:
            conn.close()
