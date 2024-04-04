
from typing import Optional, TYPE_CHECKING
from data.enums import (
    Digraphs,
    Literals,
    Miscellania,
    Monographs,
    ReservedWords,
    TokenType
)
from src.token import Token
from src.utils import (
    is_digit,
    is_alnum,
    is_alpha
)
if TYPE_CHECKING:
    from src.lox import Lox


class Scanner():
    """The scanner is responsible for reading the source text and sorting its
    characters into meaningful lexical categories (tokens).
    """

    def __init__(self, source: str, lox: "Lox") -> None:
        self.source: str = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        self.lox: "Lox" = lox

    def scan_tokens(self) -> list[Token]:
        """Analyse the source text into recognized tokens."""
        while not self.is_at_end:
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(Miscellania.EOF, "", "", self.line))
        return self.tokens

    @property
    def is_at_end(self) -> bool:
        """Flag that indicates whether the scanner has reached the 
        end of the source."""
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        """Analyze the character at the current index to see whether it can
        form a valid token.
        """
        char: str = self.advance()
        match char:
            case '(': self.add_token(Monographs.LEFT_PAREN)
            case ')': self.add_token(Monographs.RIGHT_PAREN)
            case '{': self.add_token(Monographs.LEFT_BRACE)
            case '}': self.add_token(Monographs.RIGHT_BRACE)
            case ',': self.add_token(Monographs.COMMA)
            case '.': self.add_token(Monographs.DOT)
            case '-': self.add_token(Monographs.MINUS)
            case '+': self.add_token(Monographs.PLUS)
            case ';': self.add_token(Monographs.SEMICOLON)
            case '*': self.add_token(Monographs.STAR)
            case "!": self.add_token(Digraphs.BANG_EQUAL if self.match("=") else Monographs.BANG)
            case "=": self.add_token(Digraphs.EQUAL_EQUAL if self.match("=") else Monographs.EQUAL)
            case "<": self.add_token(Digraphs.LESS_EQUAL if self.match("=") else Monographs.LESS)
            case ">": self.add_token(Digraphs.GREATER_EQUAL if self.match("=") else Monographs.GREATER)
            case "/":
                if self.match("/"):
                    while self.peek != "\n" and not self.is_at_end:
                        self.advance()
                if self.match("*"):
                    self.multiline_comment()
                else:
                    self.add_token(Monographs.SLASH)
            case ' ': pass
            case '\r': pass
            case '\t': pass
            case '\n': self.line += 1

            case '"':
                self.string()

            case _:
                if is_digit(char):
                    self.number()

                elif is_alpha(char):
                    self.identifier()

                else:
                    self.lox.error(self.line, "Unexpected character.")

    def advance(self) -> str:
        """Advance the scanner and return the new current character."""
        char = self.peek
        self.current += 1
        return char

    def add_token(self, token_type: TokenType, literal: Optional[object] = None) -> None:
        """Create a new token with the given type label and an optional 
        literal value. 
        """
        text: str = self.source[self.start: self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        """Check whether the next character is the expected character, and
        consume it if so.
        """
        if self.is_at_end:
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    @property
    def peek(self) -> str:
        """Return the current character without consuming it."""
        if self.is_at_end:
            return "\0"
        return self.source[self.current]

    @property
    def peek_next(self) -> str:
        """Return the next character without consuming it."""
        if self.current + 1 > len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    def multiline_comment(self) -> None:
        """
        Parse a multi-line comment, including nested comments.

        Ch. 2.4 challenge
        -----------------
        Add support to Lox's scanner for C-style /* ... */
        block comments. Make sure to handle newlines in them.
        Consider allowing them to nest. Is adding support for
        nesting more work than you expected? Why?

        Answer
        ------
        A multi-line comment that cannot nest will either
        have an ending */ or will be unterminated at EOF. A comment
        that can nest cannot be tested for the ending sequence without
        also knowing how deep within the nest the sequence sits. This fact
        also entails that the grammar that describes it is no longer regular.
        """
        nest_level: int = 1
        while nest_level > 0:
            if self.is_at_end:
                self.lox.error(
                    self.line, "Unterminated block comment.")
                return
            if self.peek == "\n":
                self.line += 1
            if self.peek == "/" and self.peek_next == "*":
                self.advance()
                self.advance()
                nest_level += 1
                continue
            if self.peek == "*" and self.peek_next == "/":
                self.advance()
                self.advance()
                nest_level -= 1
                continue
            self.advance()

    def number(self) -> None:
        """Parse a sequence of characters as a number literal."""
        while is_digit(self.peek):
            self.advance()
        if self.peek == '.' and is_digit(self.peek_next):
            self.advance()
            while is_digit(self.peek):
                self.advance()
        self.add_token(Literals.NUMBER, float(
            self.source[self.start: self.current]))

    def string(self) -> None:
        """Parse a sequence of characters as a string literal."""
        while self.peek != '"' and not self.is_at_end:
            if self.peek == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end:
            self.lox.error(self.line, "Unterminated string.")
            return
        # The closing '"'
        self.advance()
        # Trim the surrounding quotes.
        value = self.source[self.start+1: self.current-1]
        self.add_token(Literals.STRING, value)

    def identifier(self) -> None:
        """Parse a sequence of characters as an identifier."""
        while is_alnum(self.peek):
            self.advance()
        text: str = self.source[self.start: self.current]
        token_type = Literals.IDENTIFIER if text not in ReservedWords else ReservedWords(
            text)
        self.add_token(token_type)
