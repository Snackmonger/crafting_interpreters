# pylint:disable=invalid-name

from src.expressions import Expr, Binary, Grouping, Literal, Ternary, Unary


class ASTPrinter:
    """Creates a readable representation of an AST expression."""

    @staticmethod
    def print(expr: Expr | None, print_: bool = True) -> str:
        """Return a string representing the expression, and optionally
        print it to the console (default=True).
        """
        if expr is None:
            return "ASTPrinter error: EMPTY EXPRESSION."
        if print_:
            print(expr.accept(ASTPrinter))
        return expr.accept(ASTPrinter)
    
    @staticmethod
    def visit_BinaryExpr(expr: Binary) -> str:
        """Represent a binary expression as a string."""
        return ASTPrinter.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    @staticmethod
    def visit_GroupingExpr(expr: Grouping) -> str:
        """Represent a grouping expression as a string."""
        return ASTPrinter.parenthesize("group", expr.expression)

    @staticmethod
    def visit_LiteralExpr(expr: Literal) -> str:
        """Represent a literal expression as a string."""
        if not expr.value:
            return "nil"
        return str(expr.value)
    
    @staticmethod
    def visit_UnaryExpr(expr: Unary) -> str:
        """Represent a unary expression as a string."""
        return ASTPrinter.parenthesize(expr.operator.lexeme, expr.right)
    
    @ staticmethod
    def visit_TernaryExpr(expr: Ternary) -> str:
        """Represent a ternary expression in a string."""
        return ASTPrinter.parenthesize("?:", expr.expression, expr.then_branch, expr.else_branch)

    @staticmethod
    def parenthesize(name: str, /, *exprs: Expr) -> str:
        """Parenthesize an expression with a given name and sub-expressions."""
        string = "(" + name
        for expr in exprs:
            string += " "
            string += expr.accept(ASTPrinter)
        string += ")"
        return string