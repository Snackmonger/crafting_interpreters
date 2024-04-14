"""Main interface class for using the Lox interpreter."""
import sys
from loguru import logger

from data.enums import Miscellania
from data.errors import LoxRuntimeError
from src.expressions import Stmt
from src.interpreter import Interpreter
from src.parser import Parser
from src.token import Token
from src.scanner import Scanner


class Lox:
    """The main interface for the Lox language interpreter.
    
    Lox is a scripting language, which means it executes directly from source.
    Our interpreter supports two ways of running code. You can run a source 
    file passed as an argument to the main function, or you can run the main
    function without any arguments to enter the interactive interpreter.
    """

    def __init__(self):
        self.had_error: bool = False
        self.had_runtime_error: bool = False
        self.interpreter: Interpreter = Interpreter(self)

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
        if self.had_runtime_error:
            sys.exit(70)
        scanner: Scanner = Scanner(source, self)
        tokens: list[Token] = scanner.scan_tokens()
        parser: Parser = Parser(tokens, self)
        statements: list[Stmt] = parser.parse()
        if self.had_error:
            logger.info("Lox encountered an error.")
            return
        self.interpreter.interpret(statements)

    def run_file(self, path: str) -> None:
        """Create a"""
        with open(path, encoding="utf8") as f:
            self.run(str(f))

    def error(self, line: int | Token, message: str) -> None:
        """Configure and report an error."""
        if isinstance(line, Token):
            if line.token_type == Miscellania.EOF:
                self.report(line.line, " at end", message)
            else:
                self.report(line.line, " at '" + line.lexeme + "'", message)
        else:
            self.report(line, "", message)

    def runtime_error(self, error: LoxRuntimeError) -> None:
        """Report a runtime error and indicate that the code failed."""
        print(error.message + "\n[line " + str(error.token.line) + "]")
        self.had_runtime_error = True

    def report(self, line: int, where: str, message: str) -> None:
        """Report an error and indicate that the code failed."""
        print("[line " + str(line) + "] Error" + where + ": " + message)
        self.had_error = True
