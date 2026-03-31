"""
Lançador Oficial SGR.IA — Sistema de Atualizações
Inicia o sistema, verifica novas versões no drive Z: e atualiza com barra de progresso.
Estilo Steam / Corporativo Moderno.
"""
import customtkinter as ctk
import os
import shutil
import json
import hashlib
import subprocess
import threading
import time
from PIL import Image
from app.ui import theme as T

# Configurações do Lançador
APP_NAME = "SGR-IA"
SERVER_PATH = r"Z:\SGR-IA\Sistema"
LOCAL_PATH  = os.path.join(os.getenv("APPDATA"), APP_NAME)
EXE_NAME    = "sgr_ia.exe"

class SGRIA_Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SGR.IA — Verificação")
        self.geometry("450x180")
        self.resizable(False, False)
        self.configure(fg_color=T.BG_MAIN)
        self.overrideredirect(True) # Janela sem bordas (Splash style)
        
        # Center Window
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (450 // 2)
        y = (screen_h // 2) - (180 // 2)
        self.geometry(f"+{x}+{y}")

        self._build_ui()
        
        # Inicia verificação em 1 segundo
        self.after(1000, self.start_check)

    def _build_ui(self):
        # Outer border
        self.main_frame = ctk.CTkFrame(self, fg_color=T.BG_MAIN, border_color=T.BORDER, border_width=1)
        self.main_frame.pack(fill="both", expand=True)

        # Content
        content = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content.pack(pady=30, padx=40, fill="both", expand=True)

        # Logo and Title
        title_lbl = ctk.CTkLabel(content, text="SGR.IA — DEPARTAMENTO PESSOAL", 
                                font=ctk.CTkFont(T.FONT_FAMILY, 15, "bold"), text_color=T.TEXT)
        title_lbl.pack(anchor="w")

        self.status_lbl = ctk.CTkLabel(content, text="Verificando atualizações...", 
                                      font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.TEXT_MUTED)
        self.status_lbl.pack(anchor="w", pady=(2, 10))

        # Progress bar
        self.progress = ctk.CTkProgressBar(content, height=10, fg_color=T.BG_INPUT, progress_color=T.PRIMARY)
        self.progress.set(0)
        self.progress.pack(fill="x")

        self.percent_lbl = ctk.CTkLabel(content, text="0%", font=ctk.CTkFont(T.FONT_FAMILY, 9), text_color=T.TEXT_MUTED)
        self.percent_lbl.pack(anchor="e", pady=2)

    def start_check(self):
        threading.Thread(target=self.run_logic, daemon=True).start()

    def run_logic(self):
        try:
            if not os.path.exists(LOCAL_PATH):
                os.makedirs(LOCAL_PATH, exist_ok=True)

            # 1. Verifica se servidor está acessível
            if not os.path.exists(SERVER_PATH):
                self.log_status("Servidor offline — Iniciando versão local...")
                time.sleep(1)
                self.launch_app()
                return

            server_exe    = os.path.join(SERVER_PATH, EXE_NAME)
            local_exe     = os.path.join(LOCAL_PATH, EXE_NAME)
            server_config = os.path.join(SERVER_PATH, "config.json")
            local_config  = os.path.join(LOCAL_PATH, "config.json")
            
            # 2. Sincroniza Config se existir no servidor
            if os.path.exists(server_config):
                shutil.copy2(server_config, local_config)

            # 3. Verifica se o executável existe no servidor
            if not os.path.exists(server_exe):
                self.launch_app()
                return

            # 4. Compara Hash (MD5) para detectar mudanças no executável
            update_needed = True
            if os.path.exists(local_exe):
                server_hash = self.get_file_hash(server_exe)
                local_hash  = self.get_file_hash(local_exe)
                if server_hash == local_hash:
                    update_needed = False

            if update_needed:
                self.log_status("Nova versão disponível! Baixando...")
                self.copy_file_with_progress(server_exe, local_exe)
            else:
                self.log_status("Sistema atualizado.")
                self.progress.set(1.0)
                time.sleep(1)

            self.launch_app()


        except Exception as e:
            self.log_status(f"Erro: {e}")
            time.sleep(3)
            self.launch_app()

    def get_file_hash(self, path):
        hasher = hashlib.md5()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def copy_file_with_progress(self, source, dest):
        size = os.path.getsize(source)
        copied = 0
        with open(source, 'rb') as fs, open(dest, 'wb') as fd:
            while True:
                chunk = fs.read(1024 * 1024) # 1MB
                if not chunk:
                    break
                fd.write(chunk)
                copied += len(chunk)
                p = copied / size
                self.update_progress(p)
        
    def update_progress(self, p):
        self.progress.set(p)
        self.percent_lbl.configure(text=f"{int(p*100)}%")

    def log_status(self, text):
        self.status_lbl.configure(text=text)

    def launch_app(self):
        local_exe = os.path.join(LOCAL_PATH, EXE_NAME)
        if os.path.exists(local_exe):
            subprocess.Popen([local_exe], cwd=LOCAL_PATH)
        self.destroy()

if __name__ == "__main__":
    app = SGRIA_Launcher()
    app.mainloop()
