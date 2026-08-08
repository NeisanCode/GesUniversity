import os
import customtkinter as ctk
from PIL import Image
from config import (
    APP_NAME,
    APP_VERSION,
    APP_AUTHOR,
    APP_COPYRIGHT,
    APP_DESCRIPTION,
    APP_RELEASE,
    LOGO_PATH,
    LICENSE_PATH,
)


class InfoModal(ctk.CTkToplevel):
    """Fenêtre modale 'À propos' moderne et bien aérée."""

    def __init__(self, parent, colors: dict):
        super().__init__(parent)

        self.colors = colors
        self.license_window = None

        self.title(f"À propos - {APP_NAME}")
        self.geometry("500x520")
        self.resizable(False, False)
        self.configure(fg_color=self.colors.get("BG", "#0F172A"))

        # Conserver la modale au premier plan
        self.transient(parent)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):
        # Carte principale
        card = ctk.CTkFrame(
            self,
            fg_color=self.colors.get("CARD_BG", "#1E293B"),
            corner_radius=16,
            border_width=1,
            border_color="#334155",
        )
        card.pack(fill="both", expand=True, padx=20, pady=20)

        # 1. LOGO OU ICÔNE DE L'APPLICATION
        try:
            pil_img = Image.open(LOGO_PATH)
            logo_img = ctk.CTkImage(
                light_image=pil_img, dark_image=pil_img, size=(64, 64)
            )
            ctk.CTkLabel(card, image=logo_img, text="").pack(pady=(24, 8))
        except Exception:
            ctk.CTkLabel(card, text="🎓", font=ctk.CTkFont(size=42)).pack(pady=(24, 8))

        # 2. TITRE PRINCIPAL
        ctk.CTkLabel(
            card,
            text=APP_NAME,
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
            text_color=self.colors.get("PRIMARY", "#3B82F6"),
        ).pack(pady=(0, 2))

        # 3. VERSION
        ctk.CTkLabel(
            card,
            text=f"v{APP_VERSION} ({APP_RELEASE})",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors.get("SUBTEXT", "#94A3B8"),
        ).pack(padx=10, pady=2)

        # 4. DESCRIPTION
        ctk.CTkLabel(
            card,
            text=APP_DESCRIPTION,
            font=ctk.CTkFont(size=13),
            text_color=self.colors.get("TEXT", "#F8FAFC"),
            wraplength=420,
            justify="center",
        ).pack(pady=(0, 16), padx=20)

        # Séparateur visuel discret
        ctk.CTkFrame(card, fg_color="#334155", height=1).pack(
            fill="x", padx=40, pady=(0, 16)
        )

        # 5. DÉVELOPPEURS (AVEC RETOUR À LA LIGNE SI COMPOSÉ DE PLUSIEURS NOMS)
        ctk.CTkLabel(
            card,
            text="Développé par",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors.get("SUBTEXT", "#94A3B8"),
        ).pack()

        # Formatage des auteurs
        formatted_authors = APP_AUTHOR.replace(" & ", "\n").replace(" et ", "\n")

        ctk.CTkLabel(
            card,
            text=formatted_authors,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors.get("TEXT", "#F8FAFC"),
            justify="center",
            wraplength=400,
        ).pack(pady=(2, 8))

        # 6. COPYRIGHT
        ctk.CTkLabel(
            card,
            text=APP_COPYRIGHT,
            font=ctk.CTkFont(size=10),
            text_color="#64748B",
        ).pack(pady=(0, 20))

        # 7. BOUTONS D'ACTION
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 20), padx=25)

        ctk.CTkButton(
            btn_frame,
            text="📄 Afficher la Licence",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.colors.get("PRIMARY", "#3B82F6"),
            hover_color="#2563EB",
            height=36,
            corner_radius=8,
            command=self.open_license_modal,
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        ctk.CTkButton(
            btn_frame,
            text="Fermer",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#334155",
            hover_color="#475569",
            text_color=self.colors.get("TEXT", "#F8FAFC"),
            height=36,
            corner_radius=8,
            command=self.destroy,
        ).pack(side="right", expand=True, fill="x", padx=(6, 0))

    def open_license_modal(self):
        """Ouvre une sous-modale contenant la lecture du fichier de licence."""
        if self.license_window is not None and self.license_window.winfo_exists():
            self.license_window.focus()
            return

        self.license_window = ctk.CTkToplevel(self)
        self.license_window.title("Licence du logiciel")
        self.license_window.geometry("580x480")
        self.license_window.configure(fg_color=self.colors.get("BG", "#0F172A"))

        self.license_window.transient(self)
        self.license_window.grab_set()

        ctk.CTkLabel(
            self.license_window,
            text="Termes de la Licence",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors.get("TEXT", "#F8FAFC"),
        ).pack(pady=(16, 8))

        textbox = ctk.CTkTextbox(
            self.license_window,
            fg_color=self.colors.get("CARD_BG", "#1E293B"),
            text_color=self.colors.get("TEXT", "#F8FAFC"),
            font=ctk.CTkFont(family="Consolas", size=11),
            corner_radius=10,
            border_width=1,
            border_color="#334155",
        )
        textbox.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # Utilisation de LICENSE_PATH importé depuis config.py
        target_path = LICENSE_PATH
        if not os.path.exists(target_path):
            # Fallback si le fichier a l'extension .txt
            target_path = f"{LICENSE_PATH}.txt"

        if os.path.exists(target_path):
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                content = f"Erreur lors de la lecture de la licence : {e}"
        else:
            content = "Fichier de licence non trouvé (LICENSE)."

        textbox.insert("1.0", content)
        textbox.configure(state="disabled")

        ctk.CTkButton(
            self.license_window,
            text="Fermer",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#334155",
            hover_color="#475569",
            command=self.license_window.destroy,
            width=120,
            height=34,
            corner_radius=8,
        ).pack(pady=(0, 16))