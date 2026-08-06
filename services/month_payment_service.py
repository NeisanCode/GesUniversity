from datetime import date
from typing import Callable
from sqlalchemy.orm import Session

from models import PaymentReceiptDTO
from models import Enrollment, Month, Payment, PaymentMethod, Receipt
from repositories import MonthlyPaymentRepo
from services.errors.exceptions import EtudiantNotFoundError, PaymentValidationError


class MonthlyPaymentService:
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory

    def search_student(self, registration_number: str):
        with self.session_factory() as session:
            repo = MonthlyPaymentRepo(session)
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

            # --- CONVERSION EN DTO DANS LE SERVICE ---
            # Le repo renvoie les dictionnaires d'échéances. On convertit les objets Receipt
            # ORM contenus dans "receipt" en ReceiptDTO tant que la session est ouverte.
            dto_installments = []
            for inst in installments:
                inst_copy = dict(inst)
                receipt_orm = inst_copy.get("receipt")
                if receipt_orm is not None:
                    inst_copy["receipt"] = self._map_receipt_to_dto(
                        receipt_orm, enrollment
                    )
                dto_installments.append(inst_copy)

            return student, enrollment, dto_installments

    def record_payment(
        self,
        enrollment: Enrollment,
        month_value,
        amount_paid: float,
        payment_method_value: str,
    ) -> PaymentReceiptDTO:
        with self.session_factory() as session:
            repo = MonthlyPaymentRepo(session)

            # Re-charger l'enrollment dans la session active
            active_enrollment = repo.get_enrollment_for_student(enrollment.student)
            if not active_enrollment:
                raise PaymentValidationError("Inscription introuvable.")

            installment = repo.get_installment_for_enrollment_and_month(
                active_enrollment, month_value
            )
            if installment is None:
                raise PaymentValidationError(
                    "Le mois sélectionné n'existe pas pour cet étudiant."
                )

            existing_payment = repo.get_payment_for_installment(
                active_enrollment.id, installment.id
            )
            if existing_payment is not None:
                raise PaymentValidationError("Ce mois a déjà été payé.")

            payment_method = self._get_payment_method(payment_method_value)
            payment = Payment(
                enrollment_id=active_enrollment.id,
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

            # Attacher les relations au receipt avant le mapping
            receipt.payment = payment
            payment.installment = installment

            # Retourner directement un ReceiptDTO immunisé contre les erreurs de session
            return self._map_receipt_to_dto(receipt, active_enrollment)

    def _map_receipt_to_dto(self, receipt: Receipt, enrollment: Enrollment) -> PaymentReceiptDTO:
        """Helper privé pour transformer une entité ORM Receipt en ReceiptDTO sécurisé."""
        program = enrollment.class_group.program
        academic_year = enrollment.academic_year

        total_program_fees = sum(
            f.amount for f in program.fees if f.academic_year_id == academic_year.id
        )
        total_paid_so_far = sum(p.amount_paid for p in enrollment.payments)
        remaining_balance = max(0.0, total_program_fees - total_paid_so_far)

        payment = receipt.payment
        installment = payment.installment if payment else None

        month_name = "N/A"
        if installment and installment.month:
            month_name = (
                installment.month.value
                if hasattr(installment.month, "value")
                else str(installment.month)
            )

        return PaymentReceiptDTO(
            receipt_number=receipt.receipt_number,
            receipt_date=receipt.receipt_date,
            student_id_number=enrollment.student.student_id_number,
            student_last_name=enrollment.student.last_name,
            student_first_name=enrollment.student.first_name,
            payment_date=payment.payment_date if payment else date.today(),
            payment_method=(
                payment.payment_method.value
                if payment and hasattr(payment.payment_method, "value")
                else str(payment.payment_method)
            ),
            class_name=f"{program.major.name} - {program.level.name} ({enrollment.class_group.name})",
            academic_year_label=academic_year.label,
            month_name=month_name,
            amount_paid=payment.amount_paid if payment else 0.0,
            total_program_fees=total_program_fees,
            total_paid_so_far=total_paid_so_far,
            remaining_balance=remaining_balance,
        )

    # --- Méthodes inchangées ---
    def get_available_months(self, all_months, installments):
        paid_months = {item["month"] for item in installments if item.get("paid")}
        return [
            month
            for month in all_months
            if month not in paid_months
            and month in {item["month"] for item in installments if not item.get("paid")}
        ]

    def get_installment_amount(self, installments, month_value):
        for installment in installments:
            if self._matches_month(installment["month"], month_value):
                return installment["amount"]
        return 0.0

    def calculate_remaining_balance(self, installments):
        return sum(item["amount"] for item in installments if not item.get("paid"))

    def calculate_total_fee(self, installments):
        return sum(item["amount"] for item in installments)

    def calculate_total_paid(self, installments):
        return sum(item["amount"] for item in installments if item.get("paid"))

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