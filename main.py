import sys
import customtkinter as ctk
from interfaces import AcademicYearFormFrame

# Correctif DPI Windows
if sys.platform.startswith("win"):
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass


class MainInterface(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestion d'Élèves")
        self.geometry("1280x720")
        self.minsize(1024, 600)

        # 1. Empêcher CustomTkinter de recalculer les ratios de scale constamment
        ctk.set_widget_scaling(1.0)
        ctk.set_window_scaling(1.0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_form = AcademicYearFormFrame(self)
        self.current_form.grid(row=0, column=0, sticky="nsew")

        # 2. Gestion propre du redimensionnement Windows
        self._is_resizing = False
        self._resize_timer = None

        # Événements de capture de la souris sur la fenêtre
        self.bind("<Configure>", self._on_configure)

    def _on_configure(self, event):
        if event.widget == self:
            # Annule le refresh si on est toujours en train de redimensionner
            if self._resize_timer is not None:
                self.after_cancel(self._resize_timer)

            # Bloque la mise à jour graphique lourde pendant le drag
            self._resize_timer = self.after(60, self._end_resize)

    def _end_resize(self):
        self._resize_timer = None
        # Ne rafraîchit la géométrie qu'une fois le redimensionnement terminé
        self.update_idletasks()


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = MainInterface()
    app.mainloop()