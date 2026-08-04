class EtudiantNotFoundError(Exception):
    """Levée si un étudiant n'est pas trouvé."""

    pass


class PaymentValidationError(Exception):
    """Levée si un paiement ne peut pas être enregistré."""

    pass


class EnrollmentValidationError(Exception):
    """Levée si une inscription ne respecte pas les règles métier."""

    pass


class DuplicateStudentEmailError(EnrollmentValidationError):
    """Levée lorsqu'un email étudiant est déjà utilisé."""

    pass
