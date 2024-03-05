import os
import tkinter as tk
from typing import Callable, cast
from common.utils import Utils
from common.models import Student
from common.services import LoginService


class LoginForm(tk.Frame):
    def __init__(self, parent, success_callback: Callable[[str], None], failure_callback: Callable[[str], None], login_service: LoginService):
        super().__init__(parent)

        self.login_service = login_service

        self.success_callback = success_callback
        self.failure_callback = failure_callback

        # Labels
        self.email_label = tk.Label(
            self, text="Email", width=10, bg="#9BA4B5", anchor="sw", font=("Arial", 10, "bold"))
        self.email_label.grid(row=0, column=0, padx=10,
                              pady=(10, 0), sticky="sw")

        self.password_label = tk.Label(
            self, text="Password", width=10, bg="#9BA4B5", anchor="sw", font=("Arial", 10, "bold"))
        self.password_label.grid(
            row=2, column=0, padx=10, pady=(10, 0), sticky="sw")

        # Entries
        self.email_entry = tk.Entry(self, width=40)
        self.email_entry.grid(row=1, column=0, padx=10, pady=10)

        self.password_entry = tk.Entry(self, show="*", width=40)
        self.password_entry.grid(row=3, column=0, padx=10, pady=10)

        # Button
        self.login_button = tk.Button(
            self, text="Login", command=self.login, anchor="e")
        self.login_button.grid(row=4, column=0, padx=10, pady=10)

        

        self.bind('<Return>', self.click_login)
        self.email_entry.bind('<Return>', self.click_login)
        self.password_entry.bind('<Return>', self.click_login)
        self.login_button.bind('<Return>', self.click_login)
        self.focus_set()

    def click_login(self, event=None):
        self.login_button.invoke()

    def login(self):
        try:
            email = self.email_entry.get()
            password = self.password_entry.get()
            login_result = self.login_service.login_student(email, password)
            if login_result.success:
                student = cast(Student, login_result.data)
                self.success_callback(
                    student) if self.success_callback else None
            else:
                self.failure_callback(
                    login_result.status.value) if self.failure_callback else None
        except OSError as e:
            self.failure_callback(str(e)) if self.failure_callback else None
        except Exception as e:
            self.failure_callback("Unexpected error: " +
                                  str(e)) if self.failure_callback else None
