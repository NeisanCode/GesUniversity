import customtkinter as ctk
from .form.enrollment_form import EnrollmentFormFrame
from .form.reenrollment_form import ReEnrollmentFormFrame

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class InscriptionPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Système de Gestion Scolaire - Inscriptions & Réinscriptions")
        self.geometry("1150x760")
        self.configure(fg_color="#121927")

        # --- GESTION DES ONGLETS (CTkTabview) ---
        self.tabview = ctk.CTkTabview(
            self,
            fg_color="#1a2332",
            segmented_button_fg_color="#111827",
            segmented_button_selected_color="#3b82f6",
            segmented_button_selected_hover_color="#2563eb",
            segmented_button_unselected_color="#1f2937",
            segmented_button_unselected_hover_color="#374151",
            text_color="#e5e7eb",
            corner_radius=12,
        )
        self.tabview.pack(fill="both", expand=True, padx=25, pady=20)

        # Style de la police pour les boutons d'onglets
        self.tabview._segmented_button.configure(
            font=("Helvetica", 13, "bold"),
            corner_radius=8,  # Bords carrés légèrement arrondis
            height=45,  # Plus de hauteur pour un effet plus volumineux
        )

        # Étendre la barre d'onglets sur toute la largeur disponible (3 colonnes pour 2 onglets)
        self.tabview._segmented_button.grid(sticky="ew", padx=10, pady=10)
        self.tabview._segmented_button.grid_columnconfigure(0, weight=1)
        self.tabview._segmented_button.grid_columnconfigure(1, weight=1)

        # Création des onglets
        tab_inscription = self.tabview.add("  NOUVELLE INSCRIPTION  ")
        tab_reinscription = self.tabview.add("  RÉINSCRIPTION  ")

        # --- IMPORTATION ET EMBARQUEMENT DES COMPOSANTS ---
        self.page_inscription = EnrollmentFormFrame(tab_inscription)
        self.page_inscription.pack(fill="both", expand=True)

        self.page_reinscription = ReEnrollmentFormFrame(tab_reinscription)
        self.page_reinscription.pack(fill="both", expand=True)
