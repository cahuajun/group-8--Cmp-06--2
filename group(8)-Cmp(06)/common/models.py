import random
import os
import jsonpickle
from common.utils import Utils


class Subject:
    def __init__(self, id: str) -> None:
        self.id = id
        self._generate_mark()

    def _generate_mark(self) -> None:
        self._mark = random.randint(25, 100)
        self._grade = Utils.calculate_grade(self.mark)

    def __str__(self) -> str:
        return f"[ Subject::{self.id} -- mark = {self.mark} -- grade = {self.grade.rjust(3)}]"

    @property
    def mark(self):
        return self._mark

    @property
    def grade(self):
        return self._grade


class Student:
    MIN_PASS_MARK = 50
    MAX_SUBJECTS = 4

    
    def __init__(self, id: str, name: str, email: str, password: str) -> None:
        self.id = id
        self._name: str = name
        self._email: str = email
        self._password: str = password
        self._subjects: list[Subject] = []
        self.overall_mark: float = None
        self.overall_grade:  str = None

    def __str__(self) -> str:
        return f"{self._name}".ljust(25) + " :: " + f"{self.id}".rjust(6) + " --> " + "EMAIL: " + f"{self.email}".rjust(30)

    def grade_str(self):
        if not self.overall_mark:
            return None
        return f"{self._name} :: {self.id} --> GRADE: {self.overall_grade}  -  MARK: {round(self.overall_mark,2)}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def subjects(self) -> list[Subject]:
        return self._subjects

    def can_enroll_subject(self) -> bool:
        return len(self._subjects) < Student.MAX_SUBJECTS

    def enroll_in_subject(self, subject: Subject) -> Subject:
        self._subjects.append(subject)
        self.overall_mark = self._calculate_average_mark()
        self.overall_grade = Utils.calculate_grade(self.overall_mark)
        return subject

    def find_enrolled_subject(self, subject_id: str) -> Subject:
        return next((subject for subject in self.subjects if subject.id == subject_id), None)

    def drop_subject(self, subject_id: str) -> None:
        subject = self.find_enrolled_subject(subject_id)
        if not subject == None:
            self._subjects.remove(subject)
            self.overall_mark = self._calculate_average_mark()
            self.overall_grade = Utils.calculate_grade(self.overall_mark)

    def change_password(self, new_password: str) -> None:
        self._password = new_password

    def _calculate_average_mark(self) -> float:
        total_mark = sum(subject._mark for subject in self._subjects)
        return total_mark / len(self._subjects) if len(self._subjects) > 0 else None

    def passes_course(self) -> bool:
        return self.overall_mark >= Student.MIN_PASS_MARK if self.overall_mark else None
    
    def check_password(self, password:str) -> bool:
        return self._password == password


class Database:
    def __init__(self) -> None:
        self.FILE_NAME: str = "students.data"
        self._create_file_if_not_exists()
        self._load()

    def _create_file_if_not_exists(self) -> None:
        if not os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, 'w') as file:
                encoded = jsonpickle.encode([])
                file.write(encoded)

    def save(self) -> None:
        with open(self.FILE_NAME, 'w') as file:
            file.write(jsonpickle.encode(self.students))
        

    def _load(self) -> None:
        with open(self.FILE_NAME, 'r') as file:
            data = file.read()
            self.students: list[Student] = jsonpickle.decode(data)

    def clear(self) -> None:
        self.students = []

    def find_student_by_email(self, email: str) -> Student:
        return next((s for s in self.students if s.email == email), None)

    def find_student_by_id(self, id: str) -> Student:
        return next((s for s in self.students if s.id == id), None)

    def remove_student(self, id: str) -> bool:
        student = self.find_student_by_id(id)
        if student == None:
            return False
        self.students.remove(student)
        return True

    def register_student(self, id: str, name: str, email: str, password: str) -> Student:
        student = Student(id, name, email, password)
        self.students.append(student)
        return student

    def generate_unique_student_id(self) -> str:
        while True:
            id = str(random.randint(1, 999999)).zfill(6)
            if not self.find_student_by_id(id):
                return id

    def generate_unique_subject_id(self, student: Student) -> str:
        while True:
            id = str(random.randint(1, 999)).zfill(3)
            if not student.find_enrolled_subject(id):
                return id
    