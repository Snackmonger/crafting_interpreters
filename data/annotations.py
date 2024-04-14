"""Annotations used in type hints."""

from typing import TypeAlias

class UninitializedVariable:
    """Dummy class that serves to indicate that a declared variable does not
    yet refer to any value.
    """

LoxValue: TypeAlias = bool | float | str | None | UninitializedVariable
