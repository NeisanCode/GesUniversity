import customtkinter as ctk


class StudentFinancialModal(ctk.CTkToplevel):
    def __init__(self, parent, financial_data: dict):
        super().__init__(parent)

        self.financial_data = financial_data

        self.title("Situation Financière de l'Élève")
        self.geometry("700x550")
        self.resizable(False, False)
        self.configure(fg_color="#111827")

        # Rendre la fenêtre modale
        self.transient(parent)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. En-tête Élève
        header_frame = ctk.CTkFrame(self, fg_color="#1f2937", corner_radius=8)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        name = self.financial_data.get("student_name", "Élève Inconnu")
        mat = self.financial_data.get("student_id_number", "--")
        prog = self.financial_data.get("program", "--")
        year = self.financial_data.get("academic_year", "--")

        ctk.CTkLabel(
            header_frame,
            text=f"👤 {name} (Matricule: {mat})",
            font=("Helvetica", 14, "bold"),
            text_color="#38bdf8",
        ).pack(anchor="w", padx=15, pady=(10, 2))

        ctk.CTkLabel(
            header_frame,
            text=f"Programme : {prog}  |  Année : {year}",
            font=("Helvetica", 11),
            text_color="#9ca3af",
        ).pack(anchor="w", padx=15, pady=(0, 10))

        # 2. Carte Résumé Financier
        summary_frame = ctk.CTkFrame(self, fg_color="#1f2937", corner_radius=8)
        summary_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        summary_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        total_due = self.financial_data.get("total_due", 0.0)
        total_paid = self.financial_data.get("total_paid", 0.0)
        remaining = self.financial_data.get("balance_remaining", 0.0)
        is_paid = self.financial_data.get("is_fully_paid", False)

        status_text = "RÉGLÉ" if is_paid else "NON RÉGLÉ / IMPAYÉ"
        status_color = "#10b981" if is_paid else "#ef4444"

        self._add_stat_box(summary_frame, 0, "Frais Totaux", f"{total_due:,.0f} FCFA", "#e5e7eb")
        self._add_stat_box(summary_frame, 1, "Montant Payé", f"{total_paid:,.0f} FCFA", "#10b981")
        self._add_stat_box(summary_frame, 2, "Reste à Payer", f"{remaining:,.0f} FCFA", "#f59e0b" if remaining > 0 else "#e5e7eb")
        self._add_stat_box(summary_frame, 3, "Statut Global", status_text, status_color)

        # 3. Tableau des Mois / Échéances
        table_frame = ctk.CTkScrollableFrame(self, fg_color="#1f2937", corner_radius=8)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 15))

        headers = ["Mois / Échéance", "Type de Frais", "Dû", "Payé", "Reste", "Statut"]
        widths = [120, 140, 90, 90, 90, 90]

        for idx, (h, w) in enumerate(zip(headers, widths)):
            table_frame.grid_columnconfigure(idx, weight=1, minsize=w)
            lbl = ctk.CTkLabel(
                table_frame,
                text=h,
                font=("Helvetica", 10, "bold"),
                text_color="#38bdf8",
                fg_color="#111827",
                height=28,
            )
            lbl.grid(row=0, column=idx, sticky="ew", padx=1, pady=1)

        details = self.financial_data.get("monthly_details", [])
        if not details:
            lbl_none = ctk.CTkLabel(
                table_frame,
                text="Aucune échéance enregistrée pour cet élève.",
                font=("Helvetica", 11),
                text_color="#6b7280",
            )
            lbl_none.grid(row=1, column=0, columnspan=len(headers), pady=20)
        else:
            for row_idx, d in enumerate(details, start=1):
                st = d["status"]
                color = "#10b981" if st == "Réglé" else ("#f59e0b" if st == "Partiel" else "#ef4444")

                vals = [
                    d["month"],
                    d["fee_type"],
                    f"{d['amount_due']:,.0f}",
                    f"{d['amount_paid']:,.0f}",
                    f"{d['remaining']:,.0f}",
                    st,
                ]

                for col_idx, val in enumerate(vals):
                    lbl = ctk.CTkLabel(
                        table_frame,
                        text=val,
                        font=("Helvetica", 10),
                        text_color=color if col_idx == 5 else "#e5e7eb",
                        fg_color="#1f2937",
                        height=26,
                    )
                    lbl.grid(row=row_idx, column=col_idx, sticky="ew", padx=1, pady=1)

        # Button Fermer
        btn_close = ctk.CTkButton(
            self,
            text="Fermer",
            command=self.destroy,
            fg_color="#374151",
            hover_color="#4b5563",
            width=100,
        )
        btn_close.grid(row=3, column=0, pady=(0, 15))

    def _add_stat_box(self, parent, col: int, title: str, value: str, val_color: str):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.grid(row=0, column=col, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(
            box,
            text=title,
            font=("Helvetica", 10),
            text_color="#9ca3af",
        ).pack()

        ctk.CTkLabel(
            box,
            text=value,
            font=("Helvetica", 11, "bold"),
            text_color=val_color,
        ).pack()