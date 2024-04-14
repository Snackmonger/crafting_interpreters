# pylint:disable=too-many-public-methods
"""The main parser class.

The parser is responsible for taking a stream of tokens and organizing it 
into meaningful semantic units. It does this by following a control tree 
that mimics the structure of the grammar's syntax tree, in which all syntactic
rules are checked in order of reverse priority, and then generating AST nodes
that represent the productions of each rule. The AST nodes may contain 
references to other nodes as part of their structure, allowing semantic 
structures to be nested within one another within the limits of the syntax.
"""
from typing import TYPE_CHECKING, Optional, Sequence

from data.enums import (
    Digraphs,
    Literals,
    Miscellania,
    Monographs,
    ReservedWords,
    TokenType
)
from data.errors import ParseError
from src.token import Token
from src.expressions import (
    Expr,
    Expression,
    Stmt,
    Assign,
    Binary,
    Block,
    Grouping,
    Literal,
    Print,
    Unary,
    Ternary,
    Var,
    Variable
)
if TYPE_CHECKING:
    from src.lox import Lox


class Parser:
    """
    Each method for parsing a grammar rule produces a syntax tree 
    for that rule and returns it to the caller. When the body of 
    the rule contains a nonterminal (a reference to another rule) 
    we call that other rule's method.
    """

    def __init__(self, tokens: Sequence[Token], lox: "Lox") -> None:
        self.tokens: list[Token] = list(tokens)
        self.current: int = 0
        self.lox = lox

    def parse(self) -> list[Stmt]:
        """Main parsing method."""
        statements: list[Stmt] = []
        while not self.is_at_end:
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
        return statements

    def declaration(self) -> Optional[Stmt]:
        """Parse a declaration."""
        try:
            if self.match(ReservedWords.VAR):
                return self.var_declaration()
            return self.statement()

        except ParseError:
            self.synchronize()

    def var_declaration(self) -> Stmt:
        """Parse a variable declatation.

        ``declaration → varDecl | statement``
        """
        name: Token = self.consume(
            Literals.IDENTIFIER, "Expect variable name.")
        initializer: Optional[Expr] = None
        if self.match(Monographs.EQUAL):
            initializer = self.expression()
        self.consume(Monographs.SEMICOLON,
                     "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def statement(self) -> Stmt:
        """Parse a statement.

        ``statement → exprStmt | printStmt``
        """
        if self.match(ReservedWords.PRINT):
            return self.print_statement()
        if self.match(Monographs.LEFT_BRACE):
            return Block(self.block())
        return self.expression_statement()

    def print_statement(self) -> Stmt:
        """Parse a print statement.

        ``printStmt → "print" expression ";"``
        """
        value: Expr = self.expression()
        self.consume(Monographs.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self) -> Stmt:
        """Parse an expression statement.

        ``exprStmt → expression ";"``
        """
        expr: Expr = self.expression()
        self.consume(Monographs.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)

    def block(self) -> list[Stmt]:
        """Parse a block statement."""
        statements: list[Stmt] = []
        while not self.check(Monographs.RIGHT_BRACE) and not self.is_at_end:
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
        self.consume(Monographs.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def assignment(self) -> Expr:
        """Parse an assignment statement.

        ``assignment → IDENTIFIER "=" assignment | ternary``
        """
        expr: Expr = self.ternary()
        if self.match(Monographs.EQUAL):
            equals: Token = self.previous()
            value: Expr = self.assignment()
            if isinstance(expr, Variable):
                name: Token = expr.name
                return Assign(name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

    def expression(self) -> Expr:
        """Parse an expression.

        ``expression → ternary``
        """
        return self.assignment()

    def ternary(self) -> Expr:
        """Parse a ternary expression.

        ``ternary → binary ("?" expression ":" ternary)?``
        """
        # NOTE: Added as part of challenge 2.6.1
        condition = self.binary()
        if self.match(Monographs.QUESTION):
            true_branch = self.expression()
            self.consume(Monographs.COLON,
                         "Expect ':' after branch of ternary expression")
            false_branch = self.ternary()
            condition = Ternary(condition, true_branch, false_branch)
        return condition

    def binary(self) -> Expr:
        """Parse a binary expression.

        ``binary → equality``
        """
        return self.equality()

    def equality(self) -> Expr:
        """Parse an equality expression.

        ``equality → comparison ( ( "!=" | "==" ) comparison )* ``
        """
        expr = self.comparison()
        while self.match(Digraphs.BANG_EQUAL, Digraphs.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        """Parse a comparison expression.

        ``comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )*``

        When we're done the book, change this to:
        ``comparison → additive ( ( ">" | ">=" | "<" | "<=" ) additive )*``
        """
        expr: Expr = self.term()
        while self.match(Monographs.GREATER,
                         Digraphs.GREATER_EQUAL,
                         Monographs.LESS,
                         Digraphs.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        """Parse a term (ADDITIVE) expression.

        ``term → factor ( ( "-" | "+" ) factor )*``

        When we're done the book, change this to:
        ``additive → multiplicative ( ( "-" | "+" ) multiplicative )*``
        """
        expr: Expr = self.factor()
        while self.match(Monographs.MINUS, Monographs.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        """Parse a factor (MULTIPLICATIVE) expression.

        ``factor → unary ( ( "/" | "*" ) unary )*``

        When we're done the book, change this to:
        ``multiplicative → unary ( ( "/" | "*" ) unary )*``
        """
        expr: Expr = self.unary()
        while self.match(Monographs.SLASH, Monographs.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        """Parse a unary expression.

        ``unary → ( "!" | "-" ) unary | primary``
        """
        if self.match(Monographs.BANG, Monographs.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self) -> Expr:
        """Parse a primary expression.

        ``primary → NUMBER 
        | STRING 
        | "true" 
        | "false" 
        | "nil" 
        | "(" expression ")" 
        | IDENTIFIER
        | error``
        """
        if self.match(ReservedWords.FALSE):
            return Literal(False)
        if self.match(ReservedWords.TRUE):
            return Literal(True)
        if self.match(ReservedWords.NIL):
            return Literal(None)
        if self.match(Literals.NUMBER, Literals.STRING):
            return Literal(self.previous().literal)
        if self.match(Literals.IDENTIFIER):
            return Variable(self.previous())
        if self.match(Monographs.LEFT_PAREN):
            expr: Expr = self.expression()
            self.consume(Monographs.RIGHT_PAREN,
                         "Expect ')' after expression.")
            return Grouping(expr)
        return self.error_productions()

    def error_productions(self) -> Expr:
        """Parse an error production.

        ``error → ("==" | "!=") equality 
        | (">=" | "<=" | "<" | ">") comparison 
        | ("+") term 
        | ("*" | "/") factor``
        """
        if self.match(Digraphs.BANG_EQUAL, Digraphs.EQUAL_EQUAL):
            self.error(self.previous(), "Missing left-hand operand.")
            self.equality()

        if self.match(Monographs.GREATER,
                      Monographs.LESS,
                      Digraphs.GREATER_EQUAL,
                      Digraphs.LESS_EQUAL):
            self.error(self.previous(), "Missing left-hand operand.")
            self.comparison()

        if self.match(Monographs.PLUS):
            self.error(self.previous(), "Missing left-hand operand.")
            self.term()

        if self.match(Monographs.SLASH, Monographs.STAR):
            self.error(self.previous(), "Missing left-hand operand.")
            self.factor()

        raise self.error(self.peek(), "Expect expression")

    def consume(self, token_type: TokenType, message: str) -> Token:
        """Verify that the next token is of the expected type and consume it
        if so, or raise an error.
        """
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek(), message)

    def synchronize(self) -> None:
        """Attempt to return the parser to a valid position by seeking a 
        recognized syntactic break.
        """
        self.advance()
        while not self.is_at_end:
            if self.previous().token_type == Monographs.SEMICOLON:
                return
            if self.peek().token_type in [
                ReservedWords.CLASS,
                ReservedWords.FUN,
                ReservedWords.VAR,
                ReservedWords.FOR,
                ReservedWords.IF,
                ReservedWords.WHILE,
                ReservedWords.PRINT,
                ReservedWords.RETURN
            ]:
                return

            self.advance()

    def error(self, token: Token, message: str) -> ParseError:
        """Register an error with the Lox interpreter, and return
        a parsing error.
        """
        self.lox.error(token, message)
        return ParseError()

    def match(self, *types: TokenType) -> bool:
        """Test whether the next token is of the expected type and advance
        if so.
        """
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType) -> bool:
        """Check whether the next token is of the expected type."""
        if self.is_at_end:
            return False
        return self.peek().token_type == token_type

    def advance(self) -> Token:
        """Move the cursor forward in the list of tokens and return the
        previous token.
        """
        if not self.is_at_end:
            self.current += 1
        return self.previous()

    @property
    def is_at_end(self) -> bool:
        """Flag that says whether the cursor is at the end of the list of 
        tokens.
        """
        return self.peek().token_type == Miscellania.EOF

    def peek(self) -> Token:
        """Examine the current token without changing the cursor's position."""
        return self.tokens[self.current]

    def previous(self) -> Token:
        """Return the previous token without changing the cursor's position."""
        return self.tokens[self.current - 1]
