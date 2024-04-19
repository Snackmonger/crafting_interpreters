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
        self.loop_depth: int = 0

    def parse(self) -> list[Stmt]:
        """Main parsing method."""
        statements: list[Stmt] = []
        while not self.is_at_end:
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
        return statements

    def consume(self, token_type: TokenType, message: str) -> Token:
        """Verify that the next token is of the expected type and consume it
        if so, or raise an error.
        """
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek, message)

    def synchronize(self) -> None:
        """Attempt to return the parser to a valid position by seeking a 
        recognized syntactic break.
        """
        self.advance()
        while not self.is_at_end:
            if self.previous.token_type == Monographs.SEMICOLON:
                return
            if self.peek.token_type in [
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
        return self.peek.token_type == token_type

    def advance(self) -> Token:
        """Move the cursor forward in the list of tokens and return the
        previous token.
        """
        if not self.is_at_end:
            self.current += 1
        return self.previous

    @property
    def is_at_end(self) -> bool:
        """Flag that says whether the cursor is at the end of the list of 
        tokens.
        """
        return self.peek.token_type == Miscellania.EOF

    @property
    def peek(self) -> Token:
        """Examine the current token without changing the cursor's position."""
        return self.tokens[self.current]

    @property
    def previous(self) -> Token:
        """Return the previous token without changing the cursor's position."""
        return self.tokens[self.current - 1]

    ################
    # DECLARATIONS #
    ################
    def declaration(self) -> Optional[Stmt]:
        """Parse a declaration."""
        try:
            # The type declaration keyword does not enforce a type;
            # it's just an annotation.
            if self.match(ReservedWords.VAR,
                          ReservedWords.INT,
                          ReservedWords.FLOAT,
                          ReservedWords.BOOL,
                          ReservedWords.STR,
                          ReservedWords.CHAR):
                return self.var_declaration()
            return self.statement()

        except ParseError:
            self.synchronize()

    def var_declaration(self) -> Stmt:
        """Parse a variable declatation."""
        name: Token = self.consume(
            Literals.IDENTIFIER, "Expect variable name.")
        initializer: Optional[Expr] = None
        if self.match(Monographs.EQUAL):
            initializer = self.expression()
        self.consume(Monographs.SEMICOLON,
                     "Expect ';' after variable declaration.")
        return Var(name, initializer)

    ##############
    # STATEMENTS #
    ##############
    def statement(self) -> Stmt:
        """Parse a statement."""
        if self.match(ReservedWords.PRINT):
            return self.print_statement()
        if self.match(Monographs.LEFT_BRACE):
            return Block(self.block())
        if self.match(ReservedWords.FOR):
            return self.for_statement()
        if self.match(ReservedWords.IF):
            return self.if_statement()
        if self.match(ReservedWords.WHILE):
            return self.while_statement()
        if self.match(ReservedWords.BREAK):
            return self.break_statement()
        if self.match(ReservedWords.LOOP):
            return self.loop_statement()
        return self.expression_statement()

    def while_statement(self) -> Stmt:
        """Parse a while statement."""
        self.consume(Monographs.LEFT_PAREN, "Expect '(' after 'while'.")
        condition: Expr = self.expression()
        self.consume(Monographs.RIGHT_PAREN, "Expect ')' after condition.")
        try:
            self.loop_depth += 1
            body: Stmt = self.statement()
            return While(condition, body)

        finally:
            self.loop_depth -= 1

    def loop_statement(self) -> Stmt:
        """Parse a loop statement.

        ``loopStmt → "loop" statement ("until" "(" expression ")" )?``

        Like the for statement, the loop statement is just syntactic sugar 
        for a while statement::

            var x = 0
            loop {
                x = x + 1
            } until (x >= 10)

        Is parsed as::

            var x = 0
            x = x + 1
            while (!(x >= 10)) {
                x = x + 1
            }

        A loop without an until expression is parsed as ``while (true) {...}``
        """
        try:
            self.loop_depth += 1
            body: Stmt = self.statement()
            condition: Expr = Literal(True)
            if self.match(ReservedWords.UNTIL):
                self.consume(Monographs.LEFT_PAREN,
                             "Expect '(' after 'until'.")
                condition = Unary(Token(Monographs.BANG, "!",
                                  None, 0), self.expression())
                self.consume(Monographs.RIGHT_PAREN,
                             "Expect ')' after condition.")
            body = Block([body, While(condition, body)])
            return body
        finally:
            self.loop_depth -= 1

    def break_statement(self) -> Stmt:
        """Parse a break statement."""
        if self.loop_depth == 0:
            self.error(self.previous,
                       "Must be inside a loop to use 'break'.")
        self.consume(Monographs.SEMICOLON, "Expect ';' after 'break'.")
        return Break()

    def for_statement(self) -> Stmt:
        """
        Parse a for statement.

        A for statement is a composite statement that performs the
        function of a while loop. An initializer statement is a variable
        declaration or expression or nothing that happens once when the 
        loop starts. An increment expression takes the variable and 
        increments it, or does nothing. The condition determines whether
        the loop continues, and is True if left blank.

        ::

            for (i=0 ; i<10 ; i=i+1){
                do thing
            }
            // Is equivalent to:

            var i = 0  // initiializer
            while (i < 10){ // condition
                do thing  // body
                i = i + 1 // increment
            }
        `` ``
        """
        self.consume(Monographs.LEFT_PAREN, "Expect ')' after 'for'.")

        initializer: Optional[Stmt]
        if self.match(Monographs.SEMICOLON):
            initializer = None
        elif self.match(ReservedWords.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()
        condition: Optional[Expr] = None
        if not self.check(Monographs.SEMICOLON):
            condition = self.expression()
        self.consume(Monographs.SEMICOLON, "Expect ';' after loop condition.")

        increment: Optional[Expr] = None
        if not self.check(Monographs.RIGHT_PAREN):
            increment = self.expression()
        self.consume(Monographs.RIGHT_PAREN, "Expect ')' after for clauses.")

        try:
            self.loop_depth += 1
            body: Stmt = self.statement()
            if increment:
                body = Block([body, Expression(increment)])

            if not condition:
                condition = Literal(True)
            body = While(condition, body)

            if initializer:
                body = Block([initializer, body])

            return body
        finally:
            self.loop_depth -= 1

    def if_statement(self) -> Stmt:
        """Parse an if statement."""
        self.consume(Monographs.LEFT_PAREN, "Expect '(' after 'if'.")
        condition: Expr = self.expression()
        self.consume(Monographs.RIGHT_PAREN, "Expect '(' after if condition.")

        then_branch: Stmt = self.statement()
        else_branch: Optional[Stmt] = None
        if self.match(ReservedWords.ELSE):
            else_branch = self.statement()
        return If(condition, then_branch, else_branch)

    def print_statement(self) -> Stmt:
        """Parse a print statement."""
        value: Expr = self.expression()
        self.consume(Monographs.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self) -> Stmt:
        """Parse an expression statement."""
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

    ###############
    # EXPRESSIONS #
    ###############
    def expression(self) -> Expr:
        """Parse an expression."""
        return self.assignment()

    def assignment(self) -> Expr:
        """Parse an assignment statement."""
        expr: Expr = self.ternary()
        if self.match(Monographs.EQUAL,
                      Digraphs.ADD_ASSIGN,
                      Digraphs.MUL_ASSIGN,
                      Digraphs.SUB_ASSIGN,
                      Digraphs.DIV_ASSIGN):
            operator: Token = self.previous
            value: Expr = self.assignment()
            if isinstance(expr, Variable):
                name: Token = expr.name
                return Assign(name, operator, value)
            self.error(operator, "Invalid assignment target.")
        return expr

    def ternary(self) -> Expr:
        """Parse a ternary expression.`
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
        """Parse a binary expression."""
        return self.logic_or()

    def logic_or(self) -> Expr:
        """Parse a logical or expression."""
        expr: Expr = self.logic_and()
        while self.match(ReservedWords.OR):
            operator: Token = self.previous
            right: Expr = self.logic_and()
            expr = Logical(expr, operator, right)
        return expr

    def logic_and(self) -> Expr:
        """Parse a logical and expression."""
        expr: Expr = self.equality()
        while self.match(ReservedWords.AND):
            operator: Token = self.previous
            right: Expr = self.ternary()
            expr = Logical(expr, operator, right)
        return expr

    def equality(self) -> Expr:
        """Parse an equality expression.

        ``equality → comparison ( ( "!=" | "==" ) comparison )* ``
        """
        expr = self.comparison()
        while self.match(Digraphs.BANG_EQUAL, Digraphs.EQUAL_EQUAL):
            operator: Token = self.previous
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        """Parse a comparison expression.

        ``comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )*``

        When we're done the book, change this to:
        ``comparison → additive ( ( ">" | ">=" | "<" | "<=" ) additive )*``
        """
        expr: Expr = self.concatenation()
        while self.match(Monographs.GREATER,
                         Digraphs.GREATER_EQUAL,
                         Monographs.LESS,
                         Digraphs.LESS_EQUAL):
            operator = self.previous
            right = self.concatenation()
            expr = Binary(expr, operator, right)
        return expr

    def concatenation(self) -> Expr:
        """Parse a concatenation expression.

        """
        expr: Expr = self.term()
        while self.match(Digraphs.CONCATENATE):
            operator = self.previous
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
            operator = self.previous
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
            operator = self.previous
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        """Parse a unary expression."""
        if self.match(Monographs.BANG, Monographs.MINUS):
            operator = self.previous
            operand = self.unary()
            return Unary(operator, operand)

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
            return Literal(self.previous.literal)
        if self.match(Literals.IDENTIFIER):
            return Variable(self.previous)
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
            self.error(self.previous, "Missing left-hand operand.")
            self.equality()

        if self.match(Monographs.GREATER,
                      Monographs.LESS,
                      Digraphs.GREATER_EQUAL,
                      Digraphs.LESS_EQUAL):
            self.error(self.previous, "Missing left-hand operand.")
            self.comparison()

        if self.match(Monographs.PLUS):
            self.error(self.previous, "Missing left-hand operand.")
            self.term()

        if self.match(Monographs.SLASH, Monographs.STAR):
            self.error(self.previous, "Missing left-hand operand.")
            self.factor()

        raise self.error(self.peek, "Expect expression")
