from app.database.db_manager import DatabaseManager
from app.services.calculators import calcular_rescisao
from datetime import date

db = DatabaseManager()
db.initialize()
print("Banco inicializado OK")

dados = {
    "salario": 3000.0,
    "data_admissao": date(2022, 1, 5),
    "data_desligamento": date(2026, 3, 31),
    "tipo_rescisao": "sem_justa_causa",
    "dias_trabalhados": 31,
    "periodos_ferias": 1,
    "meses_ferias_prop": 3,
    "aviso_trabalhado": False,
    "saldo_fgts": 8000.0,
    "dependentes": 1,
    "outras_verbas": 0,
}

r = calcular_rescisao(dados)
print("=== VERBAS ===")
for k, v in r["verbas"].items():
    print(f"  {k}: R$ {v:,.2f}")
print("=== DESCONTOS ===")
for k, v in r["descontos"].items():
    print(f"  {k}: R$ {v:,.2f}")
print(f"LIQUIDO: R$ {r['totais']['liquido']:,.2f}")
print("=== CHECKLIST ===")
for c in r["checklist"]:
    print(f"  [ ] {c}")
print("OK - Calculadora funcionando!")
