"""
Script de Compilação SGR.IA
Gera o Executável Principal e o Lançador (Update).
"""
import PyInstaller.__main__
import os
import shutil
import customtkinter

# Caminhos
BASE_DIR = os.path.abspath(os.getcwd())
CTK_DIR  = os.path.dirname(customtkinter.__file__)

def build_main():
    print("--- Compilando SGR-IA (Executável Principal) ---")
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--windowed',
        '--name=sgr_ia',
        f'--icon={os.path.join(BASE_DIR, "app", "assets", "robot_report_icon.ico")}',
        '--add-data', f'{os.path.join(BASE_DIR, "app", "assets")};app/assets',
        '--add-data', f'{CTK_DIR};customtkinter',
        '--clean',
        '-y'
    ])

def build_launcher():
    print("--- Compilando Lançador (SGR-IA-Incio) ---")
    PyInstaller.__main__.run([
        'launcher.py',
        '--onefile',
        '--windowed',
        '--name=SGR-IA-Incio',
        f'--icon={os.path.join(BASE_DIR, "app", "assets", "robot_report_icon.ico")}',
        '--add-data', f'{os.path.join(BASE_DIR, "app", "assets")};app/assets',
        '--add-data', f'{CTK_DIR};customtkinter',
        '--clean',
        '-y'
    ])

def deploy_to_server():
    SERVER_DIR = r"Z:\SGR-IA\Sistema"
    dist_dir = os.path.join(BASE_DIR, "dist")
    
    if not os.path.exists(SERVER_DIR):
        print(f"Tentando criar diretório: {SERVER_DIR}")
        os.makedirs(SERVER_DIR, exist_ok=True)

    # Copia o principal para a pasta Sistema do servidor
    print(f"Propagando para o servidor: {SERVER_DIR}")
    shutil.copy2(os.path.join(dist_dir, "sgr_ia.exe"), os.path.join(SERVER_DIR, "sgr_ia.exe"))
    
    # Copia o lançador para a raiz do Z:\SGR-IA para fácil acesso
    shutil.copy2(os.path.join(dist_dir, "SGR-IA-Incio.exe"), r"Z:\SGR-IA\SGR-IA-Incio.exe")
    
    # Cria o arquivo de configuração padrão no servidor
    config_data = {"db_path": r"Z:\SGR-IA\sgr.db"}
    with open(os.path.join(SERVER_DIR, "config.json"), "w") as f:
        import json
        json.dump(config_data, f, indent=4)

    print("Deploy finalizado com sucesso!")

if __name__ == "__main__":
    build_main()
    build_launcher()
    deploy_to_server()
