import sys
from loguru import logger

from typing import Optional
from data.enums import Miscellania
from src.expressions import Expr
from src.parser import Parser
from src.token import Token
from src.scanner import Scanner
from tools.ast_printer import ASTPrinter


class Lox:
    """The main interpreter for the Lox language.
    
    Lox is a scripting language, which means it executes directly from source.
    Our interpreter supports two ways of running code. You can run a source 
    file passed as an argument to the main function, or you can run the main
    function without any arguments to enter the interactive interpreter.
    """
    had_error: bool = False

    @staticmethod
    def main(*args: str) -> None:
        if len(args) > 1:
            print("Usage: plox [script]")
            sys.exit(64)
        elif len(args) == 1:
            Lox.run_file(args[0])
        else:
            Lox.run_prompt()

    @staticmethod
    def run_prompt() -> None:
        """Run the interactive REPL (read, evaluate, print, loop)."""
        while True:
            line = input("> ")
            if line == "quit()":
                break
            Lox.run(line)
            Lox.had_error = False

    @staticmethod
    def run(source: str) -> None:
        """Run the source file as a script."""
        if Lox.had_error:
            sys.exit(65)
        scanner: Scanner = Scanner(source, Lox)
        tokens: list[Token] = scanner.scan_tokens()
        parser: Parser = Parser(tokens, Lox)
        expression: Optional[Expr] = parser.parse()
        if Lox.had_error:
            logger.info(f"Lox interpreter encountered an error.")
            return
        print(ASTPrinter.print(expression))

    @staticmethod
    def run_file(path: str) -> None:
        """Create a"""
        with open(path, encoding="utf8") as f:
            Lox.run(str(f))

    @staticmethod
    def error(line: int | Token, message: str) -> None:
        """Configure and report an error."""
        if isinstance(line, Token):
            if line.token_type == Miscellania.EOF:
                Lox.report(line.line, " at end", message)
            else:
                Lox.report(line.line, " at '" + line.lexeme + "'", message)
        else:
            Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        """Report an error and indicate to the interpreter that the code failed."""
        print("[line " + str(line) + "] Error" + where + ": " + message)
        Lox.had_error = True
