import customtkinter as ctk
from .enrollment_form import EnrollmentFormFrame
from .reenrollment_form import ReEnrollmentFormFrame


class RegistrationForm(ctk.CTkFrame):
    """Frame conteneur regroupant le formulaire d'inscription et de réinscription dans un système d'onglets."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, fg_color="#121927", *args, **kwargs)

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
            corner_radius=8,
            height=45,
        )

        # Étendre la barre d'onglets sur toute la largeur disponible
        self.tabview._segmented_button.grid(sticky="ew", padx=10, pady=10)
        self.tabview._segmented_button.grid_columnconfigure(0, weight=1)
        self.tabview._segmented_button.grid_columnconfigure(1, weight=1)

        # Création des onglets
        tab_inscription = self.tabview.add("  NOUVELLE INSCRIPTION  ")
        tab_reinscription = self.tabview.add("  RÉINSCRIPTION  ")

        # --- EMBARQUEMENT DES FORMULAIRES ---
        self.form_inscription = EnrollmentFormFrame(tab_inscription)
        self.form_inscription.pack(fill="both", expand=True)

        self.form_reinscription = ReEnrollmentFormFrame(tab_reinscription)
        self.form_reinscription.pack(fill="both", expand=True)