2.4: Scanning
-------------

1. The lexical grammars of Python and Haskell are not regular. What does that mean, and why aren't they?

    A regular grammar has at most one NON-TERMINAL SYMBOL for each PRODUCTION RULE on the right side, and that 
    symbol is always at the beginning (left-regular) or end (right-regular) of the production, but not both.

    A regular grammar generates words that can be recognized by an algorithm/machine using a constant (finite) 
    amount of memory and examining all symbols in a word one after another.
    
    All languages with a finite number of words are regular languages, because we can reduce the analysis of all 
    words to a control tree (e.g. of ``if`` statements) of constant size. Since the language has a finite number 
    of words, the control structure that analyzes it will also be finite.

    Python and Haskell use whitespace with semantic meaning; indentation denotes blocks of code within control 
    structures, and de-indentation denotes the return to a previous level of control. Because the amount of 
    indentation can grow infinitely and still be meaningful, the amount of memory needed to recognize whether 
    a word belongs to the language also grows infinitely. The language is analogous to the linear language 
    L = {a^ib^i: i >= 1} since the number of INDENT and DEDENT tokens grows in a linear manner, and thus 
    cannot be recognized with a constant amount of memory. 

    The lexical grammar of the Scanner class built in this chapter is regular (so far) because we can recognize
    all words over the alphabet by means of a simple control structure. Words are either a simple 1:1 match 
    (S -> a), or they use the ``match`` method to look at the next character (S -> aT, T -> a), or they are a 1:1 
    match with a unique sequence of characters (S -> abc). In this expression, the grammar rules I wrote are 
    "right-regular" because the single non-terminal symbol always comes on the right side of the production.

2. Aside from separating tokens—distinguishing print foo from printfoo—spaces aren't used for much in most languages. However, 
in a couple of dark corners, a space does affect how code is parsed in CoffeeScript, Ruby, and the C preprocessor. Where and 
what effect does it have in each of those languages?

    Answer: (Since I don't know these languages, I had to check the book's answers to learn about this)
    
    Ruby: Ruby allows for parentheses to be omitted in method invocations. This means that whitespace between a funtion name and its invocation
    can cause the parser to misinterpret an argument and an expression:
        f(3+2)+1 -> Function returns value, then 1 is added.
        f (3+2)+1 -> The entire group (3+2)+1 is understood as the argument of the function.
    
    CoffeScript: Same problem as Ruby.
    
    C preprocessor: Uses spaces to distinguish macro types:
    #define MACRO1 (p) (p) // Simple text macro that expanss to (p) (p) when used
    #define MACRO2(p) (p) // Function-like macro that takes paramter p and expands to (p)


3. Our scanner here, like most, discards comments and whitespace since those aren't needed by the parser. Why might you want to write a scanner that does not discard those? What would it be useful for?

    If we want to preserve documentation for the user. This might be because we are forwarding that information to
    an interactive editor when the user hovers over a function name, or something like that. If we are creating automatic
    documentation from docstrings then they are relevant. In some contexts maybe the comments serve a memoization function that
    has meaning in the production context.

4. Add support to Lox's scanner for C-style /* ... */ block comments. Make sure to handle newlines in them. Consider allowing them to nest. Is adding support for nesting more work than you expected? Why?

    For now, this seems to do the trick, but it looks a litle fragile.

.. code:: 

    def multiline_comment(self) -> None:
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

2.5: Representing Code
----------------------

1. Earlier, I said that the |, \*, and + forms we added to our grammar metasyntax were just syntactic sugar. 
Take this grammar ::

    expr → expr ( "(" ( expr ( "," expr )* )? ")" | "." IDENTIFIER )+
            | IDENTIFIER
            | NUMBER

Produce a grammar that matches the same language but does not use any of that notational sugar.

Bonus: What kind of expression does this bit of grammar encode? ::

    expr → expr invocation
        | IDENTIFIER
        | NUMBER
    args → expr 
         → args "," expr
    invocations → invocations invocation
    invocations → invocation
    invocation → "(" ")"
               | "(" args ")"
               | "." IDENTIFIER

2. The Visitor pattern lets you emulate the functional style in an object-oriented language. Devise a complementary pattern for a functional language. It should let you bundle all of the operations on one type together and let you define new types easily.

(SML or Haskell would be ideal for this exercise, but Scheme or another Lisp works as well.)

    Answer: I don't know any of those languages well enough even to be able to attempt this question. 
    I can imagine that a closure is a necessary device here, but I'm not sure how to be able to define 
    a type in a functional style

3. In reverse Polish notation (RPN), the operands to an arithmetic operator are both placed before the operator, so 1 + 2 becomes 1 2 +. Evaluation proceeds from left to right. Numbers are pushed onto an implicit stack. An arithmetic operator pops the top two numbers, performs the operation, and pushes the result. Thus, this:

(1 + 2) * (4 - 3)

in RPN becomes:

1 2 + 4 3 - *

Define a visitor class for our syntax tree classes that takes an expression, converts it to RPN, and returns the resulting string.

    I modified the AST printer class to use a different rendering function::

.. code:: 
    
    def polishize(self, name: str, /, *exprs: Expr) -> str:
        string = ""
        for expr in exprs:
            string += expr.accept(self)
            string += " "
        string += name
        return string
    

However, in RSP, the unary negation has to be applied AFTER the negated expression.
Therefore, we would have to ensure that there aren't expressions like 3 -4 + (should
be 3 4 - +)

2.6: Parsing
------------

1. In C, a block is a statement form that allows you to pack a series of statements 
where a single one is expected. The comma operator is an analogous syntax for expressions. 
A comma-separated series of expressions can be given where a single expression is expected 
(except inside a function call's argument list). At runtime, the comma operator evaluates 
the left operand and discards the result. Then it evaluates and returns the right operand.

Add support for comma expressions. Give them the same precedence and associativity as in C. 
Write the grammar, and then implement the necessary parsing code.

    Answer: I don't know C, so I had to look into this a bit. In a series of expressions, each
    one is evaluated in turn and discarded, and the rightmost expression retains the final value.

    Example::

        #include <stdio.h>

        int main() {
        int a = 5, b = 10, result;

        result = (a = a + b, b = a - b, a); // Comma operator used in an expression

        printf("Result: %d\n", result);

        return 0;
        }

    The result will be 15. First, a = a + b (a = 5 + 10 = 15), then b = a - b (b = 15 - 10 = 5), then a (a = 15).
    At this point, the assignment to b (b = a - b) is discarded, and a=15 is assigned to ``result``. If we ended with ``, b``,
    then the ``result`` would be b=5, and the a=15 would be discarded.

    Each segment of the comma expression is an expression (that is to say, an ``equality``) in its own right; because of this, the comma has
    to come HIGH in the top down parser (i.e. it has LOW precedence). A comma expression is a series of expressions, and since an expression 
    produces an equality, a comma expression is thus an equality optionally followed by a comma token and an equality (which recursively allows
    for any number of commas to constitute a comma expression). Thus, the Lox grammar that was::

        expression     → equality ;
        equality       → comparison ( ( "!=" | "==" ) comparison )* ;
    
    now becomes::

        expression  -> comma
        comma       -> equality ("," equality)*
        equality ... 

    In order to implement this, the LOW precedence demands that this rule comes HIGH in our parser's 
    logic tree. We need to create a method called by ``expression`` that checks whether the current 
    expression is followed by a comma, and create a Binary that takes the left expression, and checks
    whether the right side is also a comma or whether it is a more specific equality.

    This is the way the grammar works between ``expression`` and ``unary``. In other words, the intermediary
    rules are all types of ``binary`` but we have defined them in more specific ways. Thus, an expression
    like 5 + 7, which has a right and a left side, can be compounded like 5 + 7 + 8 + 24, and these expressions
    are equally binary, but differ in the amount of nested binary expressions in the right side. We can understand
    5 + 7 as (5) + (7) in which each each side evaluates to a unary (and ultimately, a primary). In the same way,
    5 + 7 + 8 + 24 is just a series of binaries: (5 + (7 + (8 + (24)))) that trace the descent of the binary until it
    becomes a unary, which in turn produces a primary. In the same way, a series of expressions separated by commas can
    also be understood as a binary with arbitrarily-deep nesting: 4, 5, 6, 7 represents (4, (5, (6, (7)))). Later, when
    we build the resolver, whatever occupies the rightmost slot of the last binary gets returned as the final value of 
    the expression.

    CAVEAT: If we want to implement this syntax, we will have to revisit this when the time comes to write call syntax, because
    func(3, 4, 6) should retain three separate values, rather than resolving to the last value. I don't think this language has 
    its own tuple/list/array class, but if we want to be able to do assignments like ``list = (1, 2, 3, 4);`` or ``x = 7, y = 9;``
    then we have to be able to distinguish between the comma as an expression operator, and the comma as a separator operator.

    Commas are used as separators in: 
        - multiple variable declaration
        - parameters
        - multiple conditional protases (``if (x > 5, x < 50) {...}``)
        - multiple values in loop initialization (``for (i = 0, j = 10; i < 99; i++, j--){...}``)


2. Likewise, add support for the C-style conditional or “ternary” operator ?:. 
What precedence level is allowed between the ? and :? Is the whole operator 
left-associative or right-associative?

    Answer: The ternary condition is something like ``v = x < y ? 7 : 10``,
    which means: v is equal to (if x < y) 7, (else) 10.

    So a ternary is an equality (which might be a comparison, as in the example above,
    or some other equality expression), which is followed by zero or one sequences
    of "?" expression ":" ternary, which allows any numer of ternary expressions to
    be recursively nested in the expression, but ensures that only one or fewer 
    occurrs in a single expression::

        expression     → comma
        comma          → ternary ("," ternary)*
        ternary        → equality ("?" expression ":" ternary)?
        equality       → comparison ( ( "!=" | "==" ) comparison )* ;
        ...

    If we want to make this syntax meaningful, we will have to remember to implement
    appropriate changes to accomodate it later.

3. Add error productions to handle each binary operator appearing without a left-hand 
operand. In other words, detect a binary operator appearing at the beginning of an 
expression. Report that as an error, but also parse and discard a right-hand operand 
with the appropriate precedence.

    Answer: Error reporting is not an existing feature of the grammar. We'll add an error
    as the highest priority at the bottom of the parsing tree::

        primary     -> NUMBER | STRING | 'true' | 'false' | 'nil'
                    | "(" expression ")"
                    | error
        error       -> ("=="|"!=") expression
                    | (">="|"<="|"<"|">") expression
                    | ("+") expression
                    | ("*"|"/") expression

    When I looked at the answer provided in the book, it said this instead::

        primary    → NUMBER | STRING | "true" | "false" | "nil"
                    | "(" expression ")"
                    // Error productions...
                    | ( "!=" | "==" ) equality
                    | ( ">" | ">=" | "<" | "<=" ) comparison
                    | ( "+" ) term
                    | ( "/" | "*" ) factor ;

    And gave the following explanation:

        "With the normal infix productions, the operand non-terminals are one precedence level higher 
        than the operator's own precedence. In order to handle a series of operators of the same precedence, 
        the rules explicitly allow repetition.

        With the error productions, though, the right-hand operand rule is the same precedence level. That 
        will effectively strip off the erroneous leading operator and then consume a series of infix uses 
        of operators at the same level by reusing the existing correct rule. For example:

        ``+ a - b + c - d``

        The error production for + will match the leading + and then use term to also match the rest of the 
        expression.""

    I suppose that we want to limit the amount of following tokens that could possibly be mis-parsed as part
    of the syntax error? In any case, I followed the guide in the book and updated the grammar with the correct
    answer rather than my own.

2.7: Evaluating Expressions
---------------------------

1. Allowing comparisons on types other than numbers could be useful. The operators might have a reasonable 
interpretation for strings. Even comparisons among mixed types, like 3 < "pancake" could be handy to enable 
things like ordered collections of heterogeneous types. Or it could simply lead to bugs and confusion.

    Would you extend Lox to support comparing other types? If so, which pairs of types do you allow and how 
    do you define their ordering? Justify your choices and compare them to other languages.

    Answer: It is useful to be able to compare data structures, not just arrays and mappings, but also strings.
    Lox does not support arrays, but if it did, we should be able to compare the two arrays. As far as mixed 
    types, I think I would prefer to see explicit type-casting in the code, if only for the benefit of readability.

2. Many languages define + such that if either operand is a string, the other is converted to a string and 
the results are then concatenated. For example, "scone" + 4 would yield scone4. Extend the code in 
visitBinaryExpr() to support that.

    Answer: This can be easily done in Python with a simple conditional structure. I don't want to implement
    this feature so I am going to skip this challenge.

3. What happens right now if you divide a number by zero? What do you think should happen? Justify your 
choice. How do other languages you know handle division by zero, and why do they make the choices they do?

    Change the implementation in visitBinaryExpr() to detect and report a runtime error for this case.

    Answer: Attempting to divide by zero should result in an error. It is impossible to divide by zero and
    there is no result we can return which does not represent a miscalculation. Therefore, we must raise
    an error and assume that the user will try/catch for that possibility in contexts where it is appropriate. 
    (Note: this means that we would have to add try/catch, since Lox does not support it)

2.8: Statements and State
-------------------------

1. The REPL no longer supports entering a single expression and automatically 
printing its result value. That's a drag. Add support to the REPL to let users 
type in both statements and expressions. If they enter a statement, execute it. 
If they enter an expression, evaluate it and display the result value.4

    Answer:
    .. codeblock:: 
        
        def interpret(self, statements: Sequence[Stmt | None]) -> None:
            """Interpret the given statements."""
            try:
                for statement in statements:
                    if isinstance(statement, Expression) and not isinstance(statement.expression, Assign):
                        statement = Print(statement.expression)
                    if statement:
                        self.execute(statement)
            except LoxRuntimeError as e:
                self.lox.runtime_error(e)

    If the statement is an Expression statement and does not contain an assignment, 
    then change it to a Print statement and it will be displayed to the screen. 
    This solution works for now, but it will obviously have to be updated for 
    every context in which an Expression might be used that SHOULDN'T be printed.
    Depending on the size of the language, it might not be unreasonable to use 
    this ad hoc option, but it is hardly appropriate for a larger project.

    When I looked up the answer in the back of the book, the solution was very 
    different, so I reverted my solution to the previous state. I want to see what 
    other changes happen to the code before I implement the book's solution, so 
    this is a TODO for later.

2. Maybe you want Lox to be a little more explicit about variable initialization. 
Instead of implicitly initializing variables to nil, make it a runtime error to 
access a variable that has not been initialized or assigned to, as in:

::

    // No initializers.
    var a;
    var b;

    a = "assigned";
    print a; // OK, was assigned first.

    print b; // Error!


Answer: I came up with a solution similar to the answer in the book. The variable is created with an UninitializedVariable() object, which gets
a copy of the name of the variable that it's assigned to. Then, when the interpreter encounters a Variable expression, it checks whether 
the value is an instance of the UninitializedVariable class, and prints the stored error message if so.

This pattern consists of a simple dummy object::

    class UninitializedVariable:
        def __init__(self, varname: str):
            self.message: str = f"Variable '{varname}' must be initialized before use."

and a few changes to the interpreter::

    def visit_VarStmt(self, stmt: Var) -> None:
        """Interpret a variable statement::
        
            varDecl → "var" IDENTIFIER ("=" expression)? ";"
        """
        value: LoxValue = UninitializedVariable(stmt.name.lexeme)
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visit_VariableExpr(self, expr: Variable) -> LoxValue:
        """Interpret a variable expression::
        
            IDENTIFIER → primary
        """
        value = self.environment.get(expr.name)
        if isinstance(value, UninitializedVariable):
            raise LoxRuntimeError(expr.name, value.message)
        return self.environment.get(expr.name)


3. What does the following program do?

::

    var a = 1;
    {
        var a = a + 2;
        print a;
    }

What did you expect it to do? Is it what you think it should do? What does analogous code in other languages you are familiar with do? What do you think users will expect this to do?

Answer: I expect that the console display a "3". The logic is: var (inner) a = (outer) a + 2. The assignment ``var a =`` in the code block is defined in terms of ``a``, which does not 
exist in the local scope until after the variable declaration is completed. Therefore, when the interpreter looks for ``a`` to evaluate the expression part of the assignment, it only finds
the ``a`` in the outer scope. After this, the local scope adds ``a`` to the mapping of variables with a value of outer ``a`` plus 2. Then the interpreter looks for ``a`` in the print 
statement and finds the local ``a``, so it doesn't bother looking for the global ``a``. 

This is how the assignment works in Python, which is what I'm familiar with. Users' expectations are determined by prior experience, so there's no way to know what they might expect.
It seems like the behaviour makes sense, and it's what I would expect to happen.

2.9: Control Flow
-----------------

1. A few chapters from now, when Lox supports first-class functions and dynamic dispatch, we technically won't 
need branching statements built into the language. Show how conditional execution can be implemented in 
terms of those. Name a language that uses this technique for its control flow.

    Answer: I had absolutely no idea how even to begin approaching this problem, so I cheated and looked at the
    answer in the book. Even though I don't get any points for this challenge, it was a good opportunity to learn
    a new pattern, which I have implmented in the /tests/ folder.

2. Likewise, looping can be implemented using those same tools, provided our interpreter supports an 
important optimization. What is it, and why is it necessary? Name a language that uses this technique 
for iteration.

    Answer: Looping can be implemented with recursive function calls that track their loop number
    as a depth number. What's the optimization? I suppose we need a way to track how deep the recursion
    is allowed to go, so that it does not eat up all the available memory if it gets caught in a very
    long loop.

    As usual, the book gives a better answer:
    "When you see heavy use of recursion like here where there are almost a hundred recursive calls, the 
    concern is overflowing the stack. However, in many cases, you don't need to preserve any information 
    from the previous call when beginning a recursive call. If the recursive call is in tail position -- 
    it's the last thing in the body of the function -- then you can discard any stack space used by the 
    previous call before beginning the next one.

    This tail call optimization lets you use recursion for an unbounded number of iterations while consuming 
    only a constant amount of stack space. Scheme and some other functional languages require an 
    implementation to perform this optimization so that users can safely rely on recursion for iteration."

3. Unlike Lox, most other C-style languages also support break and continue statements inside loops. 
Add support for break statements.

    The syntax is a break keyword followed by a semicolon. It should be a syntax error to have a break 
    statement appear outside of any enclosing loop. At runtime, a break statement causes execution to 
    jump to the end of the nearest enclosing loop and proceeds from there. Note that the break may be 
    nested inside other blocks and if statements that also need to be exited.
