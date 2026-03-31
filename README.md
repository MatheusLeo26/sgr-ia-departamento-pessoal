# SGR.IA — Sistema Inteligente de Departamento Pessoal

<p align="center">
  <img src="app/assets/logo_sgr.png" alt="SGR Contábil" width="120">
</p>

<p align="center">
  <b>SGR.IA</b> — Inteligência Artificial Corporativa para Departamento Pessoal<br>
  <i>Desenvolvido para escritórios contábeis brasileiros</i>
</p>

---

## 📋 Sobre

O **SGR.IA** é um sistema desktop profissional desenvolvido para automatizar rotinas de **Departamento Pessoal** em escritórios contábeis, operando como um **analista sênior de DP** com domínio completo da legislação trabalhista brasileira (CLT 2026).

## 🚀 Funcionalidades

| Módulo | Descrição |
|---|---|
| 📊 **Dashboard** | KPIs operacionais, ações rápidas e rescisões recentes |
| 📋 **Rescisão** | Calculadora completa com 5 tipos de rescisão (CLT) |
| 💰 **Folha de Pagamento** | Holerite completo com HE, DSR, adicionais e encargos |
| 🏖️ **Férias** | Cálculo com 1/3 constitucional e abono pecuniário |
| 🎄 **13º Salário** | 1ª e 2ª parcela com descontos legais |
| 👤 **Funcionários** | Cadastro completo com validação de CPF |
| 🏢 **Empresas** | Cadastro com CNPJ, regime tributário e sindicato |
| 📄 **Relatórios** | Exportação de relatórios em TXT |

## 🛠️ Stack Tecnológico

- **Python 3.12+**
- **CustomTkinter** — Interface gráfica moderna
- **SQLite3** — Banco de dados local
- **Pillow** — Manipulação de imagens
- **Arquitetura MVC** simplificada

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/MatheusLeo26/sgr-ia-dp.git
cd sgr-ia-dp

# Instale as dependências
pip install -r requirements.txt

# Execute o sistema
python main.py
```

## 📁 Estrutura do Projeto

```
sgr-ia/
├── main.py                     # Ponto de entrada
├── requirements.txt
└── app/
    ├── assets/                 # Logo e recursos visuais
    ├── database/               # SQLite — conexão e migrações
    ├── models/                 # Modelos de dados
    ├── services/               # Motores de cálculo (CLT 2026)
    ├── controllers/            # CRUD e lógica de negócios
    └── ui/                     # Interface gráfica (CustomTkinter)
        └── components/         # Componentes reutilizáveis
```

## ⚖️ Legislação

Todos os cálculos seguem a **CLT vigente em 2026**:
- Salário mínimo: **R$ 1.621,00**
- INSS progressivo (7,5% a 14%)
- IRRF com deduções por dependente
- Aviso prévio proporcional (Lei 12.506/2011)
- FGTS 8% + multa rescisória (40% ou 20%)

## 🏢 SGR Contábil

Desenvolvido e mantido pela **SGR Contábil**.

---

<p align="center">
  <b>SGR.IA v2.0</b> — Departamento Pessoal Inteligente
</p>
