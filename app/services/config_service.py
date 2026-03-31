"""
Serviço de Configuração do SGR.IA
Gerencia o arquivo config.json (ex: caminho do banco de dados).
"""
import json
import os

class ConfigService:
    def __init__(self):
        import sys
        if getattr(sys, 'frozen', False):
            # No modo executável (.exe), o root é a pasta onde o .exe está
            self.root_dir = os.path.dirname(sys.executable)
        else:
            # No modo script, o root é 3 níveis acima deste arquivo
            self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
        self.config_path = os.path.join(self.root_dir, "config.json")
        self.default_db  = os.path.join(self.root_dir, "sgr.db")

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
