from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from config import DB_PATH


DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, echo=False)


# SQLite désactive les clés étrangères par défaut : on les active pour que
# les ForeignKey/UniqueConstraint du modèle soient réellement contrôlées.


@event.listens_for(engine, "connect")
def _enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Fabrique de sessions, à utiliser dans le reste de l'application
SessionLocal = sessionmaker(bind=engine, autoflush=False)


@contextmanager
def get_session() :
    """À utiliser avec un context manager: `with get_session() as session:`"""
    session = SessionLocal()
    try:
        yield session  # Fournit la session au bloc 'with'
    finally:
        session.close()  
