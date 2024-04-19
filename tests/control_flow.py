"""
I wasn't able to answer the question for challenge 2.9.1, so I tried to 
implement the book's answer as a way to learn a bit more about how control
flow works in other languages. This is the book's explanation of the concept:

    "The basic idea is that the control flow operations become methods that 
    take callbacks for the blocks to execute when true or false. You define 
    two classes with singleton instances, one for true and one for false. The 
    implementations of the control flow methods on the true class invoke the 
    then callbacks. The ones on the false class implement the else callbacks.
    
    This is famously how Smalltalk implements its control flow."
"""

from abc import ABC
from typing import Callable, Optional, TypeVar

R = TypeVar("R")

class _Binary(ABC):
    @staticmethod
    def if_then(then_branch: Callable[..., R]) -> R:
        """True -> then(), False -> None"""
        raise NotImplementedError
    @staticmethod
    def if_then_else(then_branch: Callable[..., R], else_branch: Callable[..., R]) -> R:
        """True -> then(), False -> else()"""
        raise NotImplementedError

class _True(_Binary):
    """True returns the THEN branch."""
    @staticmethod
    def if_then(then_branch: Callable[..., R]) -> R:
        return then_branch()
    @staticmethod
    def if_then_else(then_branch: Callable[..., R], else_branch: Callable[..., R]) -> R:
        return then_branch()
    
class _False(_Binary):
    """False returns the ELSE branch, or none at all."""
    @staticmethod
    def if_then(then_branch: Callable[..., R]) -> Optional[R]:
        return None
    @staticmethod
    def if_then_else(then_branch: Callable[..., R], else_branch: Callable[..., R]) -> R:
        return else_branch()
    

def test(condition: _Binary):
    """A true should cause both functions to execute. A false will only cause
    one to execute.
    """
    print("Beginning test...")
    def if_then_fn():
        print ("if then -> then")

    # If the condition is true, then the func executes, otherwise not.
    condition.if_then(if_then_fn)

    def if_then_else_then_fn():
        print ("if then else -> then")
    def if_then_else_else_fn():
        print("if then else -> else")

    # If the condition is true, then the then executes, otherwise, the else.
    condition.if_then_else(if_then_else_then_fn, if_then_else_else_fn)


t = _True()
f = _False()

print("Test 1: True. Expect two answers.")
test(t)
print()
print("Test 2: False. Expect one answer.")
test(f)