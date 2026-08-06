import customtkinter as ctk
from models import Month
from controllers import PaymentStatsController


class PaymentStatsFormFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.selected_program_radio_var = ctk.IntVar(value=-1)
        self.controller = PaymentStatsController(self)
        self.program_badges = {}
        self.class_map = {}

        self.grid_columnconfigure(0, weight=0, minsize=270)
        self.grid_columnconfigure(1, weight=1, uniform="main_cols")
        self.grid_rowconfigure(0, weight=1)

        self.font_title = ("Helvetica", 16, "bold")
        self.font_header = ("Helvetica", 11, "bold")
        self.font_cell = ("Helvetica", 11)

        self.columns = [
            ("Matricule", 120),
            ("Nom & Prénom", 220),
            ("Email", 200),
            ("Statut Paiement", 130),
            ("Montant Réglé", 120),
        ]

        self._create_program_sidebar()
        self._create_main_content_area()

        self.controller.load_initial_data()

    def _create_program_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color="#1f2937", corner_radius=8)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(15, 10), pady=15)
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            sidebar,
            text="🎓 PROGRAMMES",
            font=("Helvetica", 13, "bold"),
            text_color="#38bdf8",
        ).grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")

        self.entry_program_search = ctk.CTkEntry(
            sidebar,
            placeholder_text="Rechercher ex: Informatique...",
            fg_color="#111827",
            border_color="#374151",
            text_color="#e5e7eb",
            height=32,
        )
        self.entry_program_search.grid(
            row=1, column=0, padx=15, pady=(0, 10), sticky="ew"
        )
        self.entry_program_search.bind(
            "<KeyRelease>", lambda e: self.controller.on_program_search_changed()
        )

        self.scroll_programs = ctk.CTkScrollableFrame(
            sidebar,
            fg_color="#111827",
            corner_radius=6,
        )
        self.scroll_programs.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def _create_main_content_area(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        main_frame.grid_columnconfigure(0, weight=1, uniform="content_col")
        main_frame.grid_rowconfigure(2, weight=1)

        # En-tête
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text="SUIVI ET ÉTAT DES PAIEMENTS",
            font=self.font_title,
            text_color="#3b82f6",
            anchor="w",
        ).pack(side="left")

        self.lbl_active_year = ctk.CTkLabel(
            header_frame,
            text="Année Académique : --",
            font=("Helvetica", 12, "bold"),
            text_color="#10b981",
        )
        self.lbl_active_year.pack(side="right")

        # Filtres & Boutons
        filter_frame = ctk.CTkFrame(main_frame, fg_color="#1f2937", corner_radius=8)
        filter_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        # Mois
        ctk.CTkLabel(
            filter_frame,
            text="Mois :",
            font=("Helvetica", 11, "bold"),
            text_color="#d1d5db",
        ).pack(side="left", padx=(15, 5), pady=10)

        month_values = [m.value for m in Month]
        self.combo_month = ctk.CTkOptionMenu(
            filter_frame,
            values=month_values,
            command=lambda v: self.controller.refresh_stats(),
            fg_color="#111827",
            button_color="#2b3544",
            button_hover_color="#374151",
            text_color="#e5e7eb",
            dropdown_fg_color="#1f2937",
            width=130,
            height=32,
        )
        self.combo_month.set(month_values[0])
        self.combo_month.pack(side="left", padx=(0, 15), pady=10)

        # Classe
        ctk.CTkLabel(
            filter_frame,
            text="Classe :",
            font=("Helvetica", 11, "bold"),
            text_color="#d1d5db",
        ).pack(side="left", padx=(0, 5), pady=10)

        self.combo_class = ctk.CTkOptionMenu(
            filter_frame,
            values=["Sélectionnez un programme"],
            command=lambda v: self.controller.refresh_stats(),
            fg_color="#111827",
            button_color="#2b3544",
            button_hover_color="#374151",
            text_color="#e5e7eb",
            dropdown_fg_color="#1f2937",
            width=170,
            height=32,
        )
        self.combo_class.pack(side="left", padx=(0, 15), pady=10)

        # Bouton 1: Imprimer SEULEMENT les non payés
        btn_print_unpaid = ctk.CTkButton(
            filter_frame,
            text="🖨️ Impayés",
            command=self.controller.print_unpaid_students,
            fg_color="#ef4444",
            hover_color="#dc2626",
            height=32,
            width=110,
            font=("Helvetica", 11, "bold"),
        )
        btn_print_unpaid.pack(side="right", padx=(5, 15), pady=10)

        # Bouton 2: Imprimer TOUS les élèves (En règle + Impayés)
        btn_print_all = ctk.CTkButton(
            filter_frame,
            text="📄 Tous",
            command=self.controller.print_all_students,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            height=32,
            width=100,
            font=("Helvetica", 11, "bold"),
        )
        btn_print_all.pack(side="right", padx=(5, 0), pady=10)

        # Tableau
        self.scrollable_table = ctk.CTkScrollableFrame(
            main_frame, fg_color="#111827", corner_radius=8
        )
        self.scrollable_table.grid(row=2, column=0, sticky="nsew")

        for idx, (_, width) in enumerate(self.columns):
            self.scrollable_table.grid_columnconfigure(
                idx, weight=1, minsize=width, uniform="table_columns"
            )

    def render_program_sidebar_list(self, programs: list):
        for widget in self.scroll_programs.winfo_children():
            widget.destroy()

        self.program_badges.clear()
        current_selected = self.controller.selected_program_id
        active_key = current_selected if current_selected is not None else -1
        self.selected_program_radio_var.set(active_key)

        if not programs:
            lbl_none = ctk.CTkLabel(
                self.scroll_programs,
                text="Aucun programme trouvé",
                font=("Helvetica", 10, "italic"),
                text_color="#9ca3af",
            )
            lbl_none.pack(pady=10)
            return

        for p in programs:
            is_selected = current_selected == p["id"]
            self._create_program_badge(
                program_id=p["id"],
                label=p["label"],
                is_selected=is_selected,
            )

    def _create_program_badge(self, program_id: int, label: str, is_selected: bool):
        badge_frame = ctk.CTkFrame(
            self.scroll_programs,
            fg_color="#1f2937",
            border_color="#374151",
            border_width=1,
            corner_radius=16,
            height=34,
            cursor="hand2",
        )
        badge_frame.pack(fill="x", pady=3, padx=2)

        def select_program_action():
            self._highlight_active_badge(program_id)
            self.after(10, lambda: self.controller.select_program(program_id))

        radio = ctk.CTkRadioButton(
            badge_frame,
            text=label,
            value=program_id,
            variable=self.selected_program_radio_var,
            font=("Helvetica", 11, "bold" if is_selected else "normal"),
            text_color="#ffffff" if is_selected else "#d1d5db",
            fg_color="#38bdf8",
            border_color="#9ca3af",
            hover_color="#0284c7",
            command=select_program_action,
        )
        radio.pack(side="left", padx=10, pady=6, fill="x", expand=True)
        self.program_badges[program_id] = {
            "frame": badge_frame,
            "radio": radio,
            "label": label,
        }
        badge_frame.bind("<Button-1>", lambda e: radio.select())

    def get_selected_program_label(self) -> str:
        selected_id = self.controller.selected_program_id
        if selected_id in self.program_badges:
            return self.program_badges[selected_id]["label"]
        return "N/A"

    def _highlight_active_badge(self, active_key: int):
        for key, components in self.program_badges.items():
            radio = components["radio"]
            if key == active_key:
                radio.configure(font=("Helvetica", 11, "bold"), text_color="#ffffff")
            else:
                radio.configure(font=("Helvetica", 11, "normal"), text_color="#d1d5db")

    def update_active_year_display(self, year_label: str):
        self.lbl_active_year.configure(text=f"Année Académique : {year_label}")

    def update_class_combobox(self, classes: list[dict]):
        self.class_map = {c["name"]: c["id"] for c in classes}
        class_names = list(self.class_map.keys())

        if class_names:
            self.combo_class.configure(values=class_names)
            self.combo_class.set(class_names[0])
        else:
            self.combo_class.configure(values=["Aucune classe disponible"])
            self.combo_class.set("Aucune classe disponible")

    def get_selected_class_id(self) -> int | None:
        selected_name = self.combo_class.get()
        return self.class_map.get(selected_name)

    def render_students_table(self, students: list):
        for widget in self.scrollable_table.winfo_children():
            widget.destroy()

        for col_idx, (col_name, _) in enumerate(self.columns):
            lbl = ctk.CTkLabel(
                self.scrollable_table,
                text=col_name,
                font=self.font_header,
                text_color="#9ca3af",
                anchor="w",
                fg_color="#1f2937",
                height=35,
            )
            lbl.grid(row=0, column=col_idx, sticky="ew", padx=1, pady=(0, 2))

        if not students:
            lbl_empty = ctk.CTkLabel(
                self.scrollable_table,
                text="Aucun élève trouvé pour cette sélection.",
                font=self.font_cell,
                text_color="#6b7280",
            )
            lbl_empty.grid(row=1, column=0, columnspan=len(self.columns), pady=20)
            return

        base_bg = "#111827"
        hover_bg = "#1e293b"

        for row_idx, student in enumerate(students, start=1):
            is_paid = student["is_paid"]
            status_text = "Payé" if is_paid else "Non Payé"
            status_color = "#10b981" if is_paid else "#ef4444"
            amount_str = f"{student['amount_paid']} FCFA" if is_paid else "-"

            values = [
                student["student_id_number"],
                student["full_name"],
                student["email"],
                status_text,
                amount_str,
            ]

            row_labels = []

            for col_idx, val in enumerate(values):
                text_color = status_color if col_idx == 3 else "#e5e7eb"

                lbl = ctk.CTkLabel(
                    self.scrollable_table,
                    text=val,
                    font=self.font_cell,
                    text_color=text_color,
                    anchor="w",
                    fg_color=base_bg,
                    height=30,
                )
                lbl.grid(row=row_idx, column=col_idx, sticky="ew", padx=1, pady=1)
                row_labels.append(lbl)

            for lbl in row_labels:
                lbl.bind(
                    "<Enter>",
                    lambda e, labels=row_labels: self._on_row_hover(labels, hover_bg),
                )
                lbl.bind(
                    "<Leave>",
                    lambda e, labels=row_labels, bg=base_bg: self._on_row_hover(
                        labels, bg
                    ),
                )

    def _on_row_hover(self, row_labels: list, color: str):
        for lbl in row_labels:
            lbl.configure(fg_color=color)
