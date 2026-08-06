from typing import TYPE_CHECKING
from tkinter import messagebox
from database import get_session
from services import StudentListService
from interfaces.form.student_edit_level import StudentEditModalLevel

if TYPE_CHECKING:
    from interfaces import StudentListFormFrame


class StudentListController:

    def __init__(self, view: "StudentListFormFrame"):
        self.view = view
        self.service = StudentListService(get_session)
        self.selected_program_id: int | None = None

    def _set_loading(self, loading: bool):
        """Active ou désactive le curseur de chargement sur l'ensemble de la fenêtre."""
        top = self.view.winfo_toplevel()
        cursor_style = "watch" if loading else ""
        top.configure(cursor=cursor_style)
        top.update_idletasks()

    def load_initial_data(self):
        self._set_loading(True)
        try:
            year_id, year_label = self.service.get_active_year_info()
            self.view.update_active_year_display(year_label)

            self.on_program_search_changed()
            self.refresh_student_list()
        finally:
            self._set_loading(False)

    def on_program_search_changed(self, *args):
        """Met à jour les boutons de programmes dans la sidebar à mesure qu'on tape."""
        self._set_loading(True)
        try:
            query = self.view.entry_program_search.get().strip()
            programs = self.service.search_programs(query if query else None)
            self.view.render_program_sidebar_list(programs)
        finally:
            self._set_loading(False)

    def select_program(self, program_id: int | None):
        """Sélectionne un programme depuis la sidebar et rafraîchit la liste."""
        self.selected_program_id = program_id
        self.refresh_student_list()

    def on_search_button_clicked(self):
        """Déclenché au clic sur le bouton 'Rechercher'."""
        self.refresh_student_list()

    def on_student_row_clicked(self, student_data: dict):
        """Déclenché au clic sur une ligne du tableau."""
        self._set_loading(True)
        try:
            programs = self.service.search_programs(query=None)

            StudentEditModalLevel(
                parent=self.view,
                student_data=student_data,
                programs_list=programs,
                get_classes_callback=self.service.get_classes_for_program,
                on_save_callback=self.save_student_changes,
            )
        finally:
            self._set_loading(False)

    def save_student_changes(self, payload: dict):
        """Appelée par la modale lors de la validation."""
        self._set_loading(True)
        try:
            success, error_message = self.service.update_student_info(
                student_id=payload["id"],
                last_name=payload["last_name"],
                first_name=payload["first_name"],
                email=payload.get("email", ""),
                address=payload.get("address", ""),
                class_group_name=payload["class_group"],
            )

            if success:
                self.refresh_student_list()
                messagebox.showinfo(
                    title="Succès",
                    message="Les informations de l'étudiant ont été mises à jour avec succès !"
                )
            else:
                messagebox.showerror(
                    title="Erreur de sauvegarde",
                    message=error_message or "Impossible de mettre à jour les informations de l'étudiant."
                )
        finally:
            self._set_loading(False)

    def refresh_student_list(self):
        self._set_loading(True)
        try:
            search_student = self.view.entry_student_search.get().strip()
            show_new = bool(self.view.chk_new_var.get())
            show_re = bool(self.view.chk_re_var.get())

            limit_val = self.view.combo_limit.get()
            if limit_val == "Tout":
                limit = None
            else:
                try:
                    limit = int(limit_val)
                except ValueError:
                    limit = 50

            students_data = self.service.get_enrolled_students(
                program_id=self.selected_program_id,
                show_new=show_new,
                show_re_enrollment=show_re,
                search_query=search_student if search_student else None,
                limit=limit,
            )

            self.view.render_student_table(students_data)
        finally:
            self._set_loading(False)