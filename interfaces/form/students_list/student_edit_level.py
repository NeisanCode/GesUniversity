import customtkinter as ctk


class StudentEditModalLevel(ctk.CTkToplevel):
    def __init__(
        self,
        parent,
        student_data: dict,
        programs_list: list,
        get_classes_callback,
        on_save_callback,
    ):
        super().__init__(parent)

        self.student_data = student_data
        self.programs_list = programs_list
        self.get_classes_callback = get_classes_callback
        self.on_save_callback = on_save_callback

        self.title("Modifier l'étudiant")
        # Hauteur réduite pour s'adapter aux petits écrans (ex: 760p / 1080p avec scaling)
        self.geometry("500x560")
        self.resizable(False, True)
        self.configure(fg_color="#111827")

        self.transient(parent)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):
        # En-tête fixe
        ctk.CTkLabel(
            self,
            text="✏️ MODIFIER L'étudiant",
            font=("Helvetica", 13, "bold"),
            text_color="#38bdf8",
        ).pack(pady=(12, 8))

        # Zone scrollable pour TOUS les champs de saisie
        form_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#1f2937",
            corner_radius=8,
        )
        form_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # --- Champ BLOQUÉ : Matricule ---
        self._create_field(
            form_frame,
            "Matricule :",
            self.student_data.get("student_id_number", ""),
            disabled=True,
        )

        # --- Champs ÉDITABLES : Nom & Prénom ---
        full_name = self.student_data.get("full_name", "")
        parts = full_name.split(" ", 1)
        last_name = parts[0] if len(parts) > 0 else ""
        first_name = parts[1] if len(parts) > 1 else ""

        self.entry_last_name = self._create_field(form_frame, "Nom :", last_name)
        self.entry_first_name = self._create_field(form_frame, "Prénom :", first_name)

        # --- Champs ÉDITABLES : Email & Adresse ---
        self.entry_email = self._create_field(
            form_frame, "Email :", self.student_data.get("email", "")
        )
        self.entry_address = self._create_field(
            form_frame, "Adresse :", self.student_data.get("address", "")
        )

        # --- Dynamic Programme Dropdown ---
        ctk.CTkLabel(
            form_frame,
            text="Programme / Filière :",
            font=("Helvetica", 10, "bold"),
            text_color="#9ca3af",
        ).pack(anchor="w", padx=10, pady=(6, 1))

        program_labels = [p["label"] for p in self.programs_list]
        current_program = self.student_data.get("program", "")

        self.combo_program = ctk.CTkOptionMenu(
            form_frame,
            values=program_labels if program_labels else [current_program],
            command=self._on_program_changed,
            fg_color="#111827",
            button_color="#374151",
            text_color="#e5e7eb",
            dropdown_fg_color="#1f2937",
            height=28,
        )
        if current_program in program_labels:
            self.combo_program.set(current_program)
        self.combo_program.pack(fill="x", padx=10, pady=(0, 6))

        # --- Dynamic Classe Dropdown ---
        ctk.CTkLabel(
            form_frame,
            text="Classe :",
            font=("Helvetica", 10, "bold"),
            text_color="#9ca3af",
        ).pack(anchor="w", padx=10, pady=(6, 1))

        self.combo_class = ctk.CTkOptionMenu(
            form_frame,
            values=[],
            fg_color="#111827",
            button_color="#374151",
            text_color="#e5e7eb",
            dropdown_fg_color="#1f2937",
            height=28,
        )
        self.combo_class.pack(fill="x", padx=10, pady=(0, 6))

        # Initialise la liste des classes selon le programme courant
        self._on_program_changed(self.combo_program.get())

        current_class = self.student_data.get("class_group", "")
        if current_class in self.combo_class.cget("values"):
            self.combo_class.set(current_class)

        # --- Champs BLOQUÉS ---
        self._create_field(
            form_frame,
            "Type d'inscription :",
            self.student_data.get("enrollment_type", ""),
            disabled=True,
        )
        self._create_field(
            form_frame,
            "Statut :",
            self.student_data.get("status", ""),
            disabled=True,
        )

        # --- Zone FIXE en bas de la fenêtre pour les boutons ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 12))

        ctk.CTkButton(
            btn_frame,
            text="Annuler",
            font=("calibri", 15, "bold"),
            fg_color="#374151",
            hover_color="#4b5563",
            width=200,
            height=32,
            command=self.destroy,
        ).pack(side="left", fill="x")

        ctk.CTkButton(
            btn_frame,
            text="Enregistrer",
            font=("calibri", 15, "bold"),
            fg_color="#16a34a",
            hover_color="#15803d",
            width=220,
            height=32,
            command=self._on_save,
        ).pack(side="right", fill="x")

    def _on_program_changed(self, selected_program_label: str):
        selected_program = next(
            (p for p in self.programs_list if p["label"] == selected_program_label),
            None,
        )

        if selected_program:
            classes = self.get_classes_callback(selected_program["id"])
            if classes:
                self.combo_class.configure(values=classes)
                self.combo_class.set(classes[0])
            else:
                self.combo_class.configure(values=["Aucune classe disponible"])
                self.combo_class.set("Aucune classe disponible")

    def _create_field(
        self, parent, label_text: str, initial_value: str, disabled: bool = False
    ):
        ctk.CTkLabel(
            parent,
            text=label_text,
            font=("Helvetica", 10, "bold"),
            text_color="#9ca3af",
        ).pack(anchor="w", padx=10, pady=(4, 1))

        entry = ctk.CTkEntry(
            parent,
            fg_color="#111827" if not disabled else "#374151",
            border_color="#374151",
            text_color="#e5e7eb" if not disabled else "#9ca3af",
            height=28,
        )
        entry.insert(0, initial_value if initial_value else "")
        if disabled:
            entry.configure(state="disabled")
        entry.pack(fill="x", padx=10, pady=(0, 4))
        return entry

    def _on_save(self):
        updated_payload = {
            "id": self.student_data.get("id"),
            "last_name": self.entry_last_name.get().strip(),
            "first_name": self.entry_first_name.get().strip(),
            "email": self.entry_email.get().strip(),
            "address": self.entry_address.get().strip(),
            "class_group": self.combo_class.get(),
        }

        self.on_save_callback(updated_payload)
        self.destroy()
