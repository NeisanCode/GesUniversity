from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, joinedload
from models import (
    ClassGroup,
    Enrollment,
    Fee,
    FeeType,
    Installment,
    Month,
    Payment,
    Program,
    Receipt,
    Student,
)
from .base_repo import BaseRepo


class MonthlyPaymentRepo(BaseRepo[Payment]):
    def __init__(self, session: Session):
        super().__init__(session, Payment)

    def find_student_by_registration(self, registration_number: str) -> Student | None:
        return self.session.scalars(
            select(Student).where(Student.student_id_number == registration_number)
        ).first()

    def get_enrollment_for_student(self, student: Student) -> Enrollment | None:
        # On va chercher directement l'inscription la plus récente en base SQL avec order_by
        # sans passer par max() qui force du lazy-loading sur student.enrollments
        from models import AcademicYear  # Import local si nécessaire

        stmt = (
            select(Enrollment)
            .join(Enrollment.academic_year)
            .where(Enrollment.student_id == student.id)
            .execution_options(populate_existing=True)
            .options(
                # 1. Étudiant & Année Académique
                joinedload(Enrollment.student),
                joinedload(Enrollment.academic_year),
                # 2. Arborescence du Cursus complète (Classe -> Programme -> Major/Level/Fees)
                selectinload(Enrollment.class_group)
                .selectinload(ClassGroup.program)
                .options(
                    joinedload(Program.major),
                    joinedload(Program.level),
                    selectinload(Program.fees).selectinload(Fee.installments),
                ),
                # 3. Arborescence des Paiements & Reçus
                selectinload(Enrollment.payments).options(
                    joinedload(Payment.installment),
                    joinedload(Payment.receipt)
                    .joinedload(Receipt.payment)
                    .options(
                        joinedload(Payment.installment),
                        joinedload(Payment.enrollment).options(
                            joinedload(Enrollment.student),
                            joinedload(Enrollment.academic_year),
                            selectinload(Enrollment.class_group)
                            .selectinload(ClassGroup.program)
                            .options(
                                joinedload(Program.major),
                                joinedload(Program.level),
                                selectinload(Program.fees),
                            ),
                        ),
                    ),
                ),
            )
            .order_by(AcademicYear.start_date.desc())
        )

        return self.session.scalar(stmt)

    def build_installment_summaries(self, enrollment: Enrollment):
        fee = self.get_tuition_fee(enrollment)
        if fee is None:
            return []

        # Association directe installment_id -> receipt pré-chargé
        payments_map = {
            payment.installment_id: payment.receipt
            for payment in enrollment.payments
            if payment.installment_id is not None
        }

        month_order = {month: index for index, month in enumerate(Month)}
        installments = sorted(
            fee.installments,
            key=lambda installment: month_order.get(
                installment.month, len(month_order)
            ),
        )

        return [
            {
                "id": installment.id,
                "month": installment.month,
                "amount": installment.amount,
                "paid": installment.id in payments_map,
                "receipt": payments_map.get(installment.id),
            }
            for installment in installments
        ]

    def get_tuition_fee(self, enrollment: Enrollment) -> Fee | None:
        return self.session.scalar(
            select(Fee)
            .join(Fee.fee_type)
            .where(
                Fee.program_id == enrollment.class_group.program_id,
                Fee.academic_year_id == enrollment.academic_year_id,
                FeeType.code == "TUITION_FEE",
            )
        )

    def get_installment_for_enrollment_and_month(
        self, enrollment: Enrollment, month_value
    ):
        fee = self.get_tuition_fee(enrollment)
        if fee is None:
            return None

        month = self._coerce_month(month_value)
        if month is None:
            return None

        return self.session.scalar(
            select(Installment).where(
                Installment.fee_id == fee.id,
                Installment.month == month,
            )
        )

    def get_payment_for_installment(
        self, enrollment_id: int, installment_id: int
    ) -> Payment | None:
        return self.session.scalar(
            select(Payment).where(
                Payment.enrollment_id == enrollment_id,
                Payment.installment_id == installment_id,
            )
        )

    def get_next_receipt_number(self) -> int:
        last_receipt = self.session.scalar(
            select(Receipt).order_by(Receipt.receipt_number.desc())
        )
        if last_receipt is None:
            return 10001
        return last_receipt.receipt_number + 1

    def _coerce_month(self, month_value):
        if isinstance(month_value, Month):
            return month_value
        for month in Month:
            if month.value == month_value:
                return month
        return None
