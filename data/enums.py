"""Enums used in the program."""
from enum import StrEnum

class TokenType(StrEnum):
    """Parent class of token type enums."""

class Groupings(TokenType):
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"

class Operators(TokenType):
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"
    BANG = "!"
    PIPE = "|"
    CARAT = "^"
    MODULO = "%"
    AMPERSAND = "&"
    COLON = ":"
    QUESTION = "?"
    EQUAL = '='
    LESS = '<'
    GREATER = '>'
    BANG_EQUAL = '!='
    EQUAL_EQUAL = '=='
    GREATER_EQUAL = '>='
    LESS_EQUAL = '<='
    LSHIFT = '<<'
    RSHIFT = '>>'
    RANGE = ".."
    FLOOR = "//"
    INCREMENT = "++"
    DECREMENT = "--"
    CONCATENATE = ":+"
    ADD_ASSIGN = "+="
    SUB_ASSIGN = "-="
    MUL_ASSIGN = "*="
    DIV_ASSIGN = "/="
    LSHIFT_ASSIGN = '<<='
    RSHIFT_ASSIGN = '>>='


class Monographs(TokenType):
    """Single-character tokens."""
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"
    BANG = "!"
    PIPE = "|"
    CARAT = "^"
    MODULO = "%"
    AMPERSAND = "&"
    COLON = ":"
    QUESTION = "?" # Challenge 2.6.2
    EQUAL = '='
    LESS = '<'
    GREATER = '>'

class Digraphs(TokenType):
    """Double-character tokens."""
    BANG_EQUAL = '!='
    EQUAL_EQUAL = '=='
    GREATER_EQUAL = '>='
    LESS_EQUAL = '<='
    LSHIFT = '<<'
    RSHIFT = '>>'
    RANGE = ".."
    FLOOR = "//"
    INCREMENT = "++"
    DECREMENT = "--"
    CONCATENATE = ":+"
    ADD_ASSIGN = "+="
    SUB_ASSIGN = "-="
    MUL_ASSIGN = "*="
    DIV_ASSIGN = "/="
    LSHIFT_ASSIGN = '<<='
    RSHIFT_ASSIGN = '>>='


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
    UNLESS = 'unless'
    NIL = 'nil'
    OR = 'or'
    PRINT = 'print'
    BREAK = 'break'
    CONTINUE = 'continue'
    LOOP = 'loop'
    UNTIL = 'until'
    RETURN = 'return'
    SUPER = 'super'
    THIS = 'this'
    TRUE = 'true'
    VAR = 'var'
    WHILE = 'while'
    INT = 'int'
    FLOAT = 'float'
    BOOL = 'bool'
    STR = 'str'
    CHAR = 'char'
    NUM = 'num'

class Miscellania(TokenType):
    """Token types that don't easily fit into another category."""
    EOF = 'eof'
    ELLIPSIS = '...'

