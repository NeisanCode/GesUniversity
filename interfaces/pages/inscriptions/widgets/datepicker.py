import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime

class DatePicker(ctk.CTkFrame):
    """Widget personnalisé de sélection de date (CTkFrame avec entry + bouton calendrier)"""

    def __init__(self, parent, label_text, placeholder="AAAA-MM-JJ", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        # Label
        ctk.CTkLabel(
            self,
            text=label_text,
            font=("Helvetica", 12, "bold"),
            text_color="#d1d5db",
            anchor="w",
        ).pack(fill="x", pady=(0, 2))

        # Frame interne pour entry + bouton
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 10))

        # Entry pour afficher la date
        self.entry = ctk.CTkEntry(
            frame,
            placeholder_text=placeholder,
            placeholder_text_color="#6b7280",
            fg_color="#111827",
            border_color="#2b3544",
            text_color="#e5e7eb",
            height=36,
            corner_radius=6,
            font=("Helvetica", 12),
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # Bouton calendrier
        self.btn_cal = ctk.CTkButton(
            frame,
            text="📅",
            width=40,
            height=36,
            fg_color="#2b3544",
            hover_color="#374151",
            corner_radius=6,
            font=("Helvetica", 14),
            command=self.open_calendar,
        )
        self.btn_cal.pack(side="right")

        # Variable interne pour stocker la date
        self.date_value = None

    def open_calendar(self):
        """Ouvre une fenêtre popup avec un calendrier tkcalendar"""
        top = ctk.CTkToplevel(self)
        top.title("Sélectionner une date")
        top.geometry("300x280")
        top.resizable(False, False)

        # On essaie de centrer la fenêtre par rapport au parent
        top.transient(self.winfo_toplevel())
        top.grab_set()

        # Calendrier
        cal = Calendar(
            top,
            selectmode="day",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
            date_pattern="yyyy-mm-dd",
            background="#1f2937",
            foreground="#e5e7eb",
            selectbackground="#3b82f6",
            selectforeground="white",
            bordercolor="#2b3544",
            headersbackground="#111827",
            headersforeground="#d1d5db",
            normalbackground="#111827",
            normalforeground="#e5e7eb",
            weekendbackground="#1f2937",
            weekendforeground="#e5e7eb",
            othermonthbackground="#1f2937",
            othermonthforeground="#6b7280",
            othermonthwebackground="#1f2937",
            othermonthweforeground="#6b7280",
        )
        cal.pack(pady=10, padx=10, fill="both", expand=True)

        def on_select():
            date_str = cal.get_date()
            self.entry.delete(0, "end")
            self.entry.insert(0, date_str)
            self.date_value = date_str
            top.destroy()

        btn_select = ctk.CTkButton(
            top,
            text="Valider",
            command=on_select,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            height=32,
            corner_radius=6,
        )
        btn_select.pack(pady=(0, 10))

    def get(self):
        """Retourne la date saisie (string)"""
        return self.entry.get()

    def set(self, date_str):
        """Définit la date dans l'entry"""
        self.entry.delete(0, "end")
        self.entry.insert(0, date_str)
        self.date_value = date_str

