"""Miscellaneous utility functions used in the program."""

from data.constants import DIGITS, ALPHA_LOWER, ALPHA_UPPER
from data.annotations import LoxValue
from data.errors import LoxRuntimeError
from src.token import Token


def is_digit(char: str) -> bool:
    """Test if a given character is an Indian-Arabic numeral."""
    return char in DIGITS


def is_alpha(char: str) -> bool:
    """Test if a given character is an alphabetic symbol."""
    return char in ALPHA_UPPER + ALPHA_LOWER


def is_alnum(char: str) -> bool:
    """Test if a given character is alphabetic or numeric."""
    return is_alpha(char) or is_digit(char) or char == "_"


def is_truthy(obj: LoxValue) -> bool:
    """
    Evaluate a value as a boolean.
    """
    if obj is None:
        return False
    if isinstance(obj, bool):
        return bool(obj)
    return True


def is_equal(a: LoxValue, b: LoxValue) -> bool:
    """Test whether two values are equal to each other."""
    if a is None and b is None:
        return True
    if a is None:
        return False
    return a == b


def check_number_operand(operator: Token, operand: LoxValue) -> None:
    """Ensure that the value type is appropriate for a unary operator by
    raising an error if not.
    """
    if isinstance(operand, float):
        return
    raise LoxRuntimeError(operator, "Operand must be a number")


def check_number_operands(operator: Token, left: LoxValue, right: LoxValue) -> None:
    """Ensure that the value types are appropriate for a binary operator by
    raising an error if not.
    """
    if isinstance(left, float) and isinstance(right, float):
        return
    raise LoxRuntimeError(operator, "Operands must be numbers.")


def stringify(value: LoxValue) -> str:
    """Turn a primary value into a string representation of that value."""
    if value is None:
        return "nil"
    if isinstance(value, float):
        text = str(value)
        if text.endswith(".0"):
            text = text[:-2]
        return text
    return str(value)
