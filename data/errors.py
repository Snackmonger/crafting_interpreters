"""Errors used in the program."""
from typing import Optional
from src.token import Token


class LoxException(Exception):
    """Base exception for the Lox program."""
    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message if isinstance(message, str) else "Exception occurred."


class ParseError(LoxException):
    """Error that indicates that the parser encountered a problem when reading
    the token stream.
    """

class LoxRuntimeError(LoxException):
    """Error that indicates that the interpreter encountered a problem when
    attempting to execute a stream of statements.
    """
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token=token
        