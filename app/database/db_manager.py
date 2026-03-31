"""
Gerenciador de Banco de Dados — SGR.IA
Suporte a Banco em Rede com modo WAL e Timeouts.
"""
import sqlite3
import os
from app.services.config_service import ConfigService

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = ConfigService()
        return cls._instance

    @property
    def db_path(self) -> str:
        return self._config.get_db_path()

    def get_connection(self) -> sqlite3.Connection:
        # timeout=10 para evitar erros quando outros usuários estão acessando o arquivo na rede
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        
        # Otimizações de Rede e Integridade
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Modo WAL: Melhora drasticamente a concorrência em rede (leitores não bloqueiam escritores)
        try:
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
        except sqlite3.OperationalError:
            # Em alguns sistemas de arquivos de rede, WAL pode falhar. Usamos o padrão nesses casos.
            pass
            
        return conn

    def initialize(self):
        from app.database.migrations import create_tables
        conn = self.get_connection()
        try:
            create_tables(conn)
        finally:
            conn.close()
