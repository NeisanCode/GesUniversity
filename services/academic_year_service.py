from datetime import date
from typing import Callable, Dict, Any, Tuple
from sqlalchemy.orm import Session

from repositories import AcademicYearRepo


class AcademicYearService:
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory

    def get_academic_years_info(self) -> Dict[str, Any]:
        """Récupère l'année active ainsi qu'une suggestion pour la suivante."""
        with self.session_factory() as session:
            repo = AcademicYearRepo(session)
            active_year = repo.get_active_year()

            if not active_year:
                return {
                    "active_year": None,
                    "next_year_suggestion": "2026 - 2027",
                }

            # Suggestion du libellé de la prochaine année (ex: 2025 - 2026 -> 2026 - 2027)
            try:
                parts = active_year.label.split("-")
                start_yr = int(parts[0].strip())
                end_yr = int(parts[1].strip())
                next_label = f"{end_yr} - {end_yr + 1}"
            except Exception:
                next_label = ""

            return {
                "active_year": {
                    "id": active_year.id,
                    "label": active_year.label,
                    "status": active_year.status.value,
                },
                "next_year_suggestion": next_label,
            }

    def close_and_start_new_year(
        self, current_year_id: int, new_label: str
    ) -> Tuple[bool, str | None]:
        """Traite les dates par défaut et délègue la clôture au dépôt."""
        if not new_label or "-" not in new_label:
            return False, "Le format du libellé est invalide. Exemple attendu : 2026 - 2027"

        try:
            parts = new_label.split("-")
            start_yr = int(parts[0].strip())
            end_yr = int(parts[1].strip())
            start_date = date(start_yr, 10, 1)  # 1er Octobre
            end_date = date(end_yr, 7, 31)     # 31 Juillet
        except Exception:
            return False, "Saisie des années invalide."

        with self.session_factory() as session:
            repo = AcademicYearRepo(session)
            return repo.close_current_and_activate_new(
                active_year_id=current_year_id,
                new_year_label=new_label,
                start_date=start_date,
                end_date=end_date,
            )