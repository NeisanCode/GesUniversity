from datetime import date
from typing import Callable
from sqlalchemy.orm import Session

from models.models_dto import StudentDTO
from models import (
    AcademicYear,
    Enrollment,
    EnrollmentStatus,
    EnrollmentType,
    Fee,
    Payment,
    PaymentMethod,
    Receipt,
    Student,
    ReceiptDTO,
)
from repositories.enrollment_repo import EnrollmentRepo
from services.errors.exceptions import (
    DuplicateStudentEmailError,
    EnrollmentValidationError,
)


class EnrollmentService:

    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory

    def get_initial_options(self) -> dict:
        with self.session_factory() as session:
            repo = EnrollmentRepo(session)
            current_year = repo.get_active_academic_year()
            return {
                "academic_years": repo.get_academic_years(),
                "majors": repo.get_majors(),
                "levels": repo.get_levels(),
                "current_year": current_year,
                "registration_fee": self._get_registration_fee_for_year(
                    repo, current_year
                ),
            }

    def get_program_fee(self, major_name: str, level_name: str) -> Fee | None:
        with self.session_factory() as session:
            repo = EnrollmentRepo(session)
            current_year = repo.get_active_academic_year()
            if current_year is None:
                return None

            program = repo.find_program(major_name, level_name)
            if program is None:
                return None

            return repo.get_registration_fee(program.id, current_year.id)

    def register_student(self, dto: StudentDTO) -> dict:
        with self.session_factory() as session:
            repo = EnrollmentRepo(session)

            try:
                current_year = repo.get_active_academic_year()
                if current_year is None:
                    raise EnrollmentValidationError(
                        "Aucune année académique active n’est disponible."
                    )

                self._validate_dto(dto, current_year)
                self._ensure_email_is_available(dto.email, repo)

                program = repo.find_program(dto.filiere, dto.niveau_etude)
                if program is None:
                    raise EnrollmentValidationError(
                        "La filière et le niveau sélectionnés ne correspondent à aucun programme enregistré."
                    )

                class_group = repo.get_class_group_for_program(
                    program.id, current_year.id
                )
                if class_group is None:
                    raise EnrollmentValidationError(
                        "Aucune classe n’est encore définie pour cette filière pendant l’année académique active."
                    )

                fee = repo.get_registration_fee(program.id, current_year.id)
                if fee is None:
                    raise EnrollmentValidationError(
                        "Aucun frais d’inscription n’est défini pour ce programme pendant l’année académique active."
                    )

                # 1. Création de l'étudiant
                student = Student(
                    last_name=dto.nom.strip().upper(),
                    first_name=dto.prenom.strip().title(),
                    student_id_number=repo.get_next_student_id_number(current_year),
                    date_of_birth=dto.date_naissance,
                    email=dto.email.strip().lower(),
                    address=dto.adresse.strip(),
                )
                student = repo.create(student)

                # 2. Création de l'inscription
                enrollment = Enrollment(
                    student_id=student.id,
                    academic_year_id=current_year.id,
                    enrollment_date=date.today(),
                    class_group_id=class_group.id,
                    enrollment_type=EnrollmentType.NEW,
                    status=EnrollmentStatus.ACTIVE,
                )
                enrollment = repo.create(enrollment)

                # 3. Création du paiement
                payment_method = self._parse_payment_method(dto.mode_paiement)
                payment = Payment(
                    enrollment_id=enrollment.id,
                    installment_id=None,
                    payment_date=date.today(),
                    payment_method=payment_method,
                    amount_paid=fee.amount,
                )
                payment = repo.create(payment)

                # 4. Création du reçu
                receipt = Receipt(
                    payment_id=payment.id,
                    receipt_number=self._get_next_receipt_number(session),
                    receipt_date=date.today(),
                )
                receipt = repo.create(receipt)

                # Synchronisation pour générer les clés primaires en base
                session.flush()

                # Récupération de l'objet complet avec eager loading
                full_receipt = repo.get_receipt_with_details(receipt.id)

                # 5. Mappage vers un DTO indépendant de la BDD (avant commit & fermeture de session)
                receipt_dto = self._map_to_receipt_dto(full_receipt)

                session.commit()

                return {
                    "student_id_number": student.student_id_number,
                    "receipt": receipt_dto,
                }

            except Exception:
                session.rollback()
                raise

    def _map_to_receipt_dto(self, receipt: Receipt) -> ReceiptDTO:
        """Convertit une entité SQLAlchemy Receipt en un DTO pur Python."""
        payment = receipt.payment
        enrollment = payment.enrollment
        student = enrollment.student
        class_group = enrollment.class_group
        program = class_group.program

        return ReceiptDTO(
            receipt_number=receipt.receipt_number,
            receipt_date=receipt.receipt_date,
            student_id_number=student.student_id_number,
            student_full_name=f"{student.last_name} {student.first_name}",
            student_email=student.email,
            academic_year=enrollment.academic_year.label,
            major_name=program.major.name,
            level_name=program.level.name,
            class_group_name=class_group.name,
            payment_method=payment.payment_method.value,
            amount_paid=payment.amount_paid,
        )

    def _validate_dto(self, dto: StudentDTO, current_year: AcademicYear) -> None:
        if not dto.nom or not dto.nom.strip():
            raise EnrollmentValidationError("Le nom de l’étudiant est obligatoire.")
        if not dto.prenom or not dto.prenom.strip():
            raise EnrollmentValidationError("Le prénom de l’étudiant est obligatoire.")
        if not dto.email or not dto.email.strip():
            raise EnrollmentValidationError("L’adresse email est obligatoire.")
        if not dto.adresse or not dto.adresse.strip():
            raise EnrollmentValidationError("L’adresse physique est obligatoire.")
        if not dto.filiere or not dto.filiere.strip():
            raise EnrollmentValidationError("La filière d’études est obligatoire.")
        if not dto.niveau_etude or not dto.niveau_etude.strip():
            raise EnrollmentValidationError("Le niveau d’étude est obligatoire.")
        if dto.annee_academique != current_year.label:
            raise EnrollmentValidationError(
                "L’inscription doit être réalisée sur l’année académique active en cours."
            )

    def _ensure_email_is_available(self, email: str, repo: EnrollmentRepo) -> None:
        normalized_email = email.strip().lower()
        if not normalized_email:
            raise EnrollmentValidationError("L’adresse email est obligatoire.")
        if repo.get_student_by_email(normalized_email) is not None:
            raise DuplicateStudentEmailError(
                "Cet email est déjà utilisé par un étudiant. Veuillez en saisir un autre."
            )

    def _parse_payment_method(self, method_name: str) -> PaymentMethod:
        for method in PaymentMethod:
            if method.value == method_name:
                return method
        raise EnrollmentValidationError("Le mode de paiement sélectionné est invalide.")

    def _get_next_receipt_number(self, session: Session) -> int:
        last_receipt = session.query(Receipt).order_by(Receipt.id.desc()).first()
        return (last_receipt.receipt_number if last_receipt else 0) + 1

    def _get_registration_fee_for_year(
        self, repo: EnrollmentRepo, current_year: AcademicYear | None
    ):
        if current_year is None:
            return None
        return repo.get_registration_fee_for_year(current_year.id)
