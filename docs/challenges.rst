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

2. Aside from separating tokens—distinguishing print foo from printfoo—spaces aren't used for much in most languages. However, in a couple of dark corners, a space does affect how code is parsed in CoffeeScript, Ruby, and the C preprocessor. Where and what effect does it have in each of those languages?

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

    .. codeblock:: Python

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