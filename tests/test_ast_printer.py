"""Chapter 2.5: Representing Code"""
from data.enums import Monographs
from src.expressions import Binary, Unary, Literal, Grouping
from src.tools.ast_printer import ASTPrinter, RPNPrinter
from src.token import Token



def test_ASTPrinter():
    expr = Binary(
    Unary(
        Token(Monographs.MINUS, "-", None, 1), 
        Literal(123)),
        Token(Monographs.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        ))
    x = ASTPrinter().print(expr)
    print(x)


def test_RPNPrinter():
    expr = Binary(Binary(Literal(1), Token(Monographs.PLUS, "+", None, 1), Literal(2)),
                  Token(Monographs.STAR, "*", None, 1),
                  Binary(Literal(4), Token(Monographs.MINUS, "-", None, 1), Literal(3)))
    RPNPrinter().print(expr)
    expr = Binary(
    Unary(
        Token(Monographs.MINUS, "-", None, 1), 
        Literal(123)),
        Token(Monographs.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        ))
    RPNPrinter().print(expr)