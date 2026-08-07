import customtkinter as ctk
from PIL import Image
from config import LOGO_PATH

# Importation des vues / formulaires
from .form.enrollment.registration_form import RegistrationForm
from .form.monthly_payement.month_payment_form import MonthlyPaymentFormFrame
from .form.students_list.student_list_form import StudentListFormFrame
from .form.payment_stat.payment_stat_form import PaymentStatsFormFrame
from .form.manage_academique_year.academic_year_form import AcademicYearFormFrame
from .form.student_archives.student_archive_form import StudentArchiveForm
from interfaces.form.admin import AdminAuthFrame, AdminDashboardFrame


class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURATION FENÊTRE PRINCIPALE ---
        self.title("Système de Gestion Scolaire - ISPSL")
        self.geometry("1180x800")
        self.minsize(1000, 700)

        # Palette de couleurs globale
        self.COLOR_BG = "#0F172A"
        self.COLOR_CARD_BG = "#1E293B"
        self.COLOR_CARD_HOVER = "#334155"
        self.COLOR_PRIMARY = "#3B82F6"
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

        # Navigation et Dashboards
        self._build_top_bar()
        self._build_main_dashboard()

        # Écrans Admin (isolés)
        self.admin_auth_frame = AdminAuthFrame(self.container, self)
        self.admin_dashboard_frame = AdminDashboardFrame(self.container, self)

        # Conteneur pour afficher les vues formulaires
        self.page_container = ctk.CTkFrame(self.container, fg_color="transparent")

        # Initialisation des vues applicatives
        self.views["registration"] = RegistrationForm(self.page_container)
        self.views["payment"] = MonthlyPaymentFormFrame(self.page_container)
        self.views["student_list"] = StudentListFormFrame(self.page_container)
        self.views["payment_stats"] = PaymentStatsFormFrame(self.page_container)
        self.views["academic_year"] = AcademicYearFormFrame(self.page_container)
        self.views["student_archive"] = StudentArchiveForm(self.page_container)

        # Démarrage sur le Dashboard Principal
        self.show_dashboard()

    # ---------- BARRE DE NAVIGATION SUPÉRIEURE ----------
    def _build_top_bar(self):
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

    # ---------- DASHBOARD PRINCIPAL ----------
    def _build_main_dashboard(self):
        self.main_dashboard_frame = ctk.CTkFrame(self.container, fg_color="transparent")

        header_frame = ctk.CTkFrame(self.main_dashboard_frame, fg_color="transparent")
        header_frame.pack(pady=(10, 5))

        try:
            pil_img = Image.open(LOGO_PATH)
            # Taille ajustée à 100x100 pour libérer de l'espace vertical
            self.logo_image = ctk.CTkImage(
                light_image=pil_img, dark_image=pil_img, size=(100, 100)
            )
            ctk.CTkLabel(header_frame, image=self.logo_image, text="").pack(pady=10)
        except Exception:
            ctk.CTkLabel(header_frame, text="🎓", font=ctk.CTkFont(size=36)).pack(
                pady=(0, 2)
            )

        ctk.CTkLabel(
            header_frame,
            text="INSTITUT SUPÉRIEUR POLYTECHNIQUE\nSAINTE LUCIE D'OYO",
            font=ctk.CTkFont(family="Helvetica", size=17, weight="bold"),
            text_color=self.COLOR_PRIMARY,
            justify="center",
        ).pack(pady=(0, 2))

        ctk.CTkLabel(
            header_frame,
            text="Système Intégré de Gestion Scolaire",
            font=ctk.CTkFont(family="Helvetica", size=12),
            text_color=self.COLOR_SUBTEXT,
        ).pack()

        cards_grid = ctk.CTkFrame(self.main_dashboard_frame, fg_color="transparent")
        cards_grid.pack(expand=True, pady=(5, 10))

        # 1. Inscriptions
        card_reg = self.create_card(
            master=cards_grid,
            icon="📝",
            title="Inscriptions & Réinscriptions",
            description="Création de nouveaux dossiers\net renouvellement annuel d'élèves.",
            command=lambda: self.show_page(
                "registration", "Inscriptions & Réinscriptions"
            ),
        )
        card_reg.grid(row=0, column=0, padx=10, pady=8)

        # 2. Paiements Mensuels
        card_pay = self.create_card(
            master=cards_grid,
            icon="💳",
            title="Paiements Mensuels",
            description="Recherche d'étudiant, encaissement\ndes mensualités et reçus.",
            command=lambda: self.show_page("payment", "Gestion des Paiements Mensuels"),
        )
        card_pay.grid(row=0, column=1, padx=10, pady=8)

        # 3. Liste des Élèves
        card_students = self.create_card(
            master=cards_grid,
            icon="📋",
            title="Liste des Étudiants",
            description="Consultation, recherche et filtrage\ndes étudiants inscrits par classe.",
            command=lambda: self.show_page("student_list", "Liste des Élèves"),
        )
        card_students.grid(row=0, column=2, padx=10, pady=8)

        # 4. Suivi des Paiements
        card_stats = self.create_card(
            master=cards_grid,
            icon="📊",
            title="Suivi des Paiements",
            description="État des règlements par mois, rapports\ndes impayés et impression.",
            command=lambda: self.show_page("payment_stats", "Suivi des Paiements"),
        )
        card_stats.grid(row=1, column=0, padx=10, pady=8)

        # 5. Archives Étudiants
        card_archive = self.create_card(
            master=cards_grid,
            icon="📁",
            title="Archives Étudiants",
            description="Consultation et recherche des étudiants\ndes années scolaires antérieures.",
            command=lambda: self.show_page("student_archive", "Archives Étudiants"),
        )
        card_archive.grid(row=1, column=1, padx=10, pady=8)

        # 6. Tuile Administration
        card_admin = self.create_card(
            master=cards_grid,
            icon="🔒",
            title="Administration",
            description="Accès restreint pour la gestion\nscolaire globale et paramètres.",
            command=self.open_admin_flow,
        )
        card_admin.grid(row=1, column=2, padx=10, pady=8)

    # ---------- REUTILISATION : CARTE DU DASHBOARD ----------
    def create_card(self, master, icon, title, description, command):
        """Génère une tuile uniforme et cliquable."""
        card = ctk.CTkFrame(
            master,
            width=280,
            height=175,  # Hauteur réduite pour laisser respirer l'interface
            fg_color=self.COLOR_CARD_BG,
            corner_radius=14,
            border_width=1,
            border_color="#334155",
        )
        card.pack_propagate(False)

        card.bind("<Button-1>", lambda e: command())

        lbl_icon = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=32),
            anchor="center",
            justify="center",
        )
        lbl_icon.pack(fill="x", pady=(12, 4))
        lbl_icon.bind("<Button-1>", lambda e: command())

        lbl_title = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=self.COLOR_TEXT,
        )
        lbl_title.pack(pady=(0, 4))
        lbl_title.bind("<Button-1>", lambda e: command())

        lbl_desc = ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=10),
            text_color=self.COLOR_SUBTEXT,
            justify="center",
        )
        lbl_desc.pack(padx=10, pady=(0, 8))
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

    # ---------- REUTILISATION : CARTE DU DASHBOARD ----------
    def create_card(self, master, icon, title, description, command):
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

        lbl_icon = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=36),
            anchor="center",
            justify="center",
        )
        lbl_icon.pack(fill="x", pady=(20, 8))
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

    # ---------- GESTION DES FLUX DE NAVIGATION ----------
    def open_admin_flow(self):
        if self.is_admin_authenticated:
            self.show_admin_dashboard()
        else:
            self.show_admin_auth()

    def _hide_all_containers(self):
        self.top_bar.pack_forget()
        self.page_container.pack_forget()
        self.main_dashboard_frame.pack_forget()
        self.admin_auth_frame.pack_forget()
        self.admin_dashboard_frame.pack_forget()

        for view in self.views.values():
            view.pack_forget()

    def show_dashboard(self):
        self._hide_all_containers()
        self.main_dashboard_frame.pack(fill="both", expand=True)

    def show_admin_auth(self):
        self._hide_all_containers()
        self.admin_auth_frame.pack(fill="both", expand=True)
        self.admin_auth_frame.focus_input()

    def show_admin_dashboard(self):
        self._hide_all_containers()
        self.admin_dashboard_frame.pack(fill="both", expand=True)

    def show_page(self, page_key: str, title: str, from_admin: bool = False):
        self._hide_all_containers()

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
