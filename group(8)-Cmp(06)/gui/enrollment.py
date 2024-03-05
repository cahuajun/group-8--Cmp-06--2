import tkinter as tk
from tkinter import messagebox
from common.models import Database, Student, Subject
from typing import Callable, cast
from common.services import StudentOperationsService
class EnrollmentForm(tk.Frame):
    def __init__(self, parent, success_callback: Callable[[str], None] , failure_callback: Callable[[str],None], student: Student, student_op_service: StudentOperationsService):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)


        self.student_op_service = student_op_service

        self.student = student
        self.subject_count_var = tk.IntVar(value=len(self.student.subjects))
        
        self.top_label = tk.Label(
            self, bg="#9BA4B5", font=("Arial", 10, "bold"))
        self.top_label.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        
        self.update_top_text()

        self.success_callback = success_callback
        self.failure_callback = failure_callback

        self.left_frame = tk.Frame(self)
        self.left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.right_frame = tk.Frame(self)
        self.right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.enroll_button = tk.Button(self.left_frame, text="Enroll", command=self.enroll)
        self.enroll_button.grid(row=0, column=0, padx=10, pady=10)        

        self.drop_button = tk.Button(self.right_frame, text="Drop Subject", command=self.drop)
        self.drop_button.grid(row=0, column=0, padx=10, pady=10)

        self.subject_id_entry = tk.Entry(self.right_frame)
        self.subject_id_entry.grid(row=0, column=1, padx=10, pady=10)

    # enroll in random subject, call student.enroll
    def update_top_text(self):
         self.top_label.config(text=f'Enrolled in {self.subject_count_var.get()} out of {Student.MAX_SUBJECTS} subjects')
    def show_info(self, text:str):
         self.bottom_label.config(text=str)

    def enroll(self):
        try:
            enrolment_result = self.student_op_service.enroll_in_subject()

            if enrolment_result.success:
                subject = cast(Subject, enrolment_result.data)
                self.subject_count_var.set(len(self.student.subjects))
                self.update_top_text()
                self.success_callback(f"Subject {subject.id} added") if self.success_callback else None
            else:
                self.failure_callback(enrolment_result.status.value.format(Student.MAX_SUBJECTS)) if self.failure_callback else None
        except OSError as e:
            self.failure_callback(str(e)) if self.failure_callback else None
        except Exception as e:
            self.failure_callback("Unexpected error: " +
                                  str(e)) if self.failure_callback else None

    # drop subject, call student.drop_subject
    def drop(self):
        try:
            subject_id = self.subject_id_entry.get()
            if messagebox.askyesno("Drop Subject", f"Are you sure you want to drop subject {subject_id}?") == False:
                return
            drop_result = self.student_op_service.drop_subject(subject_id)
            if drop_result.success:
                self.subject_count_var.set(len(self.student.subjects))
                self.update_top_text()
                self.success_callback(f"Subject {subject_id} dropped") if self.success_callback else None
            else:
                self.failure_callback(drop_result.status.value)
        except OSError as e:
            self.failure_callback(str(e)) if self.failure_callback else None
        except Exception as e:
            self.failure_callback("Unexpected error: " +
                                  str(e)) if self.failure_callback else None
       