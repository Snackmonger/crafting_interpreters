# pylint:disable=invalid-name
"""Tools used in boilerplate code generation."""

def create_visitor_expr_protocols(file: str) -> str:
    """Return a string defining a Python Protocol subclass with
    methods for each of the given classes defined in the given
    AST definition file.
    """
    classes = [(parent, name) for parent, name, _ in read_dast_file(file)]
    headers = f"from typing import Protocol\nfrom src.expressions import (\n{",\n".join("    "+x for x in [n for _, n in classes])}\n)"
    class_def = "class ExprVisitor(Protocol):\n"
    for parent, name in classes:
        if parent == "Expr":
            class_def += f"    def visit_{name}{parent}(self, expr: {name}) -> Any: ...\n"
    # In section 7, we will add Stmt classes, so here's the update code
    # in anticipation of that.
    # class_def += "\nclass StmtVisitor(Protocol):\n"
    # for parent, name in classes:
    #     if parent == "Stmt":
    #         class_def += f"    def visit_{name}{parent}(self, stmt: {name}) -> Any: ...\n"
    complete = headers + "\n\n" + class_def
    return complete


def read_dast_file(file: str) -> tuple[tuple[str, ...], ...]:
    """Read out AST definition file and return the contents as a two dimensional
    tuple containing groups of (1) the superclass name, (2) the class name, and
    (3) the arg: type pairs that define attributes.
    """
    with open(file, encoding="utf8") as f:
        reader = f.readlines()
        return tuple(tuple(x.strip().split(";")) for x in reader if not x[0] in ["#", "", "\n"])


def make_AST_class_def(data: tuple[str, str, str]) -> str:
    """Use the given data points to make a simple class definition for 
    an element in the AST.

    Parameters:
        data: A tuple consisting of the parent name, class name, and arguments.
    Returns:
        str: A string containing a Python class definition.
    """
    parent, name, args = data
    class_def = f'@dataclass\nclass {name}({parent}):\n'
    class_def += f'    """A representation of a {name.lower()} {"statement" if parent == "Stmt" else "expression"}."""\n'
    for arg in args.split(","):
        class_def += f"    {arg}\n"

    class_def += f"\n    def accept(self, visitor: {parent}Visitor) -> Any:\n"
    class_def += f"        return visitor.visit_{name}{parent}(self)\n"
    return class_def
