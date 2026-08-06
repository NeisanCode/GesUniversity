from typing import Sequence
from sqlalchemy import select, or_
from sqlalchemy.orm import Session, joinedload

from models import (
    Enrollment,
    AcademicYear,
    AcademicYearStatus,
    ClassGroup,
    Program,
    Major,
    Level,
    Payment,
)
from repositories.base_repo import BaseRepo


class PaymentStatsRepo(BaseRepo[Enrollment]):
    def __init__(self, session: Session):
        super().__init__(session, Enrollment)

    def get_active_academic_year(self) -> AcademicYear | None:
        stmt = select(AcademicYear).where(
            AcademicYear.status == AcademicYearStatus.ACTIVE
        )
        return self.session.scalars(stmt).first()

    def search_programs(self, query: str | None = None) -> Sequence[Program]:
        stmt = select(Program).options(
            joinedload(Program.major), joinedload(Program.level)
        )
        if query:
            term = f"%{query.strip()}%"
            stmt = (
                stmt.join(Program.major)
                .join(Program.level)
                .where(
                    or_(
                        Major.name.ilike(term),
                        Level.name.ilike(term),
                    )
                )
            )
        return self.session.scalars(stmt).unique().all()

    def get_class_groups_by_program_and_year(
        self, program_id: int, academic_year_id: int
    ) -> Sequence[ClassGroup]:
        stmt = (
            select(ClassGroup)
            .where(
                ClassGroup.program_id == program_id,
                ClassGroup.academic_year_id == academic_year_id,
            )
            .order_by(ClassGroup.name)
        )
        return self.session.scalars(stmt).all()

    def get_enrollments_by_class_and_year(
        self, class_group_id: int, academic_year_id: int
    ) -> Sequence[Enrollment]:
        stmt = (
            select(Enrollment)
            .options(
                joinedload(Enrollment.student),
                joinedload(Enrollment.class_group).joinedload(ClassGroup.program).joinedload(Program.level),
                joinedload(Enrollment.payments).joinedload(Payment.installment),
            )
            .where(
                Enrollment.class_group_id == class_group_id,
                Enrollment.academic_year_id == academic_year_id,
            )
            .order_by(Enrollment.id)
        )
        return self.session.scalars(stmt).unique().all()