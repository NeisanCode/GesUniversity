import customtkinter as ctk
from controllers import MonthlyPaymentController
from models import Student, Enrollment


class MonthlyPaymentFormFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = MonthlyPaymentController(self)

        # Configuration de la grille (2 colonnes principales)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Construction des colonnes
        self._create_left_column()
        self._create_right_column()

        # Chargement initial des options
        self.controller.load_initial_options()

        # Affichage par défaut (vide)
        self.display_student_info(None, None)
        self.display_schedule([])

    # ---------- CONSTRUCTION DE L'INTERFACE ----------
    def _create_left_column(self):
        """Colonne de gauche : recherche, infos étudiant, tableau des échéances."""
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Titre
        ctk.CTkLabel(
            self.left_frame,
            text="RECHERCHE ÉTUDIANT",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B82F6",
        ).pack(anchor="w", pady=(0, 10))

        # Barre de recherche
        search_box = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        search_box.pack(fill="x", pady=(0, 15))

        self.search_student_id = ctk.CTkEntry(
            search_box,
            placeholder_text="Entrer le Matricule (ex: ETU20260001)...",
            height=40,
        )
        self.search_student_id.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            search_box, text="Rechercher", height=40, command=self._on_search
        ).pack(side="right")

        # Carte d'information (Grille sur 2 colonnes)
        self.info_card = ctk.CTkFrame(self.left_frame, corner_radius=10)
        self.info_card.pack(fill="x", pady=(0, 15), ipadx=10, ipady=10)
        self.info_card.grid_columnconfigure(0, weight=1)
        self.info_card.grid_columnconfigure(1, weight=1)

        # Rangée 0: Étudiant | Niveau
        self.lbl_student_name = ctk.CTkLabel(
            self.info_card,
            text="Étudiant : --",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.lbl_student_name.grid(row=0, column=0, sticky="w", padx=10, pady=4)

        self.lbl_level = ctk.CTkLabel(
            self.info_card,
            text="Niveau : --",
            text_color="gray70",
        )
        self.lbl_level.grid(row=0, column=1, sticky="w", padx=10, pady=4)

        # Rangée 1: Programme | Filière
        self.lbl_program = ctk.CTkLabel(
            self.info_card,
            text="Programme : --",
            text_color="gray70",
        )
        self.lbl_program.grid(row=1, column=0, sticky="w", padx=10, pady=4)

        self.lbl_major = ctk.CTkLabel(
            self.info_card,
            text="Filière : --",
            text_color="gray70",
        )
        self.lbl_major.grid(row=1, column=1, sticky="w", padx=10, pady=4)

        # Rangée 2: Classe | Mensualité
        self.lbl_class_group = ctk.CTkLabel(
            self.info_card,
            text="Classe : --",
            text_color="gray70",
        )
        self.lbl_class_group.grid(row=2, column=0, sticky="w", padx=10, pady=4)

        self.lbl_monthly_fee = ctk.CTkLabel(
            self.info_card,
            text="Mensualité : -- FCFA",
            text_color="#10B981",
            font=ctk.CTkFont(weight="bold"),
        )
        self.lbl_monthly_fee.grid(row=2, column=1, sticky="w", padx=10, pady=4)

        # Rangée 3: Frais Totaux | Reste à Payer
        self.lbl_total_fee = ctk.CTkLabel(
            self.info_card,
            text="Frais Totaux : -- FCFA",
            text_color="#FFFFFF",
            font=ctk.CTkFont(weight="bold"),
        )
        self.lbl_total_fee.grid(row=3, column=0, sticky="w", padx=10, pady=4)

        self.lbl_remaining_balance = ctk.CTkLabel(
            self.info_card,
            text="Reste à Payer : -- FCFA",
            text_color="#EF4444",
            font=ctk.CTkFont(weight="bold"),
        )
        self.lbl_remaining_balance.grid(row=3, column=1, sticky="w", padx=10, pady=4)

        # --- EN-TÊTE DU TABLEAU (4 COLONNES) ---
        header = ctk.CTkFrame(self.left_frame, fg_color="#1E293B", corner_radius=6)
        header.pack(fill="x", pady=(5, 2))
        
        columns = [
            ("Mois", "w", 90),
            ("Montant", "center", 90),
            ("Statut", "center", 90),
            ("Action", "center", 90),
        ]
        
        for text, anchor, width in columns:
            ctk.CTkLabel(
                header,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=width,
                anchor=anchor,
            ).pack(side="left", padx=5, pady=8)

        # Corps du Tableau (déroulant)
        self.scroll_month = ctk.CTkScrollableFrame(
            self.left_frame, height=160, fg_color="#0F172A"
        )
        self.scroll_month.pack(fill="both", expand=True)

    def _create_right_column(self):
        """Colonne de droite : formulaire de paiement."""
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(
            self.right_frame,
            text="NOUVEAU PAIEMENT",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B82F6",
        ).pack(anchor="w", pady=(0, 15))

        # Choix du mois
        ctk.CTkLabel(self.right_frame, text="Mois à régler :").pack(
            anchor="w", pady=(0, 5)
        )
        self.combo_month = ctk.CTkOptionMenu(
            self.right_frame, height=38, command=self._on_month_changed
        )
        self.combo_month.pack(fill="x", pady=(0, 15))

        # Mode de Paiement
        ctk.CTkLabel(self.right_frame, text="Mode de Paiement :").pack(
            anchor="w", pady=(0, 5)
        )
        self.combo_method = ctk.CTkOptionMenu(self.right_frame, height=38)
        self.combo_method.pack(fill="x", pady=(0, 15))

        # Bouton de validation (placé en bas)
        self.btn_submit = ctk.CTkButton(
            self.right_frame,
            text="ENREGISTRER LE PAIEMENT & IMPRIMER REÇU",
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self._on_submit_payment,
        )
        self.btn_submit.pack(fill="x", side="bottom")

    # ---------- MÉTHODES DE MISE À JOUR ----------
    def display_student_info(
        self,
        student: Student,
        enrollment: Enrollment,
        monthly_fee: float = 0.0,
        total_fee: float = 0.0,
        remaining_balance: float = 0.0,
    ):
        """Mets à jour les labels avec les informations de l'étudiant et du cursus."""
        if student and enrollment:
            class_group = enrollment.class_group
            program = class_group.program if class_group else None
            major = program.major if program else None
            level = program.level if program else None

            program_label = f"{major.name} ({level.name})" if major and level else "--"
            self.lbl_student_name.configure(
                text=f"Étudiant : {student.last_name} - {student.first_name}"
            )
            self.lbl_program.configure(text=f"Programme : {program_label}")
            self.lbl_level.configure(text=f"Niveau : {level.name if level else '--'}")
            self.lbl_major.configure(text=f"Filière : {major.name if major else '--'}")
            self.lbl_class_group.configure(
                text=f"Classe : {class_group.name if class_group else '--'}"
            )
            self.lbl_monthly_fee.configure(text=f"Mensualité : {monthly_fee:,.0f} FCFA")
            self.lbl_total_fee.configure(text=f"Frais Totaux : {total_fee:,.0f} FCFA")

            rem_text_color = "#10B981" if remaining_balance <= 0 else "#EF4444"
            rem_prefix = "SOLDÉ (0 FCFA)" if remaining_balance <= 0 else f"{remaining_balance:,.0f} FCFA"

            self.lbl_remaining_balance.configure(
                text=f"Reste à Payer : {rem_prefix}",
                text_color=rem_text_color,
            )
        else:
            self.lbl_student_name.configure(text="Étudiant : --")
            self.lbl_program.configure(text="Programme : --")
            self.lbl_level.configure(text="Niveau : --")
            self.lbl_major.configure(text="Filière : --")
            self.lbl_class_group.configure(text="Classe : --")
            self.lbl_monthly_fee.configure(text="Mensualité : -- FCFA")
            self.lbl_total_fee.configure(text="Frais Totaux : -- FCFA")
            self.lbl_remaining_balance.configure(text="Reste à Payer : -- FCFA", text_color="#EF4444")

    def display_schedule(self, installments):
        """Reconstruit le tableau des mois avec 4 colonnes (Mois | Montant | Statut | Action)."""
        # Nettoyage du conteneur
        for widget in self.scroll_month.winfo_children():
            widget.destroy()

        if not installments:
            lbl = ctk.CTkLabel(
                self.scroll_month, text="Aucune échéance trouvée", text_color="gray50"
            )
            lbl.pack(pady=20)
            return

        for index, installment in enumerate(installments):
            month = installment["month"]
            amount = installment["amount"]
            is_paid = installment["paid"]

            row_bg = "#1E293B" if index % 2 == 0 else "#0F172A"
            row = ctk.CTkFrame(self.scroll_month, fg_color=row_bg, corner_radius=4)
            row.pack(fill="x", pady=2, ipady=2)

            # 1. Colonne MOIS
            ctk.CTkLabel(
                row, text=month, font=ctk.CTkFont(size=12), width=90, anchor="w"
            ).pack(side="left", padx=5)

            # 2. Colonne MONTANT
            ctk.CTkLabel(
                row,
                text=f"{amount:,.0f} FCFA",
                font=ctk.CTkFont(size=12),
                text_color="gray80",
                width=90,
                anchor="center",
            ).pack(side="left", padx=5)

            # 3. Colonne STATUT (Toujours présente avec badge PAYÉ ou NON PAYÉ)
            status_text, status_color, status_bg = (
                ("PAYÉ", "#10B981", "#064E3B")
                if is_paid
                else ("NON PAYÉ", "#EF4444", "#7F1D1D")
            )
            badge_frame = ctk.CTkFrame(
                row, fg_color=status_bg, corner_radius=6, width=85, height=24
            )
            badge_frame.pack(side="left", padx=5)
            badge_frame.pack_propagate(False)
            ctk.CTkLabel(
                badge_frame,
                text=status_text,
                text_color=status_color,
                font=ctk.CTkFont(size=10, weight="bold"),
            ).place(relx=0.5, rely=0.5, anchor="center")

            # 4. Colonne ACTION (Bouton reçu si payé, tiret sinon)
            action_frame = ctk.CTkFrame(row, fg_color="transparent", width=90, height=26)
            action_frame.pack(side="left", padx=5)
            action_frame.pack_propagate(False)

            if is_paid:
                ctk.CTkButton(
                    action_frame,
                    text="🖨️ Reçu",
                    width=85,
                    height=24,
                    fg_color="#2563EB",
                    hover_color="#1D4ED8",
                    font=ctk.CTkFont(size=10, weight="bold"),
                    command=lambda m=month: self.controller.reprint_receipt(m),
                ).place(relx=0.5, rely=0.5, anchor="center")
            else:
                ctk.CTkLabel(
                    action_frame,
                    text="--",
                    text_color="gray50",
                    font=ctk.CTkFont(size=12),
                ).place(relx=0.5, rely=0.5, anchor="center")

    def get_selected_month(self) -> str | None:
        """Retourne la valeur actuellement sélectionnée dans la liste des mois."""
        val = self.combo_month.get()
        return val if val and val not in ("Choisir un mois...", "Tout est réglé") else None

    def get_payment_method(self) -> str | None:
        """Retourne le mode de paiement sélectionné."""
        val = self.combo_method.get()
        return val if val and val != "Choisir un mode..." else None

    def get_student_id(self) -> str:
        """Retourne le matricule saisi dans le champ de recherche."""
        return self.search_student_id.get().strip()

    # ---------- GESTIONNAIRES D'ÉVÉNEMENTS ----------
    def _on_search(self):
        self.controller.search_student()

    def _on_month_changed(self, *_):
        self.controller.on_month_selected(self.combo_month.get())

    def _on_submit_payment(self):
        self.controller.process_payment()


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Gestion des Paiements Mensuels")
    app.geometry("950x600")
    frame = MonthlyPaymentFormFrame(app)
    frame.pack(fill="both", expand=True)
    app.mainloop()