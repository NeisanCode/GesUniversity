import customtkinter as ctk

from interfaces import StudentArchiveForm


app = ctk.CTk()
form = StudentArchiveForm(app)
form.pack(expand=True, fill="both")
app.mainloop()