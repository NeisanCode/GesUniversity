import customtkinter as ctk
from controllers import AcademicYearController


class AcademicYearFormFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        # Utilisation de CTkScrollableFrame avec couleur transparente
        super().__init__(parent, fg_color="transparent")

        self.controller = AcademicYearController(self)

        self.font_title = ("Helvetica", 16, "bold")
        self.font_section = ("Helvetica", 13, "bold")
        self.font_label = ("Helvetica", 11, "bold")
        self.font_body = ("Helvetica", 11)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_widgets()
        self.controller.load_initial_data()

    def _create_widgets(self):
        # Conteneur central délimité
        card_container = ctk.CTkFrame(
            self,
            fg_color="#1f2937",
            corner_radius=12,
            border_width=1,
            border_color="#374151",
        )
        card_container.grid(row=0, column=0, sticky="n", padx=20, pady=20)
        card_container.grid_columnconfigure(0, minsize=420)

        # En-tête
        lbl_main_title = ctk.CTkLabel(
            card_container,
            text="Gestion des années académiques",
            font=self.font_title,
            text_color="#ffffff",
            anchor="w",
        )
        lbl_main_title.pack(fill="x", padx=20, pady=(20, 15))

        # --- SECTION 1: Année académique active ---
        frame_active = ctk.CTkFrame(
            card_container,
            fg_color="#111827",
            corner_radius=8,
            border_width=1,
            border_color="#374151",
        )
        frame_active.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(
            frame_active,
            text="Année académique active",
            font=self.font_section,
            text_color="#ffffff",
        ).pack(anchor="w", padx=15, pady=(12, 8))

        ctk.CTkLabel(
            frame_active, text="Année", font=self.font_label, text_color="#9ca3af"
        ).pack(anchor="w", padx=15, pady=(2, 2))

        self.lbl_active_year_val = ctk.CTkEntry(
            frame_active,
            fg_color="#1f2937",
            border_color="#374151",
            text_color="#e5e7eb",
            height=32,
        )
        self.lbl_active_year_val.pack(fill="x", padx=15, pady=(0, 8))

        ctk.CTkLabel(
            frame_active, text="Statut", font=self.font_label, text_color="#9ca3af"
        ).pack(anchor="w", padx=15, pady=(2, 2))

        self.badge_active_status = ctk.CTkButton(
            frame_active,
            text="Actif",
            fg_color="#10b981",
            hover_color="#10b981",
            text_color="#ffffff",
            height=24,
            width=70,
            corner_radius=12,
            font=("Helvetica", 10, "bold"),
        )
        self.badge_active_status.pack(anchor="w", padx=15, pady=(0, 15))

        # --- SECTION 2: Prochaine année ---
        frame_next = ctk.CTkFrame(
            card_container,
            fg_color="#111827",
            corner_radius=8,
            border_width=1,
            border_color="#374151",
        )
        frame_next.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(
            frame_next,
            text="Prochaine année",
            font=self.font_section,
            text_color="#ffffff",
        ).pack(anchor="w", padx=15, pady=(12, 8))

        ctk.CTkLabel(
            frame_next, text="Année", font=self.font_label, text_color="#9ca3af"
        ).pack(anchor="w", padx=15, pady=(2, 2))

        self.entry_next_year = ctk.CTkEntry(
            frame_next,
            fg_color="#1f2937",
            border_color="#374151",
            text_color="#e5e7eb",
            height=32,
        )
        self.entry_next_year.pack(fill="x", padx=15, pady=(0, 8))

        ctk.CTkLabel(
            frame_next, text="Statut actuel", font=self.font_label, text_color="#9ca3af"
        ).pack(anchor="w", padx=15, pady=(2, 2))

        self.badge_next_status = ctk.CTkButton(
            frame_next,
            text="En attente",
            fg_color="#f59e0b",
            hover_color="#f59e0b",
            text_color="#ffffff",
            height=24,
            width=85,
            corner_radius=12,
            font=("Helvetica", 10, "bold"),
        )
        self.badge_next_status.pack(anchor="w", padx=15, pady=(0, 15))

        # --- SECTION 3: Avertissement ---
        frame_warning = ctk.CTkFrame(
            card_container,
            fg_color="#451a03",
            corner_radius=8,
            border_width=1,
            border_color="#78350f",
        )
        frame_warning.pack(fill="x", padx=20, pady=(0, 15))

        lbl_warn_title = ctk.CTkLabel(
            frame_warning, text="Attention", font=self.font_label, text_color="#fde047"
        )
        lbl_warn_title.pack(anchor="w", padx=12, pady=(10, 2))

        lbl_warn_text = ctk.CTkLabel(
            frame_warning,
            text="Cette opération clôturera définitivement l'année active et réinitialisera les inscriptions pour la prochaine année académique.",
            font=self.font_body,
            text_color="#fef08a",
            wraplength=380,
            justify="left",
        )
        lbl_warn_text.pack(anchor="w", padx=12, pady=(0, 10))

        # --- Bouton d'action ---
        btn_close = ctk.CTkButton(
            card_container,
            text="Clôturer l'année académique",
            command=self.controller.close_academic_year,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            height=40,
            font=("Helvetica", 12, "bold"),
        )
        btn_close.pack(fill="x", padx=20, pady=(10, 25))

    def update_active_year_display(self, label: str, status: str):
        self.lbl_active_year_val.configure(state="normal")
        self.lbl_active_year_val.delete(0, "end")
        self.lbl_active_year_val.insert(0, label)
        self.lbl_active_year_val.configure(state="readonly")
        self.badge_active_status.configure(text=status)

    def set_next_year_input(self, label: str):
        self.entry_next_year.configure(state="normal")
        self.entry_next_year.delete(0, "end")
        self.entry_next_year.insert(0, label)
        self.entry_next_year.configure(state="readonly")

    def get_next_year_input(self) -> str:
        return self.entry_next_year.get().strip()