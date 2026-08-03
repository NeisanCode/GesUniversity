from models import Payment
from sqlalchemy.orm import Session
from .base_repo import BaseRepo

class PayementRepo(BaseRepo[Payment]):
    def __init__(self, session:Session):
        super().__init__(session)
