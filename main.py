from interfaces import StudentListFormFrame
import customtkinter as ctk
    

app = ctk.CTk()
form = StudentListFormFrame(app)
form.pack(fill="both", expand=True, padx=25, pady=20)
app.mainloop()
