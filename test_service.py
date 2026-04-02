from app.services.chat_service import ChatService

def test():
    print("--- Testando Conexão com Roberta (Ollama) Direto da Classe ---")
    service = ChatService()
    
    print(f"Ollama URL configurada: {service.ollama_url}")
    print(f"Modelo configurado: {service.ollama_model}")
    print(f"Status is_ollama_ready(): {service.is_ollama_ready()}")
    
    pergunta = "Oi, responda apenas 'Teste OK'"
    print(f"Enviando Pergunta: {pergunta}")
    
    # Vamos interceptar a exceção ou o fallback, ou apenas chamar normalmente.
    try:
        resposta = service.process_message(pergunta)
        print(f"\nResposta recebida do process_message:\n{resposta}")
    except Exception as e:
        print(f"Erro inesperado no process_message: {e}")

if __name__ == "__main__":
    test()
