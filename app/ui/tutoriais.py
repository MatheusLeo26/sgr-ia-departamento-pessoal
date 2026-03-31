"""
Aba de Tutoriais — SGR.IA
Lista e abre manuais PDF da pasta /manuais.
"""
import customtkinter as ctk
import os
import subprocess
from tkinter import messagebox
from app.ui import theme as T

class TutoriaisPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=T.BG_MAIN)
        self._manual_path = os.path.join(os.getcwd(), "manuais")
        self._build()

    def _build(self):
        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=T.PAD, pady=(T.PAD, 6))
        ctk.CTkLabel(hdr, text="Centro de Treinamento", font=ctk.CTkFont(T.FONT_FAMILY, 22, "bold"), text_color=T.TEXT).pack(side="left")
        ctk.CTkLabel(hdr, text="Manuais e Guias Passo a Passo", font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.ACCENT_LIGHT).pack(side="left", padx=14, pady=4)

        # Scrollable area for cards
        self._scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._scroll.pack(fill="both", expand=True, padx=T.PAD, pady=(0, T.PAD))
        
        self.atualizar_lista()

    def atualizar_lista(self):
        # Limpa lista atual
        for w in self._scroll.winfo_children():
            w.destroy()

        if not os.path.exists(self._manual_path):
            os.makedirs(self._manual_path, exist_ok=True)

        files = [f for f in os.listdir(self._manual_path) if f.lower().endswith(".pdf")]

        if not files:
            ctk.CTkLabel(self._scroll, text="Nenhum manual PDF encontrado em /manuais", 
                         font=ctk.CTkFont(T.FONT_FAMILY, 13), text_color=T.TEXT_MUTED).pack(pady=40)
            return

        # Grid system for cards
        self._scroll.grid_columnconfigure((0, 1), weight=1, uniform="c")
        
        for i, filename in enumerate(files):
            row = i // 2
            col = i % 2
            self._create_card(filename, row, col)

    def _create_card(self, filename, row, col):
        card = ctk.CTkFrame(self._scroll, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R, border_width=1, border_color=T.BORDER)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        
        title = filename.replace("_", " ").replace(".pdf", "").title()
        
        # Icon placeholder
        ctk.CTkLabel(card, text="📄", font=ctk.CTkFont(size=30)).pack(pady=(20, 5))
        
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(T.FONT_FAMILY, 14, "bold"), 
                     text_color=T.TEXT, wraplength=250).pack(padx=20, pady=5)
        
        ctk.CTkLabel(card, text="Documento PDF Oficial", font=ctk.CTkFont(T.FONT_FAMILY, 10), 
                     text_color=T.TEXT_SEC).pack(padx=20, pady=(0, 15))

        ctk.CTkButton(card, text="ABRIR MANUAL", height=35, fg_color=T.PRIMARY, hover_color=T.PRIMARY_HOVER,
                      font=ctk.CTkFont(T.FONT_FAMILY, 11, "bold"),
                      command=lambda f=filename: self._abrir_pdf(f)).pack(fill="x", padx=20, pady=(0, 20))

    def _abrir_pdf(self, filename):
        full_path = os.path.join(self._manual_path, filename)
        try:
            # os.startfile é específico para Windows
            os.startfile(full_path)
        except Exception as e:
            messagebox.showerror("SGR.IA", f"Erro ao abrir PDF: {e}")
