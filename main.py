from interfaces import ReEnrollmentFormFrame
import customtkinter as ctk

app = ctk.CTk()
form = ReEnrollmentFormFrame(app)
form.pack(fill="both", expand=True, padx=25, pady=20)
app.mainloop()
