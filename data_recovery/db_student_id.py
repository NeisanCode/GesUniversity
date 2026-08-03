from datetime import date
from sqlalchemy import (
    select,
    func,
    create_engine,
)
from sqlalchemy.orm import Session

# Importation de tes modèles depuis models.py
from models import (
    Student,
    Enrollment,
    ClassGroup,
    Fee,
    Payment,
    AcademicYear,
)


def get_unpaid_students_matricules(session: Session, academic_year_id: int) -> list[str]:
    """
    Retourne la liste des matricules (student_id_number) des élèves n'ayant pas
    totalement réglé leurs frais pour une année académique donnée.
    """

    # 1. Sous-requête : Somme des frais dus par inscription (basé sur le programme de la classe)
    total_due_subq = (
        select(
            Enrollment.id.label("enrollment_id"),
            func.coalesce(func.sum(Fee.amount), 0.0).label("total_due"),
        )
        .join(ClassGroup, Enrollment.class_group_id == ClassGroup.id)
        .join(
            Fee,
            (Fee.program_id == ClassGroup.program_id)
            & (Fee.academic_year_id == Enrollment.academic_year_id),
        )
        .where(Enrollment.academic_year_id == academic_year_id)
        .group_by(Enrollment.id)
        .subquery()
    )

    # 2. Sous-requête : Somme des montants effectivement payés par inscription
    total_paid_subq = (
        select(
            Payment.enrollment_id.label("enrollment_id"),
            func.coalesce(func.sum(Payment.amount_paid), 0.0).label("total_paid"),
        )
        .group_by(Payment.enrollment_id)
        .subquery()
    )

    # 3. Requête principale : Filtrer les étudiants avec total_paid < total_due
    stmt = (
        select(Student.student_id_number)
        .join(Enrollment, Student.id == Enrollment.student_id)
        .join(total_due_subq, Enrollment.id == total_due_subq.c.enrollment_id)
        .outerjoin(total_paid_subq, Enrollment.id == total_paid_subq.c.enrollment_id)
        .where(Enrollment.academic_year_id == academic_year_id)
        .where(
            func.coalesce(total_paid_subq.c.total_paid, 0.0) < total_due_subq.c.total_due
        )
        .distinct()
    )

    results = session.scalars(stmt).all()
    return list(results)


# ==========================================
# Exemple d'utilisation
# ==========================================
if __name__ == "__main__":
    # Remplace par ta chaîne de connexion (ex: sqlite:///database.db ou postgresql://...)
    engine = create_engine("sqlite:///data/school.db")

    with Session(engine) as session:
        # Remplace par l'ID de l'année académique souhaitée
        target_academic_year_id = 1

        matricules_incomplets = get_unpaid_students_matricules(
            session=session,
            academic_year_id=target_academic_year_id,
        )

        print(f"--- Élèves en retard de paiement (Année ID: {target_academic_year_id}) ---")
        for matricule in matricules_incomplets:
            print(f"- Matricule : {matricule}")