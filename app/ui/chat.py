"""
Interface da Roberta Bot — SGR.IA
Chat moderno com visual de bolhas.
"""
import customtkinter as ctk
import os
from PIL import Image
from app.ui import theme as T
from app.services.chat_service import ChatService

class ChatPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=T.BG_MAIN)
        self._chat_service = ChatService()
        
        # Load Roberta Avatar
        self._avatar_img = None
        avatar_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "app", "assets", "roberta_avatar.png")
        if os.path.exists(avatar_path):
            self._avatar_img = ctk.CTkImage(light_image=Image.open(avatar_path), 
                                            dark_image=Image.open(avatar_path), 
                                            size=(40, 40))

        self._build()
        self._show_initial_greeting()

    def _build(self):
        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=T.PAD, pady=(T.PAD, 6))
        
        # Header Avatar (Optional touch)
        if self._avatar_img:
            ctk.CTkLabel(hdr, image=self._avatar_img, text="").pack(side="left", padx=(0, 10))

        ctk.CTkLabel(hdr, text="Roberta Bot", font=ctk.CTkFont(T.FONT_FAMILY, 22, "bold"), text_color=T.TEXT).pack(side="left")
        ctk.CTkLabel(hdr, text="Assistente de DP e Robô de Dúvidas", font=ctk.CTkFont(T.FONT_FAMILY, 11), text_color=T.ACCENT_LIGHT).pack(side="left", padx=14, pady=4)

        # Chat Area (Scrollable)
        self._chat_scroll = ctk.CTkScrollableFrame(self, fg_color=T.BG_PANEL, corner_radius=T.CORNER_R)
        self._chat_scroll.pack(fill="both", expand=True, padx=T.PAD, pady=(0, 10))

        # Bottom Input Area
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=T.PAD, pady=(0, T.PAD))

        self._entry = ctk.CTkEntry(input_frame, placeholder_text="Digite sua dúvida aqui (Ex: Como calcular rescisão?)...",
                                   fg_color=T.BG_INPUT, border_color=T.BORDER, text_color=T.TEXT,
                                   height=45, corner_radius=T.CORNER_R)
        self._entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self._entry.bind("<Return>", lambda e: self._send())

        self._send_btn = ctk.CTkButton(input_frame, text="ENVIAR", width=120, height=45, 
                                       fg_color=T.PRIMARY, hover_color=T.PRIMARY_HOVER,
                                       font=ctk.CTkFont(T.FONT_FAMILY, 12, "bold"),
                                       command=self._send)
        self._send_btn.pack(side="right")

    def _show_initial_greeting(self):
        initial_msg = "Olá, sou a Roberta Bot, sua assistente da SGR.IA, em que posso ajudar?"
        self._add_message("Roberta Bot", initial_msg, is_user=False)

    def _add_message(self, sender, text, is_user=False):
        # Frame da mensagem
        msg_frame = ctk.CTkFrame(self._chat_scroll, fg_color="transparent")
        msg_frame.pack(fill="x", pady=8, padx=10)

        # Bubble alignment
        color = T.PRIMARY_DARK if is_user else T.BG_CARD
        text_color = T.TEXT if is_user else T.TEXT_SEC
        
        # Container for Avatar + Bubble (for Roberta)
        container = ctk.CTkFrame(msg_frame, fg_color="transparent")
        container.pack(side="right" if is_user else "left", anchor="e" if is_user else "w")

        if not is_user and self._avatar_img:
            ctk.CTkLabel(container, image=self._avatar_img, text="").pack(side="left", anchor="n", padx=(0, 8))

        bubble = ctk.CTkFrame(container, fg_color=color, corner_radius=12)
        bubble.pack(side="left", padx=0)

        # Sender Label
        lbl_sender = ctk.CTkLabel(bubble, text=sender, font=ctk.CTkFont(T.FONT_FAMILY, 9, "bold"), 
                                  text_color=T.ACCENT if not is_user else T.ACCENT_LIGHT)
        lbl_sender.pack(anchor="w", padx=12, pady=(8, 2))

        # Text Label
        lbl_text = ctk.CTkLabel(bubble, text=text, font=ctk.CTkFont(T.FONT_FAMILY, 12),
                                text_color=text_color, wraplength=450, justify="left")
        lbl_text.pack(anchor="w", padx=12, pady=(0, 10))

        # Auto-scroll to bottom
        self._chat_scroll._parent_canvas.yview_moveto(1.0)

    def _send(self):
        msg = self._entry.get().strip()
        if not msg:
            return

        self._entry.delete(0, "end")
        self._add_message("Você", msg, is_user=True)
        
        # Resposta da Roberta
        response = self._chat_service.process_message(msg)
        self.after(500, lambda: self._add_message("Roberta Bot", response, is_user=False))
