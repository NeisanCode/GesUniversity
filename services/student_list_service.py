from typing import List, Dict, Any, Tuple, Callable
from sqlalchemy.orm import Session

from models import EnrollmentType
from repositories import StudentListRepo


class StudentListService:
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory

    def get_active_year_info(self) -> Tuple[int | None, str]:
        with self.session_factory() as session:
            repo = StudentListRepo(session)
            active_year = repo.get_active_academic_year()
            if not active_year:
                return None, "Aucune année active"
            return active_year.id, active_year.label

    def search_programs(self, query: str | None = None) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            repo = StudentListRepo(session)
            programs = repo.search_programs(query)
            return [
                {"id": p.id, "label": f"{p.major.name} - {p.level.name}"}
                for p in programs
            ]

    def get_enrolled_students(
        self,
        program_id: int | None = None,
        show_new: bool = True,
        show_re_enrollment: bool = True,
        search_query: str | None = None,
        limit: int | None = 50,
    ) -> List[Dict[str, Any]]:
        with self.session_factory() as session:
            repo = StudentListRepo(session)

            active_year = repo.get_active_academic_year()
            if not active_year:
                return []

            allowed_types = []
            if show_new:
                allowed_types.append(EnrollmentType.NEW)
            if show_re_enrollment:
                allowed_types.append(EnrollmentType.RE_ENROLLMENT)

            enrollments = repo.get_enrolled_students(
                academic_year_id=active_year.id,
                program_id=program_id,
                types=allowed_types,
                search_query=search_query,
                limit=limit,
            )

            result = []
            for e in enrollments:
                student = e.student
                program = e.class_group.program

                result.append(
                    {
                        "id": student.id,
                        "enrollment_id": e.id,
                        "student_id_number": student.student_id_number,
                        "full_name": f"{student.last_name.upper()} {student.first_name}",
                        "email": getattr(student, "email", "") or "",
                        "address": getattr(student, "address", "") or "",
                        "program": f"{program.major.name} ({program.level.name})",
                        "class_group": e.class_group.name,
                        "enrollment_type": e.enrollment_type.value,
                        "status": e.status.value,
                        "enrollment_date": e.enrollment_date.strftime("%d/%m/%Y"),
                    }
                )

            return result

    def update_student_info(
        self,
        student_id: int,
        last_name: str,
        first_name: str,
        email: str,
        address: str,
        class_group_name: str,
    ) -> Tuple[bool, str | None]:
        """Délègue la mise à jour des informations au dépôt et retourne le statut."""
        with self.session_factory() as session:
            repo = StudentListRepo(session)
            active_year = repo.get_active_academic_year()
            if not active_year:
                return False, "Aucune année académique active."

            return repo.update_student_and_enrollment(
                student_id=student_id,
                last_name=last_name,
                first_name=first_name,
                email=email,
                address=address,
                class_group_name=class_group_name,
                academic_year_id=active_year.id,
            )

    def get_classes_for_program(self, program_id: int) -> List[str]:
        """Retourne les noms de toutes les classes associées à un programme."""
        with self.session_factory() as session:
            repo = StudentListRepo(session)
            class_groups = repo.get_class_groups_by_program(program_id)
            return [cg.name for cg in class_groups]