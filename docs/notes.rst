Chapter 2, Section 4: Scanner
-----------------------------

Index off by 1 error:
    Compared to the Java syntax in the original version, we have to make an adjustment in Python. 

    .. codeblock:: Java

        private char advance() {
            return source.charAt(current++);
        }

    In Java, returning an increment returns the starting value, THEN performs the increment (post-increment). In Python,
    this syntax does not exist, so we have to extract the value, THEN increment, THEN return.

    .. codeblock:: Python

        def advance(self) -> str:
            char = self.peek()
            self.current += 1
            return char

    Another way of resolving this problem is simply:

    .. codeblock:: Python

        def advance(self) -> str:
            self.current += 1
            return self.source[self.current - 1]