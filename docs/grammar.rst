As of chapter 2.5, I will update the grammar of the program to reflect the state of 
development, plus any extra syntax that I have added as part of the challenges. In 
some cases, I have added some redundant productions to separate the different levels
in the descent more obviously.

Note: The use of "term" and "factor" are not applied correctly. We should correct this
once we reach the final state of the interpreter, but for now we will follow the book's 
terminology to avoid introducing mistakes. 
(Let's use: equality > comparison > additive > multiplicative > unary)

::

    // Start symbol
    program         
        → declaration* EOF;

    // Declarations
    declaration     
        → varDecl
        | statement
        ;
    varDecl         
        → "var" IDENTIFIER ("=" expression)? ";" 
        ;

    // Statements
    statement       
        → exprStmt
        | printStmt
        | block
        ;
    exprStmt        
        → expression ";"
        ;
    printStmt      
        → "print" expression ";"
        ;
    block
        → "{" declaration "}"

    // Expressions
    expression
        → assignment
        ; 
    assignment         
        → IDENTIFIER "=" assignment
        | ternary
        ;
    ternary         
        → binary ("?" expression ":" ternary)?
        ;

    // Binary expressions
    binary          
        → equality
        ;    
    equality        
        → comparison ( ( "!=" | "==" ) comparison )* 
        ;
    comparison      
        → term ( ( ">" | ">=" | "<" | "<=" ) term )* 
        ;
    term              
        → factor ( ( "-" | "+" ) factor )* 
        ;
    factor              
        → unary ( ( "/" | "*" ) unary )* 
        ; // modulus goes here

    // Unary expressions
    unary           
        → ( "!" | "-" ) unary 
        | primary
        ;

    // pre_increment -> ("--" | "++") primary

    // post_increment -> primary ("--" | "++") 

    // Primary terminals
    primary         
        → NUMBER 
        | STRING 
        | "true" 
        | "false" 
        | "nil" 
        | "(" expression ")" 
        | IDENTIFIER
        | error
        ;

    // Error productions
    error           
        → ("==" | "!=") equality
        | (">=" | "<=" | "<" | ">") comparison
        | ("+") term
        | ("*" | "/") factor
        ;

