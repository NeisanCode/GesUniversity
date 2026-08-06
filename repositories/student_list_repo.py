# repositories/student_list_repo.py
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
    EnrollmentType,
    Student,
)
from repositories.base_repo import BaseRepo


class StudentListRepo(BaseRepo[Enrollment]):
    def __init__(self, session: Session):
        super().__init__(session, Enrollment)

    def get_active_academic_year(self) -> AcademicYear | None:
        """Récupère l'année académique active."""
        stmt = select(AcademicYear).where(
            AcademicYear.status == AcademicYearStatus.ACTIVE
        )
        return self.session.scalars(stmt).first()

    def search_programs(self, query: str | None = None) -> Sequence[Program]:
        """Recherche les programmes/filières correspondant au texte saisi."""
        stmt = select(Program).options(
            joinedload(Program.major), joinedload(Program.level)
        )
        if query:
            term = f"%{query.strip()}%"
            stmt = stmt.join(Program.major).join(Program.level).where(
                or_(
                    Major.name.ilike(term),
                    Level.name.ilike(term),
                )
            )
        return self.session.scalars(stmt).unique().all()

    def get_enrolled_students(
        self,
        academic_year_id: int,
        program_id: int | None = None,
        types: list[EnrollmentType] | None = None,
        search_query: str | None = None,
        limit: int | None = 50,
    ) -> Sequence[Enrollment]:
        """Récupère les inscriptions filtrées par ID de programme et recherche d'étudiant."""
        stmt = (
            select(Enrollment)
            .options(
                joinedload(Enrollment.student),
                joinedload(Enrollment.class_group)
                .joinedload(ClassGroup.program)
                .joinedload(Program.major),
                joinedload(Enrollment.class_group)
                .joinedload(ClassGroup.program)
                .joinedload(Program.level),
                joinedload(Enrollment.academic_year),
            )
            .join(Enrollment.student)
            .join(Enrollment.class_group)
            .where(Enrollment.academic_year_id == academic_year_id)
        )

        if program_id:
            stmt = stmt.where(ClassGroup.program_id == program_id)

        if types:
            stmt = stmt.where(Enrollment.enrollment_type.in_(types))
        elif types is not None and len(types) == 0:
            return []

        if search_query:
            s_term = f"%{search_query.strip()}%"
            stmt = stmt.where(
                or_(
                    Student.first_name.ilike(s_term),
                    Student.last_name.ilike(s_term),
                    Student.student_id_number.ilike(s_term),
                )
            )

        stmt = stmt.order_by(Enrollment.id.desc())

        if limit is not None:
            stmt = stmt.limit(limit)

        return self.session.scalars(stmt).unique().all()