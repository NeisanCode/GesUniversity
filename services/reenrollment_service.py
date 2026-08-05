from typing import Callable
from sqlalchemy.orm import Session


class ReEnrollmentService:

    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory
