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

Chapter 2, Section 7: Evaluating Expressions
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

Chapter 2, Section 9: Control Flow
----------------------------------

This section's challenges really kicked my butt. I had to look up the answers to get anything more than a guess. I implemented the code given in
the answers and tried to learn a little from them. Then I challenged myself to use what I'd learn to implement a few new things not mentioned
in the official challenges:

a. Since the chapter introduces a for-statement as syntactic sugar for a while loop, I challenged myself to use that idea to create another syntactic sugar in
the form of a loop-statement. This will create an infinite loop in the form of a while-true-statement, but if an until-clause is given, it will be used as a 
negation of the normal while-statement. It always performs the body statement at least once before exiting. I also made sure that the break-statement works 
with the loop-until-statement.

b. One of the earlier challenges suggested the idea that we could make the plus operator automatically stringify values if one of the operands is a string. 
I didn't want to implement that idea at the time, so I skipped the challenge. Now, I added the ":+" operator specifically as a stringify-concatenate operator.
Actually, this symbol is pretty ugly, so I want to change it, but "&" should be reserved for binary AND.
Concatenation has a higher precedence than comparative operators, but lower than the arithmetic operators.

c. When I was writing lox code to test the loops in the interpreter, I was getting annoyed with the lack of arithmetic assignment operators, so I 
added support for +=, -=, /*=, /=.