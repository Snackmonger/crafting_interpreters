import sys
from src.token import Token
from src.scanner import Scanner


class Lox:
    """The main interpreter for the Lox language.
    
    Lox is a scripting language, which means it executes directly from source.
    Our interpreter supports two ways of running code. You can run a source 
    file passed as an argument to the main function, or you can run the main
    function without any arguments to enter the interactive interpreter.
    """
    had_error: bool
    def __init__(self) -> None:
        self.had_error = False

    def main(self, *args: str) -> None:
        if len(args) > 1:
            print("Usage: plox [script]")
            sys.exit(64)
        elif len(args) == 1:
            self.run_file(args[0])
        else:
            self.run_prompt()

    def run_prompt(self) -> None:
        """Run the interactive REPL (read, evaluate, print, loop)."""
        while True:
            line = input("> ")
            if line == "quit()":
                break
            self.run(line)
            self.had_error = False

    def run(self, source: str) -> None:
        """Run the source file as a script."""
        if self.had_error:
            sys.exit(65)
        scanner: Scanner = Scanner(source, self)
        tokens: list[Token] = scanner.scan_tokens()

        for token in tokens:
            print(token)

    
    def run_file(self, path: str) -> None:
        """Create a"""
        with open(path, encoding="utf8") as f:
            self.run(str(f))

    @staticmethod
    def error(line: int, message: str) -> None:
        """Configure and report an error."""
        Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        """Report an error and indicate to the interpreter that the code failed."""
        print("[line " + str(line) + "] Error" + where + ": " + message)
        Lox.had_error = True
