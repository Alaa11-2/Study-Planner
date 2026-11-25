
import customtkinter as ctk
from theme import *
from algorithms.knapsack import knapsack


class TasksPage(ctk.CTkFrame):

    def __init__(self, parent, app):

        super().__init__(parent, fg_color=BG_COLOR)

        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header
        ctk.CTkLabel(
            self,
            text="Task Selection",
            font=("Arial", 28, "bold"),
            text_color=TEXT_COLOR
        ).grid(row=0, column=0, sticky="w", pady=(5, 3))

        ctk.CTkLabel(
            self,
            text="Add your study tasks and calculate the best combination.",
            font=("Arial", 13),
            text_color=SECONDARY_TEXT
        ).grid(row=1, column=0, sticky="w", pady=(0, 15))

        # Main content
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.main_frame.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Add Task Form
        self.form = ctk.CTkFrame(
            self.main_frame,
            fg_color=CARD_COLOR,
            corner_radius=12
        )

        self.form.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        self.form.grid_columnconfigure((0, 1, 2), weight=1)

        self.name_entry = ctk.CTkEntry(
            self.form,
            placeholder_text="Task / Subject Name",
            height=40
        )
        self.name_entry.grid(
            row=0, column=0,
            padx=(15, 5), pady=15, sticky="ew"
        )

        self.hours_entry = ctk.CTkEntry(
            self.form,
            placeholder_text="Required Hours",
            height=40
        )
        self.hours_entry.grid(
            row=0, column=1,
            padx=5, pady=15, sticky="ew"
        )

        self.priority_entry = ctk.CTkEntry(
            self.form,
            placeholder_text="Priority (1 - 10)",
            height=40
        )
        self.priority_entry.grid(
            row=0, column=2,
            padx=(5, 15), pady=15, sticky="ew"
        )

        ctk.CTkButton(
            self.form,
            text="Add Task",
            height=38,
            command=self.add_task
        ).grid(
            row=1, column=0,
            columnspan=3,
            padx=15, pady=(0, 5), sticky="ew"
        )

        self.message = ctk.CTkLabel(
            self.form,
            text="",
            text_color=SUCCESS_COLOR
        )
        self.message.grid(
            row=2, column=0,
            columnspan=3,
            pady=(0, 8)
        )

        # Tasks List
        self.task_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color=CARD_COLOR,
            corner_radius=12
        )

        self.task_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=(0, 12)
        )

        # Available Hours
        self.bottom_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=CARD_COLOR,
            corner_radius=12
        )

        self.bottom_frame.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        self.bottom_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.bottom_frame,
            text="Available Study Time (Hours)",
            font=("Arial", 15, "bold"),
            text_color=TEXT_COLOR
        ).grid(
            row=0, column=0,
            padx=15, pady=(12, 5), sticky="w"
        )

        self.capacity_entry = ctk.CTkEntry(
            self.bottom_frame,
            placeholder_text="How many hours can you study?",
            height=40
        )

        self.capacity_entry.grid(
            row=1, column=0,
            padx=15, pady=5, sticky="ew"
        )

        ctk.CTkButton(
            self.bottom_frame,
            text="Calculate Best Tasks",
            height=42,
            command=self.calculate
        ).grid(
            row=2, column=0,
            padx=15, pady=(5, 12), sticky="ew"
        )

        self.refresh_tasks()

    def add_task(self):

        name = self.name_entry.get().strip()

        try:
            hours = int(self.hours_entry.get())
            priority = int(self.priority_entry.get())

            if not name or hours <= 0 or not 1 <= priority <= 10:
                raise ValueError

            if any(
                t["name"].lower() == name.lower()
                for t in self.app.tasks
            ):
                self.message.configure(
                    text="This task already exists.",
                    text_color=DANGER_COLOR
                )
                return

        except ValueError:
            self.message.configure(
                text="Enter valid task details.",
                text_color=DANGER_COLOR
            )
            return

        self.app.tasks.append({
            "name": name,
            "hours": hours,
            "priority": priority
        })

        self.name_entry.delete(0, "end")
        self.hours_entry.delete(0, "end")
        self.priority_entry.delete(0, "end")

        self.message.configure(
            text="Task added successfully!",
            text_color=SUCCESS_COLOR
        )

        self.app.selected_tasks = []
        self.refresh_tasks()

    def refresh_tasks(self):

        for widget in self.task_frame.winfo_children():
            widget.destroy()

        if not self.app.tasks:
            ctk.CTkLabel(
                self.task_frame,
                text="No tasks added yet.",
                text_color=SECONDARY_TEXT
            ).pack(pady=20)

            return

        for task in self.app.tasks:

            row = ctk.CTkFrame(
                self.task_frame,
                fg_color="#F8FAFC",
                corner_radius=8
            )

            row.pack(fill="x", padx=5, pady=5)

            info = (
                f'{task["name"]}  |  '
                f'{task["hours"]} Hours  |  '
                f'Priority: {task["priority"]}'
            )

            ctk.CTkLabel(
                row,
                text=info,
                text_color=TEXT_COLOR
            ).pack(side="left", padx=12, pady=10)

    def calculate(self):

        try:
            capacity = int(self.capacity_entry.get())

            if capacity <= 0:
                raise ValueError

        except ValueError:
            self.message.configure(
                text="Please enter valid available hours.",
                text_color=DANGER_COLOR
            )
            return

        if not self.app.tasks:
            self.message.configure(
                text="Please add tasks first.",
                text_color=DANGER_COLOR
            )
            return

        selected, total_priority = knapsack(
            self.app.tasks,
            capacity
        )

        self.app.selected_tasks = selected
        self.app.available_hours = capacity
        self.app.total_priority = total_priority

        self.message.configure(
            text="Calculation completed! Open Study Results.",
            text_color=SUCCESS_COLOR
        )
