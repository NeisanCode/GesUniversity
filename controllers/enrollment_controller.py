from datetime import date
import tkinter.messagebox as messagebox
from typing import TYPE_CHECKING

from database import get_session
from services import EnrollmentService
from models import StudentDTO
from .utils import generate_registration_pdf

if TYPE_CHECKING:
    from interfaces import EnrollmentFormFrame


class EnrollmentController:

    def __init__(self, view: "EnrollmentFormFrame"):
        """:param view: Instance of EnrollmentFormFrame (the UI view)"""
        self.view = view
        self.service = EnrollmentService(get_session)

    def validate_fields(self) -> StudentDTO | None:
        """Extracts and validates data from the enrollment form.

        Returns an EtudiantDTO if valid, otherwise displays an error dialog
        and returns None.
        """
        last_name = self.view.entry_nom.get().strip()
        first_name = self.view.entry_prenom.get().strip()
        email = self.view.entry_email.get().strip()
        address = self.view.entry_adresse.get().strip()
        academic_year = self.view.combo_annee.get().strip()
        major = self.view.combo_filiere.get().strip()
        level = self.view.combo_niveau.get().strip()
        payment_method = self.view.combo_paiement.get().strip()

        if not all(
            [
                last_name,
                first_name,
                email,
                address,
                academic_year,
                major,
                level,
                payment_method,
            ]
        ):
            messagebox.showerror(
                "Erreur", "Veuillez remplir tous les champs du formulaire."
            )
            return None

        try:
            birth_date = date.fromisoformat(self.view.date_picker.get().strip())
        except ValueError:
            messagebox.showerror(
                "Erreur", "La date de naissance doit être au format AAAA-MM-JJ."
            )
            return None

        return StudentDTO(
            nom=last_name,
            prenom=first_name,
            date_naissance=birth_date,
            email=email,
            adresse=address,
            annee_academique=academic_year,
            filiere=major,
            niveau_etude=level,
            mode_paiement=payment_method,
        )

    def process_enrollment(self):
        """Triggered by the submission button click."""
        dto = self.validate_fields()
        if dto is None:
            return

        try:
            # 1. Enregistrement en BDD via le service
            result = self.service.register_student(dto)

            # 2. Génération du reçu d'inscription au format PDF
            receipt_obj = result["receipt"]
            pdf_path = generate_registration_pdf(receipt_obj)

        except Exception as exc:
            messagebox.showerror(
                "Échec de l'inscription", f"L'inscription a été annulée :\n{exc}"
            )
            return

        self.reset_form()
        messagebox.showinfo(
            "Inscription réussie",
            f"L'inscription a bien été enregistrée.\n\n"
            f"Matricule : {result['student_id_number']}\n"
            f"Reçu PDF généré : {pdf_path}",
        )

    def reset_form(self):
        """Clears inputs and reloads initial options after a successful
        registration."""
        self.view.entry_nom.delete(0, "end")
        self.view.entry_prenom.delete(0, "end")
        self.view.entry_email.delete(0, "end")
        self.view.entry_adresse.delete(0, "end")
        self.view.date_picker.set("")
        self.load_initial_options()

    def load_initial_options(self):
        """Loads and populates initial options for the form dropdowns."""
        options = self.service.get_initial_options()
        majors = options.get("majors", [])
        levels = options.get("levels", [])
        current_year = options.get("current_year")

        # 1. Restrict Academic Year strictly to the active year
        if current_year is not None:
            self.view.combo_annee.configure(values=[current_year.label])
            self.view.combo_annee.set(current_year.label)
        else:
            self.view.combo_annee.configure(values=["Aucune année active"])
            self.view.combo_annee.set("Aucune année active")

        # 2. Populate Majors
        major_names = [major.name for major in majors]
        self.view.combo_filiere.configure(
            values=major_names if major_names else ["Sélectionner..."],
            command=self.update_fees,  # Callback triggered on major change
        )
        if major_names:
            self.view.combo_filiere.set(major_names[0])

        # 3. Populate Academic Levels
        level_names = [level.name for level in levels]
        self.view.combo_niveau.configure(
            values=level_names if level_names else ["Sélectionner..."],
            command=self.update_fees,  # Callback triggered on level change
        )
        if level_names:
            self.view.combo_niveau.set(level_names[0])

        # 4. Populate Payment Methods
        self.view.combo_paiement.configure(
            values=[m.value for m in __import__("models").PaymentMethod]
        )
        self.view.combo_paiement.set("Espèces")

        # 5. Compute registration fees immediately for default values
        self.update_fees()

    def update_fees(self, *args):
        """Recalculates and displays the registration fee based on selected
        major and level."""
        major = self.view.combo_filiere.get().strip()
        level = self.view.combo_niveau.get().strip()

        if major in ("", "Sélectionner...") or level in ("", "Sélectionner..."):
            self.view.fees_label.configure(
                text="Montant des frais d'inscription : -- FCFA"
            )
            return

        try:
            fee = self.service.get_program_fee(major, level)
            if fee is not None:
                self.view.fees_label.configure(
                    text=f"Montant des frais d'inscription : {fee.amount:,.0f} FCFA"
                )
            else:
                self.view.fees_label.configure(
                    text="Montant des frais d'inscription : Non défini"
                )
        except Exception:
            self.view.fees_label.configure(
                text="Montant des frais d'inscription : -- FCFA"
            )
