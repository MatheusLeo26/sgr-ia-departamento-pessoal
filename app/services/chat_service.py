"""
Motor de Conhecimento da Roberta Bot — SGR.IA
Especialista em DP e rotinas do sistema (Integrado ao Google Gemini).
"""

import os
import json
import google.generativeai as genai
import requests
from typing import List, Dict

class ChatService:
    def __init__(self):
        self.api_key = ""
        self._load_config()

        # Prompt de Sistema (System Instruction)
        self.system_instruction = (
            "Seu nome é Roberta. Você é a assistente virtual especializada em Recursos Humanos (RH), "
            "Departamento Pessoal (DP) e CLT (Consolidação das Leis do Trabalho) do sistema SGR.IA. "
            "Aja SEMPRE como uma especialista sênior na área. "
            "Seja SEMPRE respeitosa, formal e educada. "
            "Você foi desenvolvida para tirar as dúvidas dos usuários sobre regras trabalhistas, ponto, "
            "férias, 13º salário, rescisão, impostos e afins na legislação brasileira de 2026. "
            "Mantenha um tom profissional. Nunca invente regras legais que não existem. "
            "Seja prestativa e explique de forma clara."
        )
        
        self.chat_session = None
        self.ollama_url = "http://127.0.0.1:11434/api/chat"
        self.ollama_model = "llama3:latest"
        self._setup_gemini()

    def _load_config(self):
        from app.services.config_service import ConfigService
        try:
            config_service = ConfigService()
            config_dict = config_service._load_config()
            self.api_key = config_dict.get("gemini_api_key", "")
        except Exception as e:
            print(f"Erro ao ler config da api key: {e}")

    def _setup_gemini(self):
        if not self.api_key or self.api_key.strip() == "":
            return
        
        try:
            genai.configure(api_key=self.api_key)
            
            self.model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                system_instruction=self.system_instruction
            )
            # Inicializa o chat histórico vazio, o Gemini cuidará das mensagens ao longo da sessão
            self.chat_session = self.model.start_chat(history=[])
        except Exception as e:
            print(f"[ERRO] Falha ao inicializar o Gemini: {e}")
            self.chat_session = None

    def is_ollama_ready(self) -> bool:
        """Verifica se o Ollama está online e se o modelo está carregado."""
        try:
            # Tenta listar os modelos para ver se o serviço responde
            import requests
            res = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
            if res.status_code == 200:
                models = [m['name'] for m in res.json().get('models', [])]
                # Verifica se o modelo configurado existe na lista (ou o nome base dele)
                return any(self.ollama_model in m for m in models)
            return False
        except:
            return False

    def process_message(self, message: str) -> str:
        msg = message.strip()
        if not msg:
            return ""

        # Tenta usar Ollama (IA Local) PRIMEIRO para evitar custos/cotas
        try:
            payload = {
                "model": self.ollama_model,
                "messages": [{"role": "system", "content": self.system_instruction}, {"role": "user", "content": msg}],
                "stream": False
            }
            res = requests.post(self.ollama_url, json=payload, timeout=60)
            if res.status_code == 200:
                return res.json().get("message", {}).get("content", "Erro: Ollama retornou resposta vazia.")
        except Exception as e:
            # Se o Ollama não estiver rodando, continua para o Gemini (Fallback)
            print(f"Ollama local offline ou erro: {e}. Tentando Gemini...")

        # --- FALLBACK PARA GEMINI (Caminho Original) ---
        if not self.api_key or self.api_key.strip() == "":
            self._load_config()

        if not self.api_key or self.api_key.strip() == "":
            from app.services.config_service import ConfigService
            try:
                c = ConfigService()
                path = c.config_path
                return f"IA Local (Ollama) não encontrada e a API Key está vazia. Path: {path}. Tente instalar o Ollama ou inserir a chave no config.json"
            except Exception as e:
                return f"DEBUG FATAL ERROR: {str(e)}"

        if not self.chat_session:
            self._setup_gemini()
            
        if not self.chat_session:
            return "Ocorreu um problema ao inicializar a comunicação com a IA local e remota. Verifique as configurações."

        try:
            response = self.chat_session.send_message(msg)
            return response.text
        except Exception as e:
            # Reinicia a sessão em caso de erro de conexão para próxima tentativa
            self.chat_session = None
            erro = str(e)
            if "404" in erro:
                return f"Erro 404: O modelo de IA não foi encontrado. Contate o suporte.\nDetalhe: {erro}"
            if "429" in erro:
              return "Desculpe, a cota de uso da IA remota (Gemini) foi atingida. Por favor, certifique-se de que o Ollama está rodando localmente para uso ilimitado."
            return f"Desculpe, ocorreu um erro na comunicação com a IA: {erro}"
