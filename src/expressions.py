


from dataclasses import dataclass
from typing import Optional, Any

from data.protocols import ExprVisitor
from src.token import Token


class Expr:
    """Expression base class."""
    def accept(self, visitor: ExprVisitor) -> Any:
        """Accept a visitor and perform the associated action."""
        raise NotImplementedError


@dataclass
class Binary(Expr):
    """A representation of a binary expression."""
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_BinaryExpr(self)


@dataclass
class Grouping(Expr):
    """A representation of a grouping expression."""
    expression: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_GroupingExpr(self)


@dataclass
class Literal(Expr):
    """A representation of a literal expression."""
    value: Optional[object]

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_LiteralExpr(self)


@dataclass
class Unary(Expr):
    """A representation of a unary expression."""
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_UnaryExpr(self)

@dataclass
class Ternary(Expr):
    """A representation of a ternary expression."""
    expression: Expr
    then_branch: Expr
    else_branch: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_TernaryExpr(self)

