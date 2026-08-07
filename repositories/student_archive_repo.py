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

        # 2. Récupération des paiements effectués par l'étudiant
        payments = (
            self.session.query(Payment)
            .options(joinedload(Payment.installment))
            .filter(Payment.enrollment_id == enrollment_id)
            .all()
        )

        # Ordre des mois pour l'année scolaire (Septembre à Août)
        school_month_order = {
            "SEPTEMBER": 1, "SEPTEMBRE": 1,
            "OCTOBER": 2, "OCTOBRE": 2,
            "NOVEMBER": 3, "NOVEMBRE": 3,
            "DECEMBER": 4, "DÉCEMBRE": 4, "DECEMBRE": 4,
            "JANUARY": 5, "JANVIER": 5,
            "FEBRUARY": 6, "FÉVRIER": 6, "FEVRIER": 6,
            "MARCH": 7, "MARS": 7,
            "APRIL": 8, "AVRIL": 8,
            "MAY": 9, "MAI": 9,
            "JUNE": 10, "JUIN": 10,
            "JULY": 11, "JUILLET": 11,
            "AUGUST": 12, "AOÛT": 12, "AOUT": 12,
        }

        # 3. Extraction et tri de toutes les échéances
        all_installments = []
        for fee in fees:
            for inst in fee.installments:
                all_installments.append((fee, inst))

        def get_month_order(item):
            _, inst = item
            month_val = (
                inst.month.value
                if hasattr(inst.month, "value")
                else str(inst.month)
            )
            return school_month_order.get(month_val.upper(), 99)

        all_installments.sort(key=get_month_order)

        # 4. Détail par mois / échéances et calcul du total dû
        # 4. Détail par mois / échéances et calcul rigoureux
        monthly_details = []
        total_due = 0.0
        total_paid = 0.0  # On calcule le total payé basé sur les échéances réelles

        for fee, inst in all_installments:
            total_due += inst.amount

            inst_payments = [p for p in payments if p.installment_id == inst.id]
            inst_paid = sum(p.amount_paid for p in inst_payments)
            total_paid += inst_paid  # Sum de la scolarité uniquement

            inst_remaining = max(0.0, inst.amount - inst_paid)

            if inst_remaining == 0:
                status = "Réglé"
            elif inst_paid > 0:
                status = "Partiel"
            else:
                status = "Non réglé"

            month_name = (
                inst.month.value
                if hasattr(inst.month, "value")
                else str(inst.month)
            )

            monthly_details.append(
                {
                    "month": month_name,
                    "fee_type": fee.fee_type.name,
                    "amount_due": inst.amount,
                    "amount_paid": inst_paid,
                    "remaining": inst_remaining,
                    "status": status,
                }
            )

        if total_due == 0.0 and fees:
            total_due = sum(f.amount for f in fees)
            total_paid = sum(p.amount_paid for p in payments)

        balance_remaining = max(0.0, total_due - total_paid)
        is_fully_paid = total_paid >= total_due and total_due > 0

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