from app.database.db_manager import DatabaseManager
from typing import List, Dict, Any


class RescisaoController:
    def __init__(self):
        self.db = DatabaseManager()

    # ------------------------------------------------------------------
    def salvar(self, dados: Dict[str, Any]) -> tuple[bool, str]:
        conn = self.db.get_connection()
        try:
            conn.execute("""
                INSERT INTO rescisoes
                (funcionario_id, tipo_rescisao, data_aviso, ultimo_dia,
                 aviso_previo_dias, aviso_previo_tipo,
                 saldo_salario, ferias_vencidas, ferias_proporcionais,
                 decimo_terceiro, aviso_indenizado, fgts_rescisao, multa_fgts,
                 inss, irrf, valor_bruto, valor_liquido, saldo_fgts_total, observacoes)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                dados.get("funcionario_id"),
                dados.get("tipo_rescisao"),
                dados.get("data_aviso"),
                dados.get("ultimo_dia"),
                dados.get("aviso_previo_dias", 0),
                dados.get("aviso_previo_tipo"),
                dados.get("saldo_salario", 0),
                dados.get("ferias_vencidas", 0),
                dados.get("ferias_proporcionais", 0),
                dados.get("decimo_terceiro", 0),
                dados.get("aviso_indenizado", 0),
                dados.get("fgts_rescisao", 0),
                dados.get("multa_fgts", 0),
                dados.get("inss", 0),
                dados.get("irrf", 0),
                dados.get("valor_bruto", 0),
                dados.get("valor_liquido", 0),
                dados.get("saldo_fgts_total", 0),
                dados.get("observacoes"),
            ))
            conn.commit()
            return True, "Rescisão salva com sucesso."
        except Exception as ex:
            return False, str(ex)
        finally:
            conn.close()

    # ------------------------------------------------------------------
    def listar_recentes(self, limite: int = 10) -> List[Dict]:
        conn = self.db.get_connection()
        try:
            rows = conn.execute("""
                SELECT r.*, f.nome AS funcionario_nome, f.cargo,
                       e.razao_social AS empresa_nome
                FROM rescisoes r
                JOIN funcionarios f ON f.id = r.funcionario_id
                LEFT JOIN empresas e ON e.id = f.empresa_id
                ORDER BY r.created_at DESC
                LIMIT ?
            """, (limite,)).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    # ------------------------------------------------------------------
    def total_mes_atual(self) -> int:
        conn = self.db.get_connection()
        try:
            return conn.execute("""
                SELECT COUNT(*) FROM rescisoes
                WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now','localtime')
            """).fetchone()[0]
        finally:
            conn.close()
