from typing import Sequence, Dict, Any
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
    Student,
    Fee,
    Payment,
)
from repositories.base_repo import BaseRepo


class StudentArchiveRepo(BaseRepo[Enrollment]):
    def __init__(self, session: Session):
        super().__init__(session, Enrollment)

    def get_previous_academic_years(self) -> Sequence[AcademicYear]:
        """Récupère toutes les années académiques antérieures (non actives / terminées)."""
        stmt = (
            select(AcademicYear)
            .where(AcademicYear.status != AcademicYearStatus.ACTIVE)
            .order_by(AcademicYear.start_date.desc())
        )
        return self.session.scalars(stmt).all()

    def search_programs(self, query: str | None = None) -> Sequence[Program]:
        """Recherche les programmes par filière ou niveau."""
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

    def get_past_enrolled_students(
        self,
        program_id: int | None = None,
        year_id: int | None = None,
        search_query: str | None = None,
        limit: int | None = 50,
    ) -> Sequence[Enrollment]:
        """Récupère les élèves inscrits dans des années antérieures à l'année en cours."""
        stmt = (
            select(Enrollment)
            .options(
                joinedload(Enrollment.student),
                joinedload(Enrollment.academic_year),
                joinedload(Enrollment.class_group)
                .joinedload(ClassGroup.program)
                .joinedload(Program.major),
                joinedload(Enrollment.class_group)
                .joinedload(ClassGroup.program)
                .joinedload(Program.level),
            )
            .join(Enrollment.student)
            .join(Enrollment.academic_year)
            .join(Enrollment.class_group)
            .where(AcademicYear.status != AcademicYearStatus.ACTIVE)
        )

        if year_id:
            stmt = stmt.where(Enrollment.academic_year_id == year_id)

        if program_id:
            stmt = stmt.where(ClassGroup.program_id == program_id)

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

    def get_student_financial_summary(self, enrollment_id: int) -> Dict[str, Any]:
        """Calcule la situation financière détaillée d'un élève pour une inscription donnée."""
        enrollment = (
            self.session.query(Enrollment)
            .options(
                joinedload(Enrollment.student),
                joinedload(Enrollment.academic_year),
                joinedload(Enrollment.class_group)
                .joinedload(ClassGroup.program)
                .joinedload(Program.major),
                joinedload(Enrollment.class_group)
                .joinedload(ClassGroup.program)
                .joinedload(Program.level),
            )
            .filter(Enrollment.id == enrollment_id)
            .first()
        )

        if not enrollment:
            return {}

        program_id = enrollment.class_group.program_id
        year_id = enrollment.academic_year_id

        # 1. Récupération des frais de scolarité associés au programme et à l'année
        fees = (
            self.session.query(Fee)
            .options(joinedload(Fee.installments), joinedload(Fee.fee_type))
            .filter(Fee.program_id == program_id, Fee.academic_year_id == year_id)
            .all()
        )

        total_due = sum(f.amount for f in fees)

        # 2. Récupération des paiements effectués par l'étudiant
        payments = (
            self.session.query(Payment)
            .options(joinedload(Payment.installment))
            .filter(Payment.enrollment_id == enrollment_id)
            .all()
        )

        total_paid = sum(p.amount_paid for p in payments)
        balance_remaining = max(0.0, total_due - total_paid)
        is_fully_paid = total_paid >= total_due and total_due > 0

        # 3. Détail par mois / échéances
        monthly_details = []
        for fee in fees:
            for inst in fee.installments:
                inst_payments = [p for p in payments if p.installment_id == inst.id]
                inst_paid = sum(p.amount_paid for p in inst_payments)
                inst_remaining = max(0.0, inst.amount - inst_paid)

                if inst_remaining == 0:
                    status = "Réglé"
                elif inst_paid > 0:
                    status = "Partiel"
                else:
                    status = "Non réglé"

                monthly_details.append(
                    {
                        "month": (
                            inst.month.value
                            if hasattr(inst.month, "value")
                            else str(inst.month)
                        ),
                        "fee_type": fee.fee_type.name,
                        "amount_due": inst.amount,
                        "amount_paid": inst_paid,
                        "remaining": inst_remaining,
                        "status": status,
                    }
                )

        return {
            "student_name": f"{enrollment.student.last_name.upper()} {enrollment.student.first_name}",
            "student_id_number": enrollment.student.student_id_number,
            "academic_year": enrollment.academic_year.label,
            "program": f"{enrollment.class_group.program.major.name} - {enrollment.class_group.program.level.name}",
            "class_group": enrollment.class_group.name,
            "total_due": total_due,
            "total_paid": total_paid,
            "balance_remaining": balance_remaining,
            "is_fully_paid": is_fully_paid,
            "monthly_details": monthly_details,
        }
