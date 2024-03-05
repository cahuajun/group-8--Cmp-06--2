from abc import ABC, abstractmethod
from enum import Enum
from typing import cast
from common.operation_result import ResultStatus
from common.models import Subject, Student, Database
from common.utils import Utils
from cli.ui import UI
from common.services import StudentOperationsService, RegisterService, LoginService, AdminOperationsLogic


class NodeAddType(Enum):
    APPEND = 1
    REPLACE = 2


class IController(ABC):
    @abstractmethod
    def run(self, depth:int) -> 'NavigationNode':
        pass

class NavigationNode:
    def __init__(self, depth: int, node_add_type: NodeAddType, controller: IController) -> None:
        self.node_add_type = node_add_type
        self.controller: IController = controller
        self.depth = depth

    def run(self) -> 'NavigationNode':
        return self.controller.run(self.depth)


class UniversitySystem(IController):

    def __init__(self, db: Database, admin_ops_service: AdminOperationsLogic, login_service: LoginService, register_service: RegisterService) -> None:
        super().__init__()
        self.db = db
        self.admin_ops_service = admin_ops_service
        self.login_service = login_service
        self.register_service = register_service
        

    def run(self, depth:int) -> NavigationNode:
        ui = UI(depth)
        choice = ui.menu("The University System: (A)dmin, (S)tudent, or X: ")
        if choice == "a":
            return NavigationNode(depth + 1, NodeAddType.APPEND, AdminSubSystem(self.db, self.admin_ops_service))
        elif choice == "s":
            return NavigationNode(depth + 1, NodeAddType.APPEND, StudentSubSystem(self.db,  self.login_service, self.register_service))
        elif choice == "x":
            return None
        else:
            ui.invalid_choice()
            return NavigationNode(depth, NodeAddType.REPLACE, self)
    


class StudentSubSystem(IController):

    def __init__(self, db: Database, login_service: LoginService, register_service: RegisterService) -> None:
        super().__init__()
        self.db = db
        self.login_service = login_service
        self.register_service = register_service
        

    def run(self, depth:int) -> NavigationNode:
        ui = UI(depth)
        choice = ui.menu("The Student System (l/r/x): ")
        if choice == "l":
            return NavigationNode(depth, NodeAddType.APPEND, LoginController(self.db, self.login_service))
        elif choice == "r":
            return NavigationNode(depth, NodeAddType.APPEND, RegisterController(self.db, self.register_service))
        elif choice == "x":
            return None
        else:
            ui.invalid_choice()
            return NavigationNode(depth, NodeAddType.REPLACE, self)


class AdminSubSystem(IController):

    def __init__(self,db: Database, admin_ops_service: AdminOperationsLogic) -> None:
        super().__init__()
        self.db = db
        self.admin_ops_service = admin_ops_service
        

    def run(self, depth:int) -> NavigationNode:
        try:
            ui = UI(depth)
            choice = ui.menu("Admin System (c/g/p/r/s/x): ")
            if choice == "c":
                ui.info("Clearing students database")
                answer = ui.crit(
                    "Are you sure you want to clear the database (Y)ES/(N)O: ")
                if answer == "y":
                    self.db.clear()
                    self.db.save()
                    ui.info("Student data cleared")

            elif choice == "g":
                ui.info("Grade Grouping")
                if len(self.db.students) == 0:
                    ui.data("\t< Nothing to Display >")
                else:
                    grouped = self.admin_ops_service.group_students_by_grade()
                    for grade, group in grouped.items():
                        ui.data(f"{grade}\t--> [", end="")
                        students_with_marks = list(filter(lambda s: s.overall_mark, group))
                        index = 0
                        for student in students_with_marks:
                            print(student.grade_str(), end=", " if index < len(students_with_marks) - 1 else "")
                            index += 1
                        print("]")

            elif choice == "p":
                ui.info("PASS/FAIL Partition")
                partitioned = self.admin_ops_service.partition_students()
                for key, partition in partitioned.items():
                    ui.data(f"{key}\t--> [", end="")
                    students_with_marks = list(filter(lambda s: s.overall_mark, partition))
                    index = 0
                    for student in students_with_marks:                        
                        print(student.grade_str(), end=", " if index < len(students_with_marks) - 1 else "")
                        index += 1
                    print("]")

            elif choice == "r":
                std_id = ui.prompt("Remove by ID: ")
                remove_result = self.admin_ops_service.remove_student(std_id)
                if remove_result.success:
                    ui.info(f"Removing Student {std_id} Account")
                else:
                    ui.error(remove_result.status.value, std_id)

            elif choice == "s":
                ui.info("Student List")
                if len(self.db.students) == 0:
                    ui.data("\t< Nothing to Display >")
                else:
                    for student in self.db.students:
                        ui.data(f"{student}")

            elif choice == "x":
                return None

            else:
                ui.invalid_choice()
            return NavigationNode(depth, NodeAddType.REPLACE, self)
        except OSError as e:
            ui.error(f"Encountered error: {e}")
            return NavigationNode(depth, NodeAddType.REPLACE, self)
        except Exception as e:
            ui.error(f"Unexpected error: {e}")
            return NavigationNode(depth, NodeAddType.REPLACE, self)


