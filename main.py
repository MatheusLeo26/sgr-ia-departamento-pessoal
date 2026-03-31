"""
SGR.IA — Ponto de entrada
Departamento Pessoal Inteligente | SGR Contábil
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from app.database.db_manager import DatabaseManager
from app.ui.main_window import MainWindow


def main():
    # Inicializa banco SQLite
    db = DatabaseManager()
    db.initialize()

    # Configura CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Inicia interface
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
