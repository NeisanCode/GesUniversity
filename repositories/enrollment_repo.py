from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from models import (
    AcademicYear,
    AcademicYearStatus,
    ClassGroup,
    Enrollment,
    Fee,
    FeeType,
    Level,
    Major,
    Payment,
    Program,
    Receipt,
    Student,
)
from .base_repo import BaseRepo


class EnrollmentRepo(BaseRepo[Enrollment]):
    def __init__(self, session: Session):
        super().__init__(session, Enrollment)

    # --- NOUVELLE MÉTHODE ---
    def get_receipt_with_details(self, receipt_id: int) -> Receipt | None:
        return (
            self.session.query(Receipt)
            .options(
                joinedload(Receipt.payment)
                .joinedload(Payment.enrollment)
                .options(
                    joinedload(Enrollment.student),
                    joinedload(Enrollment.academic_year),
                    joinedload(Enrollment.class_group)
                    .joinedload(ClassGroup.program)
                    .options(
                        joinedload(Program.major),
                        joinedload(Program.level),
                    ),
                )
            )
            .filter(Receipt.id == receipt_id)
            .first()
        )

    def get_active_academic_year(self) -> AcademicYear | None:
        return (
            self.session.query(AcademicYear)
            .filter(AcademicYear.status == AcademicYearStatus.ACTIVE)
            .order_by(AcademicYear.start_date.desc())
            .first()
        )

    def get_academic_years(self) -> list[AcademicYear]:
        return (
            self.session.query(AcademicYear)
            .order_by(AcademicYear.start_date.desc())
            .all()
        )

    def get_majors(self) -> list[Major]:
        return self.session.query(Major).order_by(Major.name).all()

    def get_levels(self) -> list[Level]:
        return self.session.query(Level).order_by(Level.name).all()

    def find_program(self, major_name: str, level_name: str) -> Program | None:
        return (
            self.session.query(Program)
            .join(Major, Program.major_id == Major.id)
            .join(Level, Program.level_id == Level.id)
            .filter(Major.name == major_name, Level.name == level_name)
            .first()
        )

    def get_class_group_for_program(
        self, program_id: int, academic_year_id: int
    ) -> ClassGroup | None:
        return (
            self.session.query(ClassGroup)
            .filter(
                ClassGroup.program_id == program_id,
                ClassGroup.academic_year_id == academic_year_id,
            )
            .first()
        )

    def get_registration_fee(
        self, program_id: int, academic_year_id: int
    ) -> Fee | None:
        return (
            self.session.query(Fee)
            .join(FeeType, Fee.fee_type_id == FeeType.id)
            .filter(
                Fee.program_id == program_id,
                Fee.academic_year_id == academic_year_id,
                FeeType.code == "REGISTRATION_FEE",
            )
            .first()
        )

    def get_registration_fee_for_year(self, academic_year_id: int) -> Fee | None:
        return (
            self.session.query(Fee)
            .join(FeeType, Fee.fee_type_id == FeeType.id)
            .filter(
                Fee.academic_year_id == academic_year_id,
                FeeType.code == "REGISTRATION_FEE",
            )
            .order_by(Fee.amount.desc())
            .first()
        )

    def get_student_by_email(self, email: str) -> Student | None:
        return (
            self.session.query(Student)
            .filter(func.lower(Student.email) == func.lower(email))
            .first()
        )

    def get_next_student_id_number(self, academic_year: AcademicYear) -> str:
        year_prefix = f"ETU{academic_year.start_date.year}"
        last_student = (
            self.session.query(Student)
            .filter(Student.student_id_number.like(f"{year_prefix}%"))
            .order_by(Student.id.desc())
            .first()
        )
        if last_student is None:
            sequence = 1
        else:
            last_sequence = int(
                last_student.student_id_number[len(year_prefix) :] or "0"
            )
            sequence = last_sequence + 1
        return f"{year_prefix}{sequence:04d}"
