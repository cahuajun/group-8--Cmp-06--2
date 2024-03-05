from colorama import Fore, init, Style
init(autoreset=True)
class UI:
    def __init__(self, indent: int) -> None:
        self.indent = indent

    def menu(self, text: str) -> str:
        print(Fore.CYAN + '\t'*self.indent + text, end="")
        return input().strip().lower()

    def prompt(self, text: str) -> str:
        print('\t'*self.indent + text, end="")
        return input()

    def info(self, text: str, *args: str) -> None:
        formatted_text = text if not args else text.format(*args)
        print(Fore.YELLOW + '\t'*self.indent + formatted_text)

    def error(self, text: str, *args: str) -> None:
        formatted_text = text if not args else text.format(*args)
        print(Fore.RED + '\t'*self.indent + formatted_text)

    def auth(self, text: str, *args: str) -> None:
        formatted_text = text if not args else text.format(*args)
        print(Fore.GREEN + '\t'*self.indent + formatted_text)

    def data(self, text: str, end: str = "\r\n", *args: str) -> None:
        formatted_text = text if not args else text.format(*args)
        print('\t'*self.indent + formatted_text, end=end)

    def crit(self, text: str, *args: str) -> str:
        formatted_text = text if not args else text.format(*args)
        print(Fore.RED + '\t'*self.indent + formatted_text, end="")
        return input().strip().lower()

    def invalid_choice(self) -> None:
        self.error("Invalid choice. Please try again.")