from datetime import date

from database import get_session
from models import (
    Enrollment,
    Fee,
    FeeType,
    Month,
    Payment,
    PaymentMethod,
    Receipt,
    Student,
)
from repositories import MonthlyPaymentRepo
from services.errors.exceptions import EtudiantNotFoundError, PaymentValidationError


class MonthlyPaymentService:
    def __init__(self):
        self.repo = None

    def _get_repo(self, session):
        if self.repo is None:
            self.repo = MonthlyPaymentRepo(session)
        return self.repo

    def search_student(self, registration_number: str):
        with get_session() as session:
            repo = self._get_repo(session)
            student = repo.find_student_by_registration(registration_number)
            if student is None:
                raise EtudiantNotFoundError(
                    "Aucun étudiant ne correspond à ce matricule."
                )

            enrollment = repo.get_enrollment_for_student(student)
            if enrollment is None:
                raise EtudiantNotFoundError(
                    "Cet étudiant n'a pas d'inscription active."
                )

            installments = repo.build_installment_summaries(enrollment)
            return student, enrollment, installments

    def get_available_months(self, all_months, installments):
        paid_months = {item["month"] for item in installments if item.get("paid")}
        return [
            month
            for month in all_months
            if month not in paid_months
            and month
            in {item["month"] for item in installments if not item.get("paid")}
        ]

    def get_installment_amount(self, installments, month_value):
        for installment in installments:
            if self._matches_month(installment["month"], month_value):
                return installment["amount"]
        return 0.0

    def calculate_remaining_balance(self, installments):
        return sum(item["amount"] for item in installments if not item.get("paid"))

    def calculate_total_fee(self, installments):
        """Calcule le montant total des frais de scolarité (somme de toutes les échéances)."""
        return sum(item["amount"] for item in installments)

    def calculate_total_paid(self, installments):
        """Calcule le montant total déjà réglé."""
        return sum(item["amount"] for item in installments if item.get("paid"))

    def record_payment(
        self,
        enrollment: Enrollment,
        month_value,
        amount_paid: float,
        payment_method_value: str,
    ):
        with get_session() as session:
            repo = self._get_repo(session)
            installment = repo.get_installment_for_enrollment_and_month(
                enrollment, month_value
            )
            if installment is None:
                raise PaymentValidationError(
                    "Le mois sélectionné n'existe pas pour cet étudiant."
                )

            existing_payment = repo.get_payment_for_installment(
                enrollment.id, installment.id
            )
            if existing_payment is not None:
                raise PaymentValidationError("Ce mois a déjà été payé.")

            payment_method = self._get_payment_method(payment_method_value)
            payment = Payment(
                enrollment_id=enrollment.id,
                installment_id=installment.id,
                payment_date=date.today(),
                payment_method=payment_method,
                amount_paid=amount_paid,
            )
            session.add(payment)
            session.flush()

            receipt_number = repo.get_next_receipt_number()
            receipt = Receipt(
                payment_id=payment.id,
                receipt_number=receipt_number,
                receipt_date=date.today(),
            )
            session.add(receipt)
            session.commit()
            _ = payment.receipt.receipt_number
            _ = payment.enrollment.student.first_name
            _ = (
                payment.enrollment.class_group.name
                if payment.enrollment.class_group
                else None
            )
            _ = payment.installment.month if payment.installment else None
            return payment

    def _matches_month(self, month, month_value):
        if isinstance(month_value, Month):
            return month == month_value
        if isinstance(month, Month):
            return month.value == month_value
        return str(month) == str(month_value)

    def _get_payment_method(self, payment_method_value: str) -> PaymentMethod:
        for method in PaymentMethod:
            if method.value == payment_method_value:
                return method
        raise PaymentValidationError("Le mode de paiement sélectionné est invalide.")
