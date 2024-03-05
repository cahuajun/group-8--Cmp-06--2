import re


class Utils:
    PASSWORD_PATTERN = r"^[A-Z][a-zA-Z]{5,}[0-9]{3,}$"
    EMAIL_PATTERN = r"^\w+\.\w+@university\.com$"
    
    @staticmethod
    def verify_password(password: str) -> bool:
        return re.match(Utils.PASSWORD_PATTERN, password)

    @staticmethod
    def verify_email(email: str) -> bool:
        return re.match(Utils.EMAIL_PATTERN, email)

    @staticmethod
    def calculate_grade(mark: float) -> float:
        if mark is not None:
            if mark >= 85:
                return 'HD'
            elif mark >= 75:
                return 'D'
            elif mark >= 65:
                return 'C'
            elif mark >= 50:
                return 'P'
            else:
                return 'Z'
