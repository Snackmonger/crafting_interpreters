from typing import Optional
from data.annotations import LoxValue
from data.errors import LoxRuntimeError
from src.token import Token


class Environment:


    def __init__(self, enclosing: Optional['Environment'] = None) -> None:
        self.values: dict[str, LoxValue] = {}
        self.enclosing: Optional[Environment] = enclosing


    def define(self, name: str, value: LoxValue) -> None:
        self.values[name] = value

    def get(self, name: Token) -> LoxValue:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        
        if self.enclosing:
            return self.enclosing.get(name)
        
        raise LoxRuntimeError(name, "Undefined variable '"+ name.lexeme + "'.")
        
    def assign(self, name: Token, value: LoxValue) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing:
            self.enclosing.assign(name, value)
        raise LoxRuntimeError(name, "Undefined variable '" + name.lexeme + "'.")