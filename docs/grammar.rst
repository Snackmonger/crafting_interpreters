As of chapter 2.5, I will update the grammar of the program to reflect the state of 
development, plus any extra syntax that I have added as part of the challenges::

    expression     → comma
    comma          → ternary ("," ternary)*
    ternary        → equality ("?" expression ":" ternary)?
    equality       → comparison ( ( "!=" | "==" ) comparison )* ;
    comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    term           → factor ( ( "-" | "+" ) factor )* ;
    factor         → unary ( ( "/" | "*" ) unary )* ;
    unary          → ( "!" | "-" ) unary
                    | primary ;
    primary        → NUMBER | STRING | "true" | "false" | "nil"
                    | "(" expression ")" ;
                    | error
    error          → ("==" | "!=") equality
                    | (">=" | "<=" | "<" | ">") comparison
                    | ("+") term
                    | ("*" | "/") factor

Note: The use of "term" and "factor" are not applied correctly. We should correct this
once we reach the final state of the interpreter, but for now we will follow the book's 
terminology to avoid introducing mistakes.

A recursive descent parser is a literal translation of the grammar's rules straight 
into imperative code. Each rule becomes a function. The body of the rule translates 
to code roughly like:: 

    Grammar notation 	Code representation
    ----------------    -------------------
    Terminal	        Code to match and consume a token
    Nonterminal	        Call to that rule's function
    |	                if or switch statement
    * or +	            while or for loop
    ?	                if statement

The descent is described as “recursive” because when a grammar rule refers to 
itself--directly or indirectly--that translates to a recursive function call.