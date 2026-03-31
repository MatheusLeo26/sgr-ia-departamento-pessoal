from fpdf import FPDF
import os

class ManualPDF(FPDF):
    def header(self):
        # Logo placeholder se houver
        logo_path = os.path.join("app", "assets", "logo_sgr.png")
        if os.path.exists(logo_path):
            self.image(logo_path, 10, 8, 30)
            
        self.set_font('helvetica', 'B', 15)
        self.cell(80)
        self.cell(30, 10, 'Manual do Usuário - SGR.IA', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_manual():
    pdf = ManualPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('helvetica', 'B', 20)
    pdf.cell(0, 10, 'SGR.IA - Departamento Pessoal Inteligente', 0, 1, 'C')
    pdf.ln(10)

    # Introdução
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, '1. Introdução', 0, 1)
    pdf.set_font('helvetica', '', 12)
    intro = "Bem-vindo ao SGR.IA! Este sistema foi criado para automatizar e facilitar as rotinas de Departamento Pessoal no seu escritório contábil. A SGR.IA atua como uma analista virtual sênior, capaz de calcular folhas, férias, rescisões e 13º salário seguindo rigorosamente a CLT 2026."
    pdf.multi_cell(0, 7, intro)
    pdf.ln(5)

    # Empresas
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, '2. Cadastro de Empresas', 0, 1)
    pdf.set_font('helvetica', '', 12)
    emp_text = "Nesta área, você registrará os clientes do escritório. Informe CNPJ, Razão Social e outros detalhes. A IA validará o CNPJ automaticamente para garantir que não haja erros de digitação. É essencial que cada empresa ativa esteja cadastrada para vincular com seus respectivos funcionários."
    pdf.multi_cell(0, 7, emp_text)
    pdf.ln(5)

    # Funcionários
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, '3. Cadastro de Funcionários', 0, 1)
    pdf.set_font('helvetica', '', 12)
    func_text = "A base do sistema. Para cada empregado, registre o nome, CPF válido e salário base. Informe a data de admissão real (pois ela é usada no motor jurídico da rescisão e férias). O sistema alertará se você tentar cadastrar o mesmo funcionário duas vezes ativamente na mesma empresa."
    pdf.multi_cell(0, 7, func_text)
    pdf.ln(5)

    pdf.add_page()
    
    # Folha
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, '4. Folha de Pagamento', 0, 1)
    pdf.set_font('helvetica', '', 12)
    folha_text = "O módulo de folha mensura os fechamentos com muita precisão.\n- Insira as horas extras e o robô calculará o equivalente a 50% ou 100%, já provisionando o valor de DSR.\n- O motor da IA analisa as tabelas progressivas ativas (INSS e IRRF 2026) automaticamente para dar o valor exato a ser descontado.\n- O cálculo demonstrará os Encargos da Empresa para enviar ao cliente o custo total daquela admissão."
    pdf.multi_cell(0, 7, folha_text)
    pdf.ln(5)

    # Rescisões
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, '5. Calculadora de Rescisões', 0, 1)
    pdf.set_font('helvetica', '', 12)
    resc_text = "O destaque da SGR.IA. Se você tem um grande volume de distratos, basta informar a data de aviso e clicar em calcular.\nA IA suporta dispensas com/sem justa causa, pedidos de demissão e acordos. Ela verificará se cabe integrar aviso prévio indenizado, cobrar o FGTS sobre as projeções, definir a multa real de 40% (ou 20%) e gerar um *Checklist Documental* no relatório, evidenciando o que precisa ser colhido para homologação."
    pdf.multi_cell(0, 7, resc_text)
    pdf.ln(5)

    # Férias & 13º
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, '6. Férias & Décimo Terceiro', 0, 1)
    pdf.set_font('helvetica', '', 12)
    fer_text = "As obrigações corriqueiras também estão inclusas.\nNas férias, opte se o funcionário vendeu ou não os 10 dias (Abono pecuniário) para recalcular a base de 1/3.\nNo 13º, o sistema parcela de forma inteligente; o adiantamento de 50% sem descontos (para o mês de Novembro) e a 2ª parcela definitiva (para Dezembro) já abatendo os tributos legais."
    pdf.multi_cell(0, 7, fer_text)
    pdf.ln(5)

    # Relatórios
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, '7. Relatórios e Exportação', 0, 1)
    pdf.set_font('helvetica', '', 12)
    rel_text = "Para manter o escritório alinhado, gere extrações rápidas em TXT pela guia de Relatórios. Isso ajudará na conferência dupla ou na visualização dos processamentos daquele período para faturamento."
    pdf.multi_cell(0, 7, rel_text)
    
    # Save the PDF
    os.makedirs("manuais", exist_ok=True)
    pdf.output("manuais/SGR_IA_Manual_Usuario.pdf")

if __name__ == "__main__":
    create_manual()
    print("Manual PDF gerado com sucesso!")
