from app.database.db_manager import DatabaseManager
from app.models.empresa import Empresa
from app.services.validators import validar_cnpj
from typing import List, Optional


class EmpresaController:
    def __init__(self):
        self.db = DatabaseManager()

    # ------------------------------------------------------------------
    def listar(self, apenas_ativas: bool = True) -> List[Empresa]:
        conn = self.db.get_connection()
        try:
            q = "SELECT * FROM empresas"
            if apenas_ativas:
                q += " WHERE ativo = 1"
            q += " ORDER BY razao_social"
            rows = conn.execute(q).fetchall()
            return [Empresa.from_row(r) for r in rows]
        finally:
            conn.close()

    # ------------------------------------------------------------------
    def obter(self, id: int) -> Optional[Empresa]:
        conn = self.db.get_connection()
        try:
            row = conn.execute("SELECT * FROM empresas WHERE id = ?", (id,)).fetchone()
            return Empresa.from_row(row) if row else None
        finally:
            conn.close()

    # ------------------------------------------------------------------
    def salvar(self, e: Empresa) -> tuple[bool, str]:
        if not validar_cnpj(e.cnpj):
            return False, "CNPJ inválido."
        conn = self.db.get_connection()
        try:
            if e.id:
                conn.execute("""
                    UPDATE empresas SET cnpj=?,razao_social=?,nome_fantasia=?,cnae=?,
                    fpas=?,sindicato=?,regime_tributario=?,email=?,telefone=?,ativo=?
                    WHERE id=?
                """, (e.cnpj, e.razao_social, e.nome_fantasia, e.cnae, e.fpas,
                      e.sindicato, e.regime_tributario, e.email, e.telefone, e.ativo, e.id))
            else:
                conn.execute("""
                    INSERT INTO empresas
                    (cnpj,razao_social,nome_fantasia,cnae,fpas,sindicato,regime_tributario,email,telefone,ativo)
                    VALUES (?,?,?,?,?,?,?,?,?,?)
                """, (e.cnpj, e.razao_social, e.nome_fantasia, e.cnae, e.fpas,
                      e.sindicato, e.regime_tributario, e.email, e.telefone, e.ativo))
            conn.commit()
            return True, "Empresa salva com sucesso."
        except Exception as ex:
            return False, str(ex)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    def excluir(self, id: int) -> tuple[bool, str]:
        conn = self.db.get_connection()
        try:
            conn.execute("UPDATE empresas SET ativo=0 WHERE id=?", (id,))
            conn.commit()
            return True, "Empresa desativada."
        finally:
            conn.close()

    # ------------------------------------------------------------------
    def total_ativas(self) -> int:
        conn = self.db.get_connection()
        try:
            return conn.execute("SELECT COUNT(*) FROM empresas WHERE ativo=1").fetchone()[0]
        finally:
            conn.close()
