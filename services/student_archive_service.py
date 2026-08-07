from typing import List, Dict, Any, Tuple, Callable
from sqlalchemy.orm import Session

from repositories import StudentArchiveRepo


class StudentArchiveService:
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory

    def get_previous_years(self) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            repo = StudentArchiveRepo(session)
            years = repo.get_previous_academic_years()
            return [{"id": y.id, "label": y.label} for y in years]

    def search_programs(self, query: str | None = None) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            repo = StudentArchiveRepo(session)
            programs = repo.search_programs(query)
            return [
                {"id": p.id, "label": f"{p.major.name} - {p.level.name}"}
                for p in programs
            ]

    def get_past_students(
        self,
        program_id: int | None = None,
        year_id: int | None = None,
        search_query: str | None = None,
        limit: int | None = 50,
    ) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            repo = StudentArchiveRepo(session)
            enrollments = repo.get_past_enrolled_students(
                program_id=program_id,
                year_id=year_id,
                search_query=search_query,
                limit=limit,
            )

            result = []
            for e in enrollments:
                student = e.student
                program = e.class_group.program

                dob_str = (
                    student.date_of_birth.strftime("%d/%m/%Y")
                    if getattr(student, "date_of_birth", None)
                    else "--"
                )

                result.append(
                    {
                        "id": student.id,
                        "enrollment_id": e.id,
                        "student_id_number": student.student_id_number,
                        "last_name": student.last_name,
                        "first_name": student.first_name,
                        "full_name": f"{student.last_name.upper()} {student.first_name}",
                        "email": getattr(student, "email", "") or "",
                        "date_of_birth": dob_str,
                        "address": getattr(student, "address", "") or "",
                        "program": f"{program.major.name} ({program.level.name})",
                        "class_group": e.class_group.name,
                        "academic_year": e.academic_year.label,
                    }
                )

            return result

    def get_student_financial_details(self, enrollment_id: int) -> Dict[str, Any]:
        with self.session_factory() as session:
            repo = StudentArchiveRepo(session)
            return repo.get_student_financial_summary(enrollment_id)