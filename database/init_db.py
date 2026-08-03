from models.models import Base
from database.session import engine


def init_db() -> None:
    """
    Crée toutes les tables définies dans models.py si elles n'existent pas.
    Ne modifie pas les tables déjà existantes (pas de migration automatique) :
    pour faire évoluer un schéma déjà en production, utiliser Alembic.
    """
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée avec succès")
