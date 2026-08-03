# payment_form.py
import customtkinter as ctk
from controllers import MonthlyPaymentController


class MonthlyPaymentFormFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = MonthlyPaymentController(self)

        # Grid configuration (2 columns)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Build columns
        self._create_left_column()
        self._create_right_column()

        # Initial loading of combo boxes (via controller)
        self.controller.load_initial_options()

        # Default display (empty)
        self.display_student_info(None, None)
        self.display_schedule([])
        self.display_remaining_balance(0.0)

    # ---------- INTERFACE CONSTRUCTION ----------
    def _create_left_column(self):
        """Left column: search, student info, schedule."""
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Title
        ctk.CTkLabel(
            self.left_frame,
            text="RECHERCHE ÉTUDIANT",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B82F6",
        ).pack(anchor="w", pady=(0, 10))

        # Search bar
        search_box = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        search_box.pack(fill="x", pady=(0, 15))

        self.search_student_id = ctk.CTkEntry(
            search_box,
            placeholder_text="Entrer le Matricule (ex: ETU-2026-0001)...",
            height=40,
        )
        self.search_student_id.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            search_box,
            text="Rechercher",
            height=40,
            command=self._on_search
        ).pack(side="right")

        # Information card (2-column grid)
        self.info_card = ctk.CTkFrame(self.left_frame, corner_radius=10)
        self.info_card.pack(fill="x", pady=(0, 15), ipadx=10, ipady=10)
        self.info_card.grid_columnconfigure(0, weight=1)
        self.info_card.grid_columnconfigure(1, weight=1)

        # Row 0: Student | Level
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

        # Row 1: Program | Major
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

        # Row 2: ClassGroup | Monthly Fee
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

        # Table Header
        header = ctk.CTkFrame(self.left_frame, fg_color="#1E293B", corner_radius=6)
        header.pack(fill="x", pady=(5, 2))
        for col, (text, anchor) in enumerate([
            ("Mois", "w"),
            ("Montant", "center"),
            ("Statut", "center")
        ]):
            ctk.CTkLabel(
                header,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=110,
                anchor=anchor,
            ).pack(side="left", padx=10, pady=8)

        # Table Body (scrollable)
        self.scroll_month = ctk.CTkScrollableFrame(
            self.left_frame, height=160, fg_color="#0F172A"
        )
        self.scroll_month.pack(fill="both", expand=True)

    def _create_right_column(self):
        """Right column: payment form."""
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(
            self.right_frame,
            text="NOUVEAU PAIEMENT",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B82F6",
        ).pack(anchor="w", pady=(0, 15))

        # Month
        ctk.CTkLabel(self.right_frame, text="Mois à régler :").pack(anchor="w", pady=(0, 5))
        self.combo_month = ctk.CTkOptionMenu(self.right_frame, height=38)
        self.combo_month.pack(fill="x", pady=(0, 15))

        # Payment Method
        ctk.CTkLabel(self.right_frame, text="Mode de Paiement :").pack(anchor="w", pady=(0, 5))
        self.combo_method = ctk.CTkOptionMenu(self.right_frame, height=38)
        self.combo_method.pack(fill="x", pady=(0, 15))

        # Amount to pay
        ctk.CTkLabel(self.right_frame, text="Montant à Payer").pack(anchor="w", pady=(0, 5))
        self.amount_frame = ctk.CTkFrame(
            self.right_frame, fg_color="#1E293B", corner_radius=6, height=38
        )
        self.amount_frame.pack(fill="x", pady=(0, 15))
        self.amount_frame.pack_propagate(False)

        self.lbl_amount_value = ctk.CTkLabel(
            self.amount_frame,
            text="-- FCFA",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#34D399",
        )
        self.lbl_amount_value.pack(side="left", padx=15)

        # Validation button
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

    # ---------- UPDATE METHODS (called by controller) ----------
    def display_student_info(self, student, enrollment):
        """Updates labels with student and enrollment information."""
        if student and enrollment:
            program = f"{enrollment.program.major.name} ({enrollment.program.level.name})"
            self.lbl_student_name.configure(text=f"Étudiant : {student.last_name} - {student.first_name}")
            self.lbl_program.configure(text=f"Programme : {program}")
            self.lbl_level.configure(text=f"Niveau : {enrollment.program.level.name}")
            self.lbl_major.configure(text=f"Filière : {enrollment.program.major.name}")
            self.lbl_class_group.configure(text=f"Classe : {enrollment.class_group.name}")
        else:
            # Reset
            self.lbl_student_name.configure(text="Étudiant : --")
            self.lbl_program.configure(text="Programme : --")
            self.lbl_level.configure(text="Niveau : --")
            self.lbl_major.configure(text="Filière : --")
            self.lbl_class_group.configure(text="Classe : --")

    def display_schedule(self, installments):
        """Rebuilds the schedule table with installment statuses."""
        # Clear container
        for widget in self.scroll_month.winfo_children():
            widget.destroy()

        if not installments:
            lbl = ctk.CTkLabel(
                self.scroll_month,
                text="Aucune échéance trouvée",
                text_color="gray50"
            )
            lbl.pack(pady=20)
            return

        for index, installment in enumerate(installments):
            month = installment["month"]
            amount = installment["amount"]
            is_paid = installment["paid"]

            status, text_color, bg_badge = (
                ("PAYÉ", "#10B981", "#064E3B") if is_paid
                else ("NON PAYÉ", "#EF4444", "#7F1D1D")
            )

            row_bg = "#1E293B" if index % 2 == 0 else "#0F172A"
            row = ctk.CTkFrame(self.scroll_month, fg_color=row_bg, corner_radius=4)
            row.pack(fill="x", pady=2, ipady=2)

            ctk.CTkLabel(
                row, text=month, font=ctk.CTkFont(size=12), width=110, anchor="w"
            ).pack(side="left", padx=10)

            ctk.CTkLabel(
                row,
                text=f"{amount:,.0f} FCFA",
                font=ctk.CTkFont(size=12),
                text_color="gray80",
                width=110,
                anchor="center",
            ).pack(side="left", padx=10)

            badge_frame = ctk.CTkFrame(
                row, fg_color=bg_badge, corner_radius=6, width=110, height=26
            )
            badge_frame.pack(side="left", padx=10)
            badge_frame.pack_propagate(False)
            ctk.CTkLabel(
                badge_frame,
                text=status,
                text_color=text_color,
                font=ctk.CTkFont(size=10, weight="bold"),
            ).place(relx=0.5, rely=0.5, anchor="center")

    def display_remaining_balance(self, remaining):
        """Updates remaining balance label."""
        self.lbl_amount_value.configure(text=f"{remaining:,.0f} FCFA")

    # ---------- EVENT HANDLERS ----------
    def _on_search(self):
        self.controller.search_student()

    def _on_submit_payment(self):
        self.controller.process_payment()


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Gestion des Paiements Mensuels")
    app.geometry("950x600")
    frame = MonthlyPaymentFormFrame(app)
    frame.pack(fill="both", expand=True)
    app.mainloop()