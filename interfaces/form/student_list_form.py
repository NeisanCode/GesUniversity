# interfaces/form/student_list_form.py
import customtkinter as ctk
from controllers import StudentListController


class StudentListFormFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.chk_new_var = ctk.BooleanVar(value=True)
        self.chk_re_var = ctk.BooleanVar(value=True)

        self.controller = StudentListController(self)

        # Layout principal : 2 colonnes (Col 0 = Sidebar Programme, Col 1 = Contenu principal)
        self.grid_columnconfigure(0, weight=0, minsize=260)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.font_title = ("Helvetica", 16, "bold")
        self.font_header = ("Helvetica", 11, "bold")
        self.font_cell = ("Helvetica", 11)

        self._create_program_sidebar()
        self._create_main_content_area()

        self.controller.load_initial_data()

    def _create_program_sidebar(self):
        """Crée la sidebar de gauche dédiée à la recherche de programmes."""
        sidebar = ctk.CTkFrame(self, fg_color="#1f2937", corner_radius=8)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(15, 10), pady=15)
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_rowconfigure(2, weight=1)

        # Titre Sidebar
        ctk.CTkLabel(
            sidebar,
            text="🎓 PROGRAMMES",
            font=("Helvetica", 13, "bold"),
            text_color="#38bdf8",
        ).grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")

        # Barre de recherche de programme
        self.entry_program_search = ctk.CTkEntry(
            sidebar,
            placeholder_text="Rechercher ex: Informatique...",
            fg_color="#111827",
            border_color="#374151",
            text_color="#e5e7eb",
            height=32,
        )
        self.entry_program_search.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        self.entry_program_search.bind(
            "<KeyRelease>", lambda e: self.controller.on_program_search_changed()
        )

        # Zone déroulante des suggestions
        self.scroll_programs = ctk.CTkScrollableFrame(
            sidebar, fg_color="#111827", corner_radius=6,
        )
        self.scroll_programs.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def _create_main_content_area(self):
        """Crée la zone principale de droite (En-tête, Filtres + Bouton recherche, Tableau)."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)

        # En-tête
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text="LISTE DES ÉLÈVES INSCRITS & RÉINSCRITS",
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

        # Barre de Filtres et Bouton Rechercher
        filter_frame = ctk.CTkFrame(main_frame, fg_color="#1f2937", corner_radius=8)
        filter_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        # Zone Recherche Élève
        self.entry_student_search = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Nom, prénom, matricule...",
            fg_color="#111827",
            border_color="#374151",
            text_color="#e5e7eb",
            width=220,
            height=32,
        )
        self.entry_student_search.pack(side="left", padx=(15, 5), pady=10)

        # Bouton Rechercher
        btn_search = ctk.CTkButton(
            filter_frame,
            text="Rechercher",
            command=self.controller.on_search_button_clicked,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            width=100,
            height=32,
            font=("Helvetica", 11, "bold"),
        )
        btn_search.pack(side="left", padx=(0, 15), pady=10)

        # Checkboxes
        self.chk_new = ctk.CTkCheckBox(
            filter_frame,
            text="Inscrits",
            variable=self.chk_new_var,
            command=self.controller.refresh_student_list,
            font=("Helvetica", 11, "bold"),
            text_color="#38bdf8",
            fg_color="#0284c7",
            hover_color="#0369a1",
        )
        self.chk_new.pack(side="left", padx=5, pady=10)

        self.chk_re = ctk.CTkCheckBox(
            filter_frame,
            text="Réinscrits",
            variable=self.chk_re_var,
            command=self.controller.refresh_student_list,
            font=("Helvetica", 11, "bold"),
            text_color="#c084fc",
            fg_color="#9333ea",
            hover_color="#7e22ce",
        )
        self.chk_re.pack(side="left", padx=5, pady=10)

        # Limite
        ctk.CTkLabel(
            filter_frame,
            text="Afficher :",
            font=("Helvetica", 11, "bold"),
            text_color="#d1d5db",
        ).pack(side="left", padx=(15, 5), pady=10)

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

        # Container du Tableau
        self.scrollable_table = ctk.CTkScrollableFrame(
            main_frame, fg_color="#111827", corner_radius=8
        )
        self.scrollable_table.grid(row=2, column=0, sticky="nsew")

        self.columns = [
            ("Matricule", 110),
            ("Nom & Prénom", 180),
            ("Programme / Filière", 200),
            ("Classe", 100),
            ("Type d'inscription", 130),
            ("Statut", 90),
            ("Date d'inscription", 120),
        ]

    def render_program_sidebar_list(self, programs: list):
        """Affiche dynamiquement les suggestions de programmes sous forme de boutons."""
        for widget in self.scroll_programs.winfo_children():
            widget.destroy()

        # Option pour réinitialiser et voir tous les programmes
        btn_all = ctk.CTkButton(
            self.scroll_programs,
            text="Tous les programmes",
            anchor="w",
            fg_color="#374151" if self.controller.selected_program_id is None else "transparent",
            text_color="#e5e7eb",
            hover_color="#4b5563",
            height=30,
            command=lambda: self.controller.select_program(None),
        )
        btn_all.pack(fill="x", pady=2)

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
            is_selected = self.controller.selected_program_id == p["id"]
            btn = ctk.CTkButton(
                self.scroll_programs,
                text=p["label"],
                anchor="w",
                fg_color="#0284c7" if is_selected else "transparent",
                text_color="#ffffff" if is_selected else "#d1d5db",
                hover_color="#0369a1" if is_selected else "#374151",
                height=32,
                command=lambda pid=p["id"]: self.controller.select_program(pid),
            )
            btn.pack(fill="x", pady=2)

    def update_active_year_display(self, year_label: str):
        self.lbl_active_year.configure(text=f"Année Académique : {year_label}")

    def render_student_table(self, students: list):
        for widget in self.scrollable_table.winfo_children():
            widget.destroy()

        for idx, (_, width) in enumerate(self.columns):
            self.scrollable_table.grid_columnconfigure(idx, weight=1, minsize=width)

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

        for row_idx, student in enumerate(students, start=1):
            bg_color = "#182232" if row_idx % 2 == 0 else "#111827"

            values = [
                student["student_id_number"],
                student["full_name"],
                student["program"],
                student["class_group"],
                student["enrollment_type"],
                student["status"],
                student["enrollment_date"],
            ]

            for col_idx, val in enumerate(values):
                text_color = "#e5e7eb"
                if col_idx == 4:
                    text_color = "#38bdf8" if val == "Nouveau" else "#c084fc"

                lbl = ctk.CTkLabel(
                    self.scrollable_table,
                    text=val,
                    font=self.font_cell,
                    text_color=text_color,
                    anchor="w",
                    fg_color=bg_color,
                    height=30,
                )
                lbl.grid(row=row_idx, column=col_idx, sticky="ew", padx=1, pady=1)