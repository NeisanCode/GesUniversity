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
class PaiementDto:
    pass


@dataclass
class ReceiptDTO:
    """DTO purement Python contenant uniquement les données nécessaires
    pour l'affichage ou la génération PDF du reçu, sans dépendance BDD.
    """

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
