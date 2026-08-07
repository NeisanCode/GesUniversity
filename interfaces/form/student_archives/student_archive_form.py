import customtkinter as ctk
from controllers import StudentArchiveController


class StudentArchiveForm(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.selected_program_radio_var = ctk.IntVar(value=-1)
        self.controller = StudentArchiveController(self)
        self.program_badges = {}
        self.years_map = {}

        # Configuration de la grille globale
        self.grid_columnconfigure(0, weight=0, minsize=270)
        self.grid_columnconfigure(1, weight=1, uniform="main_cols")
        self.grid_rowconfigure(0, weight=1)

        self.font_title = ("Helvetica", 16, "bold")
        self.font_header = ("Helvetica", 11, "bold")
        self.font_cell = ("Helvetica", 11)

        # Colonnes demandées (Nom, Prénom, Email, Matricule, Date Anniversaire, Adresse)
        self.columns = [
            ("Matricule", 100),
            ("Nom", 120),
            ("Prénom", 120),
            ("Email", 160),
            ("Date Naiss.", 110),
            ("Adresse", 140),
            ("Année Acad.", 100),
        ]

        self._create_program_sidebar()
        self._create_main_content_area()

        self.controller.load_initial_data()

    def _create_program_sidebar(self):
        """Sidebar de gauche pour filtrer par programme."""
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
            placeholder_text="Rechercher programme...",
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
        """Zone principale de droite (En-tête, Filtres, Tableau)."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        main_frame.grid_columnconfigure(0, weight=1, uniform="content_col")
        main_frame.grid_rowconfigure(2, weight=1)

        # En-tête
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text="ARCHIVES - ÉTUDIANTS DES ANNÉES ANTÉRIEURES",
            font=self.font_title,
            text_color="#f59e0b",
            anchor="w",
        ).pack(side="left")

        # Filtres
        filter_frame = ctk.CTkFrame(main_frame, fg_color="#1f2937", corner_radius=8)
        filter_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        self.entry_student_search = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Nom, prénom, matricule...",
            fg_color="#111827",
            border_color="#374151",
            text_color="#e5e7eb",
            width=200,
            height=32,
        )
        self.entry_student_search.pack(side="left", padx=(15, 5), pady=10)

        btn_search = ctk.CTkButton(
            filter_frame,
            text="Rechercher",
            command=self.controller.on_search_button_clicked,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            width=90,
            height=32,
            font=("Helvetica", 11, "bold"),
        )
        btn_search.pack(side="left", padx=(0, 15), pady=10)

        # Sélection Année
        ctk.CTkLabel(
            filter_frame,
            text="Année :",
            font=("Helvetica", 11, "bold"),
            text_color="#d1d5db",
        ).pack(side="left", padx=(5, 5), pady=10)

        self.combo_years = ctk.CTkOptionMenu(
            filter_frame,
            values=["Toutes"],
            command=self._on_year_combo_changed,
            fg_color="#111827",
            button_color="#2b3544",
            button_hover_color="#374151",
            text_color="#e5e7eb",
            dropdown_fg_color="#1f2937",
            width=130,
            height=32,
        )
        self.combo_years.pack(side="left", padx=(0, 15), pady=10)

        # Limite
        ctk.CTkLabel(
            filter_frame,
            text="Afficher :",
            font=("Helvetica", 11, "bold"),
            text_color="#d1d5db",
        ).pack(side="left", padx=(5, 5), pady=10)

        self.combo_limit = ctk.CTkOptionMenu(
            filter_frame,
            values=["50", "100", "Tout"],
            command=lambda v: self.controller.refresh_student_list(),
            fg_color="#111827",
            button_color="#2b3544",
            button_hover_color="#374151",
            text_color="#e5e7eb",
            dropdown_fg_color="#1f2937",
            width=80,
            height=32,
        )
        self.combo_limit.set("50")
        self.combo_limit.pack(side="left", padx=(0, 15), pady=10)

        # Tableau
        self.scrollable_table = ctk.CTkScrollableFrame(
            main_frame, fg_color="#111827", corner_radius=8
        )
        self.scrollable_table.grid(row=2, column=0, sticky="nsew")

        for idx, (_, width) in enumerate(self.columns):
            self.scrollable_table.grid_columnconfigure(
                idx, weight=1, minsize=width, uniform="table_columns"
            )

    def render_years_combo(self, years: list):
        self.years_map = {"Toutes les années": None}
        options = ["Toutes les années"]

        for y in years:
            options.append(y["label"])
            self.years_map[y["label"]] = y["id"]

        self.combo_years.configure(values=options)
        self.combo_years.set("Toutes les années")

    def _on_year_combo_changed(self, selected_label: str):
        year_id = self.years_map.get(selected_label)
        self.controller.on_year_selected(year_id)

    def render_program_sidebar_list(self, programs: list):
        for widget in self.scroll_programs.winfo_children():
            widget.destroy()

        self.program_badges.clear()
        current_selected = self.controller.selected_program_id
        active_key = current_selected if current_selected is not None else -1
        self.selected_program_radio_var.set(active_key)

        self._create_program_badge(
            program_id=None,
            label="Tous les programmes",
            is_selected=(current_selected is None),
        )

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

    def _create_program_badge(
        self, program_id: int | None, label: str, is_selected: bool
    ):
        val_key = program_id if program_id is not None else -1

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
            self._highlight_active_badge(val_key)
            self.after(10, lambda: self.controller.select_program(program_id))

        radio = ctk.CTkRadioButton(
            badge_frame,
            text=label,
            value=val_key,
            variable=self.selected_program_radio_var,
            font=("Helvetica", 11, "bold" if is_selected else "normal"),
            text_color="#ffffff" if is_selected else "#d1d5db",
            fg_color="#38bdf8",
            border_color="#9ca3af",
            hover_color="#0284c7",
            command=select_program_action,
        )
        radio.pack(side="left", padx=10, pady=6, fill="x", expand=True)

        self.program_badges[val_key] = {"frame": badge_frame, "radio": radio}
        badge_frame.bind("<Button-1>", lambda e: radio.select())

    def _highlight_active_badge(self, active_key: int):
        for key, components in self.program_badges.items():
            radio = components["radio"]
            if key == active_key:
                radio.configure(font=("Helvetica", 11, "bold"), text_color="#ffffff")
            else:
                radio.configure(font=("Helvetica", 11, "normal"), text_color="#d1d5db")

    def render_student_table(self, students: list):
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
                text="Aucun élève trouvé pour cette sélection d'années antérieures.",
                font=self.font_cell,
                text_color="#6b7280",
            )
            lbl_empty.grid(row=1, column=0, columnspan=len(self.columns), pady=20)
            return

        base_bg = "#111827"
        hover_bg = "#1e293b"
        flash_bg = "#f59e0b"

        for row_idx, student in enumerate(students, start=1):
            values = [
                student["student_id_number"],
                student["last_name"],
                student["first_name"],
                student["email"],
                student["date_of_birth"],
                student["address"],
                student["academic_year"],
            ]

            row_labels = []

            for col_idx, val in enumerate(values):
                lbl = ctk.CTkLabel(
                    self.scrollable_table,
                    text=val,
                    font=self.font_cell,
                    text_color="#e5e7eb",
                    anchor="w",
                    fg_color=base_bg,
                    height=30,
                    cursor="hand2",
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
                lbl.bind(
                    "<Button-1>",
                    lambda e, s=student, labels=row_labels, bg=base_bg, f_bg=flash_bg: self._on_row_click(
                        s, labels, bg, f_bg
                    ),
                )

    def _on_row_hover(self, row_labels: list, color: str):
        for lbl in row_labels:
            lbl.configure(fg_color=color)

    def _on_row_click(
        self, student: dict, row_labels: list, base_bg: str, flash_bg: str
    ):
        def reset_and_open():
            for lbl in row_labels:
                lbl.configure(fg_color=base_bg)
            self.controller.on_student_row_clicked(student)

        for lbl in row_labels:
            lbl.configure(fg_color=flash_bg)

        self.after(120, reset_and_open)