class LoginController(IController):

    def __init__(self,db: Database, login_service: LoginService) -> None:
        super().__init__()
        self.db = db
        self.login_service = login_service
        

    def run(self, depth:int) -> NavigationNode:
        try:
            ui = UI(depth)
            ui.auth("Student Sign In")
            while True:
                email = ui.prompt("Email: ").strip()
                password = ui.prompt("Password: ")
                login_result = self.login_service.login_student(email, password)
                if login_result.success:
                    ui.info("Email and password formats acceptable")
                    student = cast(Student, login_result.data)
                    return NavigationNode(depth + 1, NodeAddType.REPLACE, StudentCourseController(login_result.data, self.db, StudentOperationsService(student, self.db)))
                ui.error(login_result.status.value)
                if login_result.status != ResultStatus.INVALID_CREDENTIALS:
                    break
            return None
        except OSError as e:
            ui.error(f"Encountered error: {e}")
            return NavigationNode(depth, NodeAddType.REPLACE, self)
        except Exception as e:
            ui.error(f"Unexpected error: {e}")
            return NavigationNode(depth, NodeAddType.REPLACE, self)


class RegisterController(IController):

    def __init__(self,db: Database, register_service: RegisterService) -> None:
        super().__init__()
        self.db = db
        self.register_service = register_service
        

    def run(self, depth:int) -> NavigationNode:
        try:
            ui = UI(depth)
            ui.auth("Student Sign Up")
            while True:
                email = ui.prompt("Email: ").strip()
                password = ui.prompt("Password: ")
                result = self.register_service.ensure_student_doesnot_exist(email, password)
                if result.success:
                    ui.info("Email and password formats acceptable")
                    while (name := ui.prompt("Name: ").strip()) == '':
                        ui.error("Please provide a name for the student")
                    ui.info(f"Enrolling Student {name}")
                    self.register_service.register_student(name, email, password)
                    break
                else:
                    if result.status == ResultStatus.STUDENT_ALREADY_EXISTS:
                        student = cast(Student, result.data)
                        ui.error(result.status.value, student.name)
                    else:
                        ui.error(result.status.value)
                    if (result.status != ResultStatus.INVALID_CREDENTIALS):
                        break
            return None
        except OSError as e:
            ui.error(f"Encountered error: {e}")
            return NavigationNode(depth, NodeAddType.REPLACE, self)
        except Exception as e:
            ui.error(f"Unexpected error: {e}")
            return NavigationNode(depth, NodeAddType.REPLACE, self)



class StudentCourseController(IController):
    def __init__(self,student: Student, db: Database, student_op_service: StudentOperationsService) -> None:
        self.student = student
        self.db = db
        self.student_op_service = student_op_service
        

    def run(self, depth:int) -> NavigationNode:
        try:
            ui = UI(depth)
            choice = ui.menu("Student Course Menu (c/e/r/s/x): ")
            if choice == "x":
                return None  # Handle "x" choice to exit
            elif choice == "c":
                ui.info("Updating Password")
                while True:
                    password = ui.prompt("New Password: ")
                    confirmation = ui.prompt("Confirm Password: ")
                    result = self.student_op_service.change_password(
                        password, confirmation)
                    if result.success:
                        ui.info("Password changed.")
                        break
                    else:
                        ui.error(result.status.value)
                        if result.status != ResultStatus.PASSWORD_MISMATCH:
                            break
            elif choice == "e":
                enrolment_result = self.student_op_service.enroll_in_subject()
                if enrolment_result.success:
                    subject = cast(Subject, enrolment_result.data)
                    ui.info(f"Enrolling in Subject-{subject.id}")
                    ui.info(
                        f"You are now enrolled in {len(self.student.subjects)} out of {Student.MAX_SUBJECTS} subjects")
                else:
                    ui.error(enrolment_result.status.value, Student.MAX_SUBJECTS)
            elif choice == "r":
                subject_id = ui.prompt("Remove Subject by ID: ").strip()
                drop_result = self.student_op_service.drop_subject(subject_id)
                if drop_result.success:
                    ui.info(f"Dropping Subject-{subject_id}")
                    ui.info(
                        f"You are now enrolled in {len(self.student.subjects)} out of {Student.MAX_SUBJECTS} subjects")
                else:
                    ui.error(drop_result.status.value)
            elif choice == "s":
                subject_count = len(self.student.subjects)
                if subject_count > 0:
                    ui.info(f"Showing {subject_count} subjects")
                    for subject in self.student.subjects:
                        ui.data(str(subject))
                else:
                    ui.info("Showing 0 subjects")
            else:
                ui.invalid_choice()

            return NavigationNode(depth, NodeAddType.REPLACE, self)
        except OSError as e:
            ui.error(f"Encountered error: {e}")
            return NavigationNode(depth, NodeAddType.REPLACE, self)
        except Exception as e:
            ui.error(f"Unexpected error: {e}")
            return NavigationNode(depth, NodeAddType.REPLACE, self)
