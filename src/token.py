
from data.enums import TokenType



class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: object | None, line: int) -> None:
        self.token_type: TokenType = token_type
        self.lexeme: str =  lexeme
        self.literal: object = literal
        self.line: int = line

    def __repr__(self) -> str:
        t = self.token_type.name
        return t + " " + self.lexeme + " " + str(self.literal)

