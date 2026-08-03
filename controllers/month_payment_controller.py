import os
from tkinter import messagebox
from typing import TYPE_CHECKING
import webbrowser

from models import Month, PaymentMethod
from services import MonthlyPaymentService
from services.errors.exceptions import EtudiantNotFoundError, PaymentValidationError
from .utils import generate_receipt_pdf

if TYPE_CHECKING:
    from interfaces import MonthlyPaymentFormFrame


class MonthlyPaymentController:
    def __init__(self, view: "MonthlyPaymentFormFrame"):
        self.view = view
        self.service = MonthlyPaymentService()
        self.current_student = None
        self.current_enrollment = None
        self.current_installments = []

    def load_initial_options(self):
        """Initialise les listes déroulantes et remet la vue à zéro au démarrage."""
        months = [month.value for month in Month]
        payment_methods = [method.value for method in PaymentMethod]

        self.view.combo_month.configure(values=months)
        self.view.combo_method.configure(values=payment_methods)

        if months:
            self.view.combo_month.set(months[0])
        if payment_methods:
            self.view.combo_method.set(payment_methods[0])

        self.view.display_student_info(None, None)
        self.view.display_schedule([])

    def search_student(self):
        """Recherche l'étudiant et met à jour l'ensemble de l'interface."""
        registration_number = self.view.search_student_id.get().strip()
        if not registration_number:
            messagebox.showwarning(
                "Recherche étudiant", "Veuillez saisir un matricule."
            )
            return

        try:
            student, enrollment, installments = self.service.search_student(
                registration_number
            )
        except EtudiantNotFoundError:
            messagebox.showerror(
                "Étudiant introuvable",
                "Aucun étudiant ne correspond à ce matricule.",
            )
            self.current_student = None
            self.current_enrollment = None
            self.current_installments = []
            self.view.display_student_info(None, None, 0.0, 0.0, 0.0)
            self.view.display_schedule([])
            self.view.combo_month.configure(values=[], state="disabled")
            self.view.combo_month.set("")
            self.view.btn_submit.configure(state="disabled")
            return

        self.current_student = student
        self.current_enrollment = enrollment
        self.current_installments = installments

        # Formatage des mois (sans le préfixe 'Month.')
        formatted_installments = [
            {
                **inst,
                "month": (
                    inst["month"].value
                    if hasattr(inst["month"], "value")
                    else str(inst["month"])
                ),
            }
            for inst in installments
        ]

        # --- CALCULS FINANCIERS ---
        monthly_fee = installments[0]["amount"] if installments else 0.0
        total_fee = self.service.calculate_total_fee(installments)
        remaining_balance = self.service.calculate_remaining_balance(installments)

        # Récupération des mois impayés pour la boîte de sélection
        unpaid_months = self.service.get_available_months(
            [month for month in Month], installments
        )

        month_values = [
            month.value if hasattr(month, "value") else str(month)
            for month in unpaid_months
        ]

        # Envoi des données complètes à la vue
        self.view.display_student_info(
            student=student,
            enrollment=enrollment,
            monthly_fee=monthly_fee,
            total_fee=total_fee,
            remaining_balance=remaining_balance,
        )
        self.view.display_schedule(formatted_installments)

        # Mise à jour du menu déroulant des mois
        if month_values:
            self.view.combo_month.configure(values=month_values, state="normal")
            self.view.combo_month.set(month_values[0])
            self.view.btn_submit.configure(state="normal")
        else:
            # Si plus aucun mois impayé
            self.view.combo_month.configure(values=["Tout est réglé"], state="disabled")
            self.view.combo_month.set("Tout est réglé")
            self.view.btn_submit.configure(state="disabled")

    def on_month_selected(self, selected_month):
        """Action déclenchée lors du changement de mois dans le menu déroulant (si besoin)."""
        pass

    def process_payment(self):
        """Traite le paiement en s'appuyant sur MonthlyPaymentService."""
        if not self.current_enrollment:
            messagebox.showwarning(
                "Attention", "Veuillez d'abord rechercher un étudiant."
            )
            return

        remaining_balance = self.service.calculate_remaining_balance(
            self.current_installments
        )
        if remaining_balance <= 0 or not self.current_installments:
            messagebox.showinfo(
                "Scolarité Soldée",
                "Cet étudiant a déjà réglé la totalité de ses frais de scolarité pour cette année !",
            )
            return

        selected_month = self.view.get_selected_month()
        payment_method = self.view.get_payment_method()

        if not selected_month or not payment_method:
            messagebox.showwarning(
                "Champs requis", "Veuillez sélectionner un mois et un mode de paiement."
            )
            return

        amount_to_pay = self.service.get_installment_amount(
            self.current_installments, selected_month
        )

        if amount_to_pay <= 0:
            messagebox.showerror(
                "Erreur",
                f"Échéance introuvable ou invalide pour le mois de {selected_month}.",
            )
            return

        try:
            payment = self.service.record_payment(
                enrollment=self.current_enrollment,
                month_value=selected_month,
                amount_paid=amount_to_pay,
                payment_method_value=payment_method,
            )

            # Rafraîchir immédiatement l'étudiant pour avoir les objets BDD liés et chargés proprement
            self.search_student()

            # Récupérer le reçu fraîchement chargé
            matching_inst = next(
                (
                    inst
                    for inst in self.current_installments
                    if (
                        inst["month"].value == selected_month
                        if hasattr(inst["month"], "value")
                        else str(inst["month"]) == selected_month
                    )
                ),
                None,
            )
            receipt = matching_inst.get("receipt") if matching_inst else payment.receipt

            pdf_path = generate_receipt_pdf(receipt, output_dir="receipts")

            messagebox.showinfo(
                "Paiement Validé",
                f"Paiement de {amount_to_pay:,.0f} FCFA pour le mois de {selected_month} enregistré !\n"
                f"Reçu N° REC-{receipt.receipt_number:05d}",
            )

            if os.path.exists(pdf_path):
                webbrowser.open(os.path.abspath(pdf_path))

        except PaymentValidationError as exc:
            messagebox.showerror("Validation impossible", str(exc))
        except Exception as exc:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(exc)}")

    def reprint_receipt(self, month_value: str):
        """Permet de réimprimer le reçu d'un mois déjà réglé à partir des données pré-chargées."""
        if not self.current_installments:
            return

        try:
            # On cherche le dictionnaire de l'échéance correspondant au mois sélectionné
            matching_inst = next(
                (
                    inst
                    for inst in self.current_installments
                    if (
                        inst["month"].value == month_value
                        if hasattr(inst["month"], "value")
                        else str(inst["month"]) == month_value
                    )
                ),
                None,
            )

            receipt = matching_inst.get("receipt") if matching_inst else None

            if not receipt:
                messagebox.showerror(
                    "Reçu Introuvable",
                    f"Aucun reçu enregistré trouvé pour le mois de {month_value}.",
                )
                return

            # Génération et ouverture du PDF sans aucune nouvelle requête SQL
            pdf_path = generate_receipt_pdf(receipt, output_dir="receipts")

            if os.path.exists(pdf_path):
                webbrowser.open(os.path.abspath(pdf_path))

        except Exception as exc:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le reçu : {str(exc)}")


# ETU20240098
