from common.operation_result import OperationResult, ResultStatus
from common.utils import Utils
from common.models import Database, Student, Subject


class StudentOperationsService:
    def __init__(self, student: Student, db: Database):
        self.student = student
        self.db = db

    def change_password(self, password, confirm_password) -> OperationResult:
        if password != confirm_password:
            return OperationResult.FAILURE(ResultStatus.PASSWORD_MISMATCH)
        if not Utils.verify_password(password):
            return OperationResult.FAILURE(ResultStatus.INCORRECT_PASSWORD)
        self.student.change_password(password)
        self.db.save()
        return OperationResult.SUCCESS()

    def enroll_in_subject(self) -> OperationResult:
        if not self.student.can_enroll_subject():
            return OperationResult.FAILURE(ResultStatus.ENROLL_LIMIT_REACHED)
        subject_id = self.db.generate_unique_subject_id(self.student)
        subject = Subject(subject_id)
        self.student.enroll_in_subject(subject)
        self.db.save()
        return OperationResult.SUCCESS(subject)

    def drop_subject(self, subject_id) -> OperationResult:
        if not self.student.find_enrolled_subject(subject_id):
            return OperationResult.FAILURE(ResultStatus.SUBJECT_NOT_FOUND)
        self.student.drop_subject(subject_id)
        self.db.save()
        return OperationResult.SUCCESS()


class RegisterService:
    def __init__(self, db: Database):
        self.db = db

    def ensure_student_doesnot_exist(self, email, password) -> OperationResult:
        if not Utils.verify_email(email) or not Utils.verify_password(password):
            return OperationResult.FAILURE(ResultStatus.INVALID_CREDENTIALS)
        found_student = self.db.find_student_by_email(email)
        if found_student:
            return OperationResult.FAILURE(ResultStatus.STUDENT_ALREADY_EXISTS, found_student)
        return OperationResult.SUCCESS()

    def register_student(self, name, email, password) -> OperationResult:
        student_id = self.db.generate_unique_student_id()
        student = self.db.register_student(student_id, name, email, password)
        self.db.save()
        return OperationResult.SUCCESS(student)


class LoginService:
    def __init__(self, db):
        self.db = db

    def login_student(self, email, password) -> OperationResult:
        if not Utils.verify_email(email) or not Utils.verify_password(password):
            return OperationResult.FAILURE(ResultStatus.INVALID_CREDENTIALS)
        found_student = self.db.find_student_by_email(email)
        if found_student:
            if found_student.check_password(password):
                return OperationResult.SUCCESS(found_student)
            else:
                return OperationResult.FAILURE(ResultStatus.INCORRECT_PASSWORD)
        else:
            return OperationResult.FAILURE(ResultStatus.STUDENT_NOT_FOUND)


class AdminOperationsLogic:

    def __init__(self, db: Database):
        self.db = db

    def group_students_by_grade(self) -> dict[str, list]:
        grouped_students = {}
        for student in self.db.students:
            grade = student.overall_grade
            if grade is not None:
                if grade not in grouped_students:
                    grouped_students[grade] = []
                grouped_students[grade].append(student)
        return grouped_students

    def partition_students(self) -> dict:
        partitioned_students = {"PASS": [], "FAIL": []}
        for student in self.db.students:
            if student.overall_grade is not None:
                passes_string = "PASS" if student.passes_course() else "FAIL"
                partitioned_students[passes_string].append(student)
        return partitioned_students

    def remove_student(self, student_id) -> OperationResult:
        student = self.db.find_student_by_id(student_id)
        if not student:
            return OperationResult.FAILURE(ResultStatus.F_STUDENT_NOT_FOUND, student_id)
        self.db.remove_student(student_id)
        self.db.save()
        return OperationResult.SUCCESS()
