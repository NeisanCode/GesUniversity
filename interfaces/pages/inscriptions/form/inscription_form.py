import customtkinter as ctk
from controllers import InscriptionController
from ..widgets.datepicker import DatePicker
from models import PaymentMethod


class EnrollmentFormFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.controller = InscriptionController(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.font_title = ("Helvetica", 14, "bold")
        self.font_label = ("Helvetica", 12, "bold")
        self.font_entry = ("Helvetica", 12)

        # Construction de la page
        self._create_left_column()
        self._create_right_column()

        # Chargement des données dynamiques depuis la BDD via le Contrôleur !
        self.controller.charger_options_initiales()

    def _create_left_column(self):
        col_left = ctk.CTkFrame(self, fg_color="transparent")
        col_left.grid(row=0, column=0, sticky="nsew", padx=20, pady=15)

        self.create_title(col_left, "COORDONNÉES DE L'ÉTUDIANT")
        self.entry_nom = self.create_entry(col_left, "Nom :", "Saisir le nom")
        self.entry_prenom = self.create_entry(col_left, "Prénom :", "Saisir le prénom")
        # Remplacement du champ date par le widget personnalisé
        self.date_picker = self.create_date_picker(col_left, "Date de naissance :")
        self.entry_email = self.create_entry(
            col_left, "Adresse Email :", "exemple@domaine.com"
        )
        self.entry_adresse = self.create_entry(
            col_left, "Adresse Physique :", "Adresse résidentielle"
        )

    def _create_right_column(self):
        col_right = ctk.CTkFrame(self, fg_color="transparent")
        col_right.grid(row=0, column=1, sticky="nsew", padx=20, pady=15)

        self.create_title(col_right, "ORIENTATION & PAIEMENT")
        self.combo_annee = self.create_option_menu(
            col_right, "Année Académique :", ["Sélectionner..."]
        )
        self.combo_filiere = self.create_option_menu(
            col_right, "Filière d'Études :", ["Sélectionner..."]
        )
        self.combo_niveau = self.create_option_menu(
            col_right, "Niveau d'Étude :", ["Sélectionner..."]
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
        ctk.CTkLabel(
            frame_frais,
            text="Montant des frais d'inscription : -- FCFA",
            font=("Helvetica", 11, "bold"),
            text_color="#15803d",
        ).pack(expand=True)

        ctk.CTkButton(
            col_right,
            text="VALIDER L'INSCRIPTION & GÉNÉRER REÇU",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="white",
            height=45,
            corner_radius=8,
            font=("Helvetica", 12, "bold"),
            command=self.controller.traiter_inscription,
        ).pack(fill="x", pady=(10, 0))

    # Utilitaires
    def create_title(self, parent, text):
        ctk.CTkLabel(
            parent, text=text, font=self.font_title, text_color="#3b82f6", anchor="w"
        ).pack(fill="x", pady=(0, 12))

    def create_entry(self, parent, label_text, placeholder):
        ctk.CTkLabel(
            parent,
            text=label_text,
            font=self.font_label,
            text_color="#d1d5db",
            anchor="w",
        ).pack(fill="x", pady=(0, 2))
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            placeholder_text_color="#6b7280",
            fg_color="#111827",
            border_color="#2b3544",
            text_color="#e5e7eb",
            height=36,
            corner_radius=6,
            font=self.font_entry,
        )
        entry.pack(fill="x", pady=(0, 10))
        return entry

    def create_option_menu(self, parent, label_text, values):
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
        )
        menu.pack(fill="x", pady=(0, 10))
        return menu

    def create_date_picker(self, parent, label_text):
        """Crée un widget DatePicker personnalisé"""
        picker = DatePicker(parent, label_text, placeholder="AAAA-MM-JJ")
        picker.pack(fill="x", pady=(0, 10))  # ← ajoutez cette ligne
        return picker
