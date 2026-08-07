import customtkinter as ctk

from interfaces.form.student_archive_form import StudentArchiveForm


app = ctk.CTk()
form = StudentArchiveForm(app)
form.pack(expand=True, fill="both")
app.mainloop()