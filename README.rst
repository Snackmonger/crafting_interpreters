CRAFTING INTERPRETERS
---------------------

Python implementation of the Lox language & interpreter defined in 'Crafting Interpreters' by Robert Nystrom.

As I work through the book, I am actively attempting the challenges. Since Python and Java are basically my only
languages, sometimes I am unable to answer questions about how to do quasi-OOP things in a functional language like
Haskell, simply because I don't know the idiom. So I have tried to set myself a few challenges of my own as a substitute
for the challenges I failed in the book.

Extras
++++++

Multi-line nested comments
==========================
As part of challenge 2.4.4, we added multi-line comments. I came up with a solution similar to the one that Nystrom shows
in the book, partly because I had to look at the answer for the previous question 2.4.3 and got 'inspired'. Anyway, it looks
like this::

    var x = 5;
    /* This is the multi-line comment
    it ignores anything else and keeps going until an escape
    token is found /* but if there are multiple multi-line comments
    nested together */, they all have to be exited properly, or else
    we get an error */
    print x;

Assignment Operators
====================
During the section on while-loops, while testing the code, I kept getting frustrated with having to do increment
manually. I wanted to add increment to the language, but the ++ -- syntactic sugar is kind of unappealing to me. 
Therefore, the increment is just included in the assignment operators, and any pre/post-increment decision must
be done by the user. So, we have things like::

    var x = 10;
    x += 1;
    print x == 11;
    x *= 10;
    print x == 110;

This prints ``true true``

Concatenation Operator
======================
Challenge 2.7.2 asked us to implement an addition operator that automatically converts an operand to a string 
if the other operand is a string. I want to raise an error in that situation unless the user has done an explicit
cast so we know that both operands are strings. However, if the user does want to stringify -> concatenate each
value, then we can use the concatenation operator ":+"::

    int x = 6699;
    str name = "Ned";
    float amount = 44.55;
    print "User ID: " :+ x :+ ", Name:  " + name + ", Remaining Money: " :+ amount;

This prints ``User ID: 6699, Name:  Ned, Remaining Money: 44.55``. 
Notice that strings can still be concatenated with the plus operator.

The ":+" sign is not very attractive, but I wanted to reserve the ampersand "&" for bitwise AND.

Sugar Loops
===========
Since the section on control flow had some tough challenges that stumped me, I tried to add a little sugar to compensate.
The loop-until statement is like an inverted while loop. Instead of checking the condition and then entering a loop for as
long as it's true, we enter the loop and continue until the condition is false. This means that the loop will always be 
executed at least once, and if the until expression is omitted, then it will be equivalent to while (true).

::
    // This is an infinite loop!
    int x = 0;
    loop {
        print "The current value is " :+ x;
        x += 1;
    } 

    // This loop has an exit condition.
    int y = 0;
    loop {
        print "The current value is " :+ y;
    } until (y > 10) 