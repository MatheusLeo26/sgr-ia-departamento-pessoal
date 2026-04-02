import pandas as pd
import os
from datetime import datetime
from app.models.empresa import Empresa
from app.models.funcionario import Funcionario
from app.controllers.empresa_controller import EmpresaController
from app.controllers.funcionario_controller import FuncionarioController
from app.services.validators import parse_date

class ImportService:
    def __init__(self):
        self.emp_ctrl = EmpresaController()
        self.func_ctrl = FuncionarioController()

    def importar_empresas(self, filepath: str) -> tuple[int, str]:
        """
        Importa empresas de um Excel. 
        Colunas esperadas: razao_social, cnpj, nome_fantasia, cnae, fpas, sindicato, regime_tributario, email, telefone
        """
        try:
            df = pd.read_excel(filepath)
            count = 0
            errors = []

            for _, row in df.iterrows():
                try:
                    razao = str(row.get("razao_social", "")).strip()
                    cnpj = str(row.get("cnpj", "")).strip().replace(".", "").replace("/", "").replace("-", "")
                    
                    if not razao or not cnpj:
                        continue

                    emp = Empresa(
                        razao_social=razao,
                        cnpj=cnpj,
                        nome_fantasia=str(row.get("nome_fantasia", "")) if pd.notna(row.get("nome_fantasia")) else None,
                        cnae=str(row.get("cnae", "")) if pd.notna(row.get("cnae")) else None,
                        fpas=str(row.get("fpas", "")) if pd.notna(row.get("fpas")) else None,
                        sindicato=str(row.get("sindicato", "")) if pd.notna(row.get("sindicato")) else None,
                        regime_tributario=str(row.get("regime_tributario", "")) if pd.notna(row.get("regime_tributario")) else None,
                        email=str(row.get("email", "")) if pd.notna(row.get("email")) else None,
                        telefone=str(row.get("telefone", "")) if pd.notna(row.get("telefone")) else None
                    )
                    
                    ok, msg = self.emp_ctrl.salvar(emp)
                    if ok:
                        count += 1
                    else:
                        errors.append(f"Linha {_+2} (CNPJ {cnpj}): {msg}")

                except Exception as e:
                    errors.append(f"Linha {_+2}: Erro de processamento: {e}")

            res_msg = f"{count} empresas importadas com sucesso."
            if errors:
                res_msg += "\n\nErros:\n" + "\n".join(errors[:10])
                if len(errors) > 10:
                    res_msg += f"\n...e mais {len(errors)-10} erros."
            
            return count, res_msg

        except Exception as e:
            return 0, f"Erro ao ler arquivo Excel: {e}"

    def importar_funcionarios(self, filepath: str) -> tuple[int, str]:
        """
        Importa funcionários de um Excel vinculando pelo CNPJ da Empresa.
        Colunas esperadas: nome, cpf, salario, data_admissao, rg, cargo, jornada, dependentes, vale_transporte, nome_mae, estado_civil, cnpj_empresa
        """
        try:
            df = pd.read_excel(filepath)
            count = 0
            errors = []
            
            # Cache de empresas para evitar múltiplas queries
            empresas_map = {e.cnpj: e.id for e in self.emp_ctrl.listar()}

            for _, row in df.iterrows():
                try:
                    nome = str(row.get("nome", "")).strip()
                    cpf = str(row.get("cpf", "")).strip().replace(".", "").replace("-", "")
                    cnpj_emp = str(row.get("cnpj_empresa", "")).strip().replace(".", "").replace("/", "").replace("-", "")
                    
                    if not nome or not cpf or not cnpj_emp:
                        errors.append(f"Linha {_+2}: Nome, CPF e CNPJ Empresa são obrigatórios.")
                        continue

                    # Busca ID da empresa pelo CNPJ
                    emp_id = empresas_map.get(cnpj_emp)
                    if not emp_id:
                        errors.append(f"Linha {_+2}: Empresa com CNPJ {cnpj_emp} não cadastrada no sistema.")
                        continue

                    # Trata data de admissão
                    data_raw = row.get("data_admissao")
                    if isinstance(data_raw, datetime):
                        data_iso = data_raw.strftime("%Y-%m-%d")
                    else:
                        try:
                            data_iso = parse_date(str(data_raw)).isoformat()
                        except:
                            errors.append(f"Linha {_+2}: Formato de data inválido ({data_raw}). Use DD/MM/AAAA.")
                            continue

                    func = Funcionario(
                        nome=nome,
                        cpf=cpf,
                        salario=float(row.get("salario", 0)),
                        data_admissao=data_iso,
                        empresa_id=emp_id,
                        rg=str(row.get("rg", "")) if pd.notna(row.get("rg")) else None,
                        cargo=str(row.get("cargo", "")) if pd.notna(row.get("cargo")) else None,
                        jornada=str(row.get("jornada", "44h semanais")) if pd.notna(row.get("jornada")) else "44h semanais",
                        dependentes=int(row.get("dependentes", 0)) if pd.notna(row.get("dependentes")) else 0,
                        vale_transporte=float(row.get("vale_transporte", 0)) if pd.notna(row.get("vale_transporte")) else 0.0,
                        nome_mae=str(row.get("nome_mae", "")) if pd.notna(row.get("nome_mae")) else None,
                        estado_civil=str(row.get("estado_civil", "")) if pd.notna(row.get("estado_civil")) else None
                    )

                    ok, msg = self.func_ctrl.salvar(func)
                    if ok:
                        count += 1
                    else:
                        errors.append(f"Linha {_+2} (CPF {cpf}): {msg}")

                except Exception as e:
                    errors.append(f"Linha {_+2}: Erro de processamento: {e}")

            res_msg = f"{count} funcionários importados com sucesso."
            if errors:
                res_msg += "\n\nAlertas/Erros:\n" + "\n".join(errors[:10])
                if len(errors) > 10:
                    res_msg += f"\n...e mais {len(errors)-10} erros."

            return count, res_msg

        except Exception as e:
            return 0, f"Erro ao ler arquivo Excel: {e}"

    def gerar_templates(self, directory: str):
        """Gera arquivos Excel de exemplo para o usuário."""
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Template Empresas
        df_emp = pd.DataFrame(columns=[
            "razao_social", "cnpj", "nome_fantasia", "cnae", "fpas", 
            "sindicato", "regime_tributario", "email", "telefone"
        ])
        df_emp.loc[0] = [
            "EMPRESA EXEMPLO LTDA", "12.345.678/0001-90", "EXEMPLO", "8211-3/00", 
            "515", "SINDIPAO", "Simples Nacional", "contato@exemplo.com", "(11) 99999-9999"
        ]
        df_emp.to_excel(os.path.join(directory, "modelo_empresas.xlsx"), index=False)

        # Template Funcionários
        df_func = pd.DataFrame(columns=[
            "nome", "cpf", "salario", "data_admissao", "rg", "cargo", 
            "jornada", "dependentes", "vale_transporte", "nome_mae", 
            "estado_civil", "cnpj_empresa"
        ])
        df_func.loc[0] = [
            "JOÃO DA SILVA", "123.456.789-00", 2500.50, "01/02/2024", "12.345.678-9", 
            "Auxiliar de DP", "44h semanais", 0, 150.00, "MARIA DA SILVA", "Solteiro", "12.345.678/0001-90"
        ]
        df_func.to_excel(os.path.join(directory, "modelo_funcionarios.xlsx"), index=False)
