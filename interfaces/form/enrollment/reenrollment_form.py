from models.models import PaymentMethod
from controllers import ReEnrollmentController
import customtkinter as ctk


class ReEnrollmentFormFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.font_title = ("Helvetica", 14, "bold")
        self.font_label = ("Helvetica", 12, "bold")
        self.font_entry = ("Helvetica", 12)

        # Construction de la page
        self.create_left_column()
        self.create_right_column()

        self.controller = ReEnrollmentController(self)
        self.search_button.configure(command=self.controller.search_student)
        self.submit_button.configure(command=self.controller.submit_reenrollment)
        self.submit_button.configure(state="disabled")

        self.controller.load_initial_options()

    def create_left_column(self):
        col_left = ctk.CTkFrame(self, fg_color="transparent")
        col_left.grid(row=0, column=0, sticky="nsew", padx=20, pady=15)

        self.create_title(col_left, "RECHERCHE & INFORMATIONS ÉTUDIANT")

        # Recherche Matricule
        ctk.CTkLabel(
            col_left,
            text="Matricule de l'Étudiant :",
            font=self.font_label,
            text_color="#d1d5db",
            anchor="w",
        ).pack(fill="x", pady=(0, 2))
        frame_matricule = ctk.CTkFrame(col_left, fg_color="transparent")
        frame_matricule.pack(fill="x", pady=(0, 10))

        self.entry_matricule = ctk.CTkEntry(
            frame_matricule,
            placeholder_text="Ex: ETU-2024-001",
            placeholder_text_color="#6b7280",
            fg_color="#111827",
            border_color="#2b3544",
            text_color="#e5e7eb",
            height=36,
            corner_radius=6,
            font=self.font_entry,
        )
        self.entry_matricule.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.search_button = ctk.CTkButton(
            frame_matricule,
            text="🔑 Rechercher",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="white",
            height=36,
            width=110,
            corner_radius=6,
            font=("Helvetica", 11, "bold"),
        )
        self.search_button.pack(side="right")

        # Infos désactivées
        self.entry_nom = self.create_disabled_entry(col_left, "Nom :")
        self.entry_prenom = self.create_disabled_entry(col_left, "Prénom :")
        self.entry_dob = self.create_disabled_entry(col_left, "Date de naissance :")
        self.entry_email = self.create_disabled_entry(col_left, "Adresse Email :")
        self.entry_adresse = self.create_disabled_entry(col_left, "Adresse Physique :")

    def create_right_column(self):
        col_right = ctk.CTkFrame(self, fg_color="transparent")
        col_right.grid(row=0, column=1, sticky="nsew", padx=20, pady=15)

        self.create_title(col_right, "NOUVELLE ORIENTATION & PAIEMENT")
        self.combo_annee = self.create_option_menu(
            col_right, "Année Académique :", ["Sélectionner..."]
        )
        self.combo_filiere = self.create_option_menu(
            col_right, "Filière d'Études :", ["Sélectionner..."]
        )
        self.combo_niveau = self.create_option_menu(
            col_right, "Niveau d'Étude Cible :", ["Sélectionner..."]
        )

        modes_paiement = [m.value for m in PaymentMethod]
        self.combo_paiement = self.create_option_menu(
            col_right, "Mode de Paiement :", modes_paiement
        )

        # Bannière Frais
        frame_frais = ctk.CTkFrame(
            col_right,
            fg_color="#f0fdf4",
            corner_radius=8,
            border_color="#bbf7d0",
            border_width=1,
            height=42,
        )
        frame_frais.pack(fill="x", pady=(12, 12))
        frame_frais.pack_propagate(False)
        self.fees_label = ctk.CTkLabel(
            frame_frais,
            text="Frais de réinscription : -- FCFA",
            font=("Helvetica", 11, "bold"),
            text_color="#15803d",
        )
        self.fees_label.pack(expand=True)

        self.submit_button = ctk.CTkButton(
            col_right,
            text="VALIDER LA RÉINSCRIPTION & GÉNÉRER REÇU",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="white",
            height=45,
            corner_radius=8,
            font=("Helvetica", 12, "bold"),
        )
        self.submit_button.pack(fill="x", pady=(10, 0))

    # Utilitaires
    def create_title(self, parent, text):
        ctk.CTkLabel(
            parent, text=text, font=self.font_title, text_color="#3b82f6", anchor="w"
        ).pack(fill="x", pady=(0, 12))

    def create_disabled_entry(self, parent, label_text):
        ctk.CTkLabel(
            parent,
            text=label_text,
            font=self.font_label,
            text_color="#d1d5db",
            anchor="w",
        ).pack(fill="x", pady=(0, 2))
        entry = ctk.CTkEntry(
            parent,
            placeholder_text="Charge automatiquement...",
            placeholder_text_color="#6b7280",
            fg_color="#1f2937",
            border_color="#2b3544",
            text_color="#e5e7eb",
            height=36,
            corner_radius=6,
            font=self.font_entry,
            state="disabled",
        )
        entry.pack(fill="x", pady=(0, 10))
        return entry

    def create_option_menu(self, parent, label_text, values, command=None):
        ctk.CTkLabel(
            parent,
            text=label_text,
            font=self.font_label,
            text_color="#d1d5db",
            anchor="w",
        ).pack(fill="x", pady=(0, 2))
        menu = ctk.CTkOptionMenu(
            parent,
            values=values,
            fg_color="#111827",
            button_color="#2b3544",
            button_hover_color="#374151",
            text_color="#e5e7eb",
            dropdown_fg_color="#1f2937",
            height=36,
            corner_radius=6,
            command=command,
        )
        menu.pack(fill="x", pady=(0, 10))
        return menu

    def set_student_information(self, student):
        self._set_disabled_entry(self.entry_nom, student.last_name)
        self._set_disabled_entry(self.entry_prenom, student.first_name)
        self._set_disabled_entry(
            self.entry_dob, student.date_of_birth.strftime("%Y-%m-%d")
        )
        self._set_disabled_entry(self.entry_email, student.email or "")
        self._set_disabled_entry(self.entry_adresse, student.address or "")

    def clear_student_information(self):
        self._set_disabled_entry(self.entry_nom, "")
        self._set_disabled_entry(self.entry_prenom, "")
        self._set_disabled_entry(self.entry_dob, "")
        self._set_disabled_entry(self.entry_email, "")
        self._set_disabled_entry(self.entry_adresse, "")

    def _set_disabled_entry(self, entry, value):
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, value)
        entry.configure(state="disabled")

    def get_student_matricule(self):
        return self.entry_matricule.get().strip()

    def set_academic_years(self, values):
        if values:
            self.combo_annee.configure(values=tuple(values))
            self.combo_annee.set(values[0])

    def select_default_academic_year(self):
        values = self.combo_annee.cget("values")
        if values:
            self.combo_annee.set(values[0])

    def set_majors(self, values):
        if values:
            self.combo_filiere.configure(values=tuple(values))
            self.combo_filiere.set(values[0])

    def set_levels(self, values):
        if values:
            self.combo_niveau.configure(values=tuple(values))
            self.combo_niveau.set(values[0])

    def set_payment_methods(self, values):
        if values:
            self.combo_paiement.configure(values=values)
            self.combo_paiement.set(values[0])

    def configure_selection_callbacks(
        self, year_command=None, major_command=None, level_command=None
    ):
        if year_command is not None:
            self.combo_annee.configure(command=year_command)
        if major_command is not None:
            self.combo_filiere.configure(command=major_command)
        if level_command is not None:
            self.combo_niveau.configure(command=level_command)

    def get_selected_academic_year(self):
        return self.combo_annee.get().strip()

    def get_selected_major(self):
        return self.combo_filiere.get().strip()

    def get_selected_level(self):
        return self.combo_niveau.get().strip()

    def get_selected_payment_method(self):
        return self.combo_paiement.get().strip()

    def set_fee_amount(self, text):
        self.fees_label.configure(text=text)

    def reset_after_submission(self):
        self.entry_matricule.delete(0, "end")
        self.clear_student_information()
        self.set_fee_amount("Frais de réinscription : -- FCFA")
        self.submit_button.configure(state="disabled")
