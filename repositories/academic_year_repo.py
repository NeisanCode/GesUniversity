from datetime import date
from typing import Sequence, Tuple
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import AcademicYear, AcademicYearStatus
from repositories.base_repo import BaseRepo


class AcademicYearRepo(BaseRepo[AcademicYear]):
    def __init__(self, session: Session):
        super().__init__(session, AcademicYear)

    def get_active_year(self) -> AcademicYear | None:
        """Récupère l'année académique actuellement active."""
        stmt = select(AcademicYear).where(AcademicYear.status == AcademicYearStatus.ACTIVE)
        return self.session.scalars(stmt).first()

    def get_all_years(self) -> Sequence[AcademicYear]:
        """Récupère toutes les années académiques ordonnées par date de début."""
        stmt = select(AcademicYear).order_by(AcademicYear.start_date.desc())
        return self.session.scalars(stmt).all()

    def close_current_and_activate_new(
        self, active_year_id: int, new_year_label: str, start_date: date, end_date: date
    ) -> Tuple[bool, str | None]:
        """
        Passe l'année active au statut 'Terminé' et crée/active la nouvelle année.
        """
        try:
            # 1. Clôturer l'actuelle
            current_active = self.get_by_id(active_year_id)
            if current_active:
                current_active.status = AcademicYearStatus.COMPLETED

            # 2. Créer et activer la nouvelle
            new_year = AcademicYear(
                label=new_year_label,
                start_date=start_date,
                end_date=end_date,
                status=AcademicYearStatus.ACTIVE,
            )
            self.session.add(new_year)

            self.session.commit()
            return True, None
        except Exception as e:
            self.session.rollback()
            return False, f"Erreur lors de la transition d'année : {str(e)}"