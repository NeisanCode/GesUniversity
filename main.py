
import customtkinter as ctk

from interfaces import MonthlyPaymentFormFrame
app = ctk.CTk()
app.title("Gestion des Paiements Mensuels")
app.geometry("950x600")

frame = MonthlyPaymentFormFrame(app)
frame.pack(fill="both", expand=True)

app.mainloop()
