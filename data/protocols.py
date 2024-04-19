"""Protocols that define functionality added to AST classes."""

from typing import (
    Protocol,
    Any,
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from src.expressions import (
        Binary,
        Grouping,
        Literal,
        Logical,
        Unary,
        Ternary,
        Variable,
        Assign,
        Expression,
        Break,
        If,
        Print,
        While,
        Var,
        Block
    )

class ExprVisitor(Protocol):
    """Protocol for behaviours added to subclasses of Expr."""

    def visit_BinaryExpr(self, expr:'Binary') -> Any: ...
    def visit_GroupingExpr(self, expr:'Grouping') -> Any: ...
    def visit_LiteralExpr(self, expr:'Literal') -> Any: ...
    def visit_LogicalExpr(self, expr:'Logical') -> Any: ...
    def visit_UnaryExpr(self, expr:'Unary') -> Any: ...
    def visit_TernaryExpr(self, expr:'Ternary') -> Any: ...
    def visit_VariableExpr(self, expr:'Variable') -> Any: ...
    def visit_AssignExpr(self, expr:'Assign') -> Any: ...


class StmtVisitor(Protocol):
    """Protocol for behaviours added to subclasses of Stmt."""

    def visit_ExpressionStmt(self, stmt:'Expression') -> Any: ...
    def visit_BreakStmt(self, stmt:'Break') -> Any: ...
    def visit_IfStmt(self, stmt:'If') -> Any: ...
    def visit_PrintStmt(self, stmt:'Print') -> Any: ...
    def visit_WhileStmt(self, stmt:'While') -> Any: ...
    def visit_VarStmt(self, stmt:'Var') -> Any: ...
    def visit_BlockStmt(self, stmt:'Block') -> Any: ...


