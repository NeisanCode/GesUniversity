# controllers/student_list_controller.py
from typing import TYPE_CHECKING

from database import get_session
from services.student_list_service import StudentListService

if TYPE_CHECKING:
    from interfaces import StudentListFormFrame


class StudentListController:

    def __init__(self, view: "StudentListFormFrame"):
        self.view = view
        self.service = StudentListService(get_session)
        self.selected_program_id: int | None = None

    def load_initial_data(self):
        year_id, year_label = self.service.get_active_year_info()
        self.view.update_active_year_display(year_label)
        
        # Charger tous les programmes dans la sidebar au démarrage
        self.on_program_search_changed()
        self.refresh_student_list()

    def on_program_search_changed(self, *args):
        """Met à jour les boutons de programmes dans la sidebar à mesure qu'on tape."""
        query = self.view.entry_program_search.get().strip()
        programs = self.service.search_programs(query if query else None)
        self.view.render_program_sidebar_list(programs)

    def select_program(self, program_id: int | None):
        """Sélectionne un programme depuis la sidebar et rafraîchit la liste."""
        self.selected_program_id = program_id
        self.refresh_student_list()

    def on_search_button_clicked(self):
        """Déclenché au clic sur le bouton 'Rechercher'."""
        self.refresh_student_list()

    def refresh_student_list(self):
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