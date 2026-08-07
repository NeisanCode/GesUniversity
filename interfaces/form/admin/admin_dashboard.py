import customtkinter as ctk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_view import MainView


class AdminDashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, main_app: "MainView"):
        super().__init__(parent, fg_color="transparent")
        self.app = main_app

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(40, 30))

        ctk.CTkLabel(header_frame, text="🔒", font=ctk.CTkFont(size=48)).pack(
            pady=(0, 10)
        )

        ctk.CTkLabel(
            header_frame,
            text="PANNEAU D'ADMINISTRATION",
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
            text_color="#F59E0B",
            justify="center",
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            header_frame,
            text="INSTITUT SUPÉRIEUR POLYTECHNIQUE SAINTE LUCIE D'OYO",
            font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
            text_color=self.app.COLOR_SUBTEXT,
        ).pack()

        cards_grid = ctk.CTkFrame(self, fg_color="transparent")
        cards_grid.pack(expand=True, pady=(0, 20))

        # 1. Année Académique
        card_year = self.app.create_card(
            master=cards_grid,
            icon="📅",
            title="Année Académique",
            description="Clôturer l'année active, configurer\nla nouvelle et gérer la session.",
            command=lambda: self.app.show_page(
                "academic_year",
                "Administration - Année Académique",
                from_admin=True,
            ),
        )
        card_year.grid(row=0, column=0, padx=15, pady=10)

        # Bouton Retour au Dashboard général
        ctk.CTkButton(
            self,
            text="← Quitter l'Administration",
            fg_color="#DC2626",
            hover_color="#B91C1C",
            text_color=self.app.COLOR_TEXT,
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.app.show_dashboard,
        ).pack(pady=(30, 30))