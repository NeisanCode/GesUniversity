from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepo(Generic[T]):
    """Opérations CRUD génériques pour un modèle SQLAlchemy."""

    def __init__(self, session: Session, model: Type[T]):
        """Initialise le dépôt avec une session SQLAlchemy et le modèle cible."""
        self.session = session
        self.model = model

    def create(self, entity: T) -> T:
        """Insère une entité en base et retourne l'objet persisté avec son id."""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def create_from(self, **kwargs) -> T:
        """Crée une entité à partir de champs nommés puis la persiste en base."""
        return self.create(self.model(**kwargs))

    def get_by_id(self, entity_id: int) -> T | None:
        """Récupère une entité par sa clé primaire, ou None si introuvable."""
        return self.session.get(self.model, entity_id)

    def get_all(self) -> Sequence[T]:
        """Retourne toutes les entités de la table associée au modèle."""
        return self.session.scalars(select(self.model)).all()

    def update(self, entity: T) -> T:
        """Valide les modifications déjà appliquées sur l'entité en mémoire."""
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, entity: T) -> None:
        """Supprime une entité déjà chargée en base."""
        self.session.delete(entity)
        self.session.commit()

    def delete_by_id(self, entity_id: int) -> bool:
        """Recherche une entité par id puis la supprime si elle existe."""
        entity = self.get_by_id(entity_id)
        if entity is None:
            return False
        self.delete(entity)
        return True
