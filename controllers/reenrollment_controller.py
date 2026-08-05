from datetime import date
import tkinter.messagebox as messagebox
from typing import TYPE_CHECKING
from database import get_session
from services import ReEnrollmentService
from models import StudentDTO
from .utils import gen_registration_pdf

if TYPE_CHECKING:
    from interfaces import ReEnrollmentFormFrame


class ReEnrollmentController:
    def __init__(self, view: "ReEnrollmentFormFrame"):
        pass
