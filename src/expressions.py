"""Expression and statement classes used in the Lox AST."""

from typing import (
    Any,
    Optional
)
from dataclasses import dataclass
from src.token import Token
from data.annotations import LoxValue
from data.protocols import (
    ExprVisitor,
    StmtVisitor
)

class Expr:
    """Expression base class."""
    def accept(self, visitor: ExprVisitor) -> Any:
        raise NotImplementedError

class Stmt:
    """Statement base class."""
    def accept(self, visitor: StmtVisitor) -> Any:
        raise NotImplementedError

@dataclass
class Binary(Expr):
    """Representation of a binary expression."""
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_BinaryExpr(self)

@dataclass
class Grouping(Expr):
    """Representation of a grouping expression."""
    expression: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_GroupingExpr(self)

@dataclass
class Literal(Expr):
    """Representation of a literal expression."""
    value: LoxValue

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_LiteralExpr(self)

@dataclass
class Logical(Expr):
    """Representation of a logical expression."""
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_LogicalExpr(self)

@dataclass
class Unary(Expr):
    """Representation of a unary expression."""
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_UnaryExpr(self)

@dataclass
class Ternary(Expr):
    """Representation of a ternary expression."""
    condition: Expr
    true_branch: Expr
    false_branch: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_TernaryExpr(self)

@dataclass
class Variable(Expr):
    """Representation of a variable expression."""
    name: Token

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_VariableExpr(self)

@dataclass
class Assign(Expr):
    """Representation of an assignment expression."""
    name: Token
    operator: Token
    value: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_AssignExpr(self)

@dataclass
class Expression(Stmt):
    """Representation of an expression statement."""
    expression: Expr

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_ExpressionStmt(self)

@dataclass
class Break(Stmt):
    """Representation of a break statement."""
    ...

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_BreakStmt(self)

@dataclass
class If(Stmt):
    """Representation of an if statement."""
    condition: Expr
    then_branch: Stmt
    else_branch: Optional[Stmt]

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_IfStmt(self)

@dataclass
class Print(Stmt):
    """Representation of a print statement."""
    expression: Expr

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_PrintStmt(self)

@dataclass
class While(Stmt):
    """Representation of a while statement."""
    condition: Expr
    body: Stmt

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_WhileStmt(self)

@dataclass
class Var(Stmt):
    """Representation of a variable statement."""
    name: Token
    initializer: Optional[Expr]

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_VarStmt(self)

@dataclass
class Block(Stmt):
    """Representation of a block statement."""
    statements: list[Stmt]

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_BlockStmt(self)

