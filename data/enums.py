from enum import StrEnum

class TokenType(StrEnum):
    """Parent class of token type enums."""

    @classmethod
    def as_dict(cls) -> dict[str, str]:
        """Return a dictionary of the enum values."""
        return {key: str(value) for key, value in cls.__members__.items()}


class Monographs(TokenType):
    """Single-character tokens."""
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"
    BANG = "!"
    CARAT = "^"
    MODULO = "%"
    COLON = ":"
    EQUAL = '='
    LESS = '<'
    GREATER = '>'

class Digraphs(TokenType):
    """Double-character tokens."""
    BANG_EQUAL = '!='
    EQUAL_EQUAL = '=='
    GREATER_EQUAL = '>='
    LESS_EQUAL = '<='

class Literals(TokenType):
    """Literal value tokens."""
    SINGLE_QUOTE = "'"
    DOUBLE_QUOTE = '"'
    IDENTIFIER = 'identifier'
    STRING = 'string'
    NUMBER = 'number'

class ReservedWords(TokenType):
    """Reserved keyword tokens."""
    AND = 'and'
    CLASS = 'class'
    ELSE = 'else'
    FALSE = 'false'
    FUN = 'fun'
    FOR = 'for'
    IF = 'if'
    NIL = 'nil'
    OR = 'or'
    PRINT = 'print'
    RETURN = 'return'
    SUPER = 'super'
    THIS = 'this'
    TRUE = 'true'
    VAR = 'var'
    WHILE = 'while'

class Miscellania(TokenType):
    EOF = 'eof'

