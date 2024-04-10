# pylint:disable=invalid-name
"""The main interpreter for the Lox language."""
from typing import TYPE_CHECKING, Any
from data.enums import Digraphs, Monographs
from data.errors import LoxRuntimeError
from data.annotations import LoxValue
from src.expressions import Binary, Literal, Grouping, Expr, Ternary, Unary
from src.token import Token

if TYPE_CHECKING:
    from src.lox import Lox


class Interpreter:
    """The main interpreter for the Lox language.
    """

    def __init__(self, lox: "Lox"):
        self.lox = lox

    def evaluate(self, expr: Expr) -> LoxValue:
        """Evaluate an expression by instructing it to call the 
        appropriate visitor method.
        """
        return expr.accept(self)

    def interpret(self, expression: Expr) -> None:
        """Interpret an expression."""
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except LoxRuntimeError as e:
            self.lox.runtime_error(e)

    def stringify(self, value: LoxValue) -> str:
        """Turn a primary value into a string representation of that value."""
        if value is None:
            return "nil"
        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(value)

    def visit_LiteralExpr(self, expr: Literal) -> LoxValue:
        """Interpret a literal."""
        return expr.value

    def visit_GroupingExpr(self, expr: Grouping) -> LoxValue:
        """Interpret a grouping."""
        return self.evaluate(expr.expression)

    def visit_UnaryExpr(self, expr: Unary) -> LoxValue:
        """Interpret a unary."""
        right: Any = self.evaluate(expr.right)
        match expr.operator.token_type:
            case Monographs.MINUS:
                self.check_number_operand(expr.operator, right)
                return -right
            case Monographs.BANG:
                return not self.is_truthy(right)
            # Unreachable
            case _:
                return None

    def visit_BinaryExpr(self, expr: Binary) -> LoxValue:
        """Interpret a binary."""
        left: Any = self.evaluate(expr.left)
        right: Any = self.evaluate(expr.right)

        match expr.operator.token_type:
            case Digraphs.BANG_EQUAL:
                return not self.is_equal(left, right)
            case Digraphs.EQUAL_EQUAL:
                return self.is_equal(left, right)
            case Monographs.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return left - right
            case Monographs.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return left / right
            case Monographs.STAR:
                self.check_number_operands(expr.operator, left, right)
                return left * right
            case Monographs.PLUS:
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                raise LoxRuntimeError(
                    expr.operator, "Operands must be two numbers or two strings.")
            case Monographs.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return left > right
            case Digraphs.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left >= right
            case Monographs.LESS:
                self.check_number_operands(expr.operator, left, right)
                return left < right
            case Digraphs.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left <= right
            case _:
                return None

    def visit_TernaryExpr(self, expr: Ternary) -> LoxValue:
        """Interpret a ternary."""
        cond = self.evaluate(expr.condition)
        if self.is_truthy(cond):
            return self.evaluate(expr.true_branch)
        return self.evaluate(expr.false_branch)

    # TODO: The comma operator will need to be implemented once we learn about
    # statements, since it can do x = (a =5, b=6, a+b), but it needs to be able
    # to store those var names somewhere... Right now, the comma is just a binary
    # in which the right hand might also be a comma: 
    # 4, 5, 6, 7 > (, 4 (, 5 (, 6 7)))
    #
    # def visit_CommaExpr(self, expr: Comma) -> LoxValue:
    #     ...

    def is_truthy(self, obj: LoxValue) -> bool:
        """
        Test whether a value should evaluate True when considered a boolean.
        """
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True

    def is_equal(self, a: LoxValue, b: LoxValue) -> bool:
        """Test whether two values are equal to each other."""
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def check_number_operand(self, operator: Token, operand: LoxValue) -> None:
        """Ensure that the value type is appropriate for a unary operator by
        raising an error if not.
        """
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number")

    def check_number_operands(self, operator: Token, left: LoxValue, right: LoxValue) -> None:
        """Ensure that the value types are appropriate for a binary operator by
        raising an error if not.
        """
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")
