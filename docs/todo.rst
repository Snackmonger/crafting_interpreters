To do
-----

Medium-Term Goals
+++++++++++++++++

A. I got a working answer to challenge 2.8.1, but it was very different from the book's answer, so I removed it. I want to see what other changes might happen
to the code before I implement the book's solution.

B. Implement a repeat-until style loop. The until clause should be optional, and a simple repeat statement will 
just create an infinite loop.

Grammar::

    repeatStmt
        → "repeat" statement ("until" "(" expression ")" )?
        ;

Code::

    var i = 0
    repeat {
        i = i + 1
        print i
    } until (i >= 10)

    repeat {
        print "I'm an infinite loop!"
    }

DONE: we called it loop-until statement.

C. foreach (item: array) or for (item: array)
D. Range operator ".."
E. Augmented assignment "+=" etc. DONE: Not terribly hard.
F. Lambda functions. What kind of syntax?

::

    var x = map(x -> x + 3, array)
    var x = map(x => x + 3, array)
    var x = map(x =: x + 3, array)
    var x = map(lambda x : x + 3, array)
    var x = map(func(x) return x + 3;, array)

H. Type annotations so uninitialized variables can still give information about how they should be used.

::

    int x = 0;
    float g = 55.8;
    char k = "k";
    bool f = false;
    num p = 99;
    num q = 99.99;

DOME: All of these are just substitutes for the 'var' keyword right now,, but maybe we can make runtime
type checking in the future with this as a very basic starting point. Probably we need to learn a bit more
about how to implement classes and check their types before we do that.


Long-Term Goals
+++++++++++++++
A. Revise the language to become a strongly-typed language. In fact, this goal might be better served by starting a new language from scratch.
B. Add arrays and maps.