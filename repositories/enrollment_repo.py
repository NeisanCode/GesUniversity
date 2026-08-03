from sqlalchemy.orm import Session
from models import Enrollment 
from .base_repo import BaseRepo

class EnrollmentRepo(BaseRepo[Enrollment]):
    def __init__(self, session:Session):
        super().__init__(session)
