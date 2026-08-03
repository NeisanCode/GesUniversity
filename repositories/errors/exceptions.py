class RepositoryError(Exception):
    """Exception de base pour la couche de données"""
    pass

class ResourceNotFoundError(RepositoryError):
    """Levée lorsqu'une ressource n'est pas trouvée"""
    pass

class DuplicateResourceError(RepositoryError):
    """Levée lorsqu'une contrainte d'unicité est violée"""
    pass