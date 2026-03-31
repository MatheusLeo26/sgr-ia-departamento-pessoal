"""
Motor de Conhecimento da Roberta Bot — SGR.IA
Especialista em DP e rotinas do sistema.
"""

from typing import List, Dict
import re

class ChatService:
    def __init__(self):
        # Base de conhecimento baseada no manual e CLT 2026
        self.kb = [
            {
                "keywords": ["ola", "oi", "bom dia", "boa tarde", "boa noite", "apresente", "quem e voce"],
                "response": "Olá! Eu sou a Roberta Bot, sua assistente especialista da SGR.IA. Fui treinada para tirar suas dúvidas sobre o sistema e rotinas de Departamento Pessoal. Como posso te ajudar hoje?"
            },
            {
                "keywords": ["rescisao", "rescisão", "calculo rescisao", "demissao", "justa causa", "distrato"],
                "response": "Para calcular uma rescisão, acesse o menu 'Rescisão', selecione o funcionário, o tipo de dispensa (com ou sem justa causa, pedido, etc) e a data do aviso. Eu calculo automaticamente o saldo de salário, férias, 13º, aviso prévio e a multa do FGTS. Além disso, gero um checklist documental para você não esquecer nada!"
            },
            {
                "keywords": ["empresa", "cadastrar empresa", "cnpj", "regime"],
                "response": "No menu 'Empresas', você pode gerenciar seus clientes contábeis. Informe o CNPJ (que eu valido na hora), Razão Social e o Regime Tributário. É fundamental que a empresa esteja cadastrada para que você possa vincular funcionários a ela."
            },
            {
                "keywords": ["funcionario", "funcionário", "cadastrar funcionario", "cpf", "admissao"],
                "response": "O cadastro de funcionários fica no menu 'Funcionários'. Lá você informa o CPF, cargo, salário base e a data de admissão. Lembre-se: a data de admissão é crucial para o cálculo correto das férias e do 13º salário!"
            },
            {
                "keywords": ["folha", "pagamento", "holerite", "hora extra", "dsr", "inss", "irrf"],
                "response": "O módulo de 'Folha de Pagamento' processa o fechamento mensal. Você pode lançar horas extras (50% ou 100%) e eu calculo o DSR automaticamente. Também aplico as tabelas progressivas de INSS e IRRF da CLT 2026, além de demonstrar o custo total da empresa (encargos patronais)."
            },
            {
                "keywords": ["ferias", "férias", "abono", "pecuniario", "1/3"],
                "response": "O cálculo de férias está no menu 'Férias'. Você pode definir se o funcionário vai vender 10 dias (abono pecuniário) e eu calculo o valor bruto, o 1/3 constitucional e os descontos de INSS/IRRF. O pagamento deve ser feito 2 dias antes do início do gozo."
            },
            {
                "keywords": ["13", "decimo", "décimo", "parcela", "natalino"],
                "response": "No menu '13º Salário', você pode calcular a 1ª parcela (adiantamento de 50% sem descontos) ou a 2ª parcela (valor integral com deduções de INSS, IRRF e abatimento da 1ª parcela)."
            },
            {
                "keywords": ["clt", "2026", "salario minimo", "valores"],
                "response": "O SGR.IA está atualizado com a legislação de 2026. O salário mínimo configurado é R$ 1.621,00. As tabelas de INSS e IRRF também seguem as normas vigentes para este ano."
            },
            {
                "keywords": ["relatorio", "exportar", "pdf", "txt"],
                "response": "Você pode gerar relatórios operacionais no menu 'Relatórios'. Atualmente exportamos em TXT listas de funcionários, empresas e o resumo de rescisões. PDFs de manuais podem ser encontrados na aba 'Tutoriais'."
            },
            {
                "keywords": ["ajuda", "tutorial", "manual", "como usar"],
                "response": "Se precisar de um guia detalhado, acesse a aba 'Tutoriais' no menu lateral. Lá você encontrará manuais em PDF que mostram o passo a passo de cada funcionalidade do sistema."
            }
        ]
        self.default_response = "Desculpe, não entendi sua dúvida. Sou especialista em SGR.IA e rotinas de DP. Pode perguntar sobre Folha, Férias, Rescisão, Empresas ou como usar o sistema!"

    def process_message(self, message: str) -> str:
        msg = message.lower().strip()
        if not msg:
            return ""

        # Tenta encontrar correspondência por palavras-chave
        for item in self.kb:
            for kw in item["keywords"]:
                # Use regex para encontrar a palavra exata
                if re.search(r'\b' + re.escape(kw) + r'\b', msg):
                    return item["response"]

        return self.default_response
