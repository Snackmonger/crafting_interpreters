"""
Abstract protocols used in the program.
"""
from typing import TYPE_CHECKING, Any, Protocol
if TYPE_CHECKING:
    from src.expressions import (
        Binary,
        Grouping,
        Literal,
        Unary,
        Ternary
    )


class ExprVisitor(Protocol):
    """Protocol for a visitor that provides behaviour to a
    subclass of Expr.
    """
    def visit_BinaryExpr(self, expr: "Binary") -> Any: ...
    def visit_GroupingExpr(self, expr: "Grouping") -> Any: ...
    def visit_LiteralExpr(self, expr: "Literal") -> Any: ...
    def visit_UnaryExpr(self, expr: "Unary") -> Any: ...
    def visit_TernaryExpr(self, expr: "Ternary") -> Any: ...
