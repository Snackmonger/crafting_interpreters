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
        → ("var" | type_annotation) IDENTIFIER ("=" expression)? ";" 
        ;
    type_annotation
        → ("int" | "float" | "num" | "bool" | "string" | "char" |)
        ;

    // Statements
    statement       
        → block
        | printStmt
        | ifStmt
        | iterationStmt
        | exprStmt
        | gotoStmt
        ;
    printStmt      
        → "print" expression ";"
        ;
    block
        → "{" declaration "}"
        ;
    exprStmt        
        → expression ";"
        ;
    gotoStmt
        → breakStmt
        | returnStmt
        | continueStmt 
        ;
    iterationStmt
        → whileStmt
        | forStmt
        | loopStmt
        ;
    whileStmt
        → "while" "(" expression ")" statement
        ;
    forStmt        
        → "for" "(" ( varDecl | exprStmt | ";" ) expression? ";" expression? ")" statement 
        // TODO: | "for" "(" varDecl ":" listExpr ")" statement
        ;
    loopStmt
        → "loop" statement ("until" "(" expression ")" )?
        ;
    breakStmt
        → "break" ";"
        ;
    ifStmt
        → "if" "(" expression ")" statement ( "else" statement )? 
        ;

    // Expressions
    expression
        → assignment
        ; 
    assignment         
        → IDENTIFIER ("=" | "+=" | "-=" | "*=" | "/=") assignment
        | ternary
    ternary         
        → binary ("?" expression ":" ternary)?
        ;
    // Binary expressions
    binary          
        → logic_or
        ;
    logic_or
        → logic_and ("or" logic_and)*
        ;
    logic_and
        → logic_or ("and" equality)*
        | equality
        ;
    equality        
        → comparison ( ( "!=" | "==" ) comparison )* 
        ;
    comparison      
        → concatenation ( ( ">" | ">=" | "<" | "<=" ) concatenation )* 
        ;
    concatenation
        → term (":+" concatenation)*
        ;
    term              
        → factor ( ( "-" | "+" ) factor )* 
        ;
    factor              
        → unary ( ( "/" | "*" ) unary )* 
        ; // modulus goes here

    // Unary expressions
    unary           
        → inversion
        | postfixExpr
        ;
    inversion
        → ( "!" | "-" | "~" ) unary
        ;
    postfixExpr
        → primary
        ;    

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

