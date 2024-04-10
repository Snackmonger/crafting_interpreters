.. contents::

Chapter 2, Section 4: Scanner
-----------------------------

Index off by 1 error:
    Compared to the Java syntax in the original version, we have to make an adjustment in Python. 

    .. code:: java

        private char advance() {
            return source.charAt(current++);
        }

    In Java, returning an increment returns the starting value, THEN performs the increment (post-increment). In Python,
    this syntax does not exist, so we have to extract the value, THEN increment, THEN return.

    .. code:: python

        def advance(self) -> str:
            char = self.peek()
            self.current += 1
            return char

    Another way of resolving this problem is simply:

    .. code:: python

        def advance(self) -> str:
            self.current += 1
            return self.source[self.current - 1]

Chapter 2, Section 5: Representing Code
---------------------------------------

We created a protocol to serve the same function as the interface in the Java program in the book. Because Python is dynamically
typed, the protocol is not necessary for the operation of the visitor pattern; the protocol just makes it easier to see what the
expected interface is, and it allows the strict type-checking in the linter to verify that we are passing an object that satisfies
that interface. 

The chapter also has us write some code that automatically generates some classes for the AST. Obviously,
the Python version has to generate different code. As the book says, scripting languages are ideal for this 
kind of task, so this was a fun little side track. I put all the information for the class definitions in a 
text file, and we can use that as the basis for generating the protocol class and the AST classes. A little
later in the book, we'll also think about statements, and we can modify these tools to generate those from the
same precursor file. 

Chapter 2, Section 6: Evaluating Expressions
--------------------------------------------

The Java ``Object`` that the book recommends is not necessary for our implementation of Lox, since Python is already a dynamically
typed language, and we don't need a special object to hold values of unknown types. Therefore, instead of returning a container 
class, I just marked the return using a type annotation that encompasses any valid primary value.

In order to incorporate the ternary operators ? : that we added in the last section, we added a new method to the ExprVisitor 
protocol, which has to be implemented in the interpreter::

    def visit_TernaryExpr(self, expr: Ternary) -> LoxValue:
        """Interpret a ternary."""
        cond = self.evaluate(expr.condition)
        if self.is_truthy(cond):
            return self.evaluate(expr.true_branch)
        return self.evaluate(expr.false_branch)