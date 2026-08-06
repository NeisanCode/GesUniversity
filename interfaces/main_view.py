import customtkinter as ctk
from .form.enrollment.registration_form import RegistrationForm
from .form.monthly_payement.month_payment_form import MonthlyPaymentFormFrame


class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURATION DE LA FENÊTRE PRINCIPALE ---
        self.title("Système de Gestion Scolaire - ISPSL")
        self.geometry("1100x750")
        self.minsize(950, 650)

        # Palette de couleurs (Sombre & Moderne)
        self.COLOR_BG = "#0F172A"  # Fond principal (Slate 900)
        self.COLOR_CARD_BG = "#1E293B"  # Fond des cartes (Slate 800)
        self.COLOR_CARD_HOVER = "#334155"  # Survol des cartes (Slate 700)
        self.COLOR_PRIMARY = "#3B82F6"  # Accent bleu (Blue 500)
        self.COLOR_TEXT = "#F8FAFC"  # Texte principal
        self.COLOR_SUBTEXT = "#94A3B8"  # Texte secondaire

        self.configure(fg_color=self.COLOR_BG)

        # Container principal accueillant les différentes vues
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Dictionnaire pour garder les instances des sous-pages
        self.views = {}

        # 1. Construction du Tableau de bord (Menu de cartes)
        self._build_dashboard()

        # 2. Construction de la barre d'en-tête (pour la navigation retour)
        self._build_top_bar()

        # 3. Préparation du conteneur des vues (Inscriptions / Paiements)
        self.page_container = ctk.CTkFrame(self.container, fg_color="transparent")

        # Initialisation des formulaires
        self.views["registration"] = RegistrationForm(self.page_container)
        self.views["payment"] = MonthlyPaymentFormFrame(self.page_container)

        # Affichage du dashboard au démarrage
        self.show_dashboard()

    # ---------- TABLEAU DE BORD (BOÎTES / CARTES) ----------
    def _build_dashboard(self):
        """Crée l'écran d'accueil avec l'en-tête de l'école et les cartes de navigation."""
        self.dashboard_frame = ctk.CTkFrame(self.container, fg_color="transparent")

        # En-tête / Nom de l'établissement
        header_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        header_frame.pack(pady=(40, 30))

        # Sigle / Logo textuel
        ctk.CTkLabel(
            header_frame,
            text="🎓",
            font=ctk.CTkFont(size=48),
        ).pack(pady=(0, 10))

        # Nom officiel de l'école
        ctk.CTkLabel(
            header_frame,
            text="INSTITUT SUPÉRIEUR POLYTECHNIQUE\nSAINTE LUCIE D'OYO",
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
            text_color=self.COLOR_PRIMARY,
            justify="center",
        ).pack(pady=(0, 8))

        # Sous-titre / Message de bienvenue
        ctk.CTkLabel(
            header_frame,
            text="Système Intégré de Gestion des Inscriptions & Paiements",
            font=ctk.CTkFont(family="Helvetica", size=13),
            text_color=self.COLOR_SUBTEXT,
        ).pack()

        # Grille pour afficher les cartes/boîtes côte à côte
        cards_grid = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        cards_grid.pack(expand=True, pady=(0, 20))

        # --- CARTE 1 : INSCRIPTION & RÉINSCRIPTION ---
        card_reg = self._create_nav_card(
            master=cards_grid,
            icon="📝",
            title="Inscriptions & Réinscriptions",
            description="Gérer la création de nouveaux dossiers d'élèves\net le renouvellement d'inscriptions.",
            command=lambda: self.show_page("registration"),
        )
        card_reg.pack(side="left", padx=20, pady=10)

        # --- CARTE 2 : PAIEMENT MENSUEL ---
        card_pay = self._create_nav_card(
            master=cards_grid,
            icon="💳",
            title="Paiements Mensuels",
            description="Rechercher un étudiant, encaisser les mensualités\net imprimer les reçus de paiement.",
            command=lambda: self.show_page("payment"),
        )
        card_pay.pack(side="left", padx=20, pady=10)

    def _create_nav_card(self, master, icon, title, description, command):
        """Crée un composant de type 'Carte cliquable' avec effet de survol."""
        card = ctk.CTkFrame(
            master,
            width=330,
            height=250,
            fg_color=self.COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color="#334155",
        )
        card.pack_propagate(False)

        # Rendre toute la surface de la carte cliquable au clic
        card.bind("<Button-1>", lambda e: command())

        # Icône illustrative
        lbl_icon = ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=40))
        lbl_icon.pack(pady=(25, 10))
        lbl_icon.bind("<Button-1>", lambda e: command())

        # Titre de la carte
        lbl_title = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color=self.COLOR_TEXT,
        )
        lbl_title.pack(pady=(0, 8))
        lbl_title.bind("<Button-1>", lambda e: command())

        # Description
        lbl_desc = ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color=self.COLOR_SUBTEXT,
            justify="center",
        )
        lbl_desc.pack(padx=15, pady=(0, 15))
        lbl_desc.bind("<Button-1>", lambda e: command())

        # Effets de survol (Hover effect)
        def on_enter(e):
            card.configure(
                fg_color=self.COLOR_CARD_HOVER, border_color=self.COLOR_PRIMARY
            )
            card.configure(cursor="hand2")

        def on_leave(e):
            card.configure(fg_color=self.COLOR_CARD_BG, border_color="#334155")
            card.configure(cursor="")

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        return card

    # ---------- BARRE D'EN-TÊTE / RETOUR ----------
    def _build_top_bar(self):
        """Crée la barre supérieure affichant le bouton retour et le nom court de l'école."""
        self.top_bar = ctk.CTkFrame(
            self.container, height=50, fg_color="#1E293B", corner_radius=0
        )

        # Bouton Retour au Menu
        self.btn_back = ctk.CTkButton(
            self.top_bar,
            text="←  Menu Principal",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="transparent",
            text_color=self.COLOR_TEXT,
            hover_color="#334155",
            width=140,
            height=36,
            command=self.show_dashboard,
        )
        self.btn_back.pack(side="left", padx=15, pady=7)

        # Rappel du nom de l'institut dans la barre supérieure
        ctk.CTkLabel(
            self.top_bar,
            text="ISPSL D'OYO",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#64748B",
        ).pack(side="left", padx=10)

        # Nom du module actif (Label dynamique)
        self.lbl_current_module = ctk.CTkLabel(
            self.top_bar,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.COLOR_PRIMARY,
        )
        self.lbl_current_module.pack(side="right", padx=20)

    # ---------- LOGIQUE DE NAVIGATION ----------
    def show_dashboard(self):
        """Masque les pages de travail et affiche le menu à cartes."""
        self.top_bar.pack_forget()
        self.page_container.pack_forget()
        for view in self.views.values():
            view.pack_forget()

        self.dashboard_frame.pack(fill="both", expand=True)

    def show_page(self, page_key: str):
        """Affiche la page sélectionnée et ajoute la barre avec le bouton retour."""
        self.dashboard_frame.pack_forget()

        # Titres affichés dans la barre supérieure
        titles = {
            "registration": "Gestion des Inscriptions",
            "payment": "Gestion des Paiements Mensuels",
        }
        self.lbl_current_module.configure(text=titles.get(page_key, ""))

        # Affichage de la barre supérieure et du conteneur principal
        self.top_bar.pack(fill="x", side="top")
        self.page_container.pack(fill="both", expand=True)

        # Affichage du sous-formulaire demandé
        for key, view in self.views.items():
            if key == page_key:
                view.pack(fill="both", expand=True)
            else:
                view.pack_forget()


if __name__ == "__main__":
    app = MainView()
    app.mainloop()
