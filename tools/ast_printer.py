# pylint:disable=invalid-name

from src.expressions import Expr, Binary, Grouping, Literal, Unary


class ASTPrinter:
    """Creates a readable representation of an AST expression."""

    def print(self, expr: Expr, print_: bool = True) -> str:
        """Return a string representing the expression, and optionally
        print it to the console (default=True).
        """
        if print_:
            print(expr.accept(self))
        return expr.accept(self)

    def visit_BinaryExpr(self, expr: Binary) -> str:
        """Represent a binary expression as a string."""
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visit_GroupingExpr(self, expr: Grouping) -> str:
        """Represent a grouping expression as a string."""
        return self.parenthesize("group", expr.expression)

    def visit_LiteralExpr(self, expr: Literal) -> str:
        """Represent a literal expression as a string."""
        if not expr.value:
            return "nil"
        return str(expr.value)
    
    def visit_UnaryExpr(self, expr: Unary) -> str:
        """Represent a unary expression as a string."""
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def parenthesize(self, name: str, /, *exprs: Expr) -> str:
        """Parenthesize an expression with a given name and sub-expressions."""
        string = "(" + name
        for expr in exprs:
            string += " "
            string += expr.accept(self)
        string += ")"
        return string
    

class RPNPrinter:
    """Creates a readable representation of an AST expression
    in Reverse Polish Notation.

    (Chapter 2, 5: Challenge)
    """

    def print(self, expr: Expr, print_: bool = True) -> str:
        """Return a string representing the expression, and optionally
        print it to the console (default=True).
        """
        if print_:
            print(expr.accept(self))
        return expr.accept(self)

    def visit_BinaryExpr(self, expr: Binary) -> str:
        """Represent a binary expression as a string."""
        return self.polishize(expr.operator.lexeme, expr.left, expr.right)
    
    def visit_GroupingExpr(self, expr: Grouping) -> str:
        """Represent a grouping expression as a string."""
        return self.polishize("group", expr.expression)

    def visit_LiteralExpr(self, expr: Literal) -> str:
        """Represent a literal expression as a string."""
        if not expr.value:
            return "nil"
        return str(expr.value)
    
    def visit_UnaryExpr(self, expr: Unary) -> str:
        """Represent a unary expression as a string."""
        return self.polishize(expr.operator.lexeme, expr.right)
    
    def polishize(self, name: str, /, *exprs: Expr) -> str:
        """Put the expression in reverse Polish notation."""
        string = ""
        for expr in exprs:
            string += expr.accept(self)
            string += " "
        string += name
        return string