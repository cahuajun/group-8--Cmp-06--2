from enum import StrEnum

class ResultStatus(StrEnum):
    PASSWORD_MISMATCH = "Password does not match - try again"
    INCORRECT_PASSWORD = "Invalid password"
    ENROLL_LIMIT_REACHED = "Students are allowed to enroll in {} subjects only"
    SUBJECT_NOT_FOUND = "Subject not found in student's enrollment list"
    INVALID_CREDENTIALS = "Incorrect email or password format"
    STUDENT_NOT_FOUND = "Student does not exist"
    F_STUDENT_NOT_FOUND = "Student {} does not exist"
    STUDENT_ALREADY_EXISTS = "Student {} already exists"

class OperationResult():
    def __init__(self, success:bool, status: ResultStatus, data: any = None):
        self.success = success
        self.status = status
        self.data = data

    @staticmethod
    def SUCCESS(data: any = None):
        return OperationResult(True, None, data)

    @staticmethod
    def FAILURE(status: ResultStatus, data: any = None):
        return OperationResult(False, status, data)