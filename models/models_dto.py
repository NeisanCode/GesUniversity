from dataclasses import dataclass
from datetime import date


@dataclass
class StudentDTO:
    nom: str
    prenom: str
    date_naissance: date
    email: str
    adresse: str
    annee_academique: str
    filiere: str
    niveau_etude: str
    mode_paiement: str


@dataclass
class RegistrationReceiptDTO:
    receipt_number: int
    receipt_date: date
    student_id_number: str
    student_full_name: str
    student_email: str
    academic_year: str
    major_name: str
    level_name: str
    class_group_name: str
    payment_method: str
    amount_paid: float


@dataclass
class PaymentReceiptDTO:
    receipt_number: int
    receipt_date: date
    student_id_number: str
    student_last_name: str
    student_first_name: str
    payment_date: date
    payment_method: str
    class_name: str
    academic_year_label: str
    month_name: str
    amount_paid: float
    total_program_fees: float
    total_paid_so_far: float
    remaining_balance: float
