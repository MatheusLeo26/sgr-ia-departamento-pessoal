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
        config = self._load_config()
        path = config.get("db_path", self.default_db)
        # Verifica se o caminho ainda é válido (ex: drive Z: mapeado)
        if not os.path.exists(os.path.dirname(path)):
            return self.default_db
        return path

    def set_db_path(self, path: str):
        self._update_config("db_path", path)

    def get_appearance_mode(self) -> str:
        config = self._load_config()
        # "System" é o padrão se nunca foi salvo
        return config.get("appearance_mode", "Dark")

    def set_appearance_mode(self, mode: str):
        self._update_config("appearance_mode", mode)

    def _load_config(self) -> dict:
        if not os.path.exists(self.config_path):
            return {}
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def _update_config(self, key: str, value: str):
        config = self._load_config()
        config[key] = value
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
