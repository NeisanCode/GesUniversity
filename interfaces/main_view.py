import customtkinter as ctk
from .form.enrollment.registration_form import RegistrationForm
from .form.monthly_payement.month_payment_form import MonthlyPaymentFormFrame


class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURATION DE LA FENÊTRE PRINCIPALE ---
        self.title("Système de Gestion Scolaire")
        self.geometry("1100x700")
        self.minsize(950, 600)

        # Palette de couleurs (Thème Dark Moderne)
        self.COLOR_BG = "#0B0F17"
        self.COLOR_SIDEBAR = "#111827"
        self.COLOR_BTN_ACTIVE = "#2563EB"
        self.COLOR_BTN_HOVER = "#1D4ED8"
        self.COLOR_TEXT_PRIMARY = "#F9FAFB"
        self.COLOR_TEXT_MUTED = "#9CA3AF"

        self.configure(fg_color=self.COLOR_BG)

        # Configuration de la grille globale (Sidebar + Frame de contenu)
        self.grid_columnconfigure(0, weight=0)  # Largeur fixe pour la barre latérale
        self.grid_columnconfigure(1, weight=1)  # Le contenu prend le reste de l'espace
        self.grid_rowconfigure(0, weight=1)

        # Stockage des vues chargées
        self.views = {}
        self.nav_buttons = {}

        # Construction des composants
        self._build_sidebar()
        self._build_content_area()

        # Affichage de la vue par défaut (Inscription)
        self._show_view("registration")

    # ---------- COMPOSANTS D'INTERFACE ----------
    def _build_sidebar(self):
        """Crée le menu latéral avec le titre de l'application et la navigation."""
        self.sidebar_frame = ctk.CTkFrame(
            self, width=240, fg_color=self.COLOR_SIDEBAR, corner_radius=0
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(3, weight=1)  # Espacement flexible

        # En-tête / Logo
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="🎓 ACADEMIA",
            font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"),
            text_color=self.COLOR_TEXT_PRIMARY,
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(25, 30), sticky="w")

        # Bouton Navigation 1: Inscriptions
        self.nav_buttons["registration"] = ctk.CTkButton(
            self.sidebar_frame,
            text="📝  Inscriptions",
            anchor="w",
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="transparent",
            text_color=self.COLOR_TEXT_MUTED,
            hover_color="#1F2937",
            command=lambda: self._show_view("registration"),
        )
        self.nav_buttons["registration"].grid(
            row=1, column=0, padx=12, pady=4, sticky="ew"
        )

        # Bouton Navigation 2: Paiements Mensuels
        self.nav_buttons["payment"] = ctk.CTkButton(
            self.sidebar_frame,
            text="💳  Paiements Mensuels",
            anchor="w",
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="transparent",
            text_color=self.COLOR_TEXT_MUTED,
            hover_color="#1F2937",
            command=lambda: self._show_view("payment"),
        )
        self.nav_buttons["payment"].grid(row=2, column=0, padx=12, pady=4, sticky="ew")

        # Pied de la barre latérale (Badge de version)
        self.version_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="v1.0.0",
            font=ctk.CTkFont(size=11),
            text_color="gray50",
        )
        self.version_label.grid(row=4, column=0, padx=20, pady=15, sticky="s")

    def _build_content_area(self):
        """Conteneur principal accueillant dynamiquement les formulaires."""
        self.content_container = ctk.CTkFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.content_container.grid(row=0, column=1, sticky="nsew")

        # Instanciation unique des deux vues
        self.views["registration"] = RegistrationForm(self.content_container)
        self.views["payment"] = MonthlyPaymentFormFrame(self.content_container)

    # ---------- GESTION DE LA NAVIGATION ----------
    def _show_view(self, view_key: str):
        """Affiche le module demandé et met à jour l'état visuel du menu."""
        # 1. Masquer toutes les vues
        for view in self.views.values():
            view.pack_forget()

        # 2. Réinitialiser le style des boutons du menu
        for key, btn in self.nav_buttons.items():
            btn.configure(fg_color="transparent", text_color=self.COLOR_TEXT_MUTED)

        # 3. Afficher la vue ciblée et activer le bouton correspondant
        self.views[view_key].pack(fill="both", expand=True)
        self.nav_buttons[view_key].configure(
            fg_color=self.COLOR_BTN_ACTIVE,
            hover_color=self.COLOR_BTN_HOVER,
            text_color=self.COLOR_TEXT_PRIMARY,
        )


if __name__ == "__main__":
    app = MainView()
    app.mainloop()
