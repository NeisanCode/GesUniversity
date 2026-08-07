import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_view import MainView


class AdminAuthFrame(ctk.CTkFrame):
    def __init__(self, parent, main_app: "MainView"):
        super().__init__(parent, fg_color="transparent")
        self.app = main_app

        # Carte centrale de connexion
        auth_card = ctk.CTkFrame(
            self,
            width=420,
            fg_color=self.app.COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color="#334155",
        )
        auth_card.pack(expand=True, pady=40, padx=20)

        ctk.CTkLabel(auth_card, text="🔐", font=ctk.CTkFont(size=48)).pack(
            pady=(30, 10)
        )

        ctk.CTkLabel(
            auth_card,
            text="Espace Administration",
            font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"),
            text_color=self.app.COLOR_TEXT,
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            auth_card,
            text="Veuillez saisir vos identifiants pour continuer",
            font=ctk.CTkFont(size=12),
            text_color=self.app.COLOR_SUBTEXT,
        ).pack(pady=(0, 25))

        # Champ Nom d'utilisateur
        ctk.CTkLabel(
            auth_card,
            text="Nom d'utilisateur",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.app.COLOR_TEXT,
            anchor="w",
        ).pack(fill="x", padx=40, pady=(0, 5))

        self.entry_username = ctk.CTkEntry(
            auth_card,
            placeholder_text="Entrez votre nom...",
            height=40,
            fg_color="#0F172A",
            border_color="#334155",
            text_color=self.app.COLOR_TEXT,
        )
        self.entry_username.pack(fill="x", padx=40, pady=(0, 15))

        # Champ Mot de Passe
        ctk.CTkLabel(
            auth_card,
            text="Mot de passe",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.app.COLOR_TEXT,
            anchor="w",
        ).pack(fill="x", padx=40, pady=(0, 5))

        self.entry_password = ctk.CTkEntry(
            auth_card,
            show="•",
            placeholder_text="Entrez votre mot de passe...",
            height=40,
            fg_color="#0F172A",
            border_color="#334155",
            text_color=self.app.COLOR_TEXT,
        )
        self.entry_password.pack(fill="x", padx=40, pady=(0, 20))
        self.entry_password.bind("<Return>", lambda e: self._handle_login())

        # Boutons de Validation / Annulation
        btn_box = ctk.CTkFrame(auth_card, fg_color="transparent")
        btn_box.pack(fill="x", padx=40, pady=(0, 30))

        ctk.CTkButton(
            btn_box,
            text="Annuler",
            fg_color="#334155",
            hover_color="#475569",
            height=38,
            width=110,
            command=self.app.show_dashboard,
        ).pack(side="left")

        ctk.CTkButton(
            btn_box,
            text="Se connecter",
            fg_color=self.app.COLOR_PRIMARY,
            hover_color="#2563EB",
            height=38,
            width=180,
            font=ctk.CTkFont(weight="bold"),
            command=self._handle_login,
        ).pack(side="right", padx=(10, 0))

    def focus_input(self):
        self.entry_username.focus_set()

    def _handle_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        if username == self.app.ADMIN_USERNAME and password == self.app.ADMIN_PASSWORD:
            self.app.is_admin_authenticated = True
            self.entry_username.delete(0, "end")
            self.entry_password.delete(0, "end")
            self.app.show_admin_dashboard()
        else:
            messagebox.showerror(
                "Échec d'authentification",
                "Nom d'utilisateur ou mot de passe incorrect.",
            )