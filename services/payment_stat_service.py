from typing import List, Dict, Any, Tuple, Callable
from sqlalchemy.orm import Session

from models import Month
from repositories import PaymentStatsRepo


class PaymentStatsService:
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory

    def get_active_year_info(self) -> Tuple[int | None, str]:
        with self.session_factory() as session:
            repo = PaymentStatsRepo(session)
            active_year = repo.get_active_academic_year()
            if not active_year:
                return None, "Aucune année active"
            return active_year.id, active_year.label

    def search_programs(self, query: str | None = None) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            repo = PaymentStatsRepo(session)
            programs = repo.search_programs(query)
            return [
                {"id": p.id, "label": f"{p.major.name} - {p.level.name}"}
                for p in programs
            ]

    def get_classes_for_program(
        self, program_id: int, academic_year_id: int
    ) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            repo = PaymentStatsRepo(session)
            classes = repo.get_class_groups_by_program_and_year(
                program_id=program_id, academic_year_id=academic_year_id
            )
            return [{"id": c.id, "name": c.name} for c in classes]

    def get_payment_stats_for_class(
        self, class_group_id: int, month_value: str, academic_year_id: int
    ) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            repo = PaymentStatsRepo(session)
            enrollments = repo.get_enrollments_by_class_and_year(
                class_group_id=class_group_id, academic_year_id=academic_year_id
            )

            try:
                target_month = Month(month_value)
            except ValueError:
                return []

            results = []
            for e in enrollments:
                student = e.student
                level_name = "N/A"
                if e.class_group and e.class_group.program and e.class_group.program.level:
                    level_name = e.class_group.program.level.name

                is_paid = False
                amount_paid = 0.0
                monthly_fee = 0.0

                for pmt in e.payments:
                    if pmt.installment and pmt.installment.month == target_month:
                        is_paid = True
                        amount_paid = pmt.amount_paid
                        monthly_fee = getattr(pmt.installment, "amount", 0.0)
                        break

                results.append(
                    {
                        "student_id": student.id,
                        "student_id_number": student.student_id_number,
                        "full_name": f"{student.last_name.upper()} {student.first_name}",
                        "email": getattr(student, "email", "") or "N/A",
                        "level_name": level_name,
                        "monthly_fee": monthly_fee,
                        "is_paid": is_paid,
                        "amount_paid": amount_paid,
                    }
                )

            return results