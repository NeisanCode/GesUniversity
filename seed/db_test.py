"""
Large Scale Database Seeding Script
Populates the database with hundreds of records across multiple academic years
to perform stress testing on queries and UI performance.
"""

from datetime import date, timedelta
import random
from faker import Faker

# Database setup imports
from database import get_session, init_db

# SQLAlchemy Model imports
from models import (
    AcademicYear,
    AcademicYearStatus,
    ClassGroup,
    Enrollment,
    EnrollmentStatus,
    EnrollmentType,
    Fee,
    FeeType,
    Installment,
    Level,
    Major,
    Month,
    Payment,
    PaymentMethod,
    Program,
    Receipt,
    Student,
)

fake = Faker("fr_FR")


def seed_large_dataset(
    num_students: int = 300,
    start_year: int = 2024,
    years_count: int = 5,
):
    """
    Generates a large volume of relational data.

    :param num_students: Total number of unique students to generate.
    :param start_year: The starting calendar year for academic cycles.
    :param years_count: How many consecutive academic years to generate.
    """
    print("Initializing database schema...")
    init_db()

    with get_session() as session:
        print("Creating core reference data (Majors, Levels, Fee Types)...")

        # ----------------------------------------------------
        # 1. Majors & Levels (with short code mapping)
        # ----------------------------------------------------
        majors_map = {
            "Génie Informatique": "GI",
            "Gestion d'Entreprise": "GE",
            "Droit des Affaires": "DA",
            "Marketing Digital": "MD",
            "Comptabilité & Finance": "CF",
        }

        levels_map = {
            "Licence 1": "L1",
            "Licence 2": "L2",
            "Licence 3": "L3",
            "Master 1": "M1",
            "Master 2": "M2",
        }

        majors = [Major(name=name) for name in majors_map.keys()]
        levels = [Level(name=name) for name in levels_map.keys()]
        session.add_all(majors + levels)
        session.flush()

        # Helper lookups to fetch short codes
        major_by_id = {m.id: majors_map[m.name] for m in majors}
        level_by_id = {l.id: levels_map[l.name] for l in levels}

        # ----------------------------------------------------
        # 2. Fee Types (Ajout des frais d'inscription et de réinscription)
        # ----------------------------------------------------
        tuition_fee_type = FeeType(
            name="Frais de Scolarité",
            code="TUITION_FEE",
            is_system=True,
        )
        registration_fee_type = FeeType(
            name="Frais d'Inscription",
            code="REGISTRATION_FEE",
            is_system=True,
        )
        re_enrollment_fee_type = FeeType(
            name="Frais de Réinscription",
            code="RE_ENROLLMENT_FEE",
            is_system=True,
        )
        library_fee_type = FeeType(
            name="Frais de Bibliothèque",
            code="LIBRARY_FEE",
            is_system=False,
        )
        session.add_all(
            [
                tuition_fee_type,
                registration_fee_type,
                re_enrollment_fee_type,
                library_fee_type,
            ]
        )
        session.flush()

        # Build Programs (Combination of Majors & Levels)
        programs = []
        for m in majors:
            for l in levels:
                prog = Program(major_id=m.id, level_id=l.id)
                programs.append(prog)
        session.add_all(programs)
        session.flush()

        # Exactly 10 Academic Months per year
        academic_months = [
            Month.OCTOBER,
            Month.NOVEMBER,
            Month.DECEMBER,
            Month.JANUARY,
            Month.FEBRUARY,
            Month.MARCH,
            Month.APRIL,
            Month.MAY,
            Month.JUNE,
            Month.JULY,
        ]

        receipt_counter = 10001
        all_created_students = []

        # ----------------------------------------------------
        # 3. Create Students Pool
        # ----------------------------------------------------
        print(f"Generating {num_students} students...")
        for i in range(1, num_students + 1):
            student = Student(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                student_id_number=f"ETU{start_year}{i:04d}",  # e.g., ETU20240001
                date_of_birth=fake.date_of_birth(minimum_age=17, maximum_age=26),
                email=fake.unique.email(),
                address=fake.address().replace("\n", ", "),
            )
            all_created_students.append(student)

        session.add_all(all_created_students)
        session.flush()

        # ----------------------------------------------------
        # 4. Generate Academic Years & Loop
        # ----------------------------------------------------
        for y_idx in range(years_count):
            year_start = start_year + y_idx
            year_end = year_start + 1
            label = f"{year_start} - {year_end}"  # ex: 2024 - 2025

            # Si l'année dépasse l'année courante (2026), on stoppe la génération
            if year_start > 2026:
                break

            # Définition du statut : seule l'année 2026 est ACTIVE, les précédentes sont COMPLETED
            if year_start == 2026:
                status = AcademicYearStatus.ACTIVE
            else:
                status = AcademicYearStatus.COMPLETED

            academic_year = AcademicYear(
                label=label,
                start_date=date(year_start, 10, 1),
                end_date=date(year_end, 7, 31),
                status=status,
            )
            session.add(academic_year)
            session.flush()

            print(f"Processing Academic Year {label}...")

            year_classes = []
            year_installments = (
                {}
            )  # program_id -> list of Installment objects (Tuition)
            year_registration_fees = {}  # program_id -> Fee object (Inscription)
            year_re_enrollment_fees = {}  # program_id -> Fee object (Réinscription)

            for prog in programs:
                # Group codes formatted like GIL1A, GEM1B, etc.
                major_code = major_by_id[prog.major_id]
                level_code = level_by_id[prog.level_id]
                section_letter = random.choice(["A", "B"])

                class_group = ClassGroup(
                    name=f"{major_code}{level_code}{section_letter}",
                    program_id=prog.id,
                    academic_year_id=academic_year.id,
                )
                year_classes.append(class_group)

                # --- 4.1 Frais d'Inscription ---
                reg_amount = float(random.choice([25000, 35000, 50000, 75000]))
                reg_fee = Fee(
                    program_id=prog.id,
                    academic_year_id=academic_year.id,
                    fee_type_id=registration_fee_type.id,
                    amount=reg_amount,
                    is_split=False,
                )
                session.add(reg_fee)
                year_registration_fees[prog.id] = reg_fee

                # --- 4.2 Frais de Réinscription ---
                re_reg_amount = reg_amount * 0.7  # 30% de réduction pour réinscription
                re_reg_fee = Fee(
                    program_id=prog.id,
                    academic_year_id=academic_year.id,
                    fee_type_id=re_enrollment_fee_type.id,
                    amount=re_reg_amount,
                    is_split=False,
                )
                session.add(re_reg_fee)
                year_re_enrollment_fees[prog.id] = re_reg_fee

                # --- 4.3 Frais de Scolarité ---
                total_tuition = float(random.choice([500000, 600000, 750000]))
                tuition_fee = Fee(
                    program_id=prog.id,
                    academic_year_id=academic_year.id,
                    fee_type_id=tuition_fee_type.id,
                    amount=total_tuition,
                    is_split=True,
                )
                session.add(tuition_fee)
                session.flush()

                # Generate 10 Monthly Installments for Tuition
                monthly_amount = total_tuition / len(academic_months)

                prog_installments = []
                for m in academic_months:
                    inst = Installment(
                        fee_id=tuition_fee.id,
                        month=m,
                        amount=monthly_amount,
                    )
                    prog_installments.append(inst)

                session.add_all(prog_installments)
                session.flush()
                year_installments[prog.id] = prog_installments

            session.add_all(year_classes)
            session.flush()

            # ----------------------------------------------------
            # 5. Enroll Students & Generate Payments
            # ----------------------------------------------------
            # Génère des inscriptions principalement pour les années passées et en cours
            if year_start <= 2026:
                active_students = random.sample(
                    all_created_students, k=int(num_students * random.uniform(0.6, 0.9))
                )

                for student in active_students:
                    assigned_class = random.choice(year_classes)
                    enrollment_type = random.choice(
                        [EnrollmentType.NEW, EnrollmentType.RE_ENROLLMENT]
                    )
                    enrollment_date = date(year_start, 9, random.randint(1, 28))

                    enrollment = Enrollment(
                        student_id=student.id,
                        academic_year_id=academic_year.id,
                        class_group_id=assigned_class.id,
                        enrollment_date=enrollment_date,
                        enrollment_type=enrollment_type,
                        status=EnrollmentStatus.ACTIVE,
                    )
                    session.add(enrollment)
                    session.flush()

                    # --- 5.1 Sélection du montant des frais ---
                    if enrollment_type == EnrollmentType.NEW:
                        entry_fee_obj = year_registration_fees[
                            assigned_class.program_id
                        ]
                    else:
                        entry_fee_obj = year_re_enrollment_fees[
                            assigned_class.program_id
                        ]

                    # --- 5.2 Réglement des Frais d'Inscription / Réinscription ---
                    entry_payment = Payment(
                        enrollment_id=enrollment.id,
                        installment_id=None,
                        payment_date=enrollment_date,
                        payment_method=random.choice(list(PaymentMethod)),
                        amount_paid=entry_fee_obj.amount,
                    )
                    session.add(entry_payment)
                    session.flush()

                    entry_receipt = Receipt(
                        payment_id=entry_payment.id,
                        receipt_number=receipt_counter,
                        receipt_date=enrollment_date,
                    )
                    receipt_counter += 1
                    session.add(entry_receipt)

                    # --- 5.3 Réglement des Mensualités de Scolarité ---
                    prog_insts = year_installments[assigned_class.program_id]

                    payment_behavior = random.choices(
                        population=["FULL", "PARTIAL", "NONE"],
                        weights=[0.6, 0.3, 0.1],
                        k=1,
                    )[0]

                    if payment_behavior == "NONE":
                        continue

                    installments_to_pay = (
                        prog_insts
                        if payment_behavior == "FULL"
                        else prog_insts[: random.randint(1, len(prog_insts) - 1)]
                    )

                    for inst in installments_to_pay:
                        pay_method = random.choice(list(PaymentMethod))
                        pay_date = date(year_start, 10, 10) + timedelta(
                            days=random.randint(0, 180)
                        )

                        payment = Payment(
                            enrollment_id=enrollment.id,
                            installment_id=inst.id,
                            payment_date=pay_date,
                            payment_method=pay_method,
                            amount_paid=inst.amount,
                        )
                        session.add(payment)
                        session.flush()

                        receipt = Receipt(
                            payment_id=payment.id,
                            receipt_number=receipt_counter,
                            receipt_date=pay_date,
                        )
                        receipt_counter += 1
                        session.add(receipt)

        # ----------------------------------------------------
        # 6. Commit Everything
        # ----------------------------------------------------
        print("Committing all transactions to the database...")
        session.commit()
        print("Large dataset populated successfully!")


if __name__ == "__main__":
    seed_large_dataset(
        num_students=100,
        start_year=2024,
        years_count=5,
    )
