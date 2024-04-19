# pylint:disable=invalid-name,too-many-return-statements
"""The main interpreter for the Lox language.

The interpreter is responsible for taking the parsed AST expressions and 
reducing them to their primitive values, and taking parsed AST statements
and executing their instructions about state in the appropriate enviromment.
"""
from typing import TYPE_CHECKING, Any, Sequence

# from loguru import logger
from data.enums import (
    Digraphs,
    Monographs,
    ReservedWords
)
from data.errors import BreakException, LoxRuntimeError
from data.annotations import LoxValue, UninitializedVariable
from src import utils
from src.environment import Environment
from src.expressions import (
    Expr,
    Expression,
    If,
    Stmt,
    Assign,
    Binary,
    Block,
    Break,
    Grouping,
    Literal,
    Logical,
    Print,
    Unary,
    Ternary,
    Var,
    Variable,
    While
)

if TYPE_CHECKING:
    from src.lox import Lox


class Interpreter:
    """The main interpreter for the Lox language.

    The code of the interpreter closely matches the basic grammar of the 
    language::

        Grammar notation    Code representation
        ----------------    -------------------
        Terminal            Code to match and consume a token
        Nonterminal         Call to that rule's function
        |                   if or switch statement
        * or +              while or for loop
        ?                   if statement 

        Symbol              Meaning
        ------              -------
        |                   or 
        ""                  contents appear in literal form
        ()*                 contents appear 0 or many times
        ()+                 contents appear 1 or many times
        ()?                 contents appear 1 or 0 times
    """

    def __init__(self, lox: "Lox"):
        self.lox = lox
        self.environment = Environment()

    def interpret(self, statements: Sequence[Stmt | None]) -> None:
        """Interpret the given statements."""
        try:
            for statement in statements:
                if statement:
                    self.execute(statement)
        except LoxRuntimeError as e:
            self.lox.runtime_error(e)

    def evaluate(self, expr: Expr) -> LoxValue:
        """Evaluate an expression by instructing it to accept the interpreter
        as a visitor who will supply the appropriate functionality.
        """
        return expr.accept(self)

    def execute(self, stmt: Stmt) -> None:
        """Execute a statement by instructing it to accept the interpreter 
        as a visitor who will supply the appropriate functionality..
        """
        stmt.accept(self)

    def execute_block(self, statements: list[Stmt], environment: Environment) -> None:
        """Execute a block statement.
        """
        previous: Environment = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    ###############################
    # STATEMENT VISITOR INTERFACE #
    ###############################
    def visit_BlockStmt(self, stmt: Block) -> None:
        """Interpret a block statement.
        """
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_VarStmt(self, stmt: Var) -> None:
        """Interpret a variable statement"""
        value: LoxValue = UninitializedVariable()
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visit_WhileStmt(self, stmt: While) -> None:
        """Interpret a while statement."""
        try:
            while utils.is_truthy(self.evaluate(stmt.condition)):
                self.execute(stmt.body)
        except BreakException:
            pass

    def visit_BreakStmt(self, stmt: Break) -> None:
        """Interpret a break statement."""
        raise BreakException()


    def visit_AssignExpr(self, expr: Assign) -> None:
        """Interpret an assignment expression."""
        value: LoxValue = self.evaluate(expr.value)
        if expr.operator.token_type == Monographs.EQUAL:
            self.environment.assign(expr.name, value)
            
        else:
            old = self.environment.get(expr.name)
            utils.check_number_operands(expr.operator, value, old)
            assert isinstance(old, float)
            assert isinstance(value, float)
            match expr.operator.token_type:
                case Digraphs.ADD_ASSIGN:
                    value += old
                    self.environment.assign(expr.name, value)
                case Digraphs.SUB_ASSIGN:
                    value -= old
                    self.environment.assign(expr.name, value)
                case Digraphs.MUL_ASSIGN:
                    value *= old
                    self.environment.assign(expr.name, value)
                case Digraphs.DIV_ASSIGN:
                    value /= old
                    self.environment.assign(expr.name, value)
                case _:
                    raise LoxRuntimeError(expr.operator, "Unknown operator.")

    def visit_ExpressionStmt(self, stmt: Expression) -> None:
        """Interpret an expression statement"""
        self.evaluate(stmt.expression)

    def visit_IfStmt(self, stmt: If) -> None:
        """Interpret a conditional statement.
        
        """
        if utils.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch:
            self.execute(stmt.else_branch)


    def visit_PrintStmt(self, stmt: Print) -> None:
        """Interpret a print statement"""
        value: LoxValue = self.evaluate(stmt.expression)
        print(utils.stringify(value))

    ################################
    # EXPRESSION VISITOR INTERFACE #
    ################################
    def visit_TernaryExpr(self, expr: Ternary) -> LoxValue:
        """Interpret a ternary"""
        cond = self.evaluate(expr.condition)
        if utils.is_truthy(cond):
            return self.evaluate(expr.true_branch)
        return self.evaluate(expr.false_branch)

    def visit_BinaryExpr(self, expr: Binary) -> LoxValue:
        """Interpret a binary.

        ``binary → equality``
        ``equality → comparison ( ( "!=" | "==" ) comparison )*``
        ``comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )*``
        ``term → factor ( ( "-" | "+" ) factor )*``
        ``factor → unary ( ( "/" | "*" ) unary )*``
        """
        left: Any = self.evaluate(expr.left)
        right: Any = self.evaluate(expr.right)

        match expr.operator.token_type:
            # Equality
            case Digraphs.BANG_EQUAL:
                return not utils.is_equal(left, right)
            case Digraphs.EQUAL_EQUAL:
                return utils.is_equal(left, right)
            # Comparison
            case Monographs.GREATER:
                utils.check_number_operands(expr.operator, left, right)
                return left > right
            case Digraphs.GREATER_EQUAL:
                utils.check_number_operands(expr.operator, left, right)
                return left >= right
            case Monographs.LESS:
                utils.check_number_operands(expr.operator, left, right)
                return left < right
            case Digraphs.LESS_EQUAL:
                utils.check_number_operands(expr.operator, left, right)
                return left <= right
            # Concatenative
            case Digraphs.CONCATENATE:
                return utils.stringify(left) + utils.stringify(right)
            # Additive
            case Monographs.MINUS:
                utils.check_number_operands(expr.operator, left, right)
                return left - right
            case Monographs.PLUS:
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                raise LoxRuntimeError(
                    expr.operator, "Operands must be two numbers or two strings.")
            # Multiplicative
            case Monographs.SLASH:
                utils.check_number_operands(expr.operator, left, right)
                return left / right
            case Monographs.STAR:
                utils.check_number_operands(expr.operator, left, right)
                return left * right
            case _:
                return None

    def visit_UnaryExpr(self, expr: Unary) -> LoxValue:
        """Interpret a unary.

        ``unary → ( "!" | "-" ) unary | primary``
        """
        right: Any = self.evaluate(expr.right)
        match expr.operator.token_type:
            case Monographs.MINUS:
                utils.check_number_operand(expr.operator, right)
                return -right
            case Monographs.BANG:
                return not utils.is_truthy(right)
            # Unreachable
            case _:
                return

    def visit_VariableExpr(self, expr: Variable) -> LoxValue:
        """Interpret a variable expression.

        ``IDENTIFIER → primary``
        """
        value = self.environment.get(expr.name)
        if isinstance(value, UninitializedVariable):
            raise LoxRuntimeError(expr.name, f"Variable '{
                                  expr.name.lexeme}' must be initialized before use.")
        return self.environment.get(expr.name)

    def visit_LiteralExpr(self, expr: Literal) -> LoxValue:
        """Interpret a literal expression::

        ``NUMBER | STRING | "true" | "false" | "nil"``
        """
        return expr.value
    
    def visit_LogicalExpr(self, expr: Logical) -> LoxValue:
        """Interpret a logical expression.
        
        
        `` ``
        """
        left: LoxValue = self.evaluate(expr.left)
        if expr.operator.token_type == ReservedWords.OR:
            if utils.is_truthy(left):
                return left
        if not utils.is_truthy(left):
            return left
        return self.evaluate(expr.right)

    def visit_GroupingExpr(self, expr: Grouping) -> LoxValue:
        """Interpret a grouping expression.

        ``"(" expression ")"``
        """
        return self.evaluate(expr.expression)
