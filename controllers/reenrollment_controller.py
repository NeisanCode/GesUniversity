import tkinter.messagebox as messagebox
from typing import TYPE_CHECKING
from database import get_session
from services import ReEnrollmentService
from services.errors.exceptions import EtudiantNotFoundError, EnrollmentValidationError
from .utils import gen_reregistration_pdf

if TYPE_CHECKING:
    from interfaces import ReEnrollmentFormFrame


class ReEnrollmentController:
    def __init__(self, view: "ReEnrollmentFormFrame"):
        self.view = view
        self.service = ReEnrollmentService(session_factory=get_session)
        self.current_student = None

    def load_initial_options(self) -> None:
        """Initialise les valeurs et événements au démarrage de la vue."""
        self.view.set_academic_years(self.service.get_academic_years())
        self.view.set_majors(self.service.get_majors())
        self.view.set_levels(self.service.get_levels())
        self.view.set_payment_methods(self.service.get_payment_methods())

        self.view.configure_selection_callbacks(
            year_command=self.on_selection_changed,
            major_command=self.on_selection_changed,
            level_command=self.on_selection_changed,
        )

        self.view.select_default_academic_year()
        self.update_fee_display()

    def on_selection_changed(self, _value=None) -> None:
        self.update_fee_display()

    def update_fee_display(self) -> None:
        fee = self.service.get_reenrollment_fee(
            year_label=self.view.get_selected_academic_year(),
            major_name=self.view.get_selected_major(),
            level_name=self.view.get_selected_level(),
        )

        text = (
            f"Frais de réinscription : {fee:,.0f} FCFA"
            if fee
            else "Frais de réinscription : -- FCFA"
        )
        self.view.set_fee_amount(text)

    def search_student(self) -> None:
        matricule = self.view.get_student_matricule()
        if not matricule:
            messagebox.showwarning("Recherche", "Veuillez saisir un matricule.")
            return

        try:
            student = self.service.find_student_by_matricule(matricule)
            self.current_student = student
            self.view.set_student_information(student)
            self.view.submit_button.configure(state="normal")
        except EtudiantNotFoundError:
            self._handle_student_not_found()

    def submit_reenrollment(self) -> None:
        if not self.current_student:
            messagebox.showwarning(
                "Réinscription", "Veuillez d'abord rechercher un étudiant."
            )
            return

        year = self.view.get_selected_academic_year()
        major = self.view.get_selected_major()
        level = self.view.get_selected_level()
        payment_method = self.view.get_selected_payment_method()

        if (
            not year
            or year == "Sélectionner..."
            or not major
            or not level
            or not payment_method
        ):
            messagebox.showwarning(
                "Incomplet", "Veuillez remplir tous les champs du formulaire."
            )
            return

        try:
            receipt = self.service.register_reenrollment(
                matricule=self.current_student.student_id_number,
                year_label=year,
                major_name=major,
                level_name=level,
                payment_method=payment_method,
            )

            pdf_path = gen_reregistration_pdf(receipt, output_dir="receipts")
            messagebox.showinfo(
                "Succès",
                f"Réinscription enregistrée !\nReçu N° : REC-{receipt.receipt_number:05d}\nFichier : {pdf_path}",
            )

            self.current_student = None
            self.view.reset_after_submission()

        except EnrollmentValidationError as exc:
            messagebox.showerror("Validation", str(exc))
        except EtudiantNotFoundError:
            self._handle_student_not_found()
        except Exception as exc:
            messagebox.showerror(
                "Erreur Inattendue", f"Une erreur s'est produite : {exc}"
            )

    def _handle_student_not_found(self) -> None:
        messagebox.showerror(
            "Introuvable", "Aucun étudiant ne correspond à ce matricule."
        )
        self.current_student = None
        self.view.clear_student_information()
        self.view.submit_button.configure(state="disabled")
