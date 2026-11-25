
import customtkinter as ctk
from theme import *


class ResultsPage(ctk.CTkFrame):

    def __init__(self, parent, app):

        super().__init__(parent, fg_color=BG_COLOR)

        self.app = app

        ctk.CTkLabel(
            self,
            text="Study Results",
            font=("Arial", 30, "bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(15, 5))

        ctk.CTkLabel(
            self,
            text="Your optimized study plan.",
            font=("Arial", 14),
            text_color=SECONDARY_TEXT
        ).pack(anchor="w", pady=(0, 25))

        self.result_frame = ctk.CTkFrame(
            self,
            fg_color=CARD_COLOR,
            corner_radius=12
        )

        self.result_frame.pack(fill="both", expand=True)

        self.refresh()

    def refresh(self):

        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if not self.app.selected_tasks:

            ctk.CTkLabel(
                self.result_frame,
                text="No results yet. Calculate your best tasks first.",
                font=("Arial", 15),
                text_color=SECONDARY_TEXT
            ).pack(pady=40)

            return

        ctk.CTkLabel(
            self.result_frame,
            text="Recommended Tasks",
            font=("Arial", 22, "bold"),
            text_color=PRIMARY_COLOR
        ).pack(pady=20)

        for task in self.app.selected_tasks:

            ctk.CTkLabel(
                self.result_frame,
                text=f'{task["name"]} | {task["hours"]} Hours',
                font=("Arial", 15),
                text_color=TEXT_COLOR
            ).pack(pady=8)

        total_hours = sum(
            task["hours"]
            for task in self.app.selected_tasks
        )

        ctk.CTkLabel(
            self.result_frame,
            text=f"Available Hours: {self.app.available_hours}",
            text_color=SECONDARY_TEXT
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self.result_frame,
            text=f"Used Hours: {total_hours}",
            font=("Arial", 16, "bold"),
            text_color=TEXT_COLOR
        ).pack(pady=5)

        ctk.CTkLabel(
            self.result_frame,
            text=f"Total Priority: {self.app.total_priority}",
            font=("Arial", 18, "bold"),
            text_color=SUCCESS_COLOR
        ).pack(pady=15)
