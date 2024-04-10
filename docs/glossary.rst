
.. contents::

Lexical Analysis
----------------
A scanner/lexer takes in a linear stream of characters and chunks them
together into a series of something more akin to "words". Each of these 
words is called a token. Some tokens are single characters, like ( and , .
Others may be several characters long, like numbers (123), strings ("hi!"), 
and identifiers (min). Some characters are not semantically relevant, and may
be discarded by the lexer.

Parsing
-------
A parser takes a flat sequence of tokens and builds a tree structure that 
mirrors the nested nature of the grammar. The trees have a couple of different names:
"parse tree" or "abstract syntax tree", depending on how close to the bare syntactic
structure of the source language they are.

Static Analysis
---------------
In order to be able to contextualize what identifiers refer to, language analysis must
"bind" or "resolve" the identifiers' names to some defined scope. That is, to associate them
with a region of source code where the name can be referred to its declaration.

If the language is statically typed, this is where we type check. Once we know where a variable
is declared, we can find out its type. If those types are not compatible with the enclosing context,
we can report an error.

The resulting data from the static analysis may be stored in a few different ways:
- stored as attributes in the syntax tree itself -- extra fields in the nodes that aren't initialized
during parsing but get filled in later.
- stored in a lookup table. Typically, the keys to the table are identifiers. In that case, we call it a 
symbol table and the values it associates with each key tell us what the identifier refers to.
- stored by transforming the tree into a new data structure that more directly expresses the semantics
of the code.


Intermediate Representations
----------------------------
An intermediate representation is a way of storing code that isn't tied closely to either the
source or destination forms. The representation acts as an interface between the two languages. Shared
intermediates between different compilers allow us to simplify the process of compiling the code on many 
different architectures.

An intermediate might be useful in making code more efficient. A complex expression can be calculated by 
the compiler, and the final code can simply contain the resulting value. This process is referred to as a 
compile-time optimization.

Code Generation
---------------
In this context, code generation refers to the creation of assembly-like instructions a CPU runs.
The code may be generated for a specific CPU architecture, or for an idealized virtual architecture
that can then be implemented in real CPUs. This idealized code can be called "bytecode". These syntetic 
instructions are designed to map a little more closely to the language's semantics and not be so tied to
the peculiarities of any one architecture.

Virtual Machine
---------------
The virtual machine (VM) emulates the architecture of a hypothetical CPU that supports the 
idealized virtual architecture involved in the bytecode generation. Running the bytecode in
a VM is slower than translating it to the native code, but it is simpler for the programmer 
and more portable in the simulated form. For instance, a VM implemented in C can run on any
platform that has a C compiler.

Runtime
-------
Services provided by the language while the program is running. For example, if the language automatically manages memory,
we need a garbage collector going in order to reclaim unused bits. If the language supports "instance of" tests, then we need
some representations to keep track of the type of each object during execution.

Single-Pass compiler
--------------------
A compiler that weaves the parsing, analysis, and code generation so that they produce output code
directly in the parser, without ever allocating any syntax trees or other representations. Such a compiler restricts 
the design of the language. Since there is no intermediate data structures to store global information about the program,
and since the parser doesn't revisit any previously parsed part of the code, it means that any expression
encountered by the parser needs to be complete enough to be correctly compiled. For instance, requiring that a variable
be prefaced with an explicit type, or requiring that a function only be called below its declaration.

Tree-walk Interpreters
----------------------
An interpreter that traverses the AST one branch and leaf at a time, evaluating each node as it goes.

This implementation is fine for smaller projects, but tends to be slow.

Transpilers
-----------
Rather than write code generation for a lower-level language, a transpiler (transcompiler/source-to-source compiler)
allos us to compile our language to an existing language that itself can compile to a lower level language.
In this context, the secondary language serves as a sort of intermediate representation.

Scanning
--------
The first step of any compiler or interpreter. The scanner takes in raw source code as a series of 
characters and groups it into a series of chunks we call tokens. These are the meaningful "words" and "punctuation" that 
make up the language's grammar. This might be called "lexical analysis", or simply "lexing".

Context-Free Grammar
--------------------
A grammar is said to be context-free when the left side of its production rules consist solely of single non-terminal symbols.
Another way of thinking about this is that prodcution rules can be applied to non-terminal symbols regardless of their context.

A context-free grammar G is defined by the 4-tuple G = ( V , Σ , R , S ) {\displaystyle G=(V,\Sigma ,R,S)}, where[6]

    V is a finite set; each element v ∈ V {\displaystyle v\in V} is called a nonterminal character or a variable. Each variable represents a different type of phrase or clause in the sentence. Variables are also sometimes called syntactic categories. Each variable defines a sub-language of the language defined by G.
    Σ is a finite set of terminals, disjoint from V, which make up the actual content of the sentence. The set of terminals is the alphabet of the language defined by the grammar G.
    R is a finite relation in V x ( V ∪ Σ )*, where the asterisk represents the Kleene star operation. The members of R are called the (rewrite) rules or productions of the grammar. (also commonly symbolized by a P)
    S is the start variable (or start symbol), used to represent the whole sentence (or program). It must be an element of V.

These production rules are context-free:
S -> aSb
S -> a
S -> A
A -> b

These production rules are not context-free:
S -> aSb
aS -> bb
SS -> aba

The rule aS -> bb depends on a terminal symbol being contextualized by a non-terminal symbol.
The rule SS -> aba depends on a terminal symbol being contextualized by another terminal symbol.

Regular Grammar
---------------
Every regular grammar is context-free, but not all context-free grammars are regular.

A grammar is regular if:
    - all production rules have at most one non-terminal symbol on the right side
    - that the non-terminal symbol is always either at the beginning or the end of the rule's right side, and that both positions are not mixed in the grammar

This entails that all words over the grammar's alphabet can be mapped with a tree of finite and constant size.

Visitor Pattern
---------------
Goal: Separate an algorithm from the object structure.

This pattern allows us to create functions for objects that already 
exist without having to add methods to the objects themselves. It can
be thought of as a way of bridging the gap between a functional approach
and an object-oriented approach.

An object is defined with a method to ACCEPT a VISITOR.

The VISITOR contains methods corresponding to various different object types that are supported in its interface.

When the object ACCEPTS the VISITOR, it passes itself to the VISITOR's VISIT method. In languages with method signatures, this can be defined with a common
name and different implementations. In the Python version, we just give the different implementations different names.

The VISIT method in the VISITOR provides some kind of functionality that uses the object's data and returns
it to the object's ACCEPT method that originally invoked the VISITOR's VISIT method. 

In this way, the original object is able to return the result of a function that uses its own specific data
structure, but without having to have that function defined within itself (or even knowing anything about the
function and its return).


Precedence
----------
When evaluating an expression, precedence determines which operator is evaluated first in an expression
containing a mixture of different operators.

Associativity
-------------
When evaluating an expression, assiciativity determines which operator is evaluated first in a series of
the same operator. When an operator that is left-associative, operators on the left will evaluate before those
on the right, and vice-versa. 

Left associative: 5 - 3 - 1 >> (5 - 3) - 1
Right associative: a = b = c >> a = (b = c)

An operator may also be non-associative, meaning that it cannot be used more than once in a sequence.

Panic Mode
----------
When the parser encounters an error, it enters panic mode. It knows that at least one token doesn't make sense
in its current state in the middle of some stack of grammar productions.

Before it can get back to parsin, it needs to get its state and the sequence of forthcoming
tokens aligned such that the next token does match the rule being parsed. This process is called synchronization.

To do that, we select a rule in the grammar that will mark the synchronization point. The parser fixes its state by 
jumping out of any nested productions until it gets back to this rule. Then it synchronizes the token stream by
discarding tokens until it reaches one that can appear at that point in the rule.

