
import customtkinter as ctk

from theme import *
from pages.dashboard import DashboardPage
from pages.tasks import TasksPage
from pages.results import ResultsPage


class StudyPlanner(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Study Planner")
        self.geometry("1200x750")
        self.minsize(950, 600)
        self.configure(fg_color=BG_COLOR)

        self.tasks = []
        self.selected_tasks = []
        self.available_hours = 0
        self.total_priority = 0

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()

        self.content = ctk.CTkFrame(
            self,
            fg_color=BG_COLOR,
            corner_radius=0
        )

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=25,
            pady=20
        )

        self.show_page("Dashboard")

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            fg_color=SIDEBAR_COLOR,
            corner_radius=0
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="Study Planner",
            font=("Arial", 24, "bold"),
            text_color=PRIMARY_COLOR
        ).pack(pady=(35, 45))

        buttons = [
            ("Dashboard", "▦"),
            ("Task Selection", "✓"),
            ("Study Results", "▤")
        ]

        for page, symbol in buttons:

            ctk.CTkButton(
                self.sidebar,
                text=f"{symbol}   {page}",
                anchor="w",
                height=48,
                corner_radius=10,
                fg_color="transparent",
                text_color=TEXT_COLOR,
                hover_color="#EFF6FF",
                font=("Arial", 14),
                command=lambda p=page: self.show_page(p)
            ).pack(fill="x", padx=15, pady=6)

        ctk.CTkLabel(
            self.sidebar,
            text="Organize your time.\nAchieve your goals.",
            font=("Arial", 12),
            text_color=SECONDARY_TEXT
        ).pack(side="bottom", pady=25)

    def show_page(self, page_name):

        for widget in self.content.winfo_children():
            widget.destroy()

        if page_name == "Dashboard":

            page = DashboardPage(self.content, self)

        elif page_name == "Task Selection":

            page = TasksPage(self.content, self)

        elif page_name == "Study Results":

            page = ResultsPage(self.content, self)

        page.pack(fill="both", expand=True)


if __name__ == "__main__":

    app = StudyPlanner()
    app.mainloop()
