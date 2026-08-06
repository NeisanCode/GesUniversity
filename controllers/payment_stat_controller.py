import os
import platform
import subprocess
from typing import TYPE_CHECKING
from tkinter import messagebox
from database import get_session
from services import PaymentStatsService
from .utils import payment_stat_pdf

if TYPE_CHECKING:
    from interfaces import PaymentStatsFormFrame


class PaymentStatsController:
    def __init__(self, view: "PaymentStatsFormFrame"):
        self.view = view
        self.service = PaymentStatsService(get_session)
        self.selected_program_id: int | None = None
        self.active_year_id: int | None = None
        self.current_students_data: list[dict] = []

    def _set_loading(self, loading: bool):
        top = self.view.winfo_toplevel()
        cursor_style = "watch" if loading else ""
        top.configure(cursor=cursor_style)
        top.update_idletasks()

    def load_initial_data(self):
        self._set_loading(True)
        try:
            year_id, year_label = self.service.get_active_year_info()
            self.active_year_id = year_id
            self.view.update_active_year_display(year_label)
            self.on_program_search_changed()
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
        self._set_loading(True)
        try:
            self.selected_program_id = program_id
            if program_id and self.active_year_id:
                classes = self.service.get_classes_for_program(
                    program_id=program_id, academic_year_id=self.active_year_id
                )
                self.view.update_class_combobox(classes)
            else:
                self.view.update_class_combobox([])

            self.refresh_stats()
        finally:
            self._set_loading(False)

    def refresh_stats(self):
        self._set_loading(True)
        try:
            class_id = self.view.get_selected_class_id()
            selected_month = self.view.combo_month.get()

            if not self.selected_program_id or not class_id or not self.active_year_id:
                self.current_students_data = []
                self.view.render_students_table([])
                return

            self.current_students_data = self.service.get_payment_stats_for_class(
                class_group_id=class_id,
                month_value=selected_month,
                academic_year_id=self.active_year_id,
            )
            self.view.render_students_table(self.current_students_data)
        finally:
            self._set_loading(False)

    def export_pdf_report(self, only_unpaid: bool = False):
        """Génère le PDF et l'ouvre automatiquement."""
        if not self.current_students_data:
            messagebox.showwarning("Attention", "Aucune donnée disponible à exporter.")
            return

        students_to_export = self.current_students_data
        if only_unpaid:
            students_to_export = [s for s in self.current_students_data if not s["is_paid"]]
            if not students_to_export:
                messagebox.showinfo("Information", "Aucun élève en retard de paiement trouvé.")
                return

        self._set_loading(True)
        try:
            selected_month = self.view.combo_month.get()
            selected_class = self.view.combo_class.get()
            selected_program = self.view.get_selected_program_label()
            academic_year_label = self.view.lbl_active_year.cget("text").replace("Année Académique : ", "")

            pdf_path = payment_stat_pdf(
                month_name=selected_month,
                class_name=selected_class,
                program_name=selected_program,
                academic_year=academic_year_label,
                students=students_to_export,
                only_unpaid=only_unpaid
            )

            # Ouverture du fichier avec la visionneuse par défaut
            if platform.system() == "Linux":
                subprocess.Popen(["xdg-open", pdf_path])
            elif platform.system() == "Windows":
                os.startfile(pdf_path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", pdf_path])

        except Exception as e:
            messagebox.showerror("Erreur PDF", f"Impossible de générer le PDF : {str(e)}")
        finally:
            self._set_loading(False)

    def print_all_students(self):
        """Impression / Export PDF de TOUS les élèves (En règle + Impayés)."""
        self.export_pdf_report(only_unpaid=False)

    def print_unpaid_students(self):
        """Impression / Export PDF de SEULEMENT les impayés."""
        self.export_pdf_report(only_unpaid=True)