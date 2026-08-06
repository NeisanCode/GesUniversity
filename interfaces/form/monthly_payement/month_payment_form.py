import customtkinter as ctk
from controllers import MonthlyPaymentController
from models import Student, Enrollment


class MonthlyPaymentFormFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = MonthlyPaymentController(self)

        # Configuration des polices harmonisées avec EnrollmentFormFrame
        self.font_title = ("Helvetica", 14, "bold")
        self.font_label = ("Helvetica", 12, "bold")
        self.font_entry = ("Helvetica", 12)

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

    # ---------- HELPERS DE STYLISATION (IDENTIQUES À ENROLLMENT) ----------
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

    def create_option_menu(self, parent, label_text, values, command=None):
        ctk.CTkLabel(
            parent,
            text=label_text,
            font=self.font_label,
            text_color="#d1d5db",
            anchor="w",
        ).pack(fill="x", pady=(0, 2))
        
        kwargs = {}
        if command:
            kwargs["command"] = command

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
            **kwargs,
        )
        menu.pack(fill="x", pady=(0, 10))
        return menu

    # ---------- CONSTRUCTION DE L'INTERFACE ----------
    def _create_left_column(self):
        """Colonne de gauche : recherche, infos étudiant, tableau des échéances."""
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=15)

        # Titre section
        self.create_title(self.left_frame, "RECHERCHE ÉTUDIANT")

        # Barre de recherche avec style entry/button
        search_box = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        search_box.pack(fill="x", pady=(0, 15))

        self.search_student_id = ctk.CTkEntry(
            search_box,
            placeholder_text="Entrer le Matricule (ex: ETU20260001)...",
            placeholder_text_color="#6b7280",
            fg_color="#111827",
            border_color="#2b3544",
            text_color="#e5e7eb",
            height=38,
            corner_radius=6,
            font=self.font_entry,
        )
        self.search_student_id.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            search_box,
            text="Rechercher",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="white",
            height=38,
            corner_radius=6,
            font=("Helvetica", 12, "bold"),
            command=self._on_search,
        ).pack(side="right")

        # Carte d'information stylisée
        self.info_card = ctk.CTkFrame(
            self.left_frame,
            fg_color="#111827",
            border_color="#2b3544",
            border_width=1,
            corner_radius=8,
        )
        self.info_card.pack(fill="x", pady=(0, 15), ipadx=10, ipady=10)
        self.info_card.grid_columnconfigure(0, weight=1)
        self.info_card.grid_columnconfigure(1, weight=1)

        # Labels dans la carte d'information
        self.lbl_student_name = ctk.CTkLabel(
            self.info_card,
            text="Étudiant : --",
            font=("Helvetica", 13, "bold"),
            text_color="#e5e7eb",
        )
        self.lbl_student_name.grid(row=0, column=0, sticky="w", padx=10, pady=4)

        self.lbl_level = ctk.CTkLabel(
            self.info_card,
            text="Niveau : --",
            font=("Helvetica", 12),
            text_color="#9ca3af",
        )
        self.lbl_level.grid(row=0, column=1, sticky="w", padx=10, pady=4)

        self.lbl_program = ctk.CTkLabel(
            self.info_card,
            text="Programme : --",
            font=("Helvetica", 12),
            text_color="#9ca3af",
        )
        self.lbl_program.grid(row=1, column=0, sticky="w", padx=10, pady=4)

        self.lbl_major = ctk.CTkLabel(
            self.info_card,
            text="Filière : --",
            font=("Helvetica", 12),
            text_color="#9ca3af",
        )
        self.lbl_major.grid(row=1, column=1, sticky="w", padx=10, pady=4)

        self.lbl_class_group = ctk.CTkLabel(
            self.info_card,
            text="Classe : --",
            font=("Helvetica", 12),
            text_color="#9ca3af",
        )
        self.lbl_class_group.grid(row=2, column=0, sticky="w", padx=10, pady=4)

        self.lbl_monthly_fee = ctk.CTkLabel(
            self.info_card,
            text="Mensualité : -- FCFA",
            text_color="#10b981",
            font=("Helvetica", 12, "bold"),
        )
        self.lbl_monthly_fee.grid(row=2, column=1, sticky="w", padx=10, pady=4)

        self.lbl_total_fee = ctk.CTkLabel(
            self.info_card,
            text="Frais Totaux : -- FCFA",
            text_color="#e5e7eb",
            font=("Helvetica", 12, "bold"),
        )
        self.lbl_total_fee.grid(row=3, column=0, sticky="w", padx=10, pady=4)

        self.lbl_remaining_balance = ctk.CTkLabel(
            self.info_card,
            text="Reste à Payer : -- FCFA",
            text_color="#ef4444",
            font=("Helvetica", 12, "bold"),
        )
        self.lbl_remaining_balance.grid(row=3, column=1, sticky="w", padx=10, pady=4)

        # En-tête du Tableau
        header = ctk.CTkFrame(self.left_frame, fg_color="#1f2937", corner_radius=6)
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
                font=("Helvetica", 11, "bold"),
                text_color="#d1d5db",
                width=width,
                anchor=anchor,
            ).pack(side="left", padx=5, pady=6)

        # Tableau déroulant
        self.scroll_month = ctk.CTkScrollableFrame(
            self.left_frame, height=160, fg_color="#111827", corner_radius=6
        )
        self.scroll_month.pack(fill="both", expand=True)

    def _create_right_column(self):
        """Colonne de droite : formulaire de paiement."""
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=15)

        self.create_title(self.right_frame, "NOUVEAU PAIEMENT")

        # Sélecteur de mois
        self.combo_month = self.create_option_menu(
            self.right_frame,
            "Mois à régler :",
            ["Sélectionner..."],
            command=self._on_month_changed,
        )

        # Mode de Paiement
        self.combo_method = self.create_option_menu(
            self.right_frame, "Mode de Paiement :", ["Sélectionner..."]
        )

        # Bouton de validation (Harmonisé avec EnrollmentFormFrame)
        self.btn_submit = ctk.CTkButton(
            self.right_frame,
            text="ENREGISTRER LE PAIEMENT & IMPRIMER REÇU",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="white",
            height=45,
            corner_radius=8,
            font=("Helvetica", 12, "bold"),
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
        """Met à jour les labels d'information."""
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

            rem_text_color = "#10b981" if remaining_balance <= 0 else "#ef4444"
            rem_prefix = (
                "SOLDÉ (0 FCFA)"
                if remaining_balance <= 0
                else f"{remaining_balance:,.0f} FCFA"
            )

            self.lbl_remaining_balance.configure(
                text=f"Reste à Payer : {rem_prefix}", text_color=rem_text_color
            )
        else:
            self.lbl_student_name.configure(text="Étudiant : --")
            self.lbl_program.configure(text="Programme : --")
            self.lbl_level.configure(text="Niveau : --")
            self.lbl_major.configure(text="Filière : --")
            self.lbl_class_group.configure(text="Classe : --")
            self.lbl_monthly_fee.configure(text="Mensualité : -- FCFA")
            self.lbl_total_fee.configure(text="Frais Totaux : -- FCFA")
            self.lbl_remaining_balance.configure(
                text="Reste à Payer : -- FCFA", text_color="#ef4444"
            )

    def display_schedule(self, installments):
        """Reconstruit le tableau des échéances."""
        for widget in self.scroll_month.winfo_children():
            widget.destroy()

        if not installments:
            lbl = ctk.CTkLabel(
                self.scroll_month, text="Aucune échéance trouvée", text_color="#6b7280"
            )
            lbl.pack(pady=20)
            return

        for index, installment in enumerate(installments):
            month = installment["month"]
            amount = installment["amount"]
            is_paid = installment["paid"]

            row_bg = "#1f2937" if index % 2 == 0 else "#111827"
            row = ctk.CTkFrame(self.scroll_month, fg_color=row_bg, corner_radius=4)
            row.pack(fill="x", pady=2, ipady=2)

            # 1. MOIS
            ctk.CTkLabel(
                row,
                text=month,
                font=("Helvetica", 11),
                text_color="#e5e7eb",
                width=90,
                anchor="w",
            ).pack(side="left", padx=5)

            # 2. MONTANT
            ctk.CTkLabel(
                row,
                text=f"{amount:,.0f} FCFA",
                font=("Helvetica", 11),
                text_color="#9ca3af",
                width=90,
                anchor="center",
            ).pack(side="left", padx=5)

            # 3. STATUT
            status_text, status_color, status_bg = (
                ("PAYÉ", "#10b981", "#064e3b")
                if is_paid
                else ("NON PAYÉ", "#ef4444", "#7f1d1d")
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
                font=("Helvetica", 10, "bold"),
            ).place(relx=0.5, rely=0.5, anchor="center")

            # 4. ACTION
            action_frame = ctk.CTkFrame(row, fg_color="transparent", width=90, height=26)
            action_frame.pack(side="left", padx=5)
            action_frame.pack_propagate(False)

            if is_paid:
                ctk.CTkButton(
                    action_frame,
                    text="🖨️ Reçu",
                    width=85,
                    height=24,
                    fg_color="#3b82f6",
                    hover_color="#2563eb",
                    text_color="white",
                    font=("Helvetica", 10, "bold"),
                    command=lambda m=month: self.controller.reprint_receipt(m),
                ).place(relx=0.5, rely=0.5, anchor="center")
            else:
                ctk.CTkLabel(
                    action_frame,
                    text="--",
                    text_color="#6b7280",
                    font=("Helvetica", 11),
                ).place(relx=0.5, rely=0.5, anchor="center")

    def get_selected_month(self) -> str | None:
        val = self.combo_month.get()
        return val if val and val not in ("Choisir un mois...", "Tout est réglé", "Sélectionner...") else None

    def get_payment_method(self) -> str | None:
        val = self.combo_method.get()
        return val if val and val != "Sélectionner..." else None

    def get_student_id(self) -> str:
        return self.search_student_id.get().strip()

    # ---------- GESTIONNAIRES D'ÉVÉNEMENTS ----------
    def _on_search(self):
        self.controller.search_student()

    def _on_month_changed(self, *_):
        self.controller.on_month_selected(self.combo_month.get())

    def _on_submit_payment(self):
        self.controller.process_payment()