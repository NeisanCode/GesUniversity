from typing import TYPE_CHECKING
from database import get_session
from services import StudentArchiveService
from interfaces.form.student_archives.student_financial_level import StudentFinancialModal


if TYPE_CHECKING:
    from interfaces import StudentArchiveForm


class StudentArchiveController:

    def __init__(self, view: "StudentArchiveForm"):
        self.view = view
        self.service = StudentArchiveService(get_session)
        self.selected_program_id: int | None = None
        self.selected_year_id: int | None = None

    def _set_loading(self, loading: bool):
        top = self.view.winfo_toplevel()
        cursor_style = "watch" if loading else ""
        top.configure(cursor=cursor_style)
        top.update_idletasks()

    def load_initial_data(self):
        self._set_loading(True)
        try:
            years = self.service.get_previous_years()
            self.view.render_years_combo(years)

            self.on_program_search_changed()
            self.refresh_student_list()
        finally:
            self._set_loading(False)

    def on_program_search_changed(self, *args):
        self._set_loading(True)
        try:
            query = self.view.entry_program_search.get().strip()
            programs = self.service.search_programs(query if query else None)
            self.view.render_program_sidebar_list(programs)
        finally:
            self._set_loading(False)

    def select_program(self, program_id: int | None):
        self.selected_program_id = program_id
        self.refresh_student_list()

    def on_year_selected(self, year_id: int | None):
        self.selected_year_id = year_id
        self.refresh_student_list()

    def on_search_button_clicked(self):
        self.refresh_student_list()

    def on_student_row_clicked(self, student_data: dict):
        """Déclenché au clic sur un étudiant : ouvre la modal financière."""
        self._set_loading(True)
        try:
            enrollment_id = student_data["enrollment_id"]
            financial_info = self.service.get_student_financial_details(enrollment_id)

            if financial_info:
                StudentFinancialModal(
                    parent=self.view,
                    financial_data=financial_info,
                )
        finally:
            self._set_loading(False)

    def refresh_student_list(self):
        self._set_loading(True)
        try:
            search_student = self.view.entry_student_search.get().strip()

            limit_val = self.view.combo_limit.get()
            if limit_val == "Tout":
                limit = None
            else:
                try:
                    limit = int(limit_val)
                except ValueError:
                    limit = 50

            students_data = self.service.get_past_students(
                program_id=self.selected_program_id,
                year_id=self.selected_year_id,
                search_query=search_student if search_student else None,
                limit=limit,
            )

            self.view.render_student_table(students_data)
        finally:
            self._set_loading(False)