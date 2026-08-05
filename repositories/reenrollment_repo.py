from sqlalchemy.orm import Session
from models import (
    Student,
    AcademicYear,
    AcademicYearStatus,
    Major,
    Level,
    Program,
    Fee,
    FeeType,
    Enrollment,
    EnrollmentStatus,
    ClassGroup,
    Receipt,
)


class ReEnrollmentRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_active_and_future_academic_years(self) -> list[AcademicYear]:
        """Récupère l'année académique active ainsi que toutes les années postérieures existantes en BDD."""
        all_years = (
            self.session.query(AcademicYear)
            .order_by(AcademicYear.start_date.asc())
            .all()
        )
        if not all_years:
            return []

        # Recherche de l'index de l'année ACTIVE
        active_idx = next(
            (i for i, y in enumerate(all_years) if y.status == AcademicYearStatus.ACTIVE),
            None,
        )

        # Si aucune année n'est marquée ACTIVE, on renvoie toutes les années par sécurité
        if active_idx is None:
            return all_years

        # Renvoie l'année active et toutes les années postérieures
        return all_years[active_idx:]

    def get_all_majors(self) -> list[Major]:
        return self.session.query(Major).order_by(Major.name).all()

    def get_all_levels(self) -> list[Level]:
        return self.session.query(Level).order_by(Level.name).all()

    def find_student_by_matricule(self, matricule: str) -> Student | None:
        return (
            self.session.query(Student)
            .filter_by(student_id_number=matricule)
            .one_or_none()
        )

    def find_academic_year_by_label(self, label: str) -> AcademicYear | None:
        clean_label = label.replace(" ", "").replace("–", "-").strip()
        for year in self.session.query(AcademicYear).all():
            if year.label.replace(" ", "").replace("–", "-").strip() == clean_label:
                return year
        return None

    def find_program(self, major_name: str, level_name: str) -> Program | None:
        return (
            self.session.query(Program)
            .join(Major)
            .join(Level)
            .filter(Major.name == major_name, Level.name == level_name)
            .one_or_none()
        )

    def get_reenrollment_fee(
        self, program_id: int, academic_year_id: int
    ) -> Fee | None:
        fee_type = (
            self.session.query(FeeType)
            .filter_by(code="RE_ENROLLMENT_FEE")
            .one_or_none()
        )
        if not fee_type:
            return None

        return (
            self.session.query(Fee)
            .filter_by(
                program_id=program_id,
                academic_year_id=academic_year_id,
                fee_type_id=fee_type.id,
            )
            .one_or_none()
        )

    def find_class_group(
        self, program_id: int, academic_year_id: int
    ) -> ClassGroup | None:
        return (
            self.session.query(ClassGroup)
            .filter_by(program_id=program_id, academic_year_id=academic_year_id)
            .order_by(ClassGroup.name)
            .first()
        )

    def is_student_enrolled(self, student_id: int, academic_year_id: int) -> bool:
        enrollment = (
            self.session.query(Enrollment)
            .filter_by(student_id=student_id, academic_year_id=academic_year_id)
            .one_or_none()
        )
        return enrollment is not None and enrollment.status == EnrollmentStatus.ACTIVE

    def get_next_receipt_number(self) -> int:
        last_receipt = (
            self.session.query(Receipt)
            .order_by(Receipt.receipt_number.desc())
            .first()
        )
        return (last_receipt.receipt_number + 1) if last_receipt else 10001