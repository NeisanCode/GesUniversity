"""
SQLAlchemy Models - School Management System
Compatible with SQLAlchemy 2.0 (Declarative style using Mapped / mapped_column)
"""

from datetime import date
import enum

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
    String,
    Float,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


# ==========================================
# Enums (Values set back to French)
# ==========================================

class AcademicYearStatus(enum.Enum):
    ACTIVE = "Actif"
    COMPLETED = "Terminé"


class EnrollmentType(enum.Enum):
    NEW = "Nouveau"
    RE_ENROLLMENT = "Réinscription"


class EnrollmentStatus(enum.Enum):
    ACTIVE = "Actif"
    WITHDRAWN = "Retiré"
    COMPLETED = "Terminé"


class PaymentMethod(enum.Enum):
    CASH = "Espèces"
    BANK_TRANSFER = "Virement bancaire"
    CARD = "Carte"
    MOBILE_MONEY = "Mobile money"
    CHECK = "Chèque"


class Month(enum.Enum):
    OCTOBER = "Octobre"
    NOVEMBER = "Novembre"
    DECEMBER = "Décembre"
    JANUARY = "Janvier"
    FEBRUARY = "Février"
    MARCH = "Mars"
    APRIL = "Avril"
    MAY = "Mai"
    JUNE = "Juin"
    JULY = "Juillet"


# ==========================================
# Models
# ==========================================

class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(100))
    student_id_number: Mapped[str] = mapped_column(String(20), unique=True)
    date_of_birth: Mapped[date]
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    address: Mapped[str | None] = mapped_column(String(255))

    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )


class AcademicYear(Base):
    __tablename__ = "academic_year"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(20))
    start_date: Mapped[date]
    end_date: Mapped[date]
    status: Mapped[AcademicYearStatus]

    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="academic_year"
    )
    fees: Mapped[list["Fee"]] = relationship(back_populates="academic_year")
    classes: Mapped[list["ClassGroup"]] = relationship(
        back_populates="academic_year"
    )


class Major(Base):
    __tablename__ = "major"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    programs: Mapped[list["Program"]] = relationship(back_populates="major")


class Level(Base):
    __tablename__ = "level"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    programs: Mapped[list["Program"]] = relationship(back_populates="level")


class Program(Base):
    __tablename__ = "program"

    id: Mapped[int] = mapped_column(primary_key=True)
    major_id: Mapped[int] = mapped_column(ForeignKey("major.id"))
    level_id: Mapped[int] = mapped_column(ForeignKey("level.id"))

    major: Mapped["Major"] = relationship(back_populates="programs")
    level: Mapped["Level"] = relationship(back_populates="programs")

    fees: Mapped[list["Fee"]] = relationship(back_populates="program")
    classes: Mapped[list["ClassGroup"]] = relationship(back_populates="program")


class Enrollment(Base):
    __tablename__ = "enrollment"
    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "academic_year_id",
            "class_group_id",
            name="uq_enrollment_composite",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    academic_year_id: Mapped[int] = mapped_column(ForeignKey("academic_year.id"))
    enrollment_date: Mapped[date]
    class_group_id: Mapped[int] = mapped_column(ForeignKey("class_group.id"))
    enrollment_type: Mapped[EnrollmentType]
    status: Mapped[EnrollmentStatus] = mapped_column(
        default=EnrollmentStatus.ACTIVE
    )

    student: Mapped["Student"] = relationship(back_populates="enrollments")
    academic_year: Mapped["AcademicYear"] = relationship(
        back_populates="enrollments"
    )
    payments: Mapped[list["Payment"]] = relationship(back_populates="enrollment")
    class_group: Mapped["ClassGroup"] = relationship(
        back_populates="enrollments"
    )


class ClassGroup(Base):
    __tablename__ = "class_group"
    __table_args__ = (
        UniqueConstraint(
            "name",
            "academic_year_id",
            name="uq_class_academic_year",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    program_id: Mapped[int] = mapped_column(ForeignKey("program.id"))
    academic_year_id: Mapped[int] = mapped_column(ForeignKey("academic_year.id"))

    program: Mapped["Program"] = relationship(back_populates="classes")
    academic_year: Mapped["AcademicYear"] = relationship(
        back_populates="classes"
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="class_group", cascade="all, delete-orphan"
    )


class FeeType(Base):
    __tablename__ = "fee_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_system: Mapped[bool] = mapped_column(default=False)

    fees: Mapped[list["Fee"]] = relationship(back_populates="fee_type")


class Fee(Base):
    __tablename__ = "fee"
    __table_args__ = (
        UniqueConstraint(
            "program_id",
            "academic_year_id",
            "fee_type_id",
            name="uq_fee_composite",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("program.id"))
    academic_year_id: Mapped[int] = mapped_column(ForeignKey("academic_year.id"))
    fee_type_id: Mapped[int] = mapped_column(ForeignKey("fee_type.id"))
    amount: Mapped[float] = mapped_column(Float)
    is_split: Mapped[bool] = mapped_column(default=False)

    program: Mapped["Program"] = relationship(back_populates="fees")
    academic_year: Mapped["AcademicYear"] = relationship(back_populates="fees")
    fee_type: Mapped["FeeType"] = relationship(back_populates="fees")
    installments: Mapped[list["Installment"]] = relationship(
        back_populates="fee", cascade="all, delete-orphan"
    )


class Installment(Base):
    __tablename__ = "installment"
    __table_args__ = (
        UniqueConstraint(
            "fee_id",
            "month",
            name="uq_fee_month",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    fee_id: Mapped[int] = mapped_column(ForeignKey("fee.id"), nullable=False)
    month: Mapped[Month]
    amount: Mapped[float] = mapped_column(Float)

    fee: Mapped["Fee"] = relationship(back_populates="installments")
    payments: Mapped[list["Payment"]] = relationship(back_populates="installment")


class Payment(Base):
    __tablename__ = "payment"
    __table_args__ = (
        UniqueConstraint(
            "enrollment_id",
            "installment_id",
            name="uq_payment_installment",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    enrollment_id: Mapped[int] = mapped_column(ForeignKey("enrollment.id"))
    installment_id: Mapped[int | None] = mapped_column(
        ForeignKey("installment.id"), nullable=True
    )
    payment_date: Mapped[date]
    payment_method: Mapped[PaymentMethod]
    amount_paid: Mapped[float] = mapped_column(Float)

    enrollment: Mapped["Enrollment"] = relationship(back_populates="payments")
    installment: Mapped["Installment"] = relationship(back_populates="payments")
    receipt: Mapped["Receipt"] = relationship(
        back_populates="payment",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Receipt(Base):
    __tablename__ = "receipt"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_id: Mapped[int] = mapped_column(ForeignKey("payment.id"), unique=True)
    receipt_number: Mapped[int] = mapped_column(unique=True)
    receipt_date: Mapped[date]

    payment: Mapped["Payment"] = relationship(back_populates="receipt")