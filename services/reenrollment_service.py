from datetime import date
from typing import Callable
from sqlalchemy.orm import Session

from models import (
    Student,
    Enrollment,
    EnrollmentType,
    EnrollmentStatus,
    Payment,
    Receipt,
    PaymentMethod,
)
from models.models_dto import RegistrationReceiptDTO
from repositories import ReEnrollmentRepo
from services.errors.exceptions import EtudiantNotFoundError, EnrollmentValidationError


class ReEnrollmentService:
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory

    def get_academic_years(self) -> list[str]:
        """Récupère les libellés des années académiques disponibles pour la réinscription."""
        with self.session_factory() as session:
            repo = ReEnrollmentRepo(session)
            db_years = repo.get_active_and_future_academic_years()
            return [y.label for y in db_years]

    def get_majors(self) -> list[str]:
        with self.session_factory() as session:
            repo = ReEnrollmentRepo(session)
            return [m.name for m in repo.get_all_majors()]

    def get_levels(self) -> list[str]:
        with self.session_factory() as session:
            repo = ReEnrollmentRepo(session)
            return [l.name for l in repo.get_all_levels()]

    def get_payment_methods(self) -> list[str]:
        return [method.value for method in PaymentMethod]

    def find_student_by_matricule(self, matricule: str) -> Student:
        with self.session_factory() as session:
            repo = ReEnrollmentRepo(session)
            student = repo.find_student_by_matricule(matricule)
            if not student:
                raise EtudiantNotFoundError()
            return student

    def get_reenrollment_fee(
        self, year_label: str, major_name: str, level_name: str
    ) -> float | None:
        if not year_label or year_label == "Sélectionner...":
            return None

        with self.session_factory() as session:
            repo = ReEnrollmentRepo(session)
            year = repo.find_academic_year_by_label(year_label)
            program = repo.find_program(major_name, level_name)

            if not year or not program:
                return None

            fee = repo.get_reenrollment_fee(program.id, year.id)
            return fee.amount if fee else None

    def register_reenrollment(
        self,
        matricule: str,
        year_label: str,
        major_name: str,
        level_name: str,
        payment_method: str,
    ) -> RegistrationReceiptDTO:
        with self.session_factory() as session:
            repo = ReEnrollmentRepo(session)

            # 1. Validation des entités
            student = repo.find_student_by_matricule(matricule)
            if not student:
                raise EtudiantNotFoundError()

            year = repo.find_academic_year_by_label(year_label)
            if not year:
                raise EnrollmentValidationError("Année académique invalide.")

            program = repo.find_program(major_name, level_name)
            if not program:
                raise EnrollmentValidationError(
                    "Programme introuvable pour cette filière et ce niveau."
                )

            class_group = repo.find_class_group(program.id, year.id)
            if not class_group:
                raise EnrollmentValidationError(
                    "Aucune classe disponible pour ce programme cette année."
                )

            # 2. Vérification d'unicité (Double réinscription)
            if repo.is_student_enrolled(student.id, year.id):
                raise EnrollmentValidationError(
                    "Cet étudiant est déjà réinscrit pour cette année académique."
                )

            fee = repo.get_reenrollment_fee(program.id, year.id)
            if not fee:
                raise EnrollmentValidationError(
                    "Les frais de réinscription ne sont pas configurés pour ce programme."
                )

            # 3. Enregistrement des données (Transaction)
            enrollment = Enrollment(
                student_id=student.id,
                academic_year_id=year.id,
                class_group_id=class_group.id,
                enrollment_date=date.today(),
                enrollment_type=EnrollmentType.RE_ENROLLMENT,
                status=EnrollmentStatus.ACTIVE,
            )
            session.add(enrollment)
            session.flush()

            payment = Payment(
                enrollment_id=enrollment.id,
                installment_id=None,
                payment_date=date.today(),
                payment_method=payment_method,
                amount_paid=fee.amount,
            )
            session.add(payment)
            session.flush()

            receipt_num = repo.get_next_receipt_number()
            receipt = Receipt(
                payment_id=payment.id,
                receipt_number=receipt_num,
                receipt_date=date.today(),
            )
            session.add(receipt)
            session.commit()

            # Alignement complet avec le ReceiptDTO
            return RegistrationReceiptDTO(
                receipt_number=receipt_num,
                receipt_date=receipt.receipt_date,
                student_id_number=student.student_id_number,
                student_full_name=f"{student.first_name} {student.last_name}",
                student_email=student.email,
                academic_year=year.label,
                major_name=major_name,
                level_name=level_name,
                class_group_name=class_group.name,
                payment_method=payment_method,
                amount_paid=fee.amount,
            )