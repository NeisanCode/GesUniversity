from interfaces import PaiementMensuelFormFrame
import customtkinter as ctk
app = ctk.CTk()
app.title("Gestion des Paiements Mensuels")
app.geometry("950x600")

frame = PaiementMensuelFormFrame(app)
frame.pack(fill="both", expand=True)

app.mainloop()
