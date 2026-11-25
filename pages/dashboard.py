
import customtkinter as ctk
from theme import *


class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent, app):

        super().__init__(parent, fg_color=BG_COLOR)

        self.app = app

        ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Arial", 30, "bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(15, 5))

        ctk.CTkLabel(
            self,
            text="Welcome! Here's your study overview.",
            font=("Arial", 14),
            text_color=SECONDARY_TEXT
        ).pack(anchor="w", pady=(0, 25))

        self.stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.stats_frame.pack(fill="x")

        for i in range(3):
            self.stats_frame.grid_columnconfigure(i, weight=1)

        self.cards = []

        for i in range(3):

            card = ctk.CTkFrame(
                self.stats_frame,
                fg_color=CARD_COLOR,
                corner_radius=12,
                height=120
            )

            card.grid(
                row=0,
                column=i,
                padx=7,
                sticky="nsew"
            )

            card.grid_propagate(False)
            self.cards.append(card)

        ctk.CTkLabel(
            self,
            text="Your Study Tasks",
            font=("Arial", 20, "bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(35, 15))

        self.task_list = ctk.CTkScrollableFrame(
            self,
            fg_color=CARD_COLOR,
            corner_radius=12
        )

        self.task_list.pack(fill="both", expand=True)

        self.refresh()

    def refresh(self):

        tasks = self.app.tasks

        total = len(tasks)
        hours = sum(t["hours"] for t in tasks)
        priority = sum(t["priority"] for t in tasks)

        values = [
            ("Total Tasks", total),
            ("Study Hours", hours),
            ("Total Priority", priority)
        ]

        for card, (label, value) in zip(self.cards, values):

            for widget in card.winfo_children():
                widget.destroy()

            ctk.CTkLabel(
                card,
                text=label,
                font=("Arial", 14),
                text_color=SECONDARY_TEXT
            ).pack(pady=(20, 8))

            ctk.CTkLabel(
                card,
                text=str(value),
                font=("Arial", 28, "bold"),
                text_color=PRIMARY_COLOR
            ).pack()

        for widget in self.task_list.winfo_children():
            widget.destroy()

        if not tasks:

            ctk.CTkLabel(
                self.task_list,
                text="No tasks added yet. Go to Task Selection to get started.",
                text_color=SECONDARY_TEXT
            ).pack(pady=30)

        for task in tasks:

            row = ctk.CTkFrame(
                self.task_list,
                fg_color="#F8FAFC",
                corner_radius=8
            )

            row.pack(fill="x", padx=8, pady=5)

            ctk.CTkLabel(
                row,
                text=task["name"],
                font=("Arial", 14, "bold"),
                text_color=TEXT_COLOR
            ).pack(side="left", padx=15, pady=15)

            ctk.CTkLabel(
                row,
                text=f'{task["hours"]} Hours',
                text_color=SECONDARY_TEXT
            ).pack(side="right", padx=15)
