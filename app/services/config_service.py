"""
Serviço de Configuração do SGR.IA
Gerencia o arquivo config.json (ex: caminho do banco de dados).
"""
import json
import os

class ConfigService:
    def __init__(self):
        self.config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "config.json"
        )
        self.default_db = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "sgr.db"
        )

    def get_db_path(self) -> str:
        if not os.path.exists(self.config_path):
            return self.default_db
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                path = config.get("db_path", self.default_db)
                # Verifica se o caminho ainda é válido (ex: drive Z: mapeado)
                if not os.path.exists(os.path.dirname(path)):
                    return self.default_db
                return path
        except:
            return self.default_db

    def set_db_path(self, path: str):
        config = {"db_path": path}
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
