# pylint:disable=invalid-name
"""Functions relating to generating the .py files that define classes in the 
program.
"""

# NOTE: DO NOT use the automatic IDE re-formatting tool on this file. It will
# fail to recognize multi-line strings within other strings, and will attempt
# to split at inappropriate places.

import json

def test_display_AST_files(definition_filepath: str) -> None:
    """Display a preview of the generated files."""
    protocols = create_protocols(definition_filepath)
    expressions = create_expression_classes(definition_filepath)
    print("Beginning protocols .py file:\n")
    print(protocols)
    print("Beginning expressions .py file:\n")
    print(expressions)


def remake_AST_files(definition_filepath: str, protocols_filepath: str, expressions_filepath: str) -> None:
    """Run the AST generation functions to create/update the AST files to the
    given specification.
    """
    print("The following action may OVERWRITE existing files. \
          Preview the files below and confirm overwrite.")
    test_display_AST_files(definition_filepath)

    while True:
        x = input("Are you sure you want to continue? (Y/N)")
        if x in ["y", "Y"]:
            protocols = create_protocols(definition_filepath)
            expressions = create_expression_classes(definition_filepath)
            write_new_file(protocols, protocols_filepath)
            write_new_file(expressions, expressions_filepath)
            return
        if x in ["n", "N"]:
            return


def read_ast_definition_file(file: str) -> dict[str, dict[str, str | list[str]]]:
    """Read a json file with the AST class definitions and return a Python
    dictionary of the contents.
    """
    with open(file, 'r', encoding="utf8") as f:
        return json.load(f)


def write_new_file(file_contents: str, output_file_path: str) -> None:
    """Write the given string to a file at the given path."""
    with open(output_file_path, "w", encoding="utf8") as f:
        f.write(file_contents)


def create_expression_classes(file: str) -> str:
    """Generate a string representing a .py file for the classes in the 
    given define_AST.json file.
    """
    module_docstring = '"""Expression and statement classes used in the Lox AST."""\n\n'
    imports: dict[str, list[str]] = {"typing": ["Any", "Optional"],
                                     "dataclasses": ["dataclass"],
                                     "src.token": ["Token"],
                                     "data.annotations": ["LoxValue"],
                                     "data.protocols": []
                                     }
    parent_defs = ""
    classdefs = ""
    items = read_ast_definition_file(file)

    for expr_data in items.values():
        parent_name = str(expr_data["name"])
        parent_symbol = str(expr_data["symbol"])
        members = expr_data["members"]
        title = parent_name.removeprefix("an").removeprefix("a").strip(" ")
        imports["data.protocols"].append(parent_symbol+"Visitor")

        parent_defs += f"class {parent_symbol}:\n"
        parent_defs += f'    """{title.capitalize()} base class."""\n'
        parent_defs += f'    def accept(self, visitor: {parent_symbol}Visitor) -> Any:\n'
        parent_defs += '        raise NotImplementedError\n\n'

        for member in members:
            name = member["name"]  # type: ignore
            symbol = member["symbol"]  # type: ignore
            args = member["args"]  # type: ignore

            classdefs += "@dataclass\n"
            classdefs += f"class {symbol}({parent_symbol}):\n"
            classdefs += f'    """Representation of {name}."""\n'
            for arg in args:
                classdefs += f"    {arg}\n"
            classdefs += "\n"
            classdefs += f"    def accept(self, visitor: {parent_symbol}Visitor) -> Any:\n"
            classdefs += f"        return visitor.visit_{symbol}{parent_symbol}(self)\n\n"

    header = format_imports(imports)
    header += "\n"
    return module_docstring + header + parent_defs + classdefs


def create_protocols(file: str) -> str:
    """Generate the protocol classes used by the Lox AST."""
    module_docstring = '"""Protocols that define functionality added to AST classes."""\n\n'
    imports: dict[str, list[str]] = {
        "typing": ["Protocol", "Any", "TYPE_CHECKING"]}
    type_check_imports: dict[str, list[str]] = {"src.expressions": []}
    classdefs = ""
    items = read_ast_definition_file(file)
    for expr_data in items.values():
        parent_symbol = str(expr_data["symbol"])
        members = expr_data["members"]
        classdefs += f"class {parent_symbol}Visitor(Protocol):\n"
        classdefs += f'    """Protocol for behaviours added to subclasses of {parent_symbol}."""\n\n'
        for member in members:
            symbol = member["symbol"]  # type: ignore
            type_check_imports["src.expressions"].append(symbol)
            classdefs += f"    def visit_{symbol}{parent_symbol}(self, {parent_symbol.lower()}:'{symbol}') -> Any: ...\n"
        classdefs += "\n\n"

    header = format_imports(imports)
    if type_check_imports:
        header += "\nif TYPE_CHECKING:\n"
        header += format_imports(type_check_imports, 1)
    header += "\n"

    return module_docstring + header + classdefs

def format_imports(imports: dict[str, list[str]], indents: int = 0) -> str:
    """Return a pretty formatted import statement, using parentheses if there
    are more than one import from the same source, and optionally indenting
    the given amount.

    Example
    -------
    from typing import (
        Protocol,
        Any,
        TYPE_CHECKING
    )
    if TYPE_CHECKING:
        from src.expressions import (
            Binary,
            Grouping,
            Literal,
            Unary,
            Ternary,
            Expression,
            Print
        )
    """
    indent = "    " * indents
    header = ""
    for source, import_list in imports.items():
        header += f"{indent}from {source} import "
        if len(import_list) == 1:
            header += import_list[0]
            header += "\n"
        else:
            header += "(\n"
            for i, import_ in enumerate(import_list):
                
                header += f"{indent}    {import_}" + \
                ("," if i < len(import_list) - 1 else "") + "\n"
            header += f"{indent})\n"
    return header
        

