"""Chapter 2.5: Representing Code"""
from data.enums import Monographs
from src.expressions import Binary, Unary, Literal, Grouping
from src.token import Token
from tools.ast_printer import ASTPrinter



def test_ASTPrinter():
    expr = Binary(
    Unary(
        Token(Monographs.MINUS, "-", None, 1), 
        Literal(123)),
        Token(Monographs.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        ))
    x = ASTPrinter.print(expr)
    print(x)


