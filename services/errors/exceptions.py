class EtudiantNotFoundError(Exception):
    """Levée si un étudiant n'est pas trouvé."""

    pass


class PaymentValidationError(Exception):
    """Levée si un paiement ne peut pas être enregistré."""

    pass
