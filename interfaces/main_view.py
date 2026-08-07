import customtkinter as ctk
from tkinter import messagebox

# Importation des 5 vues / formulaires
from .form.enrollment.registration_form import RegistrationForm
from .form.monthly_payement.month_payment_form import MonthlyPaymentFormFrame
from .form.student_list.student_list_form import StudentListFormFrame
from .form.payment_stat.payment_stat_form import PaymentStatsFormFrame
from .form.manage_academique_year.academic_year_form import AcademicYearFormFrame


class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURATION FENÊTRE PRINCIPALE ---
        self.title("Système de Gestion Scolaire - ISPSL")
        self.geometry("1180x800")
        self.minsize(1000, 700)

        # Palette de couleurs globale
        self.COLOR_BG = "#0F172A"  # Slate 900
        self.COLOR_CARD_BG = "#1E293B"  # Slate 800
        self.COLOR_CARD_HOVER = "#334155"  # Slate 700
        self.COLOR_PRIMARY = "#3B82F6"  # Blue 500
        self.COLOR_TEXT = "#F8FAFC"
        self.COLOR_SUBTEXT = "#94A3B8"

        self.configure(fg_color=self.COLOR_BG)

        # Identifiants de connexion Admin
        self.ADMIN_USERNAME = "admin"
        self.ADMIN_PASSWORD = "admin123"
        self.is_admin_authenticated = False

        # Conteneur racine
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.views = {}

        # Construction des composants de navigation et écrans principaux
        self._build_top_bar()
        self._build_main_dashboard()
        self._build_admin_auth_page()
        self._build_admin_dashboard()

        # Conteneur pour afficher les 5 vues formulaires
        self.page_container = ctk.CTkFrame(self.container, fg_color="transparent")

        # Initialisation des vues
        self.views["registration"] = RegistrationForm(self.page_container)
        self.views["payment"] = MonthlyPaymentFormFrame(self.page_container)
        self.views["student_list"] = StudentListFormFrame(self.page_container)
        self.views["payment_stats"] = PaymentStatsFormFrame(self.page_container)
        self.views["academic_year"] = AcademicYearFormFrame(self.page_container)

        # Démarrage sur le Dashboard Principal
        self.show_dashboard()

    # ---------- BARRE DE NAVIGATION SUPÉRIEURE ----------
    def _build_top_bar(self):
        """Barre d'en-tête affichée lors de la consultation des formulaires."""
        self.top_bar = ctk.CTkFrame(
            self.container, height=50, fg_color="#1E293B", corner_radius=0
        )

        self.btn_back = ctk.CTkButton(
            self.top_bar,
            text="← Menu Principal",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="transparent",
            text_color=self.COLOR_TEXT,
            hover_color="#334155",
            width=140,
            height=36,
            command=self.show_dashboard,
        )
        self.btn_back.pack(side="left", padx=15, pady=7)

        ctk.CTkLabel(
            self.top_bar,
            text="ISPSL D'OYO",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#64748B",
        ).pack(side="left", padx=10)

        self.lbl_current_module = ctk.CTkLabel(
            self.top_bar,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.COLOR_PRIMARY,
        )
        self.lbl_current_module.pack(side="right", padx=20)

    # ---------- 1. DASHBOARD PRINCIPAL ----------
    def _build_main_dashboard(self):
        """Dashboard général (sans l'année académique, avec bouton Admin)."""
        self.main_dashboard_frame = ctk.CTkFrame(self.container, fg_color="transparent")

        header_frame = ctk.CTkFrame(self.main_dashboard_frame, fg_color="transparent")
        header_frame.pack(pady=(30, 20))

        ctk.CTkLabel(header_frame, text="🎓", font=ctk.CTkFont(size=44)).pack(
            pady=(0, 5)
        )

        ctk.CTkLabel(
            header_frame,
            text="INSTITUT SUPÉRIEUR POLYTECHNIQUE\nSAINTE LUCIE D'OYO",
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
            text_color=self.COLOR_PRIMARY,
            justify="center",
        ).pack(pady=(0, 6))

        ctk.CTkLabel(
            header_frame,
            text="Système Intégré de Gestion Scolaire",
            font=ctk.CTkFont(family="Helvetica", size=13),
            text_color=self.COLOR_SUBTEXT,
        ).pack()

        cards_grid = ctk.CTkFrame(self.main_dashboard_frame, fg_color="transparent")
        cards_grid.pack(expand=True, pady=(0, 20))

        # 1. Inscriptions
        card_reg = self._create_card(
            master=cards_grid,
            icon="📝",
            title="Inscriptions & Réinscriptions",
            description="Création de nouveaux dossiers\net renouvellement annuel d'élèves.",
            command=lambda: self.show_page(
                "registration", "Inscriptions & Réinscriptions"
            ),
        )
        card_reg.grid(row=0, column=0, padx=15, pady=15)

        # 2. Paiements Mensuels
        card_pay = self._create_card(
            master=cards_grid,
            icon="💳",
            title="Paiements Mensuels",
            description="Recherche d'étudiant, encaissement\ndes mensualités et reçus.",
            command=lambda: self.show_page("payment", "Gestion des Paiements Mensuels"),
        )
        card_pay.grid(row=0, column=1, padx=15, pady=15)

        # 3. Liste des Élèves
        card_students = self._create_card(
            master=cards_grid,
            icon="📋",
            title="Liste des Élèves",
            description="Consultation, recherche et filtrage\ndes étudiants inscrits par classe.",
            command=lambda: self.show_page("student_list", "Liste des Élèves"),
        )
        card_students.grid(row=1, column=0, padx=15, pady=15)

        # 4. Suivi des Paiements
        card_stats = self._create_card(
            master=cards_grid,
            icon="📊",
            title="Suivi des Paiements",
            description="État des règlements par mois, rapports\ndes impayés et impression.",
            command=lambda: self.show_page("payment_stats", "Suivi des Paiements"),
        )
        card_stats.grid(row=1, column=1, padx=15, pady=15)

        # 5. Tuile Administration (Redirige vers la page d'authentification)
        card_admin = self._create_card(
            master=cards_grid,
            icon="🛡️",
            title="Administration",
            description="Accès restreint pour la gestion\nscolaire globale et paramètres.",
            command=self.open_admin_flow,
        )
        card_admin.grid(row=0, column=2, rowspan=2, padx=15, pady=15)

    # ---------- 2. PAGE D'AUTHENTIFICATION ADMIN ----------
    def _build_admin_auth_page(self):
        """Page intermédiaire de connexion demandant Nom d'utilisateur et Mot de passe."""
        self.admin_auth_frame = ctk.CTkFrame(self.container, fg_color="transparent")

        # Carte centrale de connexion
        auth_card = ctk.CTkFrame(
            self.admin_auth_frame,
            width=420,
            fg_color=self.COLOR_CARD_BG,
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
            text_color=self.COLOR_TEXT,
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            auth_card,
            text="Veuillez saisir vos identifiants pour continuer",
            font=ctk.CTkFont(size=12),
            text_color=self.COLOR_SUBTEXT,
        ).pack(pady=(0, 25))

        # Champ Nom d'utilisateur
        lbl_user = ctk.CTkLabel(
            auth_card,
            text="Nom d'utilisateur",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.COLOR_TEXT,
            anchor="w",
        )
        lbl_user.pack(fill="x", padx=40, pady=(0, 5))

        self.entry_username = ctk.CTkEntry(
            auth_card,
            placeholder_text="Entrez votre nom...",
            height=40,
            fg_color="#0F172A",
            border_color="#334155",
            text_color=self.COLOR_TEXT,
        )
        self.entry_username.pack(fill="x", padx=40, pady=(0, 15))

        # Champ Mot de Passe
        lbl_pwd = ctk.CTkLabel(
            auth_card,
            text="Mot de passe",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.COLOR_TEXT,
            anchor="w",
        )
        lbl_pwd.pack(fill="x", padx=40, pady=(0, 5))

        self.entry_password = ctk.CTkEntry(
            auth_card,
            show="•",
            placeholder_text="Entrez votre mot de passe...",
            height=40,
            fg_color="#0F172A",
            border_color="#334155",
            text_color=self.COLOR_TEXT,
        )
        self.entry_password.pack(fill="x", padx=40, pady=(0, 20))
        self.entry_password.bind("<Return>", lambda e: self._handle_admin_login())

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
            command=self.show_dashboard,
        ).pack(side="left")

        ctk.CTkButton(
            btn_box,
            text="Se connecter",
            fg_color=self.COLOR_PRIMARY,    
            hover_color="#2563EB",   
            height=38,
            width=180,
            font=ctk.CTkFont(weight="bold"),
            command=self._handle_admin_login,
        ).pack(side="right", padx=(10, 0))  # Marge de 10px à gauche pour séparer les deux boutons

    # ---------- 3. DASHBOARD ADMIN ----------
    def _build_admin_dashboard(self):
        """Dashboard Administration débloqué (contient l'Année Académique)."""
        self.admin_dashboard_frame = ctk.CTkFrame(
            self.container, fg_color="transparent"
        )

        header_frame = ctk.CTkFrame(self.admin_dashboard_frame, fg_color="transparent")
        header_frame.pack(pady=(40, 30))

        ctk.CTkLabel(header_frame, text="🛡️", font=ctk.CTkFont(size=48)).pack(
            pady=(0, 10)
        )

        ctk.CTkLabel(
            header_frame,
            text="PANNEAU D'ADMINISTRATION",
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
            text_color="#F59E0B",  # Ambre
            justify="center",
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            header_frame,
            text="INSTITUT SUPÉRIEUR POLYTECHNIQUE SAINTE LUCIE D'OYO",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            text_color=self.COLOR_SUBTEXT,
        ).pack()

        cards_grid = ctk.CTkFrame(self.admin_dashboard_frame, fg_color="transparent")
        cards_grid.pack(expand=True, pady=(0, 20))

        # --- Tuile unique dans l'Espace Admin : Année Académique ---
        card_year = self._create_card(
            master=cards_grid,
            icon="📅",
            title="Année Académique",
            description="Clôturer l'année active, configurer\nla nouvelle et gérer la session.",
            command=lambda: self.show_page(
                "academic_year",
                "Administration - Année Académique",
                from_admin=True,
            ),
        )
        card_year.pack(side="left", padx=20, pady=10)

        # Bouton Retour au Dashboard général
        ctk.CTkButton(
            self.admin_dashboard_frame,
            text="← Quitter l'Administration",
            fg_color="#DC2626",      # Rouge vif (Red 600)
            hover_color="#B91C1C",   # Rouge plus foncé au survol (Red 700)
            text_color=self.COLOR_TEXT,
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.show_dashboard,
        ).pack(pady=(0, 30))

    # ---------- REUTILISATION : CARTE DU DASHBOARD ----------
    def _create_card(self, master, icon, title, description, command):
        """Génère une tuile uniforme et cliquable."""
        card = ctk.CTkFrame(
            master,
            width=290,
            height=200,
            fg_color=self.COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color="#334155",
        )
        card.pack_propagate(False)

        card.bind("<Button-1>", lambda e: command())

        lbl_icon = ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=36))
        lbl_icon.pack(pady=(20, 8))
        lbl_icon.bind("<Button-1>", lambda e: command())

        lbl_title = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(family="Helvetica", size=15, weight="bold"),
            text_color=self.COLOR_TEXT,
        )
        lbl_title.pack(pady=(0, 6))
        lbl_title.bind("<Button-1>", lambda e: command())

        lbl_desc = ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=11),
            text_color=self.COLOR_SUBTEXT,
            justify="center",
        )
        lbl_desc.pack(padx=12, pady=(0, 12))
        lbl_desc.bind("<Button-1>", lambda e: command())

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

    # ---------- LOGIQUE DE VALIDATION ADMIN ----------
    def open_admin_flow(self):
        """Redirige vers le Dashboard Admin si déjà connecté, sinon vers la page de login."""
        if self.is_admin_authenticated:
            self.show_admin_dashboard()
        else:
            self.show_admin_auth()

    def _handle_admin_login(self):
        """Vérifie le Nom et le Mot de passe."""
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        if username == self.ADMIN_USERNAME and password == self.ADMIN_PASSWORD:
            self.is_admin_authenticated = True
            # Vider les champs
            self.entry_username.delete(0, "end")
            self.entry_password.delete(0, "end")
            self.show_admin_dashboard()
        else:
            messagebox.showerror(
                "Échec d'authentification",
                "Nom d'utilisateur ou mot de passe incorrect.",
            )

    # ---------- GESTION DES AFFICHAGES / NAVIGATION ----------
    def _hide_all_containers(self):
        """Masque l'intégralité des conteneurs pour permettre une bascule propre."""
        self.top_bar.pack_forget()
        self.page_container.pack_forget()
        self.main_dashboard_frame.pack_forget()
        self.admin_auth_frame.pack_forget()
        self.admin_dashboard_frame.pack_forget()

        for view in self.views.values():
            view.pack_forget()

    def show_dashboard(self):
        """Affiche le menu principal."""
        self._hide_all_containers()
        self.main_dashboard_frame.pack(fill="both", expand=True)

    def show_admin_auth(self):
        """Affiche la page de saisie du nom et du mot de passe."""
        self._hide_all_containers()
        self.admin_auth_frame.pack(fill="both", expand=True)
        self.entry_username.focus_set()

    def show_admin_dashboard(self):
        """Affiche l'Espace Admin avec l'Année Académique."""
        self._hide_all_containers()
        self.admin_dashboard_frame.pack(fill="both", expand=True)

    def show_page(self, page_key: str, title: str, from_admin: bool = False):
        """Affiche l'un des 5 formulaires applicatifs."""
        self._hide_all_containers()

        # Configuration du bouton de retour selon l'origine
        if from_admin:
            self.btn_back.configure(
                text="← Menu Admin", command=self.show_admin_dashboard
            )
        else:
            self.btn_back.configure(
                text="← Menu Principal", command=self.show_dashboard
            )

        self.lbl_current_module.configure(text=title)
        self.top_bar.pack(fill="x", side="top")
        self.page_container.pack(fill="both", expand=True)

        for key, view in self.views.items():
            if key == page_key:
                view.pack(fill="both", expand=True)
            else:
                view.pack_forget()


if __name__ == "__main__":
    app = MainView()
    app.mainloop()
