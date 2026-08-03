from dataclasses import dataclass
from datetime import date


@dataclass
class EtudiantDTO:
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
