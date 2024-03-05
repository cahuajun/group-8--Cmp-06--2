import tkinter as tk
from tkinter import  ttk
from tkinter import messagebox
from common.models import Database, Student


class SubjectsForm(tk.Frame):
    def __init__(self, parent, student:Student):
        super().__init__(parent)        
        self.tree = ttk.Treeview(self, columns=("ID", "Mark", "Grade"), show="headings")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Mark", text="Mark")
        self.tree.heading("Grade", text="Grade")

        self.tree.column("ID", width=100)
        self.tree.column("Mark", width=100)
        self.tree.column("Grade", width=100)

        self.tree.pack(pady=20)

        for subject in student.subjects:
            self.tree.insert("", tk.END, values=(subject.id, subject.mark, subject.grade))