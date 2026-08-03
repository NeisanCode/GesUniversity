from datetime import datetime
import re
from tkinter import messagebox
from typing import TYPE_CHECKING
from services import EnrollmentService
from .models.models_dto import EtudiantDTO
from database import get_session

if TYPE_CHECKING:
    from interfaces import EnrollmentFormFrame


class EnrollmentController:

    def __init__(self, view: EnrollmentFormFrame):
        """
        :param view: Instance de EnrollmentFormFrame (la vue)
        """
        self.view = view
        self.service = EnrollmentService(get_session)

    def valider_champs(self) -> EtudiantDTO | None:
        """
        Extrait, valide les données du formulaire d'inscription et retourne un
        dictionnaire si tout est valide, sinon affiche une erreur et retourne None.
        """

    def traiter_inscription(self):
        """
        Action déclenchée par le bouton de validation.
        """
        pass

    def reinitialiser_formulaire(self):
        """Vide les champs après une inscription réussie."""
        pass

    def charger_options_initiales(self):
        """Méthode appelée au lancement pour remplir les menus déroulants."""
        pass
