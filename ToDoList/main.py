import customtkinter as ctk

# --- Configuration & Styling ---
APP_THEME = "dark"
PRIMARY_COLOR = "#1f538d"
DANGER_COLOR = "#922b21"
DANGER_HOVER = "#7b241c"


class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Niko's Task Manager")
        self.geometry("500x600")
        ctk.set_appearance_mode(APP_THEME)
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- UI Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.title_label = ctk.CTkLabel(
            self.header_frame, text="Things to do:",
            font=ctk.CTkFont(family="Helvetica", size=28, weight="bold")
        )
        self.title_label.pack(side="left")

        self.counter_label = ctk.CTkLabel(
            self.header_frame, text="0 Tasks Remaining",
            font=ctk.CTkFont(size=12), text_color="gray"
        )
        self.counter_label.pack(side="right", pady=(10, 0))

        # --- Input Area ---
        self.entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entry_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry_frame.grid_columnconfigure(0, weight=1)

        self.task_entry = ctk.CTkEntry(
            self.entry_frame, placeholder_text="What needs to be done?",
            height=45, font=ctk.CTkFont(size=14)
        )
        self.task_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        self.add_button = ctk.CTkButton(
            self.entry_frame, text="Add Task", width=100, height=45,
            font=ctk.CTkFont(weight="bold"), command=self.add_task
        )
        self.add_button.grid(row=0, column=1)

        # --- Scrollable Task List ---
        self.tasks_list = ctk.CTkScrollableFrame(self, label_text="Your Tasks", label_font=("Helvetica", 14, "bold"))
        self.tasks_list.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # --- Footer Actions ---
        self.clear_button = ctk.CTkButton(
            self, text="Clear All Tasks", fg_color="transparent",
            text_color="gray", hover_color="#333333", command=self.clear_all
        )
        self.clear_button.grid(row=3, column=0, pady=10)

        self.task_widgets = []

    def add_task(self):
        text = self.task_entry.get().strip()
        if text:
            self.create_task_row(text)
            self.task_entry.delete(0, 'end')
            self.update_counter()

    def create_task_row(self, text):
        task_frame = ctk.CTkFrame(self.tasks_list, fg_color="transparent")
        task_frame.pack(fill="x", pady=5, padx=5)

        # Variable for completion state
        check_var = ctk.StringVar(value="off")

        # Checkbox with toggle effect
        checkbox = ctk.CTkCheckBox(
            task_frame, text=text, variable=check_var,
            onvalue="on", offvalue="off",
            command=lambda: self.toggle_task(checkbox, check_var)
        )
        checkbox.pack(side="left", padx=5, expand=True, fill="x")

        delete_btn = ctk.CTkButton(
            task_frame, text="✕", fg_color=DANGER_COLOR,
            hover_color=DANGER_HOVER, width=30, height=30,
            command=lambda: self.delete_task(task_frame)
        )
        delete_btn.pack(side="right", padx=5)

        self.task_widgets.append(task_frame)

    def toggle_task(self, checkbox, var):
        if var.get() == "on":
            checkbox.configure(text_color="gray")
        else:
            checkbox.configure(text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        self.update_counter()

    def delete_task(self, frame):
        frame.destroy()
        self.task_widgets.remove(frame)
        self.update_counter()

    def clear_all(self):
        for widget in self.task_widgets:
            widget.destroy()
        self.task_widgets.clear()
        self.update_counter()

    def update_counter(self):
        count = len(self.task_widgets)
        self.counter_label.configure(text=f"{count} Tasks Total")


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()