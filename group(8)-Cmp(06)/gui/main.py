import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path else None

import tkinter as tk
from tkinter import messagebox, Button
from gui.login import LoginForm
from gui.enrollment import EnrollmentForm
from common.models import Database, Student
from gui.subjects import SubjectsForm
from common.services import LoginService, StudentOperationsService

class MainForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.title("University System")
        self.configure(bg="#394867")

        self.menu_frame = tk.Frame(self, bg="#212A3E", width=100)
        self.menu_frame.pack(side="left", fill="y", pady=20, padx=20)
        self.menu_frame.pack_propagate(False)

        

        self.wrapper_frame = tk.Frame(self, width=10, bg="#9BA4B5")
        self.wrapper_frame.pack(
            side="right", fill="both", expand=True, pady=20, padx=20)
        self.wrapper_frame.columnconfigure(0, weight=1)
        self.wrapper_frame.rowconfigure(1, weight=1)


        self.content_frame = tk.Frame(self.wrapper_frame, bg="#9BA4B5")
        self.content_frame.grid(row=0, column=0, sticky="nsew")

      

        self.bottom_label = tk.Label(self.wrapper_frame, bg="#708573", font=("Arial", 10, "bold"), foreground="#212A3E")
        self.bottom_label.grid(row=1, column=0, sticky="sew")

        self.load_login_form()

        self.selected_menu_index = tk.IntVar()

    def clear_frame_contents(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def show_selected_menu_item(self, button: Button):
        self.current_menu_button = button
        self.menu_enrollment

    def login_success(self, logged_in_student: Student):
        self.logged_in_student = logged_in_student
        self.selected_menu_index.set(0)
        self.load_enrollment_form()
        self.load_main_menu()

    def clear_info(self):
        self.bottom_label.config(text="")

    # show info for specified time and then clear
    def show_info(self, message, time):
        self.bottom_label.config(text=message)
        self.after(time, self.clear_info)

    def enroll_success(self, text:str):
        self.show_info(text, 8000)

    def failure_callback(self, message):
        messagebox.showerror("Login failed", message)

    def load_login_form(self):
        self.clear_frame_contents(self.content_frame)
        login_service = LoginService(self.db)
        login_form = LoginForm(
            self.content_frame, self.login_success, self.failure_callback, login_service)
        login_form.pack(fill="both", expand=True, padx=20, pady=20)
        login_form.configure(bg='#9BA4B5')

    def load_main_menu(self):
        self.menu_items = {
            0: {"label": "Enrollment", "function": self.load_enrollment_form},
            1: {"label": "Subjects", "function": self.load_subjects_form},
            2: {"label": "Log out", "function": self.log_out}
        }
        for key, value in self.menu_items.items():
            rb = tk.Radiobutton(
                self.menu_frame,
                text=value["label"],
                variable=self.selected_menu_index,
                value=key,
                command=value["function"],
                indicatoron=False,
                width=20,

            )
            rb.pack(pady=10, padx=10, anchor=tk.W)

    def load_enrollment_form(self):
        self.clear_frame_contents(self.content_frame)
        student_op_service = StudentOperationsService(self.logged_in_student, self.db)
        enrollment_form = EnrollmentForm(
            self.content_frame, self.enroll_success, self.failure_callback, self.logged_in_student, student_op_service)
        enrollment_form.pack(fill="both", expand=True)

    def load_subjects_form(self):
        self.clear_frame_contents(self.content_frame)
        subjects_form = SubjectsForm(self.content_frame, self.logged_in_student)
        subjects_form.pack(fill="both", expand=False)

    def log_out(self):
        if messagebox.askyesno("Log out", "Are you sure you want to log out?") == False:
            return
        self.clear_frame_contents(self.content_frame)
        self.clear_frame_contents(self.menu_frame)        
        self.logged_in_student = None
        self.selected_menu_index.set(-1)
        self.load_login_form()


def main():
    try:
        app = MainForm()
        app.geometry("800x600")
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", e)


if __name__ == "__main__":
    main()