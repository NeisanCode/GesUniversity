from interfaces import RegistrationForm
import customtkinter as ctk

app = ctk.CTk()
form = RegistrationForm(app)
form.pack(fill="both", expand=True, padx=25, pady=20)
app.mainloop()
