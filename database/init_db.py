from models.models import Base
from database.session import engine


def init_db() -> None:
    """
    Crée toutes les tables définies dans models.py si elles n'existent pas.
    """
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée avec succès")
