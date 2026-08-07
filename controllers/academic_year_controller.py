from typing import TYPE_CHECKING
from tkinter import messagebox
from database import get_session
from services import AcademicYearService

if TYPE_CHECKING:
    from interfaces import  AcademicYearFormFrame


class AcademicYearController:
    def __init__(self, view: "AcademicYearFormFrame"):
        self.view = view
        self.service = AcademicYearService(get_session)
        self.current_active_id: int | None = None

    def _set_loading(self, loading: bool):
        top = self.view.winfo_toplevel()
        cursor_style = "watch" if loading else ""
        top.configure(cursor=cursor_style)
        top.update_idletasks()

    def load_initial_data(self):
        self._set_loading(True)
        try:
            data = self.service.get_academic_years_info()
            active_year = data.get("active_year")
            next_suggestion = data.get("next_year_suggestion", "")

            if active_year:
                self.current_active_id = active_year["id"]
                self.view.update_active_year_display(
                    label=active_year["label"], status=active_year["status"]
                )
            else:
                self.current_active_id = None
                self.view.update_active_year_display(
                    label="Aucune année active", status="N/A"
                )

            self.view.set_next_year_input(next_suggestion)
        finally:
            self._set_loading(False)

    def close_academic_year(self):
        if not self.current_active_id:
            messagebox.showwarning(
                "Action impossible", "Aucune année académique active à clôturer."
            )
            return

        next_label = self.view.get_next_year_input()
        
        confirm = messagebox.askyesno(
            "Confirmation de clôture",
            f"Êtes-vous sûr de vouloir clôturer l'année en cours et démarrer l'année {next_label} ?\n\n"
            "Cette action archivera l'année actuelle en 'Terminé' et permettra les réinscriptions sur la nouvelle.",
        )

        if not confirm:
            return

        self._set_loading(True)
        try:
            success, error_msg = self.service.close_and_start_new_year(
                current_year_id=self.current_active_id,
                new_label=next_label,
            )

            if success:
                messagebox.showinfo(
                    "Succès",
                    f"L'année académique {next_label} est désormais active !",
                )
                self.load_initial_data()
            else:
                messagebox.showerror(
                    "Erreur", error_msg or "Une erreur est survenue."
                )
        finally:
            self._set_loading(False)